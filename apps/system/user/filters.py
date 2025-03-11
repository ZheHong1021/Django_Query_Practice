from django_filters import rest_framework as filters
from .models import User, UserDeactivateLog
from common.filters import SearchFilter, IDsFilter
from django.db.models import Q

class UserFilter(SearchFilter, IDsFilter):
    is_line_connected = filters.BooleanFilter(
        field_name='is_line_connected',
        label='Line 連線狀態',
        help_text='Line 連線狀態',
    )

    class Meta:
        model = User
        fields = [
            'username',
            'is_staff',
            'is_active',
            'is_line_connected',
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