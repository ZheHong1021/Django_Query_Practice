# Generated by Django 4.2.17 on 2025-02-01 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('menu', '0005_alter_menu_component_alter_menu_name_alter_menu_path_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='groups',
            field=models.ManyToManyField(blank=True, db_table='group_menus', help_text='選擇可以訪問此菜單的群組', related_name='menus', to='auth.group', verbose_name='菜單群組'),
        ),
    ]
