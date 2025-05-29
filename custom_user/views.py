"""Custom user views for handling login and registration."""
from django.shortcuts import render
from django.views import View


class LoginRegisterView(View):
    """Class-based view to display the login-register.html template."""

    def get(self, request):
        """Handle GET requests and render the login-register template."""
        return render(request, "login-register.html")
