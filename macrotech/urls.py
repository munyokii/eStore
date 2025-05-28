"""Application URL configuration for the Macrotech app."""
from django.urls import path
from . import views

urlpatterns = [
  path("", views.HomeView.as_view(), name="home"),
  path("product/details/", views.ProductDetailView.as_view(), name="product_detail"),
  path("cart/", views.CartView.as_view(), name="cart"),
  path("checkout/", views.CheckoutView.as_view(), name="checkout"),
  path("blog/", views.BlogView.as_view(), name="blog"),
  path("about/", views.AboutView.as_view(), name="about"),
  path("category/", views.CategoryView.as_view(), name="category"),
]
