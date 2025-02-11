from rest_framework import serializers


class UserRelatedSerializerMixin:
    def get_user_related_fields(self):
        """獲取與用戶相關的欄位定義"""
        return {
            'created_by_user_fullname': serializers.CharField(read_only=True),
            'updated_by_user_fullname': serializers.CharField(read_only=True),
            'created_by_user': serializers.HiddenField(
                default=serializers.CurrentUserDefault()
            ),
            'updated_by_user': serializers.HiddenField(
                default=serializers.CurrentUserDefault()
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 動態添加用戶相關欄位
        for field_name, field in self.get_user_related_fields().items():
            self.fields[field_name] = field