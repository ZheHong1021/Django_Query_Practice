from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def api_404_handler(request, exception=None):
    if request.path.startswith('/api/'):
        error_response = {
            'type': 'NotFound',
            'message': f'找不到路徑: {request.path}',
            'status_code': status.HTTP_404_NOT_FOUND,
            'detail': {
                'timestamp': datetime.now(),
                'errors': [{
                    'field': 'path',
                    'message': '請求的 API 端點不存在'
                }],
                'path': request.path
            }
        }
        return Response(error_response, status=status.HTTP_404_NOT_FOUND)
    
    # 如果不是 API 請求，使用 Django 默認的 404 處理
    from django.views.defaults import page_not_found
    return page_not_found(request, exception)