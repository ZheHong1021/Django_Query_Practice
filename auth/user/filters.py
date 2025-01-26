from django_filters import rest_framework as filters
from .models import User
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