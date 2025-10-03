"""Application URL configuration for the Macrotech app."""
from django.urls import path
from . import views

urlpatterns = [
  path("", views.HomeView.as_view(), name="home"),
  path("product/details/<int:product_id>/",
       views.ProductDetailView.as_view(), name="product_detail"),
  path('cart/add/', views.AddToCartView.as_view(), name='add-to-cart'),
  path('update-cart/', views.UpdateCartView.as_view(), name='update-cart'),
  path("cart/", views.CartView.as_view(), name="cart"),
  path("checkout/", views.CheckoutView.as_view(), name="checkout"),
  path("blog/", views.BlogView.as_view(), name="blog"),
  path("blog/details/<int:post_id>/", views.BlogDetailView.as_view(), name="blog_detail"),
  path("search/", views.BlogSearchView.as_view(), name="blog-search"),
  path("category/", views.CategoryView.as_view(), name="category"),
  path("about/", views.AboutView.as_view(), name="about"),
  path("macrotech/contact-us/", views.ContactView.as_view(), name="contact"),
  path("newsletter/signup/", views.NewsletterView.as_view(), name="newsletter"),
  path("support/", views.SupportView.as_view(), name="support"),
  path("shipping-info/", views.ShippingInfoView.as_view(), name="shipping_info"),
  path("return-policy/", views.ReturnPolicyView.as_view(), name="return_policy"),
  path("terms/", views.TermsOfServiceView.as_view(), name="terms"),
  path("privacy/", views.PrivacyView.as_view(), name="privacy"),
  path("my-account/", views.AccountView.as_view(), name="account"),
]
