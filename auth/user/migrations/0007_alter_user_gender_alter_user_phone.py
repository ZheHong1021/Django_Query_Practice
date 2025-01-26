# Generated by Django 4.2.17 on 2025-01-26 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_gender_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', '男性'), ('F', '女性'), ('O', '其他'), ('N', '不公開')], default='N', max_length=1, verbose_name='性別'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='聯絡電話'),
        ),
    ]
