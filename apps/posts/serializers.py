from rest_framework import serializers
from .models import Post, PostImage
from common.serializers import UserRelatedSerializerMixin, BaseImageSerializer
from common.validators import FileSizeValidator, FileTypeValidator

class PostSerializer(UserRelatedSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"



class PostImageSerializer(UserRelatedSerializerMixin, BaseImageSerializer):
    path = serializers.FileField(
        validators=[
            FileSizeValidator(max_size_mb=10), # 限制檔案大小
            FileTypeValidator(allowed_types=[ # 限制檔案類型
                'image/png',
                'image/jpg',
                'image/jpeg',
                'image/gif',
                'image/bmp',
                'image/webp',
                'image/svg+xml'
            ])
        ]
    )
    class Meta:
        model = PostImage
        fields = "__all__"
        read_only_fields = (
            'id', 
            'created_by_user', 'created_at', 
            'updated_by_user', 'updated_at',
        )