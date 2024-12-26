from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from .filters import PostFilter

from common.pagination import CustomPageNumberPagination

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse

@extend_schema(
    tags=['貼文'],
    request={
        'multipart/form-data': PostSerializer
    },
)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter
    pagination_class = CustomPageNumberPagination