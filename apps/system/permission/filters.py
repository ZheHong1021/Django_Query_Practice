from django_filters import rest_framework as filters
from .models import Permission
from common.filters import SearchFilter, IDsFilter
from django.db.models import Q

class PermissionFilter(SearchFilter, IDsFilter):
    class Meta:
        model = Permission
        fields = [
        ]