from django.core.management.base import BaseCommand
from apps.system.menu.models import Menu
from pathlib import Path
import json

class Command(BaseCommand):
    help = '建立預設菜單結構'

    def get_data_file_path(self):
        FILENAME = 'default_menus.json'
        current_dir = Path(__file__).resolve()
        return current_dir.parent / 'data' / FILENAME
    
    def handle(self, *args, **kwargs):
        data_file = self.get_data_file_path()
        if not data_file.exists():
            self.stdout.write(
                self.style.WARNING(
                    "找不到預設菜單數據文件"
                )
            )
            return
        
        self.process_file(data_file)

    def process_file(self, file_path):
        """處理 JSON 文件並創建或更新菜單"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                menu_data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'找不到檔案 {file_path}'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('無效的 JSON 格式'))
            return

        # 處理每個頂層菜單
        for menu_item in menu_data:
            self.process_menu_item(menu_item)

        self.stdout.write(self.style.SUCCESS('成功創建/更新菜單結構'))

    def process_menu_item(self, item, parent=None):
        """遞迴處理菜單項目及其子項目"""
        try:
            # 嘗試查找具有相同標題的現有菜單
            menu_obj, created = Menu.objects.update_or_create(
                title=item.get('title'),
                parent=parent,
                defaults={
                    'priority': item.get('priority'),
                    'name': item.get('name'),
                    'path': item.get('path'),
                    'component': item.get('component'),
                    'redirect': item.get('redirect', ''),
                    'is_menu': item.get('is_menu', True),
                    'is_directory': item.get('is_directory', False),
                    'is_disabled': item.get('is_disabled', False),
                    'icon': item.get('icon'),
                }
            )

            action = '創建' if created else '更新'
            self.stdout.write(
                self.style.SUCCESS(f'{action}菜單: {menu_obj.title} (ID: {menu_obj.id})')
            )

            # 處理子菜單
            children = item.get('children', [])
            for child in children:
                self.process_menu_item(child, parent=menu_obj)

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'處理菜單 {item.get("title")} 時發生錯誤: {str(e)}')
            )