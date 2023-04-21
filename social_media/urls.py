from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    PostListView,
    UserFollowingView,
    UserFollowedView
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("users/following/", UserFollowingView.as_view(), name="user-following"),
    path("users/followers/", UserFollowedView.as_view(), name="user-followers"),
]

app_name = "api"
