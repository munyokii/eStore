"""Application views for the app."""
from django.shortcuts import render
from django.views import View


class HomeView(View):
    """Class-based view to display the home.html template."""

    def get(self, request):
        """Handle GET requests and render the home template."""
        return render(request, "home.html")


class ProductDetailView(View):
    """Class-based view to display the product_detail.html template."""

    def get(self, request):
        """Handle GET requests and render the product detail template."""
        return render(request, "product-details.html")


class CartView(View):
    """Class-based view to display the cart.html template."""

    def get(self, request):
        """Handle GET requests and render the cart template."""
        return render(request, "cart.html")


class CheckoutView(View):
    """Class-based view to display the checkout.html template."""

    def get(self, request):
        """Handle GET requests and render the checkout template."""
        return render(request, "user/checkout.html")


class BlogView(View):
    """Class-based view to display the blog.html template."""

    def get(self, request):
        """Handle GET requests and render the blog template."""
        return render(request, "blog.html")


class BlogDetailView(View):
    """Class-based view to display the blog-details.html template."""

    def get(self, request):
        """Handle GET requests and render the blog-details template."""
        return render(request, "blog-details.html")


class AboutView(View):
    """Class-based view to display the about.html template."""

    def get(self, request):
        """Handle GET requests and render the about template."""
        return render(request, "about.html")


class CategoryView(View):
    """Class-based view to display the category.html template."""

    def get(self, request):
        """Handle GET requests and render the category template."""
        return render(request, "category.html")


class ContactView(View):
    """Class-based view to display the contact.html template."""

    def get(self, request):
        """Handle GET requests and render the contact template."""
        return render(request, "contact.html")
