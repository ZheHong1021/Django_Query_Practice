from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from .utils.serializers import UserBaseSerializer, UserFieldSerializer
from django.contrib.auth.models import Group
from apps.system.group.serializers import GroupSerializer
from rest_framework.exceptions import ValidationError

class UserSerializer(UserFieldSerializer):
    username = serializers.CharField( # 帳號
        label='帳號', # 欄位名稱
        help_text="帳號 (長度為 4-20 個字元)",
        min_length=4, # 最小長度
        max_length=20, # 最大長度
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="此帳號已被使用"  # 自定義訊息
            )
        ],
        error_messages={
            'required': '請輸入帳號', # 必填
            'min_length': '帳號長度需大於 4', # 長度需大於 4
            'max_length': '帳號長度需小於 20', # 長度需小於 20
        }
    )

    # 用於編輯的 group_ids
    group_ids = serializers.PrimaryKeyRelatedField(
        source='groups',  # 關鍵是這個 source 參數
        many=True,
        queryset=Group.objects.all(),
        required=False,
        write_only=True
    )

    groups = GroupSerializer( # 用於顯示的 group
        many=True, read_only=True
    )

    user_permissions = serializers.SlugRelatedField( # 權限
        many=True, read_only=True, 
        slug_field='codename' # 顯示權限名稱
    )

    class Meta:
        model = User
        exclude = ('password', ) # 排除密碼
        read_only_fields = ['id', 'created_at', 'updated_at', 'date_joined', 'last_login', 'is_superuser']


    # 修改用戶
    def update(self, instance, validated_data):
        #region (Group)
        # 角色處理
        group_ids = validated_data.pop('group_ids', None)

        # 如果沒帶入 groups，則不處理
        if group_ids is not None:
            instance.groups.clear() # 清空權限
            instance.groups.add(*group_ids) # 重新設定權限
        #endregion

        return super().update(instance, validated_data)
    


class UserCurrentSerializer(UserFieldSerializer):
    """用於用戶自身資料更新的序列化器"""
    class Meta:
        model = User
        # 只允許以下字段更新
        fields = ('id', 'username', 'first_name', 'last_name', 'phone', 'gender')
        read_only_fields = ('id', 'username')


# 修改密碼序列化器
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate_new_password(self, value):
        """驗證新密碼"""
        if len(value) < 6:
            raise ValidationError("密碼長度至少需要6個字符")
        if not any(char.isdigit() for char in value):
            raise ValidationError("密碼必須包含數字")
        if not any(char.isupper() for char in value):
            raise ValidationError("密碼必須包含大寫字母")
        if not any(char.islower() for char in value):
            raise ValidationError("密碼必須包含小寫字母")
        return value
    
    def validate(self, data):
        # 驗證新密碼確認
        if data['new_password'] != data['confirm_password']:
            raise ValidationError({
                "confirm_password": "兩次輸入的新密碼不一致"
            })

        # 驗證新舊密碼不能相同
        if data['old_password'] == data['new_password']:
            raise ValidationError({
                "new_password": "新密碼不能與舊密碼相同"
            })

        # 驗證舊密碼是否正確
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise ValidationError({
                "old_password": "舊密碼不正確"
            })

        return data
    
    def save(self, **kwargs):
        """保存新密碼"""
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
