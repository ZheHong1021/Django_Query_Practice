from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from .models import GENDER_CHOICES
from .utils.serializers import UserBaseSerializer

class UserSerializer(UserBaseSerializer):
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
    first_name = serializers.CharField( # 帳號
        label='名字', # 欄位名稱
        help_text="名字 (長度為 1-10 個字元)",
        min_length=1, # 最小長度
        max_length=10, # 最大長度
        error_messages={
            'required': '請輸入名字', # 必填
            'min_length': '名字長度需大於 1', # 長度需大於 4
            'max_length': '名字長度需小於 10', # 長度需小於 20
        }
    )
    last_name = serializers.CharField( # 姓氏
        label='姓氏', # 欄位名稱
        help_text="姓氏 (長度為 1-10 個字元)",
        min_length=1, # 最小長度
        max_length=10, # 最大長度
        error_messages={
            'min_length': '姓氏長度需大於 1', # 長度需大於 4
            'max_length': '姓氏長度需小於 10', # 長度需小於 20
        },
        required=False # 非必填
    )
    phone = serializers.CharField( # 手機號碼
        label='手機號碼', # 欄位名稱
        help_text="手機號碼 (長度為 8-15 個字元)",
        min_length=10, # 最小長度
        max_length=10, # 最大長度
        error_messages={
            'min_length': '手機號碼長度只能為 10碼',
            'max_length': '手機號碼長度只能為 10碼',
        },
        required=False # 非必填
    )
    gender = serializers.ChoiceField( # 性別
        label='性別', # 欄位名稱
        choices=GENDER_CHOICES, # 選項
        help_text="性別",
        error_messages={
            'invalid_choice': '無效的選擇', # 無效選擇
        },
        required=False # 必填
    )

    groups = serializers.SlugRelatedField( # 群組
        many=True, read_only=True, 
        slug_field='name' # 顯示群組名稱
    )
    user_permissions = serializers.SlugRelatedField( # 權限
        many=True, read_only=True, 
        slug_field='codename' # 顯示權限名稱
    )

    class Meta:
        model = User
        exclude = ('password', ) # 排除密碼
        read_only_fields = ['id', 'created_at', 'updated_at', 'date_joined', 'last_login', 'is_superuser']
        write_only_fields = ('password',) # 只允許寫入