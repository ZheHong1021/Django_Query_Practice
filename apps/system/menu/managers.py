from django.db import models
from common.managers import SoftDeleteManager, AlreadySoftDeleteManager
from django.db.models import F, Case, When, Value, BooleanField, OuterRef, Subquery, Exists
class MenuQuerySet(models.QuerySet):
    # 地區別
    def annotate_is_children(self):
        return self.annotate(
            is_children=Case(
                When(parent__isnull=False, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
    

# 不會查詢到被軟刪除的數據
class MenuManager(SoftDeleteManager):
    def get_queryset(self):
        # 擷取軟刪除filter
        qs = super().get_queryset()

        # 得到定義好的QuerySet
        return MenuQuerySet(self.model, using=self._db).filter(id__in=qs.values('id'))
  
    def annotate_is_children(self):
        return self.get_queryset().annotate_is_children()
  