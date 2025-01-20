from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from common.pagination import CustomPageNumberPagination

from .models import User
from .serializers import UserSerializer
from .filters import UserFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse, OpenApiExample

from common.views import PermissionMixin, SwaggerSchemaMixin


@extend_schema(
    tags=['系統管理 - 用戶'],
    request={
        'multipart/form-data': UserSerializer,
    },
    examples=[
        OpenApiExample(
            '創建用戶範例',
            value={
                'username': 'test_user',
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'password': 'password123'
            }
        )
    ]
)
class UserViewSet(PermissionMixin, SwaggerSchemaMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] # 需要驗證
    filterset_class = UserFilter # 篩選
    pagination_class = CustomPageNumberPagination # 分頁

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password("sr2024")
        serializer.save()