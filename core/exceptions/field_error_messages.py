# error_messages.py
from django.utils.translation import gettext_lazy as _

FIELD_ERROR_MESSAGES = {
    'min_length': _('長度不得少於 {min_length} 個字元'),
    'max_length': _('長度不得超過 {max_length} 個字元'),
    'required': _('此欄位為必填'),
    'blank': _('此欄位不能為空白'),
    'unique': _('此{field_name}已被使用'),
    'null': _('此欄位不允許空值'),
}