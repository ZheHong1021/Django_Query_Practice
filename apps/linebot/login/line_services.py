from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import jwt
import requests
import json
from apps.system.user.models import User
from apps.linebot.lineuser.models import LineUser
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken

class LineLoginService:
    """處理 LINE Login 相關的服務邏輯"""
    
    def __init__(self):
        self.token_url = "https://api.line.me/oauth2/v2.1/token" # 與 LINE 平台交換 token 的 URL
        self.profile_url = "https://api.line.me/v2/profile" # 獲取用戶信息的 URL
        
    def _get_auth_params(self, request):
        """統一獲取授權參數的邏輯"""
        if request.method == 'GET':
            return {
                'code': request.GET.get('code'), # 狀態碼
                'state': request.GET.get('state'), # 狀態
                'error': request.GET.get('error'), # 錯誤
                'error_description': request.GET.get('error_description') # 錯誤描述
            }
            
        try:
            if request.body:
                data = json.loads(request.body) # 嘗試從請求體獲取 JSON 數據
                return {
                    'code': data.get('code'), # 狀態碼
                    'state': data.get('state'), # 狀態
                    'error': data.get('error'), # 錯誤
                    'error_description': data.get('error_description') # 錯誤描述
                }
        except json.JSONDecodeError:
            pass
            
        return {
            'code': request.POST.get('code') or request.GET.get('code'),
            'state': request.POST.get('state') or request.GET.get('state'),
            'error': request.POST.get('error') or request.GET.get('error'),
            'error_description': (request.POST.get('error_description') or 
                                request.GET.get('error_description'))
        }

    def _exchange_token(self, code):
        """與 LINE 平台交換 token"""
        token_data = { # 請求參數
            'grant_type': 'authorization_code', # 授權類型
            'code': code, # 授權碼
            'redirect_uri': settings.LINE_LOGIN_CALLBACK_URL, # 重定向 URL
            'client_id': settings.LINE_LOGIN_CHANNEL_ID, # LINE Login Channel ID
            'client_secret': settings.LINE_LOGIN_CHANNEL_SECRET # LINE Login Channel Secret
        }

        try:
            # 發送請求，獲取 token
            response = requests.post(self.token_url, data=token_data)

            # 解析 JSON 數據
            token_json = response.json()
            
            # 檢查是否有錯誤
            if 'error' in token_json:
                return False, {
                    'error': token_json.get('error'),
                    'message': token_json.get('error_description', '獲取 Token 失敗')
                }
            
            return True, token_json
            
        except requests.RequestException as e:
            return False, {
                'error': 'request_error',
                'message': f'與 LINE 平台通信時發生錯誤: {str(e)}'
            }

    def _get_user_info_from_id_token(self, id_token):
        """從 ID Token 中解析用戶信息"""
        try:
            decoded = jwt.decode( # 解碼 ID Token (簡化版本，不進行完整驗證)
                id_token, 
                options={"verify_signature": False}
            )
            return {
                'id': decoded.get('sub'), # 用戶 ID
                'name': decoded.get('name'), # 用戶名稱
                'picture': decoded.get('picture'), # 用戶頭像
                'email': decoded.get('email') # 用戶郵箱
            }
        except Exception as e:
            print(f"ID Token 解析錯誤: {e}")
            return None

    def _get_user_info_from_api(self, access_token):
        """使用 API 獲取用戶信息"""
        try:
            # JWT 認證
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(self.profile_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'id': data.get('userId'), # 用戶 ID
                    'name': data.get('displayName'), # 用戶名稱
                    'picture': data.get('pictureUrl'), # 用戶頭像
                    'status_message': data.get('statusMessage') # 用戶狀態消息
                }
        except requests.RequestException:
            return None
        
        return None
    

    def _create_or_get_django_user(self, user_data):
        """創建或獲取 Django User"""
        if not user_data.get('email'):
            return None
            
        try:
            # 嘗試通過 email 找到現有用戶
            user = User.objects.get(email=user_data['email'])
        except User.DoesNotExist:
            # 用戶帳號
            username = f"line_{user_data['id']}"

            # 使用預設密碼創建用戶
            default_password = getattr(settings, 'DEFAULT_USER_PASSWORD', 'sr2024')

            # 新增用戶
            user = User.objects.create_user(
                username=username,
                email=user_data['email'],
                first_name=user_data.get('name', ''),
                password=default_password,  # 使用預設密碼
            )
            
        return user
    
    def save_user_data(self, user_data, token_data):
        """儲存或更新用戶資料"""
        # 計算 token 過期時間
        expires_in = token_data.get('expires_in', 3600)
        token_expiry = timezone.now() + timedelta(seconds=expires_in)
        
        # 獲取或創建 Django User
        user = self._create_or_get_django_user(user_data)
        
        # 更新或創建 LINE User
        line_user, created = LineUser.objects.update_or_create(
            line_id=user_data['id'],
            defaults={
                'user': user,
                'display_name': user_data.get('name'),
                'picture_url': user_data.get('picture'),
                'email': user_data.get('email'),
                'access_token': token_data.get('access_token'),
                'token_expires_at': token_expiry,
                'last_login': timezone.now(),
            }
        )
        
        return line_user, created

    def process_login(self, request):
        """處理登入流程的主要邏輯"""
        # 獲取授權參數
        auth_params = self._get_auth_params(request)
        
        # 檢查錯誤
        if auth_params.get('error'):
            return False, {
                'success': False,
                'error': auth_params['error'],
                'message': auth_params.get('error_description') or '登入時發生錯誤'
            }, status.HTTP_400_BAD_REQUEST
            
        # 檢查授權碼
        code = auth_params.get('code')
        if not code:
            return False, {
                'success': False,
                'error': 'authorization_code_missing',
                'message': '未收到授權碼'
            }, status.HTTP_400_BAD_REQUEST
            
        # 交換 token
        success, token_data = self._exchange_token(code)
        if not success:
            return False, {
                'success': False,
                **token_data
            }, status.HTTP_400_BAD_REQUEST
            
        # 獲取用戶信息
        user_data = None
        # 嘗試從 ID Token 中獲取用戶信息
        if token_data.get('id_token'):
            user_data = self._get_user_info_from_id_token(token_data['id_token'])
        
        # 如果 ID Token 無效，則使用 API 獲取用戶信息
        if not user_data and token_data.get('access_token'):
            user_data = self._get_user_info_from_api(token_data['access_token'])
        
        # 如果都還是無法獲取用戶信息，返回錯誤
        if not user_data or not user_data.get('id'):
            return False, {
                'success': False,
                'error': 'user_data_missing',
                'message': '無法獲取用戶資料'
            }, status.HTTP_400_BAD_REQUEST
            
        try:
            # 儲存用戶資料
            line_user, created = self.save_user_data(user_data, token_data)
            
            # 如果有關聯的 Django 用戶，執行登入
            if line_user.user:
                login(request, line_user.user)
            
            # 生成 JWT token
            refresh = RefreshToken.for_user(line_user.user)

            # 返回成功響應
            return True, {
                'success': True,
                'user': {
                    'line_id': line_user.user_id,
                    'name': line_user.display_name,
                    'picture': line_user.picture_url,
                    'email': line_user.email,
                    'is_new_user': created
                },
                'tokens': {
                    'access': line_user.access_token,
                    'refresh': str(refresh),
                    'expires_in': token_data.get('expires_in', 3600)
                }
            }, status.HTTP_200_OK
            
        except Exception as e:
            return False, {
                'success': False,
                'error': 'database_error',
                'message': f'儲存用戶資料時發生錯誤: {str(e)}'
            }, status.HTTP_500_INTERNAL_SERVER_ERROR