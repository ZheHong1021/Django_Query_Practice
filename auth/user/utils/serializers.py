from rest_framework import serializers


class UserBaseSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    fullname = serializers.CharField(read_only=True)
     