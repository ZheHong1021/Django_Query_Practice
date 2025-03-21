# Generated by Django 4.2.17 on 2025-01-31 04:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_rename_created_by_post_created_by_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_by_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
