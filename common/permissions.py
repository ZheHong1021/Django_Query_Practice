from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    def has_permission(self, request, view):
        # 用戶資訊
        user = request.user

        # 如果用戶是超級使用者 => 直接PASS
        if user.is_superuser: return True

        # 當前API Action需要的權限 codename
        required_permission = getattr(view, 'required_permission', None)

        # 需要驗證
        if required_permission:
            # 當前用戶可以執行的權限(codename)
            permissions = set() # 使用集合(查詢效率較高且不重複)

            # 用戶的Permission
            user_permissions = user.user_permissions.values_list("codename", flat=True)
            permissions.update(user_permissions)

            # 該用戶的群組資訊
            groups = user.groups.all()

            for group in groups:
                # 群組的Permission
                # group_permissions = group.permissions.values()
                group_permissions = group.permissions.values_list("codename", flat=True)
                permissions.update(group_permissions)

            return required_permission in permissions # 驗證是否存在
            

        return True