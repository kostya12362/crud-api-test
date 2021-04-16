from rest_framework import serializers, status
from rest_framework.response import Response
from crud.models import Post, Comment
from django.contrib.auth.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class CommentSerializer(serializers.ModelSerializer):
    author_comments = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        print(request.user)
        validated_data["author"] = request.user
        obj = Comment.objects.create(**validated_data)
        return obj


class PostSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "link", "author", "create", "upvotes_count")


class PostDetailCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "created",
            "author",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    comments = PostDetailCommentSerializer(many=True, read_only=True)
    author = UserDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "link",
            "create",
            "upvotes_count",
            "comments",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        print(request.user)
        validated_data["author"] = request.user
        obj = Post.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if instance.author == request.user:
            obj = Post.objects.update(**validated_data)
            return obj
        else:
            raise serializers.ValidationError({"error": "You did not update this post"})
