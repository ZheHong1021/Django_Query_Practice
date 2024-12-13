from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 自訂 TokenObtainPairSerializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # 將 user_id 加入 data 中
        # data['user_id'] = self.user.id
        return data
