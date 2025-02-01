from rest_framework import serializers
from .models import Menu

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

# 沒有 Children
class MenuSerializerWithoutChildren(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted', 'deleted_by_user']

# 有 Children
class MenuSerializerWithChildren(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = "__all__"
        

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_children(self, instance):
        # 獲取 request，如果不存在則提供預設值
        # request = self.context.get('request')
        is_menu = self.context.get('is_menu', None)
        is_disabled = self.context.get('is_disabled', None)
        group_ids = self.context.get('group_ids', None)
        children_is_directory = self.context.get('children_is_directory', None)


        # 構建過濾條件
        filters = {}

        if is_menu is not None:
            filters['is_menu'] = is_menu.lower() == 'true'

        if is_disabled is not None:
            filters['is_disabled'] = is_disabled.lower() == 'true'

        if group_ids is not None:
            filters['groups__id__in'] = group_ids
        
        if children_is_directory is not None:
            filters['is_directory'] = children_is_directory

        # 使用構建的過濾條件查詢子菜單
        children = instance.children.filter(**filters).order_by("priority")
        
        # 確保傳遞相同的 context 到子序列化器
        return MenuSerializerWithChildren(
            children, 
            many=True, 
            context=self.context
        ).data