from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from datetime import datetime
from .error_types import ERROR_TYPE_MESSAGES
from django.http import Http404
from rest_framework.exceptions import (
    APIException,
    ValidationError,
    NotAuthenticated,
    AuthenticationFailed,
    PermissionDenied,
    NotFound,
    MethodNotAllowed,
    Throttled
)

# 建立自訂的 Exception Handler
def custom_exception_handler(exc, context):
    # 呼叫預設的 exception_handler
    response = exception_handler(exc, context)

    # 定義錯誤回應格式
    error_response = {
        'type': exc.__class__.__name__, # 錯誤類型
        'message': '', # 錯誤訊息
        'status_code': '', # 錯誤狀態碼
        'detail': {
            'timestamp': datetime.now(), # 錯誤時間
            'errors': [], # 錯誤訊息
            'path': context['request'].path # 錯誤路徑
        }
    }

    # 從 ERROR_TYPE_MESSAGES 取得對應的錯誤訊息
    error_type = exc.__class__.__name__
    error_response['message'] = ERROR_TYPE_MESSAGES.get(
        error_type,
        ERROR_TYPE_MESSAGES['default']
    )

    # 如果 response 不是 None (代表有錯誤)
    if response is not None:
        error_response['status_code'] = response.status_code # 錯誤狀態碼

        # 處理 Method Not Allowed (405)
        if isinstance(exc, MethodNotAllowed):
            error_response['message'] = ERROR_TYPE_MESSAGES['MethodNotAllowed'].format(context['request'].method)
            error_response['errors'] = [{ # 錯誤訊息
                'field': 'method',
                'message': str(exc)
            }],
            return Response(error_response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # 處理 Not Found (404)
        if isinstance(exc, Http404):
            error_response['message'] = ERROR_TYPE_MESSAGES.get('Http404', '找不到指定的資源')
            error_response['errors'] = [{ # 錯誤訊息
                'field': 'id',
                'message': str(exc)
            }]
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

        # 定義錯誤訊息
        if isinstance(exc.detail, dict):
            errors = [
                {
                    'field': field, # 欄位
                    'message': str(error[0]) if isinstance(error, list) else str(error)
                }
                for field, error in exc.detail.items()
            ]
            error_response['detail']['errors'] = errors

        return Response(error_response, status=response.status_code)

    # 處理非 DRF 例外
    else:
        error_response['message'] = str(exc) # 錯誤訊息
        error_response['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)