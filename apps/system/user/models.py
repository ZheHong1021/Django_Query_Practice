from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid
from .managers import CustomUserManager
from common.models import TimeStampedModel, CreatedByModel, UpdatedByModel
from apps.system.menu.models import Menu
from apps.system.menu.serializers import MenuSerializerWithChildren
from django.db.models import CharField, Value, Case, When
from django.db.models.functions import Concat

GENDER_CHOICES = (
    ('M', _('男性')),
    ('F', _('女性')),
    ('O', _('其他')),
    ('N', _('不公開')),
)

class User(AbstractBaseUser, PermissionsMixin):
    # UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, db_comment="使用者帳號")
    email = models.EmailField(blank=True, null=True, db_comment="電子郵件")
    is_staff = models.BooleanField(default=False, db_comment="是否為管理員")
    is_active = models.BooleanField(default=True, db_comment="是否啟用")
    date_joined = models.DateTimeField(default=timezone.now, db_comment="註冊時間")
    first_name = models.CharField("名字", max_length=30, blank=True, null=False, db_comment="名字")
    last_name = models.CharField("姓氏", max_length=30, blank=True, null=True, db_comment="姓氏")
    phone = models.CharField("聯絡電話", max_length=15, blank=True, null=True, db_comment="聯絡電話")
    gender = models.CharField("性別", max_length=1, choices=GENDER_CHOICES, blank=True, default='N', db_comment="性別")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    @property
    def display_fullname(self):
        if self.is_superuser: # 如果是超級用戶，直接顯示名字
            return "系統管理員"
        return f"{self.last_name}{self.first_name}"

    @classmethod
    def get_fullname_annotation(cls):
        return Case(
            When(
                is_superuser=True,
                then=Value('系統管理員')
            ),
            default=Concat('last_name', 'first_name')
        )

    class Meta:
        db_table = "user"
        verbose_name = '用戶'  # 這會影響權限名稱
        verbose_name_plural = '用戶列表'
        indexes = [
            models.Index(fields=['first_name', 'last_name'])
        ]
        permissions = [
            ("export_user", "匯出使用者"),
        ]


class UserDeactivateLog(TimeStampedModel, CreatedByModel, UpdatedByModel):
    user = models.ForeignKey( # 被註銷的使用者
        User, 
        verbose_name="使用者",
        on_delete=models.CASCADE, 
        related_name='deactivate_logs',
        db_comment="使用者ID",
    )
    deactivate_date = models.DateField("註銷日期", blank=True, default=timezone.now, db_comment="註銷日期")    
    reason = models.TextField("註銷原因", blank=True, null=True, db_comment="註銷原因")
 

    def __str__(self):
        return f"{self.user.username} deactivated at {self.deactivate_date}"

    class Meta:
        verbose_name = '使用者註銷紀錄'
        verbose_name_plural = '使用者註銷紀錄'
        ordering = ['-created_at']
        db_table = "user_deactivate_log"

    
    