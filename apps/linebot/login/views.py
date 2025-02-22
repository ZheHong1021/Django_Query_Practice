# views.py
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
import uuid
from .line_services import LineLoginService

@api_view(['GET'])
@permission_classes([AllowAny])
def get_line_login_url(request):
    """
    獲取 LINE Login URL
    """
    # 生成隨機 state 和 nonce
    state = str(uuid.uuid4())
    nonce = str(uuid.uuid4())
    
    # 保存至 session 或 Redis 進行後續驗證
    request.session['line_login_state'] = state
    request.session['line_login_nonce'] = nonce
    
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
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    line_login_url = f"{auth_url}?{query_string}"
    
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
        service = LineLoginService()
        success, response_data, status_code = service.process_login(request)
        return Response(response_data, status=status_code)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'unexpected_error',
            'message': f'處理登入時發生未預期的錯誤: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)