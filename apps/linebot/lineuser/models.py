# models.py
from django.db import models
from django.utils import timezone
from common.models import TimeStampedModel
from apps.system.user.models import User

class LineUser(TimeStampedModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name="line_user",
        blank=True,
        db_comment="用戶"
    )

    line_id = models.CharField(
        max_length=255, 
        unique=True, 
        primary_key=True,
        db_comment="LINE ID"
    )
    display_name = models.CharField(
        max_length=255,
        db_comment="顯示名稱"
    )
    picture_url = models.URLField(
        max_length=1024, 
        null=True, blank=True,
        db_comment="頭像"
    )
    email = models.EmailField(
        null=True, blank=True,
        db_comment="電子郵件"
    )
    access_token = models.TextField(db_comment="存取權杖")
    token_expires_at = models.DateTimeField(db_comment="權杖過期時間")
    last_login = models.DateTimeField(
        default=timezone.now,
        db_comment="最後登入時間"
    )

    class Meta:
        db_table = "line_user"
        verbose_name = "LINE 用戶"
        verbose_name_plural = "LINE 用戶"

    def __str__(self):
        return f"{self.display_name} ({self.line_id})"