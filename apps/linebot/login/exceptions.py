# exceptions.py
from rest_framework.exceptions import APIException
from rest_framework import status

class LineAccountNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "未找到綁定的 LINE 帳號"
    default_code = "line_user_not_found"

class LineUnbindError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "解除綁定時發生錯誤"
    default_code = "database_error"