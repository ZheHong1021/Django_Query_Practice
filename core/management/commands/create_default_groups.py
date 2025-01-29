from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from auth.group.models import GroupProfile  # 請替換 your_app 為你的 app 名稱

class Command(BaseCommand):
    help = '建立預設的群組角色：系統管理員(admin)和一般管理員(manager)'

    def handle(self, *args, **options):
        # 建立系統管理員群組
        admin_group, admin_created = Group.objects.get_or_create(name='admin')
        if admin_created:
            GroupProfile.objects.create(
                group=admin_group,
                name_zh='系統管理員'
            )
            self.stdout.write(self.style.SUCCESS('成功建立系統管理員(admin)群組'))
        else:
            self.stdout.write(self.style.WARNING('系統管理員(admin)群組已存在'))

        # 建立一般管理員群組
        manager_group, manager_created = Group.objects.get_or_create(name='manager')
        if manager_created:
            GroupProfile.objects.create(
                group=manager_group,
                name_zh='一般管理員'
            )
            self.stdout.write(self.style.SUCCESS('成功建立一般管理員(manager)群組'))
        else:
            self.stdout.write(self.style.WARNING('一般管理員(manager)群組已存在'))