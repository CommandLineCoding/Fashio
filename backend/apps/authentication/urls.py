from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterationView.as_view(), name="register"),
]
