from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, generics

from social_media.models import Post, User
from .serializers import (
    UserSerializer,
    UserListSerializer,
    UserDetailSerializer,
    PostListSerializer,
    UserFollowingSerializer,
    UserFollowedSerializer,
)


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows users to be
    viewed, created, updated, or deleted.
    """
    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        elif self.action == "retrieve":
            return UserDetailSerializer
        else:
            return UserSerializer

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        if self.action == "list":
            return queryset.prefetch_related("followers", "following", "posts")
        elif self.action == "retrieve":
            return queryset.prefetch_related("followers", "following", "posts")
        else:
            return UserSerializer


class PostListView(generics.CreateAPIView, generics.ListAPIView):
    """
    API endpoint that allows posts to be listed.
    """
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class UserFollowingView(generics.ListAPIView):
    """
    API endpoint that allows users to see who they are following.
    """
    serializer_class = UserFollowingSerializer

    def get_queryset(self):
        user = self.request.user
        return user.following.all()


class UserFollowedView(generics.ListAPIView):
    """
    API endpoint that allows users to see who is following them.
    """
    serializer_class = UserFollowedSerializer

    def get_queryset(self):
        user = self.request.user
        return user.followers.all()
