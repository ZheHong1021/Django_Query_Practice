from django.urls import path
from .views import (
    CustomTokenObtainPairView, 
    CustomTokenVerifyView, 
    CustomTokenRefreshView, 
    LogoutView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # 登入取得Token
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 驗證Token是否有效
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),

    # 刷新Token
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    # 登出
    path('logout/', LogoutView.as_view(), name='logout'),
]