"""Custom user app URL configuration."""
from django.urls import path
from .views import LoginRegisterView

urlpatterns = [
    path("user-login/", LoginRegisterView.as_view(), name="login_register")
]
