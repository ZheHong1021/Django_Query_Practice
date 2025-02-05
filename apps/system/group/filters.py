from django_filters import rest_framework as filters
from .models import Group
from common.filters import SearchFilter, IDsFilter
from django.db.models import Q

class GroupFilter(SearchFilter, IDsFilter):
    class Meta:
        model = Group
        fields = [
        ]