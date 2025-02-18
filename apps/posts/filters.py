from django_filters import rest_framework as filters
from .models import Post, PostImage
from common.filters import CreatedByFilter, UpdatedByFilter

class PostFilter(CreatedByFilter, UpdatedByFilter):
    class Meta:
        model = Post
        fields = []

class PostImageFilter(CreatedByFilter, UpdatedByFilter):
    post_id = filters.NumberFilter(field_name='post_id')
    class Meta:
        model = PostImage
        fields = ['post_id']