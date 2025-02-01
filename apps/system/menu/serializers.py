from rest_framework import serializers
from .models import Menu

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

# 沒有 Children
class MenuSerializerWithoutChildren(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"

# 有 Children
class MenuSerializerWithChildren(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = "__all__"

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_children(self, instance):
        request = self.context.get('request')
        is_menu = request.query_params.get('is_menu', None)
        is_disabled = request.query_params.get('is_disabled', None)

        filters = {}
        if is_menu is not None:
            filters['is_menu'] = is_menu.lower() == 'true'

        if is_disabled is not None:
            filters['is_disabled'] = is_disabled.lower() == 'true'

        children = instance.children.filter(**filters).order_by("priority")
        return MenuSerializerWithChildren(children, many=True, context=self.context).data