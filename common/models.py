from django.db import models

# 創建、修改日期的 Abstract Model
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# 創建可以記錄是誰創建的 Abstract Model
class CreatedByModel(models.Model):
    created_by = models.ForeignKey(
        "user.User", 
        on_delete=models.CASCADE, 
        related_name="%(class)s_created_by",
        blank=True,
        null=True
    )

    class Meta:
        abstract = True