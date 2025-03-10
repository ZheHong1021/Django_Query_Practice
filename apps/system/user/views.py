from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from common.pagination import CustomPageNumberPagination
from common.views import CreateWithUserMixin, UpdateWithUserMixin, PermissionMixin
from rest_framework.exceptions import ValidationError

from .models import \
    User, \
    UserDeactivateLog
from .serializers import \
    UserSerializer, \
    UserCurrentSerializer, \
    ChangePasswordSerializer, \
    UserDeactivationSerializer, \
    UserDeactivateLogSerializer
from .filters import \
    UserFilter, \
    UserDeactivateLogFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse, OpenApiExample

from common.views import PermissionMixin, SwaggerSchemaMixin

from django.db.models import Q, F, Value, Case, When
from django.db.models.functions import Concat


@extend_schema(
    tags=['系統管理 - 用戶'],
    request={
        'multipart/form-data': UserSerializer,
    },
)
class UserViewSet(PermissionMixin, SwaggerSchemaMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] # 需要驗證
    filterset_class = UserFilter # 篩選
    pagination_class = CustomPageNumberPagination # 分頁

    def get_serializer_class(self):
        """根據不同的操作返回不同的序列化器"""
        # 當前用戶
        if self.action == 'current':
            return UserCurrentSerializer
        # 修改密碼
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        # 註銷使用者
        elif self.action == 'deactivate':
            return UserDeactivationSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password("sr2024")
        user.save()
    
    def get_queryset(self):
        # 獲取查詢集
        qs = super().get_queryset()

        # 關聯欄位(全名)
        qs = qs.annotate(
            fullname=User.get_fullname_annotation()
        )

        # 關聯欄位(是否連接 Line 帳號)
        qs = qs.with_is_line_connected()

        return qs

    #region (管理當前用戶資訊)
    @extend_schema(
        summary="管理當前用戶資訊",
        description="獲取或更新當前登入用戶的資訊",
        request=UserCurrentSerializer,
        responses={
            200: OpenApiResponse(
                response=UserCurrentSerializer,
                description='操作成功'
            ),
            400: OpenApiResponse(
                description='請求數據無效'
            )
        },
    )
    @action(
        detail=False,  # 不需要指定 ID
        methods=['get', 'put', 'patch'], # 支援的 HTTP 方法
        url_path='current', # 路由名稱
        url_name='current', # 路由別名
        permission_classes=[IsAuthenticated]  # 明確指定權限
    )
    
    def current(self, request):
        """處理當前用戶的資訊獲取和更新"""
        # [GET] 獲取當前用戶資訊
        if request.method == 'GET':
            return self._handle_current_get(request)
    
        # [PUT/PATCH] 更新當前用戶資訊
        return self._handle_current_update(request)

    def _handle_current_get(self, request):
        """處理獲取當前用戶資訊"""
        user = self.get_queryset().annotate(
            fullname=User.get_fullname_annotation()
        ).get(id=request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def _handle_current_update(self, request):
        """處理更新當前用戶資訊"""
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=request.method == 'PATCH'
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 保存更新
        serializer.save()
        return Response(serializer.data)
    #endregion


    #region (修改密碼)
    @extend_schema(
        summary="修改密碼",
        description="修改當前登入用戶的密碼",
        request={
            'multipart/form-data': ChangePasswordSerializer,
        },
        responses={
            200: OpenApiResponse(
                description='操作成功'
            ),
            400: OpenApiResponse(
                description='請求數據無效'
            )
        },
        examples=[
            OpenApiExample(
                '修改密碼',
                value={
                    'old_password': 'password',
                    'new_password': 'password123',
                    'confirm_password': 'password123',
                }
            )
        ]
    )
    @action(
        detail=False,  # 不需要指定 ID
        methods=['post'], # 支援的 HTTP 方法
        url_path='change-password', # 路由名稱
        url_name='change-password', # 路由別名
    )
    def change_password(self, request):
        """修改密碼"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 使用 raise_exception=True
        
        # 如果有其他錯誤，也使用 raise
        try:
            serializer.save()
        except Exception as e:
            raise ValidationError(str(e))

        return Response({
            "message": "密碼修改成功",
            "status": "success"
        })
      
    #endregion

    @extend_schema(
        summary="註銷使用者",
        description="將指定使用者設為不可用",
        request={
            'multipart/form-data': UserDeactivationSerializer,
        },
        responses={
            200: OpenApiResponse(description='使用者successfully註銷'),
            400: OpenApiResponse(description='無效的請求')
        }
    )
    @action(
        detail=True,  # 需要指定用戶ID
        methods=['PATCH'],
        url_path='deactivate',
        permission_classes=[IsAdminUser],  # 只有管理員可以註銷
        serializer_class=UserDeactivationSerializer  # 明確指定序列化器
    )
    def deactivate(self, request, pk=None):
        """
        註銷指定的使用者
        """
        user = self.get_object()
        
        serializer = self.get_serializer(
            user, 
            data={
                'is_active': False,
                'reason': request.data.get('reason', None),
                'deactivate_date': request.data.get('deactivate_date', None) 
            }, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        
        # 如果有其他錯誤，也使用 raise
        try:
            serializer.save()
        except Exception as e:
            print(e)
            raise ValidationError(str(e))

        return Response({
            "message": "註銷成功",
            "status": "success"
        })



@extend_schema(
    tags=['系統管理 - 用戶註銷紀錄'],
    request={
        'multipart/form-data': UserDeactivateLogSerializer,
    },
)
class UserDeactivateLogViewSet(PermissionMixin, SwaggerSchemaMixin, CreateWithUserMixin, UpdateWithUserMixin, viewsets.ModelViewSet):
    queryset = UserDeactivateLog.objects.all()
    serializer_class = UserDeactivateLogSerializer
    permission_classes = [IsAuthenticated] # 需要驗證
    filterset_class = UserDeactivateLogFilter # 篩選
    pagination_class = CustomPageNumberPagination # 分頁