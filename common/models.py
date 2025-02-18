from django.db import models
from django.utils import timezone
from .managers import SoftDeleteManager, AlreadySoftDeleteManager
from .mixins import UserFullnameMixin
import os
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from pathlib import Path
from uuid import uuid4

# 創建、修改日期的 Abstract Model
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(db_comment="新增時間", auto_now_add=True)
    updated_at = models.DateTimeField(db_comment="更新時間", auto_now=True)

    class Meta:
        abstract = True


# 創建可以記錄是誰創建的 Abstract Model
class CreatedByModel(UserFullnameMixin, models.Model):
    created_by_user = models.ForeignKey(
        "user.User", 
        db_comment="創建用戶",
        on_delete=models.CASCADE, 
        related_name="%(class)s_created_by_user",
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

# 創建可以記錄是誰修改的 Abstract Model
class UpdatedByModel(UserFullnameMixin, models.Model):
    updated_by_user = models.ForeignKey(
        "user.User", 
        db_comment="修改用戶",
        on_delete=models.CASCADE, 
        related_name="%(class)s_updated_by_user",
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


# UUID作為主鍵
class BaseUUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    class Meta: 
        abstract = True


# 軟刪除
class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(db_comment="是否被軟刪除", default=False)
    deleted_at = models.DateTimeField(db_comment="刪除時間", null=True, blank=True, default=None)
    deleted_by_user = models.ForeignKey(
        "user.User",
        db_comment="刪除用戶",
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



#region (圖片上傳)
def sanitize_filename(filename):
    """安全的檔名處理，避免特殊字元和空白"""
    name, ext = os.path.splitext(filename)
    # 使用 slugify 處理檔名，移除特殊字元
    safe_name = slugify(name)
    if not safe_name:  # 如果 slugify 後為空
        safe_name = uuid4().hex
    return f"{safe_name}{ext.lower()}"

def generate_uuid_filename(filename):
    """生成 UUID 檔名"""
    ext = filename.split('.')[-1].lower()
    return f'{uuid4().hex}.{ext}'

def image_upload_path(instance, filename):
    """處理圖片上傳路徑"""
    filename = generate_uuid_filename(filename)
    # 如果 instance.name 還沒設定，順便設定它
    if not instance.name:
        instance.name = os.path.splitext(filename)[0]
    return os.path.join(instance.get_upload_to(), filename)

def validate_image_size(value):
    """驗證圖片大小（預設最大 10MB）"""
    max_size = getattr(settings, 'MAX_IMAGE_SIZE', 10 * 1024 * 1024)  # 5MB
    if value.size > max_size:
        raise ValidationError(
            _('圖片大小不能超過 %(size)s MB'),
            params={'size': max_size / (1024 * 1024)}
        )

class ImageModel(models.Model):
    name = models.CharField(
        '檔名',
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        error_messages={
            'unique': "這個檔名已經存在。"
        },
        help_text=_('可選。如果不指定，將使用上傳的原始檔名'),
        db_comment="檔名"
    )

    path = models.ImageField(
        '路徑',
        upload_to=image_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'],
                message=_('只允許上傳 jpg, jpeg, png, gif, webp 格式的圖片')
            ),
            validate_image_size
        ],
        null=True,
        blank=True,
        help_text=_('支援的格式：JPG, JPEG, PNG, GIF, WebP'),
        db_comment="圖片路徑"
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']
        verbose_name = _('圖片')
        verbose_name_plural = _('圖片')

    def __str__(self):
        return self.name or str(self.path)

    def get_upload_to(self):
        """
        定義上傳路徑，可被子類別覆寫
        預設路徑為 'images/模型名稱/'
        """
        model_name = self._meta.model_name
        return os.path.join('images', model_name)

    def clean(self):
        """額外的驗證邏輯"""
        super().clean()
        if self.name:
            self.name = sanitize_filename(self.name)

    def save(self, *args, **kwargs):
        # 如果更新圖片，刪除舊檔案
        if self.pk:
            try:
                old_instance = self.__class__.objects.get(pk=self.pk)
                if old_instance.path and self.path != old_instance.path:
                    old_path = os.path.join(settings.MEDIA_ROOT, str(old_instance.path))
                    if os.path.exists(old_path):
                        os.remove(old_path)
            except self.__class__.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """刪除實例時同時刪除實體檔案"""
        if self.path:
            img_path = os.path.join(settings.MEDIA_ROOT, str(self.path))
            if os.path.exists(img_path):
                os.remove(img_path)
        super().delete(*args, **kwargs)

    @property
    def file_size(self):
        """取得檔案大小（bytes）"""
        if self.path and os.path.exists(self.path.path):
            return os.path.getsize(self.path.path)
        return 0

    @property
    def file_extension(self):
        """取得檔案副檔名"""
        if self.path:
            return os.path.splitext(self.path.name)[1].lower()
        return ''
#endregion