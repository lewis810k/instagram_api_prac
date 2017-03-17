from rest_framework import serializers

from post.models import PostPhoto, Post

__all__ = (
    'PostPhotoSerializer',
)


class PostPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostPhoto
        fields = (
            'post',
            'photo',
            'created_date',
        )
