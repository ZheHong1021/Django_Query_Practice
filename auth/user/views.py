from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from common.pagination import CustomPageNumberPagination

from .models import User
from .serializers import UserSerializer
from .filters import UserFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse

@extend_schema(
    tags=['系統管理 - 用戶'],
    request={
        'multipart/form-data': UserSerializer
    },
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] # 需要驗證
    filterset_class = UserFilter # 篩選
    pagination_class = CustomPageNumberPagination # 分頁
