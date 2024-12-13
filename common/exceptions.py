from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

# 建立自訂的 Exception Handler
def custom_exception_handler(exc, context):
    # 呼叫預設的 exception_handler
    response = exception_handler(exc, context)

    
    # 如果 response 不是 None (代表有錯誤)
    if response is not None:
        # 自定義錯誤格式
        response.data = {
            'error': {
                'type': exc.__class__.__name__, # 錯誤類型
                'message': response.data.get('detail', str(exc)), # 錯誤訊息
                'status_code': response.status_code, # 錯誤狀態碼
            }
        }
    
    # 處理非 DRF 例外
    else:
        response = Response(
            {
                'error': {
                    'type': exc.__class__.__name__, # 錯誤類型
                    'message': str(exc), # 錯誤訊息
                    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, # 錯誤狀態碼
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return response
    