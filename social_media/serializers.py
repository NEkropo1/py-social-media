import uuid

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from social_media.models import Post, PostImage


class BaseUserSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "is_staff",
            "posts_count",
            "following_count",
            "followers_count",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def get_posts_count(self, obj):
        return obj.posts.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + (
            "posts", "following", "followers"
        )

    @transaction.atomic
    def create(self, validated_data):
        following = validated_data.pop("following", [])
        followers = validated_data.pop("followers", [])
        posts = validated_data.pop("posts", [])
        user = super().create(validated_data)
        user.following.set(following)
        user.followers.set(followers)
        user.posts.set(posts)
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        following = validated_data.pop("following", [])
        followers = validated_data.pop("followers", [])
        posts = validated_data.pop("posts", [])
        user = super().create(validated_data)
        user.following.set(following)
        user.followers.set(followers)
        user.posts.set(posts)
        return user


class UserListSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields


class UserDetailSerializer(BaseUserSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="post-detail"
    )
    following = UserSerializer(many=True, read_only=True)
    followers = UserSerializer(many=True, read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + (
            "posts", "following", "followers"
        )


class PostImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("image", "title")

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
    image = serializers.SerializerMethodField()

    image_upload = serializers.ImageField(
        allow_empty_file=True,
        allow_null=True,
        write_only=True,
    )

    class Meta:
        model = Post
        fields = ("id", "message", "owner_email", "hashtags", "image", "image_upload")

    def get_hashtags(self, obj):
        return obj.hashtags()

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.Images.exists():
            image = obj.Images.first()
            return request.build_absolute_uri(image.image.url)
        return None

    def create(self, validated_data):
        image = validated_data.pop("image_upload", None)  # Use the new field for uploading images
        owner_id = self.context["request"].user.id
        post = Post.objects.create(owner_id=owner_id, **validated_data)

        if image:
            title = f"{post.id}-{uuid.uuid4()}"
            PostImage.objects.create(image=image, title=title, post=post)

        return post


class UserFollowingSerializer(serializers.ModelSerializer):
    follow = serializers.StringRelatedField(source=get_user_model().following)
    class Meta:
        model = get_user_model()
        fields = ("followed",)


class UserFollowedSerializer(serializers.ModelSerializer):
    follow = serializers.StringRelatedField(source=get_user_model().followers)
    class Meta:
        model = get_user_model()
        fields = ("followed",)
