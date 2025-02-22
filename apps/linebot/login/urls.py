# urls.py
from django.urls import path
from .views import (
    get_line_login_url, 
    line_login_callback, 
)

urlpatterns = [
    # LINE Login 相關 API
    path('api/line-login/url/', get_line_login_url, name='get_line_login_url'),
    path('api/line-login/callback/', line_login_callback, name='line_login_callback'),
]