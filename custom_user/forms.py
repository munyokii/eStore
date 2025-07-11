"""User forms for login and registration."""
from django import forms
from django.contrib.auth import authenticate
from .models import User


class UserLoginForm(forms.Form):
    """Form for user login."""
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean_email(self):
        """Validate the email field."""
        email = self.cleaned_data.get("email")
        ex_email = User.objects.filter(email="email")
        if not email:
            raise forms.ValidationError("Email is required.")
        elif email != ex_email:
            raise forms.ValidationError(
                "Seems like you don't have an account with us. Please register first.")
        return email

    def clean_password(self):
        """Validate the password field."""
        password = self.cleaned_data.get("password")
        ex_password = User.objects.filter(password="password")
        if not password:
            raise forms.ValidationError("Password is required.")
        elif password != ex_password:
            raise forms.ValidationError("Incorrect password!")
        return password

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password.")
            self.user = user

        return cleaned_data


class UserRegisterForm(forms.ModelForm):
    """Form for user registration."""
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        """Meta class for UserRegisterForm."""
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_first_name(self):
        """Validate the first name field."""
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError("First name is required.")
        if not first_name.isalpha():
            raise forms.ValidationError("First name should contain only letters.")
        return first_name

    def clean_last_name(self):
        """Validate the last name field."""
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise forms.ValidationError("Last name is required.")
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should contain only letters.")
        return last_name

    def clean_email(self):
        """Validate the email field."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
