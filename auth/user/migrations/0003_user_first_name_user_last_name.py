# Generated by Django 4.2.17 on 2025-01-20 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='名字'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='姓氏'),
        ),
    ]
