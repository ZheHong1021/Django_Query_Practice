from django.db import models
from common.models import BaseUUIDModel, SoftDeleteModel, TimeStampedModel
from django.db.models import Q
from django.contrib.auth.models import Group
import uuid
from .managers import MenuManager


# Create your models here.
class Menu(BaseUUIDModel, SoftDeleteModel, TimeStampedModel):
    priority = models.IntegerField("顯示順位", null=True, blank=True, db_comment="顯示順位")
    title = models.CharField("菜單名稱", max_length=50, blank=True, db_comment="菜單名稱")
    name = models.CharField("菜單路由名稱", max_length=50, blank=True, null=True, db_comment="菜單路由名稱")
    path = models.CharField("菜單路由路徑", max_length=50, blank=True, null=True, db_comment="菜單路由路徑")
    component = models.CharField("菜單路由組件", max_length=50, blank=True, null=True, db_comment="菜單路由組件")
    redirect = models.CharField("跳轉路徑", max_length=50, blank=True, null=True, db_comment="跳轉路徑")
    is_menu = models.BooleanField("是否為菜單", blank=True, default=True, db_comment="是否為菜單")
    is_directory = models.BooleanField("是否為目錄", blank=True, default=False, db_comment="是否為目錄")
    is_disabled = models.BooleanField("是否停用", blank=True, default=False, db_comment="是否停用")
    icon = models.CharField("菜單圖案", max_length=50, blank=True, null=True, db_comment="菜單圖案")
    parent = models.ForeignKey(
        'self',
        verbose_name="父級菜單",
        null=True, blank=True, 
        related_name='children', 
        on_delete=models.CASCADE,
        help_text="選擇此菜單項目的父級菜單",
        db_comment="父級菜單ID",
    )

    # 添加與 Group 的多對多關係
    groups = models.ManyToManyField(
        Group,
        verbose_name="菜單群組",
        related_name='menus',
        blank=True,
        help_text="選擇可以訪問此菜單的群組",
        db_table="group_menus"  # 自定義中間表名稱
    )

    objects = MenuManager()
    
    class Meta:
        db_table = "menus"
        ordering = ['priority']
        indexes = [
            models.Index(fields=['priority']),
            models.Index(fields=['parent', 'priority']),
        ]
        constraints = [
            # 條件型唯一索引：只對非 NULL 值進行唯一性檢查
            models.UniqueConstraint(
                fields=['name'],
                name='unique_name_when_not_null',
                condition=Q(name__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['path'],
                name='unique_path_when_not_null',
                condition=Q(path__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['component'],
                name='unique_component_when_not_null',
                condition=Q(component__isnull=False)
            ),
        ]
    
    # 取得菜單名稱
    def __str__(self):
        return self.title or self.name

    # 取得菜單的絕對路徑
    def get_absolute_url(self):
        return self.path

    # 取得菜單的組件
    @property
    def has_children(self):
        return self.children.exists()