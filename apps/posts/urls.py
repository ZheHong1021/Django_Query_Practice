
# 建立路由
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')


urlpatterns = [
    path(r'', include(router.urls)),
]