from rest_framework import generics

from social_media.models import Post
from .serializers import (
    PostListSerializer, PostDetailSerializer
)


class PostListView(generics.CreateAPIView, generics.ListAPIView):
    """
    API endpoint that allows posts to be listed.
    """
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint that allows a post to be retrieved.
    """
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
