"""Application URL configuration for the Macrotech app."""
from django.urls import path
from . import views

urlpatterns = [
  path("", views.HomeView.as_view(), name="home"),
  path("blog/", views.BlogView.as_view(), name="blog"),
]
