from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterationView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("<str:provider>/", views.OAuthLoginView.as_view()),
    path("<str:provider>/callback/", views.OAuthCallbackView.as_view()),
    # path("google/",views.GoogleLogin.as_view(),name="google_login"),
]
