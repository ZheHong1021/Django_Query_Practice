from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import Group, Permission
from .serializers import GroupSerializer
from .filters import GroupFilter
from common.pagination import CustomPageNumberPagination
from common.views import PermissionMixin, SwaggerSchemaMixin
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse

@extend_schema(
    tags=['系統管理 - 角色'],
    request={
        'multipart/form-data': GroupSerializer
    },
)
class GroupViewSet(PermissionMixin, SwaggerSchemaMixin, viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_class = GroupFilter
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return self.queryset.filter(profile__is_deleted=False)

    def perform_destroy(self, instance):
        instance.profile.is_deleted = True
        instance.profile.deleted_at = timezone.now()
        instance.profile.deleted_by = self.request.user
        instance.profile.save()

    @extend_schema(
        summary="更新群組權限",
        description="更新指定群組的權限列表",
        request={"application/json": {
            "type": "object",
            "properties": {
                "permissions": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "權限ID列表"
                }
            }
        }},
        responses={
            200: OpenApiResponse(description="權限更新成功"),
            400: OpenApiResponse(description="更新失敗"),
            404: OpenApiResponse(description="群組不存在")
        }
    )
    @action(detail=True, methods=['patch'])
    def update_permissions(self, request, pk=None):
        """更新群組權限"""
        group = self.get_object()
        permission_ids = request.data.get('permissions', [])
        
        try:
            # 驗證權限 ID 是否存在
            permissions = Permission.objects.filter(id__in=permission_ids)
            if len(permissions) != len(permission_ids):
                return Response(
                    {'error': '某些權限 ID 不存在'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 更新權限
            group.permissions.set(permissions)
            
            return Response({
                'message': '權限更新成功',
                'permissions': list(permissions.values('id', 'name', 'codename'))
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )