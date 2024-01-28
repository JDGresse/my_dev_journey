# post/serializer.py

from rest_framework import serializers
from .models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "body",
            "created_on",
        ]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post", "liked_by", "liked_on"]
