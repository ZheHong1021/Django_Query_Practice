from django.db import models
from common.models import TimeStampedModel, CreatedByModel
from datetime import datetime

class Post(TimeStampedModel, CreatedByModel):
    title = models.CharField("標題", max_length=100)
    content = models.TextField("內容")
    record_date = models.DateField("貼文日期", blank=True, default=datetime.today)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "post"
        ordering = ["-created_at"]