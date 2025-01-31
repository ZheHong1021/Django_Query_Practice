from django.db import models
from django.utils import timezone
from .managers import SoftDeleteManager, AlreadySoftDeleteManager


# 創建、修改日期的 Abstract Model
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# 創建可以記錄是誰創建的 Abstract Model
class CreatedByModel(models.Model):
    created_by_user = models.ForeignKey(
        "user.User", 
        on_delete=models.CASCADE, 
        related_name="%(class)s_created_by_user",
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

# 創建可以記錄是誰修改的 Abstract Model
class UpdatedByModel(models.Model):
    updated_by_user = models.ForeignKey(
        "user.User", 
        on_delete=models.CASCADE, 
        related_name="%(class)s_updated_by_user",
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


# UUID作為主鍵
import uuid
class BaseUUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta: 
        abstract = True


# 軟刪除
class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    deleted_by_user = models.ForeignKey(
        "user.User",
        related_name='deleted_%(class)s',
        on_delete=models.CASCADE,
        null=True, blank=True, default=None
    )

    objects = SoftDeleteManager() # 預設管理器 
    all_objects = models.Manager() # 當需要搜尋到被軟刪除資料的管理器。[使用方式] Model.all_objects.all()
    delete_objects = AlreadySoftDeleteManager() # 已經被軟刪除的數據

    class Meta:
        abstract = True

    # 軟刪除
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now() # 添加刪除時間
        self.deleted_by_user = self.user # 添加刪除者

        # 保存刪除相關資訊
        super(SoftDeleteModel, self).save(
            update_fields=[
                'is_deleted', 
                'deleted_at', 
                'deleted_by_user'
            ])

    # 硬刪除
    def hard_delete(self, *args, **kwargs):
        super(SoftDeleteModel, self).delete()

    
    # 恢復軟刪除數據
    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by_user = None
        self.save()

