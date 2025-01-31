from django_filters import rest_framework as filters
from .models import User, UserDeactivateLog
from common.filters import SearchFilter, IDsFilter
from django.db.models import Q

class UserFilter(SearchFilter, IDsFilter):
    class Meta:
        model = User
        fields = [
            'username',
            'is_staff',
            'is_active',
        ]

class UserDeactivateLogFilter(SearchFilter, IDsFilter):
    user_id = filters.CharFilter(
        field_name='user',
        lookup_expr='exact',
        label='用戶 ID',
        help_text='用戶 ID',
    )
    class Meta:
        model = UserDeactivateLog
        fields = [
            'user_id'
        ]