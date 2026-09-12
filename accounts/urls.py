from django.urls import path

from .views import LoginView, RegisterView

# Authentication endpoints for registration and login.

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
