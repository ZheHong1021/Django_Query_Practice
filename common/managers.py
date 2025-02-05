from django.db import models

# 不顯示被軟刪除的數據
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

# 只顯示被軟刪除的數據
class AlreadySoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)