from rest_framework import serializers
from django.contrib.auth.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    content_type_name = serializers.CharField(
        read_only=True, required=False
    )
    
    model_verbose_name = serializers.CharField(
        read_only=True, required=False
    )
    
    content_type_app_label = serializers.CharField(
        read_only=True, required=False
    )

    action = serializers.CharField( # 操作動作
        read_only=True, required=False
    )

    codename = serializers.CharField( # 不允許修改
        read_only=True, required=False
    )
    content_type = serializers.CharField( # 不允許修改
        read_only=True, required=False
    )
 
    class Meta:
        model = Permission
        fields = "__all__"
      
