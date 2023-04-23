from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from user.permissions import IsAdminOrOwnerOrIfAuthenticatedReadOnly, IsAdminOrIfAuthenticatedReadOnly
from user.serializers import (
    UserSerializer,
    ProfileDetailUpdateDeleteSerializer,
    ProfileListSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """
    JWT logout custom class
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class ProfileList(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileListSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class ProfileDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileDetailUpdateDeleteSerializer
    permission_classes = [IsAdminOrOwnerOrIfAuthenticatedReadOnly]

    def get_object(self):
        obj = get_user_model().objects.get(id=self.request.user.id)
        print(f"Object: {obj}")
        self.check_object_permissions(self.request, obj)
        return obj

