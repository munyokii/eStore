"""Application views for the app."""
from django.shortcuts import render
from django.views import View


class HomeView(View):
    """Class-based view to display the home.html template."""

    def get(self, request):
        """Handle GET requests and render the home template."""
        return render(request, "home.html")


class BlogView(View):
    """Class-based view to display the blog.html template."""

    def get(self, request):
        """Handle GET requests and render the blog template."""
        return render(request, "blog.html")


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
