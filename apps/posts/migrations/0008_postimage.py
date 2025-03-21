# Generated by Django 4.2.17 on 2025-02-18 03:33

import common.mixins
import common.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0007_post_updated_by_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_comment='新增時間')),
                ('updated_at', models.DateTimeField(auto_now=True, db_comment='更新時間')),
                ('name', models.CharField(blank=True, error_messages={'unique': '這個檔名已經存在。'}, help_text='可選。如果不指定，將使用上傳的原始檔名', max_length=255, null=True, unique=True, verbose_name='檔名')),
                ('path', models.ImageField(blank=True, help_text='支援的格式：JPG, JPEG, PNG, GIF, WebP', null=True, upload_to=common.models.image_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'], message='只允許上傳 jpg, jpeg, png, gif, webp 格式的圖片'), common.models.validate_image_size], verbose_name='路徑')),
                ('created_by_user', models.ForeignKey(blank=True, db_comment='創建用戶', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by_user', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='posts.post')),
                ('updated_by_user', models.ForeignKey(blank=True, db_comment='修改用戶', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_by_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '貼文圖片',
                'verbose_name_plural': '貼文圖片列表',
                'db_table': 'post_image',
                'ordering': ['-created_at'],
            },
            bases=(common.mixins.UserFullnameMixin, models.Model),
        ),
    ]
