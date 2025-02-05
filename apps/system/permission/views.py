from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.contrib.auth.models import Permission
from django.db.models import F, Value, CharField, Case, When

from common.pagination import CustomPageNumberPagination
from common.views import PermissionMixin, SwaggerSchemaMixin

from .serializers import PermissionSerializer
from .filters import PermissionFilter

@extend_schema(
    tags=['系統管理 - 權限'],
    request={
        'multipart/form-data': PermissionSerializer
    },
)
class PermissionViewSet(PermissionMixin, SwaggerSchemaMixin, viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filterset_class = PermissionFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(
            content_type_name=F('content_type__model'), # 透過外鍵取得(content_type中的name)欄位
            content_type_app_label=F('content_type__app_label'), # 透過外鍵取得(content_type中的app_label)欄位
            action = Case(
                When(codename__contains='view', then=Value('查看')),
                When(codename__contains='add', then=Value('新增')),
                When(codename__contains='change', then=Value('修改')),
                When(codename__contains='delete', then=Value('刪除')),
                When(codename__contains='export', then=Value('匯出')),
                default=Value('其他'),
                output_field=CharField()
            )
        )
        return qs
    