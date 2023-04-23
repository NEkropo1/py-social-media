from django.db.models import Q
from rest_framework import generics

from social_media.models import Post
from .serializers import (
    PostListSerializer,
    PostDetailSerializer
)


class PostListView(generics.CreateAPIView, generics.ListAPIView):
    """
    API endpoint that allows posts to be listed.
    """
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def get_queryset(self):
        followed_users_ids = (
            self.request.user.followers.all()
        )
        user_profile_id = self.request.user.id

        queryset = self.queryset.filter(
            owner__in=list(followed_users_ids) + [user_profile_id]
        )

        hashtags = self.request.query_params.get("hashtags")
        if hashtags:
            query = Q()
            for hashtag in hashtags.split(','):
                query |= Q(message__icontains=f"#{hashtag}")
            queryset = queryset.filter(query)

        return queryset.distinct()


class PostDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint that allows a post to be retrieved.
    """
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
