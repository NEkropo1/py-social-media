import uuid

from django.db import transaction
from rest_framework import serializers
from rest_framework.reverse import reverse

from social_media.models import Post, PostImage


class PostImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("image", "title")


class PostListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source="owner.email")
    hashtags = serializers.SerializerMethodField()
    message_link = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    image_upload = serializers.ImageField(
        allow_empty_file=True,
        allow_null=True,
        write_only=True,
    )

    class Meta:
        model = Post
        fields = (
            "owner_email",
            "hashtags",
            "message_short",
            "message",
            "message_link",
            "image",
            "image_upload"
        )
        extra_kwargs = {"message": {"write_only": True, "min_length": 1}}

    def get_hashtags(self, obj):
        return obj.hashtags()

    def get_message_link(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(reverse("api:post-detail", args=[obj.id]))

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.Images.exists():
            image = obj.Images.first()
            return request.build_absolute_uri(image.image.url)
        return None

    def create(self, validated_data):
        image = validated_data.pop("image_upload", None)
        owner_id = self.context["request"].user.id
        post = Post.objects.create(owner_id=owner_id, **validated_data)

        if image:
            title = f"{post.id}-{uuid.uuid4()}"
            PostImage.objects.create(image=image, title=title, post=post)

        return post


class PostDetailSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source="owner.email")
    hashtags = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "hashtags",
            "message",
            "owner_email",
            "image",
        )
    def get_hashtags(self, obj):
        return obj.hashtags()

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.Images.exists():
            image = obj.Images.first()
            return request.build_absolute_uri(image.image.url)
        return None
