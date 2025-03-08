# views.py
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
from .line_services import LineLoginService
from django.shortcuts import redirect
from decouple import config
from urllib.parse import urlencode
from django.core.cache import cache
from apps.system.user.models import User
import json
from django.utils import timezone

@api_view(['GET'])
@permission_classes([AllowAny])
def get_line_login_url(request):
    """
    獲取 LINE Login URL
    """
    # 獲取模式參數 (login 或 binding)
    mode = request.GET.get('mode', 'login')

    # 確認在綁定模式下用戶必須已登入
    if mode == 'binding' and not request.user.is_authenticated:
        return Response({
            'success': False,
            'error': 'auth_required',
            'message': '必須登入才能綁定 LINE 帳號'
        }, status=status.HTTP_401_UNAUTHORIZED)
    


    # 生成隨機 state 和 nonce
    state = str(uuid.uuid4())
    nonce = str(uuid.uuid4())
    
    # 使用緩存存儲 state (10分鐘過期)
    # 將模式信息附加到 state
    cache_key = f"line_state_{state}"
    cache_data = {
        'state': state,
        'mode': mode,
        'user_id': str(request.user.id) if request.user.is_authenticated else None,
    }
    # 使用緩存存儲 state 和模式信息 (10分鐘過期)
    cache.set(cache_key, json.dumps(cache_data), 600)
    
    # LINE Login 參數
    params = {
        'response_type': 'code',
        'client_id': settings.LINE_LOGIN_CHANNEL_ID,
        'redirect_uri': settings.LINE_LOGIN_CALLBACK_URL,
        'state': state,
        'scope': 'profile openid email',
        'nonce': nonce
    }
    
    # 構建 URL（前端會使用此 URL 導向 LINE Login）
    auth_url = 'https://access.line.me/oauth2/v2.1/authorize'
    line_login_url = f"{auth_url}?{urlencode(params)}"
    
    # 最終會回傳此 URL
    return Response({'login_url': line_login_url})


