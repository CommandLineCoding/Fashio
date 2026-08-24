from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile
from .serializers import LoginSerializer, RegisterSerializer


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


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwags):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        profile = UserProfile.objects.get(user=user)
        return Response(
            {
                "success": True,
                "data": {
                    "tokens": {
                        "access_token": serializer.validated_data["access_token"],
                        "refresh_token": serializer.validated_data["refresh_token"],
                    },
                    "user": {
                        "id": str(profile.id),
                        "username": user.username,
                        "created_at": user.date_joined,
                    },
                },
            },
            status=status.HTTP_200_OK,
        )


"""  
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1:8000/accounts/google/login/callback/"
"""


class OAuthLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, provider):
        if provider != "google":
            return Response({"error": "Unsupported provider"}, status=400)
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
        }
        google_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
        return redirect(google_url)


class OAuthCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, provider):
        if provider != "google":
            return Response({"error": "Unsupported provider"}, status=400)
        code = request.GET.get("code")
        if not code:
            return Response({"error": "Authorization code missing"}, status=400)
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return Response({"error": "Failed to get access_token"}, status=400)
        user_response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_response.json()
        return Response(user_data)
