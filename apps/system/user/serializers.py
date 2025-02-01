from rest_framework import serializers
from .models import User, UserDeactivateLog
from rest_framework.validators import UniqueValidator
from .utils.serializers import UserBaseSerializer, UserFieldSerializer
from django.contrib.auth.models import Group
from apps.system.group.serializers import GroupSerializer
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from apps.system.menu.models import Menu
from apps.system.menu.serializers import MenuSerializerWithChildren

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
        read_only_fields = ['id', 'created_at', 'updated_at', 'date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'user_permissions']


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
    groups = GroupSerializer( # 用於顯示的 group
        many=True, read_only=True
    )

    menus = serializers.SerializerMethodField() # 用戶菜單

    """用於用戶自身資料更新的序列化器"""
    class Meta:
        model = User
        # 只允許以下字段更新
        fields = ('id', 'username', 'first_name', 'last_name', 'phone', 'gender', 'groups', 'menus')
        read_only_fields = ('id', 'username', 'groups')
    
    def get_menus(self, instance):
        filters = {}
        # 如果是超級用戶，則不做任何過濾
        if instance.is_superuser:
            group_ids = None
            pass
    
        # 如果是一般用戶，則只顯示啟用的菜單
        else:
            group_ids = instance.groups.values_list('id', flat=True)
            filters['groups__id__in'] = group_ids

        menu_qs = Menu.objects.filter(
            is_disabled=False,
            parent__isnull=True,
            **filters
        ).select_related('parent')\
        .prefetch_related('children')\
        .order_by('priority')

        menus = MenuSerializerWithChildren(
            menu_qs, # QuerySet
            many=True, # 是否為多個
            context={
                "group_ids": group_ids,
            }
        ).data

        """獲取用戶菜單"""
        return menus

class UserDeactivationSerializer(serializers.ModelSerializer):
    reason = serializers.CharField(
        label='註銷原因', # 欄位名稱
        help_text="註銷原因 (長度為 4-100 個字元)",
        write_only=True,  # 只用於寫入，不顯示在回傳資料中
        required=True,   # 非必填
        min_length=4, # 最小長度
        max_length=100, # 最大長度
        error_messages={
            'required': '請輸入註銷原因', # 必填
            'min_length': '註銷原因長度需大於 4', # 長度需大於 4
            'max_length': '註銷原因長度需小於 100', # 長度需小於 100
        }
    )

    deactivate_date = serializers.DateField(
        label='註銷日期', # 欄位名稱
        help_text="註銷日期",
        write_only=True,  # 只用於寫入，不顯示在回傳資料中
        required=False,   # 非必填
    )

    def validate_deactivate_date(self, value):
        """驗證註銷日期"""
        if value is not None and value > timezone.now().date():
            raise ValidationError("註銷日期不能超過今天")
        return value
    
    def validate(self, attrs):
        # 如果 is_active 原本就已經為 False，則不允許註銷
        if self.instance.is_active is False:
            raise ValidationError("用戶已經註銷，無法再次註銷")

        return super().validate(attrs)

    """用於用戶用於註銷的序列化器"""
    class Meta:
        model = User
        # 只允許以下字段更新
        fields = ('id', 'username', 'is_active', 'reason', 'deactivate_date')
        read_only_fields = ('id', 'username')
    
    def update(self, instance, validated_data):
        # 從 validated_data 中取出 reason（如果有的話）
        reason = validated_data.pop('reason', '')
        deactivate_date = validated_data.pop('deactivate_date', None)

        # 如果傳入 is_active 為 False，則進行註銷
        if validated_data.get('is_active') is False:
            # 創建註銷紀錄
            UserDeactivateLog.objects.create(
                user=instance,
                reason=reason,
                deactivate_date=deactivate_date,
                created_by_user=self.context.get('request').user
            )
        
        return super().update(instance, validated_data)


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



# 使用者註銷紀錄
class UserDeactivateLogSerializer(serializers.ModelSerializer):
    user = UserCurrentSerializer( # 被註銷的使用者
        read_only=True
    )
    created_by_user = UserCurrentSerializer( # 註銷者
        read_only=True
    )

    class Meta:
        model = UserDeactivateLog
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_user']