@api_view(['GET', 'POST'])  # 同時支持 GET 和 POST 方法
@permission_classes([AllowAny])
def line_login_callback(request):
    """
    處理 LINE Login 的授權碼
    前端從 URL 獲取授權碼後調用此 API
    """

    """處理 LINE Login 的回調"""
    if request.method not in ['GET', 'POST']:
        return Response({
            'success': False,
            'error': 'method_not_allowed',
            'message': f'不支持的方法: {request.method}'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    try:
        # 驗證 state參數以防止 CSRF 攻擊
        received_state = request.GET.get('state')
        if not received_state:
            print("LINE 回調 - 錯誤: 缺少 state 參數")
            return Response({
                'success': False,
                'error': 'missing_state',
                'message': '缺少 state 參數'
            }, status=status.HTTP_400_BAD_REQUEST)
    
        # 從緩存中獲取 state 數據
        cache_key = f"line_state_{received_state}"
        cached_data_json = cache.get(cache_key)

        if not cached_data_json:
            print("LINE 回調 - 錯誤: state 參數無效或已過期")
            return Response({
                'success': False,
                'error': 'invalid_state',
                'message': 'state 參數無效或已過期'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 將 JSON 字符串解析為 Python 對象
        cached_data = json.loads(cached_data_json)
        stored_state = cached_data.get('state') # 獲取存儲的 state
        mode = cached_data.get('mode', 'login')  # 獲取模式，默認為 login
        user_id = cached_data.get('user_id', None)  # 用戶資訊(如果mode=binding)

        # 檢查 state 參數是否匹配
        if received_state != stored_state:
            print("LINE 回調 - 錯誤: state 參數不匹配")
            return Response({
                'success': False,
                'error': 'invalid_state',
                'message': 'state 參數不匹配'
            }, status=status.HTTP_400_BAD_REQUEST)
        

        # 使用後刪除(一次性使用)
        cache.delete(cache_key)

        # 建立 LINE 服務實例
        service = LineLoginService()
        FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')

        # 處理綁定模式
        if mode == 'binding':
            return handle_binding_mode(request, user_id, service, FRONTEND_URL)
        # 處理登入模式
        else:  # mode == 'login'
            return handle_login_mode(request, service, FRONTEND_URL)
            
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"LINE 登入錯誤: {error_traceback}")
        
        # 嘗試將錯誤信息編碼並傳遞給前端
        error_message = str(e)
        encoded_error = urlencode({'error': 'unexpected_error', 'message': error_message})
        
        # 重定向到前端的錯誤頁面
        FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')
        error_redirect_url = f"{FRONTEND_URL}/error?{encoded_error}"
        return redirect(error_redirect_url)
        
    except Exception as e:
        import traceback
        print(f"LINE 登入錯誤: {traceback.format_exc()}")
        
        return Response({
            'success': False,
            'error': 'unexpected_error',
            'message': f'處理登入時發生未預期的錯誤: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def handle_binding_mode(request, user_id, service, frontend_url):
    """處理 LINE 帳號綁定模式的邏輯"""
    # 檢查是否提供了用戶ID
    if not user_id:
        print("LINE 回調 - 錯誤: 綁定模式下缺少用戶ID")
        return Response({
            'success': False,
            'error': 'missing_user_id',
            'message': '無法識別用戶身份，請重新登入後再嘗試綁定'
        }, status=status.HTTP_400_BAD_REQUEST)
            
    try:
        # 嘗試獲取用戶
        user = User.objects.get(id=user_id)
        # 手動設置 request.user，以便 bind_account 可以正確識別用戶
        request.user = user
        
        # 處理綁定
        success, response_data, status_code = service.bind_account(request)
        
        # 檢查綁定結果
        if not success:
            error_params = {
                'error': response_data.get('error', 'binding_failed'),
                'message': response_data.get('message', '綁定失敗')
            }
            encoded_error = urlencode(error_params)
            
            # 重定向到前端的錯誤頁面
            error_redirect_url = f"{frontend_url}/account/profile?{encoded_error}"
            return redirect(error_redirect_url)
        
        # 綁定成功，生成臨時令牌
        temp_token = str(uuid.uuid4())
        
        # 存儲登入結果
        cache.set(
            f"temp_auth_{temp_token}",
            {'success': True, 'binding_result': response_data},
            timeout=300  # 5分鐘過期
        )

        # 重定向到前端
        redirect_url = f"{frontend_url}/auth/line-callback?temp_token={temp_token}&mode=binding"
        return redirect(redirect_url)
            
    except User.DoesNotExist:
        print(f"LINE 回調 - 錯誤: 找不到用戶 ID {user_id}")
        return Response({
            'success': False,
            'error': 'user_not_found',
            'message': '找不到對應的用戶，請重新登入後再嘗試綁定'
        }, status=status.HTTP_404_NOT_FOUND)


def handle_login_mode(request, service, frontend_url):
    """處理 LINE 登入模式的邏輯"""
    success, response_data, status_code = service.process_login(request)
    
    # 如果處理失敗，返回錯誤信息
    if not success:
        error_params = {
            'error': response_data.get('error', 'login_failed'),
            'message': response_data.get('message', '登入失敗')
        }
        encoded_error = urlencode(error_params)
        
        # 重定向到前端的錯誤頁面
        error_redirect_url = f"{frontend_url}/account/profile?{encoded_error}"
        return redirect(error_redirect_url)

    # 生成臨時令牌
    temp_token = str(uuid.uuid4())
    
    # 存儲登入結果
    query_params = {
        'success': True,
        'access_token': response_data['tokens']['access'],
        'refresh_token': response_data['tokens']['refresh'],
        'user_id': response_data['user']['id'],
        'username': response_data['user']['username'],
    }

    cache.set(
        f"temp_auth_{temp_token}",
        query_params,
        timeout=300  # 5分鐘過期
    )

    # 重定向到前端
    redirect_url = f"{frontend_url}/auth/line-callback?temp_token={temp_token}&mode=login"
    return redirect(redirect_url)



@api_view(['POST'])
@permission_classes([AllowAny])
def exchange_temp_token(request):
    temp_token = request.data.get('temp_token')
    
    # 如果沒有提供臨時令牌，返回錯誤
    if not temp_token:
        return Response({'error': 'missing_token'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 從緩存獲取存儲的令牌和用戶數據
    auth_data = cache.get(f"temp_auth_{temp_token}")

    print(auth_data)

    if not auth_data:
        return Response({'error': 'invalid_or_expired_token'}, status=status.HTTP_400_BAD_REQUEST)

    # 使用完即刪除，確保一次性使用
    cache.delete(f"temp_auth_{temp_token}")
    
    # 返回實際令牌和用戶數據
    return Response(auth_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unbind_account(request):
    """解除 LINE 帳號綁定"""
    try:
        service = LineLoginService()
        response_data = service.unbind_account(request)
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        # 任何未捕獲的例外都會由你的 exception_handler 處理
        raise e