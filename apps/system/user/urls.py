
# 建立路由
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'user/deactivate-logs', UserDeactivateLogViewSet, basename='user-deactivation-log')


urlpatterns = [
    path(r'', include(router.urls)),
]