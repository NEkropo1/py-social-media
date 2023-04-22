from requests import Response
from rest_framework import generics, status
from rest_framework.decorators import action

from social_media.models import Post
from .serializers import (
    PostImageUploadSerializer, PostListSerializer, PostDetailSerializer,
)


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


class PostDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint that allows a post to be retrieved.
    """
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
