from django_filters import rest_framework as filters
from django.db.models import Q, CharField, TextField


# 透過搜尋內容篩選數據 (?search=)
class SearchFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search_fields')

    class Meta:
        abstract = True

    # 搜尋所有欄位(包含 annotate)
    def get_search_fields(self, queryset):
        # Get model fields
        model_fields = [
            f.name 
            for f in queryset.model._meta.get_fields() 
            if f.concrete
        ]

        # Get annotated fields
        annotated_fields = list(queryset.query.annotations.keys())
        return model_fields, annotated_fields

    def filter_search_fields(self, queryset, name, value):

        # 從繼承Meta那邊取得 search_fields
        search_fields = getattr(self.Meta, 'search_fields', [])
        annotated_fields = list() # annotate欄位

        # 如果沒有就滾蛋
        model_fields, annotated_fields = self.get_search_fields(queryset)

        # 如果從子 Meta沒拿到 search => 就用全部欄位篩選
        if not search_fields:
            search_fields = model_fields

        query = Q()
        # For raw fields
        for field in search_fields:
            field_object = self.get_field_object(queryset, field)
            if isinstance(field_object, (CharField, TextField)):
                query |= Q(**{f"{field}__icontains": value})
        
        # For annotate fields
        for field in annotated_fields:
            query |= Q(**{f"{field}__icontains": value})

        return queryset.filter(query)
    
    # 得到欄位的屬性
    def get_field_object(self, queryset, field_name):
        """
        Utility method to get the field object from the field name.
        """
        model = queryset.model
        try:
            field_object = model._meta.get_field(field_name)
        except Exception:
            field_object = None

        return field_object



# 透過id列表篩選數據 (?ids=<id1>,<id2>)
class IDsFilter(filters.FilterSet):
    # id列表 (121,131) => 要陣列轉成String
    ids = filters.BaseInFilter(field_name='id', lookup_expr='in')

    class Meta:
        abstract = True

