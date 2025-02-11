from django.db.models import CharField, F, Value, Case, When
from django.db.models.functions import Concat


# 得到綁定用戶的全名
class UserFullnameMixin:
    @classmethod
    def get_user_fullname_annotation(cls, field_prefix):
        """獲取用戶全名的 annotation"""
        return Case(
            When(
                **{f'{field_prefix}__is_superuser': True},
                then=Value('系統管理員')
            ),
            default=Concat(
                F(f'{field_prefix}__last_name'),
                F(f'{field_prefix}__first_name'),
                output_field=CharField()
            )
        )

    @classmethod
    def with_user_fullname(cls):
        """添加創建者和修改者的全名註解"""
        return cls.objects.annotate(
            created_by_user_fullname=cls.get_user_fullname_annotation('created_by_user'),
            updated_by_user_fullname=cls.get_user_fullname_annotation('updated_by_user')
        )