from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "is_staff"
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

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


class ProfileListSerializer(UserSerializer):
    profile_detail_link = serializers.HyperlinkedIdentityField(
        view_name="users:profile_update",
        lookup_field="pk"
    )
    followers_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "followers_count",
            "first_name",
            "last_name",
            "bio",
            "image",
            "profile_detail_link",
        )


class ProfileDetailUpdateDeleteSerializer(UserSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta(UserSerializer.Meta):
        fields = (UserSerializer.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "bio",
            "image",
            "following",
            "followers",
        ))
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def validate_password(self, value):
        if not value:
            return self.instance.password
        else:
            return value

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class FollowUnfollowSerializer(serializers.Serializer):
    def save(self, **kwargs):
        request = self.context.get("request")
        followed_user = self.context.get("followed_user")
        following_user = request.user

        followed_user.follow_unfollow_user(following_user)

        return followed_user
