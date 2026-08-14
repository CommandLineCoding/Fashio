from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile
from .serializers import RegisterSerializer


class RegisterationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = UserProfile.objects.create(user=user)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "success": True,
                "data": {
                    "tokens": {
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                    },
                    "user": {
                        "id": str(profile.id),
                        "username": user.username,
                        "email": user.email,
                        "created_at": user.date_joined,
                    },
                },
            },
            status=status.HTTP_201_CREATED,
        )
