from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'menus', views.MenuViewSet)

urlpatterns = [
    path('', include(router.urls)),
]