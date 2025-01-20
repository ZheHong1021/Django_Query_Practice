from django.utils.translation import gettext_lazy as _

ERROR_TYPE_MESSAGES = {
    # DRF 內建的錯誤類型
    'ValidationError': _('資料驗證失敗'),
    'NotAuthenticated': _('請先進行登入'),
    'AuthenticationFailed': _('身份驗證失敗'),
    'PermissionDenied': _('您沒有權限執行此操作'),
    'NotFound': _('找不到請求的資源'),
    'MethodNotAllowed': _('不允許的請求方法'),
    'Throttled': _('請求次數過多，請稍後再試'),
    
    # 資料庫相關
    'DatabaseError': _('資料庫操作失敗'),
    'IntegrityError': _('資料完整性錯誤'),
    
    # HTTP 相關
    'Http404': _('找不到請求的資源'),
    
    # 自定義業務錯誤
    'BusinessError': _('業務邏輯錯誤'),
    'ResourceNotFoundError': _('找不到請求的資源'),
    'InvalidOperationError': _('無效的操作'),
    
    # 預設錯誤
    'default': _('發生未預期的錯誤')
}