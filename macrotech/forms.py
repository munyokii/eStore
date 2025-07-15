
"""Forms for handling user input in the Macrotech application."""
from django import forms
from django.core.exceptions import ValidationError

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    """Contact Message Form"""
    class Meta:
        """Class Meta"""
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def clean_name(self):
        """Cleaning and validating name"""
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("This field is required.")
        if len(name) < 3:
            raise ValidationError("Name must be at least 3 characters long.")
        return name

    def clean_email(self):
        """Cleaning and validating email"""
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("This field is required.")
        if not forms.EmailField().clean(email):
            raise ValidationError("Enter a valid email address.")
        return email

    def clean_subject(self):
        """Cleaning and validating subject"""
        subject = self.cleaned_data.get('subject')
        if not subject:
            raise ValidationError("This field is required.")
        return subject

    def clean_message(self):
        """Cleaning and validating project description"""
        message = self.cleaned_data.get('message')
        if not message:
            raise ValidationError("This field is required.")

        return message
