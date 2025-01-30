from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from .models import GroupProfile
# from core.auth.permissions.serializers import PermissionSerializer
from django.db import transaction
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator


# MySQL View(Merge Profile and Group)
class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField( # 群組代號
        required=True,
        help_text="請輸入字元長度2~20且不重複的群組代號。",
        min_length=2,
        max_length=20,
        validators = [
            UniqueValidator(
                queryset=Group.objects.filter(profile__is_deleted=False),
                message="該群組代號已經被使用，請使用其他群組代號!"
            )
        ],
        error_messages={
            'required': '群組代號是必填的，請提供完整。',
            'min_length': '群組代號長度需大於 2', # 長度需大於 2
            'max_length': '群組代號長度需小於 20', # 長度需小於 20
        },
    )

    name_zh = serializers.CharField( # 角色中文名稱
        source='profile.name_zh',
        required=True,
        help_text="請輸入字元長度2~8且不重複的群組名稱。",
        min_length=2,
        max_length=8,
        error_messages={
            'required': '群組名稱是必填的，請提供完整。',
            'min_length': '群組名稱長度需大於 2', # 長度需大於 2
            'max_length': '群組名稱長度需小於 8', # 長度需小於 8
        },
    )

    permissions = serializers.SlugRelatedField( # 群組
        many=True, read_only=True, 
        slug_field='id' # 顯示群組名稱
    )

    # # 權限
    # permissions = serializers.CharField(
    #     required=True,
    #     help_text="請填寫權限ID，多個權限ID請用逗號分隔(EX: id_1,id_2,id_3)。",
    #     error_messages={
    #         'required': '分配權限是必填的，請提供完整。',
    #     },
    # )

    class Meta:
        model = Group
        fields = "__all__"
        
    
    # 驗證群組名稱是否存在 (透過這樣方式不會有多餘的查詢)
    def validate_name_zh(self, value):
        # 如果是更新且名稱沒有變更，則不驗證
        if self.instance and self.instance.profile.name_zh == value:
            return value
        
        # 如果名稱已經存在，則拋出錯誤
        if GroupProfile.objects.filter(name_zh__exact=value).exists():
            raise serializers.ValidationError("該角色名稱已經存在!")
        return value

    # 創建
    @transaction.atomic # 確認都正確才執行操作
    def create(self, validated_data):
        # 取出 profile data
        profile_data = validated_data.pop('profile')

        # # 取出權限
        # permissions = validated_data.pop('permissions', None) # 取出權限
        
        try:
            # 創建 Group
            group = Group.objects.create(**validated_data) # 創建 Group

            # 創建 Group Profile
            group_profile = GroupProfile.objects.create( 
                **profile_data,
                group=group, 
            )

            # # 權限
            # if permissions:
            #     permissions = permissions.split(',') # 轉換成 List
            #     group.permissions.add(*permissions) # 添加權限

        except Exception as e:
            raise serializers.ValidationError(str(e))
       
        return group

    @transaction.atomic # 確認都正確才執行操作
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None) # 取出 Profile Data
        # permissions_data = validated_data.pop('permissions', None) # 取出 Group Data

        # 更新 Profile
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        # # 權限
        # if permissions_data is not None:
        #     instance.permissions.clear() # 清空權限
        #     if permissions_data:
        #         permissions_data = permissions_data.split(',') # 轉換成 List
        #         instance.permissions.add(*permissions_data) # 添加權限

        return super().update(instance, validated_data)
    
     # # 如果还需要通过GET方法获取权限数据
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['permissions'] = PermissionSerializer(
    #         instance.permissions.all(), many=True
    #     ).data
    #     return representation