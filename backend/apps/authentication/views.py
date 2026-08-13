from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import RegisterSerializer


class RegisterationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
