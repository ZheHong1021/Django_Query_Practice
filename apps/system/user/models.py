from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid
from .managers import CustomUserManager

GENDER_CHOICES = (
    ('M', _('男性')),
    ('F', _('女性')),
    ('O', _('其他')),
    ('N', _('不公開')),
)

class User(AbstractBaseUser, PermissionsMixin):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    first_name = models.CharField("名字", max_length=30, blank=True, null=False)
    last_name = models.CharField("姓氏", max_length=30, blank=True, null=True)

    phone = models.CharField("聯絡電話", max_length=15, blank=True, null=True)
    gender = models.CharField("性別", max_length=1, choices=GENDER_CHOICES, blank=True, default='N')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"
        verbose_name = '用戶'  # 這會影響權限名稱
        verbose_name_plural = '用戶列表'

        permissions = [
            ("export_user", "匯出使用者"),
        ]