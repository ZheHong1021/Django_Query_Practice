from rest_framework import viewsets
from .models import Post, PostImage
from .serializers import PostSerializer, PostImageSerializer
from .filters import PostFilter, PostImageFilter

from common.pagination import CustomPageNumberPagination
from common.views import CreateWithUserMixin, UpdateWithUserMixin
from django.db.models import Value

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse

@extend_schema(
    tags=['貼文'],
    request={
        'multipart/form-data': PostSerializer
    },
)
class PostViewSet(
    CreateWithUserMixin, 
    UpdateWithUserMixin, 
    viewsets.ModelViewSet
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        qs = Post.with_user_fullname()
        return qs

@extend_schema(
    tags=['貼文圖片'],
    request={
        'multipart/form-data': PostImageSerializer
    },
)
class PostImageViewSet(
    CreateWithUserMixin, 
    UpdateWithUserMixin, 
    viewsets.ModelViewSet
):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    pagination_class = CustomPageNumberPagination
    filterset_class = PostImageFilter

    def get_queryset(self):
        qs = PostImage.with_user_fullname()
        return qs