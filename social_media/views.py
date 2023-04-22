from django.contrib.auth import get_user_model
from requests import Response
from rest_framework import viewsets, mixins, generics, status
from rest_framework.decorators import action

from social_media.models import Post, User
from .serializers import (
    UserSerializer,
    UserListSerializer,
    UserDetailSerializer,
    PostListSerializer,
    UserFollowingSerializer,
    UserFollowedSerializer, PostImageUploadSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
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

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        # permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """API endpoint for uploading image to specific post"""
        post = self.get_object()
        serializer = PostImageUploadSerializer(data=request.data, context={"post": post})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
