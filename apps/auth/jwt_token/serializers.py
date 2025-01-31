# 客製化Obtain Token
# 【客製化JWT View】
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils import timezone


from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate, get_user_model
from apps.system.user.models import User


# 覆寫錯誤訊息的回傳 (直接覆寫Serializer)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer, TokenObtainSerializer):
    # Overiding validate function in the TokenObtainSerializer  
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field], # 取得 username
            'password': attrs['password'], # 取得 password
        }
        try:
            # 取得 request資訊
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass # 如果request不存在
        

        #region (錯誤訊息設定)
        IS_NOT_ACTIVE_MESSAGE = '該帳號已經停止使用'
        IS_NOT_EXISTS_USERNAME_MESSAGE = '查無使用該帳號的用戶'
        IS_NOT_AUNTENTICATED_MESSAGE = '請確認帳號密碼是否正確!'
        #endregion (錯誤訊息設定)

        try:
            # 取得 user資訊
            user = User.objects.get(username=authenticate_kwargs['username'])

            # 【帳號啟用】
            if not user.is_active: # 如果當前使用者已經停止使用 (is_active = False)
                # 設定錯誤訊息 (如果當前使用者已經停止使用 (is_active = False))
                self.error_messages['no_active_account'] = _(
                    IS_NOT_ACTIVE_MESSAGE # 錯誤訊息
                )
                # 拋出錯誤訊息
                raise AuthenticationFailed(
                    self.error_messages['no_active_account'],
                    'no_active_account',
                )

        # 【帳號查找】找不到該帳號資訊，代表無該帳號資訊
        except User.DoesNotExist:
            # 設定錯誤訊息 (如果該使用者帳號找不到)
            self.error_messages['no_active_account'] =_(
                IS_NOT_AUNTENTICATED_MESSAGE)
                # IS_NOT_EXISTS_USERNAME_MESSAGE)
            raise AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
            
        '''
        We come here if everything above goes well.
        Here we authenticate the user.
        The authenticate function return None if the credentials do not match 
        or the user account is inactive. However here we can safely raise the exception
        that the credentials did not match as we do all the checks above this point.
        '''
        
        # 【驗證】如果失敗則會拋出異常
        self.user = authenticate(**authenticate_kwargs)
        if self.user is None:
            # 設定錯誤訊息 (如果該驗證失敗)
            self.error_messages['no_active_account'] = _(
                IS_NOT_AUNTENTICATED_MESSAGE)
            raise AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        return super().validate(attrs)




class MyTokenObtainPairSerializer(CustomTokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data