from django_filters import rest_framework as filters
from .models import Menu
from common.filters import SearchFilter, SelectFieldsFilter

# 轉移出貨
class MenuFilter(SearchFilter, SelectFieldsFilter, filters.FilterSet):
    # 是否為子路由
    is_children = filters.BooleanFilter(
        method='filter_is_children'
    )
    # 是否為Sidebar菜單
    is_menu = filters.BooleanFilter(
        method='filter_is_menu'
    )
    # 是否為目錄
    is_directory = filters.BooleanFilter(
        field_name='is_directory',
    )
    # 是否停用
    is_disabled = filters.BooleanFilter(
        method='filter_is_disabled'
    )
    # 是否包含Children
    include_children = filters.BooleanFilter(
        method='filter_include_children'
    )

    class Meta:
        model = Menu
        fields = ['is_children', 'is_menu', 'include_children']
    
    def filter_is_children(self, queryset, name, value):
        if value:
            return queryset.filter(parent__isnull=False)
        return queryset.filter(parent__isnull=True)
    
    def filter_is_menu(self, queryset, name, value):
        return queryset.filter(is_menu=value)
    
    
    def filter_is_disabled(self, queryset, name, value):
        return queryset.filter(is_disabled=value)
    
    def filter_include_children(self, queryset, name, value):
        return queryset
    