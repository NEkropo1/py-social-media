from django.contrib.auth import get_user_model
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


class UserListSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields


class UserDetailSerializer(BaseUserSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="post-detail"
    )
    following = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="user-detail"
    )
    followers = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="user-detail"
    )

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + (
            "posts", "following", "followers"
        )


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("id", "image")


class PostListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source="owner.email")
    hashtags = serializers.SerializerMethodField()
    images = PostImageSerializer(many=True)

    class Meta:
        model = Post
        fields = ("id", "message", "owner_email", "hashtags", "images")

    def get_hashtags(self, obj):
        return obj.hashtags()


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
