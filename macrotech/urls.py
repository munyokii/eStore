"""Application URL configuration for the Macrotech app."""
from django.urls import path
from . import views

urlpatterns = [
  path("", views.HomeView.as_view(), name="home"),
  path("product/details/", views.ProductDetailView.as_view(), name="product_detail"),
  path("cart/", views.CartView.as_view(), name="cart"),
  path("checkout/", views.CheckoutView.as_view(), name="checkout"),
  path("blog/", views.BlogView.as_view(), name="blog"),
  path("blog/details/", views.BlogDetailView.as_view(), name="blog_detail"),
  path("category/", views.CategoryView.as_view(), name="category"),
  path("about/", views.AboutView.as_view(), name="about"),
  path("contact/", views.ContactView.as_view(), name="contact"),
  path("support/", views.SupportView.as_view(), name="support"),
]
