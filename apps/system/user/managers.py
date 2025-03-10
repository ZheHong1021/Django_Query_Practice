from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Exists, OuterRef

class UserQuerySet(models.QuerySet):
    def with_is_line_connected(self):
        from apps.linebot.lineuser.models import LineUser
        return self.annotate(
            is_line_connected=Exists(
                LineUser.objects.filter(
                    user=OuterRef("id")
                )
            )
        )



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username and password.
        """
        if not username:
            raise ValueError(_("The username must be set"))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)
    
    def with_is_line_connected(self):
        return self.get_queryset().with_is_line_connected()