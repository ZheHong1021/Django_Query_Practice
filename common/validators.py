from rest_framework import serializers
from django.core.files.uploadedfile import UploadedFile

# [驗證檔案大小]
# ● max_size_mb: 最大檔案大小(MB)
# ------------------------------------------------
# 【Example】
# FileSizeValidator(max_size_mb=10)
class FileSizeValidator:
    def __init__(self, max_size_mb):
        self.max_size_mb = max_size_mb

    def __call__(self, value):
        if isinstance(value, UploadedFile):
            if value.size > self.max_size_mb * 1024 * 1024:
                raise serializers.ValidationError(
                    f'檔案大小不能超過 {self.max_size_mb}MB。'
                    f'目前大小：{value.size / (1024 * 1024):.2f}MB'
                )

# [驗證檔案類型]
# ● allowed_types: 支援的檔案類型
# ------------------------------------------------
# 【Example】
# FileTypeValidator(allowed_types=[
#     'video/mp4',
#     'video/quicktime',
#     'video/x-msvideo'
# ])
class FileTypeValidator:
    def __init__(self, allowed_types):
        self.allowed_types = allowed_types

    def __call__(self, value):
        if isinstance(value, UploadedFile):
            if value.content_type not in self.allowed_types:
                raise serializers.ValidationError(
                    f'不支援的檔案類型：{value.content_type}。'
                    f'支援的類型：{", ".join(self.allowed_types)}'
                )