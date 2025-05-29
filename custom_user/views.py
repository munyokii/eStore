"""Custom user views for handling login and registration."""
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserLoginForm, UserRegisterForm


class LoginRegisterView(View):
    """View for handling user login and registration."""

    def get(self, request):
        """Render the login and registration form."""
        login_form = UserLoginForm(auto_id='login_%s')
        register_form = UserRegisterForm(auto_id='register_%s')
        return render(request, "login-register.html", {
            "login_form": login_form,
            "register_form": register_form,
            "active_tab": "login"
        })

    def post(self, request):
        """Handle POST requests for login and registration."""
        if "login-email" in request.POST:
            login_form = UserLoginForm(request.POST, auto_id='login_%s')
            register_form = UserRegisterForm(auto_id='register_%s')
            active_tab = "login"
            if login_form.is_valid():
                login(request, login_form.user)
                messages.success(request, "Login successful!")
                return redirect("home")
        else:
            login_form = UserLoginForm(auto_id='login_%s')
            register_form = UserRegisterForm(request.POST, auto_id='register_%s')
            active_tab = "register"
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect("home")

        return render(request, "login-register.html", {
            "login_form": login_form,
            "register_form": register_form,
            "active_tab": active_tab
        })


class LogoutView(View):
    """View for handling user logout."""
    def get(self, request):
        """Handle user logout."""
        logout(request)
        messages.success(request, "Logout successful!")
        return redirect("home")
