from rest_framework import serializers
from ..models import GENDER_CHOICES

# 用戶基本序列化器
class UserBaseSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(
        source='get_gender_display', read_only=True,
        help_text="性別"
    )
    fullname = serializers.CharField(
        read_only=True,
        help_text="全名"
    )
    is_line_connected = serializers.BooleanField(
        read_only=True,
        help_text="是否連接 Line 帳號"
    )
     
    
# 用戶欄位序列化器
class UserFieldSerializer(UserBaseSerializer):
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
        required=True # 非必填
    )
    phone = serializers.CharField( # 手機號碼
        label='手機號碼', # 欄位名稱
        help_text="手機號碼 (長度為 10 個字元)",
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

    email = serializers.EmailField( # 電子郵件(暫時用不到)
        required=False,
    )