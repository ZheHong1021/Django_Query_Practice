from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r'linebot/users', LineUserViewSet, basename='line_user')


urlpatterns = [
    path(r'', include(router.urls)),
]