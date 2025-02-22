from rest_framework import serializers
from .models import LineUser

class LineUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineUser
        fields = "__all__"
        read_only_fields = [
            # 以下資訊為 Line Login API 回傳的用戶資訊(不可修改)
            'line_id', 'display_name', 'picture_url', 'email', 'access_token', 'token_expires_at', 'last_login',
            # 以下資訊為系統自動產生(不可修改)
            'created_at', 'updated_at',
            # 以下為關聯欄位(不可修改)
            'user'
        ]
    
  
