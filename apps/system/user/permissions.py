from rest_framework import permissions

class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # 檢查是否已認證
        if not request.user.is_authenticated:
            return False
            
        # 允許列表操作
        if view.action == 'list':
            # 如果是管理員或有特定權限的用戶允許訪問列表
            return request.user.is_superuser or request.user.has_perm('user.view_user')
        
        # 允許獲取當前用戶資訊
        if view.action == 'me':
            return True
            
        return True  # 其他操作通過 has_object_permission 控制

    def has_object_permission(self, request, view, obj):
        # 訪客角色只能訪問自己的資料
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_superuser or request.user.has_perm('user.change_user') or obj.id == request.user.id
            
        return False