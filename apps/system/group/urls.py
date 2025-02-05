from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'groups', views.GroupViewSet)

# 不需要這個額外的 URL pattern，因為已經通過 @action 裝飾器定義了
# path('groups/<int:pk>/update_permissions/', views.update_permissions),  # 移除這行

urlpatterns = [
    path('', include(router.urls)),
]