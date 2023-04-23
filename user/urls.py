from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import (
    CreateUserView,
    FollowUnfollowAPIView,
    ProfileList,
    ProfileDetailUpdateDeleteAPIView,
    LogoutView,
    ManageUserView,
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("profiles/", ProfileList.as_view(), name="profile_list"),
    path(
        "profiles/<int:pk>/",
        ProfileDetailUpdateDeleteAPIView.as_view(),
        name="profile_detail"
    ),
    path(
        "profiles/<int:pk>/follow/",
        FollowUnfollowAPIView.as_view(),
        name="follow"
    ),
]

app_name = "user"
