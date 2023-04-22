import uuid

from django.db import transaction
from rest_framework import serializers
from rest_framework.reverse import reverse

from social_media.models import Post, PostImage


class PostImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("image", "title")

    @transaction.atomic
    def create(self, validated_data):
        post = self.context["post"]
        image = validated_data["image"]
        title = image.name
        post_image = PostImage.objects.create(
            post=post,
            image=image,
            title=title
        )
        return post_image


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
            "id",
            "owner_email",
            "hashtags",
            "message_short",
            "message_link",
            "image",
            "image_upload",
        )

    def get_hashtags(self, obj):
        return obj.hashtags()

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.Images.exists():
            image = obj.Images.first()
            return request.build_absolute_uri(image.image.url)
        return None

    def get_message_link(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(reverse("api:post-detail", args=[obj.id]))

    @transaction.atomic
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
        exclude = ("id",)
        read_only_fields = ("owner_email", "hashtags", "owner",)

    def get_hashtags(self, obj):
        return obj.hashtags()

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.Images.exists():
            image = obj.Images.first()
            return request.build_absolute_uri(image.image.url)
        return None
