from rest_framework import viewsets
from .models import Menu
from .serializers import \
    MenuSerializerWithoutChildren, \
    MenuSerializerWithChildren
from .filters import MenuFilter
from rest_framework.permissions import IsAuthenticated # 權限
from common.pagination import CustomPageNumberPagination
from common.views import PermissionMixin, SwaggerSchemaMixin, SoftDeleteModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse

@extend_schema(
    tags=['系統管理 - 菜單'],
    request={
        'multipart/form-data': MenuSerializerWithoutChildren
    },
)
class MenuViewSet(PermissionMixin, SwaggerSchemaMixin, SoftDeleteModelViewSet, viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    filterset_class = MenuFilter
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializerWithoutChildren
    pagination_class = CustomPageNumberPagination

    # 將query傳遞給 Serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()

        # 子菜單是否為目錄
        children_is_directory = self.request.query_params.get('children_is_directory', None)
        context["children_is_directory"] = children_is_directory.lower() == 'true' \
                                            if children_is_directory is not None \
                                            else None
        # context.update({"request": self.request})
        return context
    
    # 挑選要哪一個
    def get_serializer_class(self):

        # 是否包含子菜單
        include_children = self.request.query_params.get('include_children', 'false').lower() == 'true'
        if include_children:
            return MenuSerializerWithChildren
        return self.serializer_class