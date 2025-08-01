"""Utility functions for the application."""
from functools import wraps

from django.shortcuts import redirect
from django.contrib import messages

def custom_login_required(message="You must be logged in to view this page. Please login below"):
    """Decorator to ensure that a user is logged in before accessing a view.
    If the user is not authenticated, they will be redirected to the login page with a message."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, message)
                return redirect('login_register')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
