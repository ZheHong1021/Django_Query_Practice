from rest_framework import viewsets
from .models import LineUser
from .serializers import LineUserSerializer

from common.pagination import CustomPageNumberPagination
from common.views import SwaggerSchemaMixin
from django.db.models import Value

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse

@extend_schema(
    tags=['Line服務 - 用戶'],
    request={
        'multipart/form-data': LineUserSerializer
    },
)
class LineUserViewSet(
    SwaggerSchemaMixin,
    viewsets.ModelViewSet
):
    queryset = LineUser.objects.all()
    serializer_class = LineUserSerializer
    pagination_class = CustomPageNumberPagination