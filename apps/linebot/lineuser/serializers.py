from rest_framework import serializers
from .models import LineUser

class LineUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineUser
        fields = [
            'display_name', 'picture_url', 
            'created_at', 'updated_at', 'last_login'
            # 其他安全的欄位
        ]
        read_only_fields = [
            # 以下資訊為 Line Login API 回傳的用戶資訊(不可修改)
            'display_name', 'picture_url', 'last_login',
            # 以下資訊為系統自動產生(不可修改)
            'created_at', 'updated_at',
        ]

    
  
