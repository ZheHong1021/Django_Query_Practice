from django.db import models
from common.models import TimeStampedModel, CreatedByModel, UpdatedByModel, ImageModel, BaseUUIDModel
from datetime import datetime, date

class Post(TimeStampedModel, CreatedByModel, UpdatedByModel):
    title = models.CharField("標題", max_length=100)
    content = models.TextField("內容")
    record_date = models.DateField("貼文日期", blank=True, default=date.today)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "post"
        ordering = ["-created_at"]

        verbose_name = '貼文訊息'  # 這會影響權限名稱
        verbose_name_plural = '貼文訊息列表'

class PostImage(BaseUUIDModel, TimeStampedModel, CreatedByModel, UpdatedByModel, ImageModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    class Meta:
        db_table = "post_image"
        ordering = ["-created_at"]

        verbose_name = '貼文圖片'  # 這會影響權限名稱
        verbose_name_plural = '貼文圖片列表'
    
    