# core/management/commands/update_all_permissions.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

class Command(BaseCommand):
    help = '更新整個專案的所有權限顯示名稱'

    def add_arguments(self, parser):
        parser.add_argument(
            '--exclude-apps',
            nargs='+',
            default=[],  # 設定默認值為空列表
            help='要排除的應用列表，例如 admin contenttypes sessions'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='預覽將要進行的更改，但不實際執行'
        )
        parser.add_argument(
            '--language',
            default='zh',
            help='指定語言，預設為中文(zh)'
        )

    def get_permission_mapping(self, language='zh'):
        """
        根據語言返回權限名稱映射
        """
        mappings = {
            'zh': {
                'add': '新增',
                'change': '編輯',
                'delete': '刪除',
                'view': '查看',
                'export': '導出',
                'import': '導入',
            },
            'en': {
                'add': 'Create',
                'change': 'Edit',
                'delete': 'Delete',
                'view': 'View',
                'export': 'Export',
                'import': 'Import',
            }
        }
        return mappings.get(language, mappings['en'])

    def get_model_verbose_name(self, model, language='zh'):
        """
        獲取模型的顯示名稱，針對特殊模型進行處理
        """
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        # 特殊模型的顯示名稱映射
        special_models = {
            'zh': {
                ('admin', 'logentry'): '操作日誌',
                ('auth', 'group'): '角色',
                ('auth', 'permission'): '權限',
                ('token_blacklist', 'blacklistedtoken'): '黑名單憑證',
                ('token_blacklist', 'outstandingtoken'): '已發行憑證',
            },
            'en': {
                ('admin', 'logentry'): 'Operation Log',
                ('auth', 'group'): 'Group',
                ('auth', 'permission'): 'Permission',
                ('token_blacklist', 'blacklistedtoken'): 'Blacklisted Token',
                ('token_blacklist', 'outstandingtoken'): 'Outstanding Token',
            }
        }

        # 檢查是否為特殊模型
        model_key = (app_label, model_name)
        if model_key in special_models.get(language, {}):
            return special_models[language][model_key]
        
        return str(model._meta.verbose_name)

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        language = options['language']
        exclude_apps = list(options.get('exclude_apps', []))  # 確保是列表
        
        # 默認排除的應用，移除 'admin', 'auth'
        default_exclude = ['contenttypes', 'sessions']
        exclude_apps.extend(default_exclude)
        
        # 獲取權限名稱映射
        permission_mapping = self.get_permission_mapping(language)
        
        # 統計信息
        updated_count = 0
        skipped_count = 0
        error_count = 0
        
        # 獲取所有已安裝的應用
        all_models = apps.get_models(include_auto_created=True)
        
        self.stdout.write(self.style.NOTICE('開始更新權限名稱...'))
        
        # 處理每個模型的權限
        for model in all_models:
            app_label = model._meta.app_label
            
            # 跳過被排除的應用
            if app_label in exclude_apps:
                self.stdout.write(f'跳過應用: {app_label}')
                continue
                
            model_name = model._meta.model_name
            verbose_name = self.get_model_verbose_name(model, language)
            
            self.stdout.write(f'\n處理模型: {app_label}.{model_name} ({verbose_name})')
            
            try:
                content_type = ContentType.objects.get_for_model(model)
                permissions = Permission.objects.filter(content_type=content_type)
                
                for permission in permissions:
                    try:
                        # 解析權限代碼名
                        action = next(
                            (k for k in permission_mapping.keys() 
                             if permission.codename.startswith(f'{k}_')),
                            None
                        )
                        
                        if action:
                            old_name = permission.name
                            new_name = f'{permission_mapping[action]}{verbose_name}'
                            
                            if old_name != new_name:
                                self.stdout.write(
                                    f'  {old_name} -> {new_name}'
                                )
                                
                                if not dry_run:
                                    permission.name = new_name
                                    permission.save()
                                    updated_count += 1
                            else:
                                skipped_count += 1
                        else:
                            # 處理自定義權限
                            self.stdout.write(
                                self.style.WARNING(
                                    f'  跳過自定義權限: {permission.codename}'
                                )
                            )
                            skipped_count += 1
                            
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f'  更新權限出錯 {permission.codename}: {str(e)}'
                            )
                        )
                        error_count += 1
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'處理模型出錯 {app_label}.{model_name}: {str(e)}'
                    )
                )
                error_count += 1
                continue
        
        # 輸出統計信息
        self.stdout.write('\n' + '='*50)
        status = '預覽' if dry_run else '更新'
        self.stdout.write(self.style.SUCCESS(
            f'{status}完成！\n'
            f'- 更新的權限數量: {updated_count}\n'
            f'- 跳過的權限數量: {skipped_count}\n'
            f'- 錯誤的權限數量: {error_count}'
        ))