
"""Forms for handling user input in the Macrotech application."""
from django import forms
from django.core.exceptions import ValidationError

from .models import ContactMessage, Review


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


class ReviewForm(forms.ModelForm):
    """ Review Form """
    class Meta:
        """ Class Meta"""
        model = Review
        fields = ['rating', 'reviewer_name',
                  'reviewer_email', 'review_title', 'review_description']

    def clean_reviewer_name(self):
        """Cleaning and validating reviewer name"""
        reviewer_name = self.cleaned_data.get('reviewer_name')
        if not reviewer_name:
            raise ValidationError("This field is required.")
        return reviewer_name

    def clean_reviewer_email(self):
        """Cleaning and validating reviewer email"""
        reviewer_email = self.cleaned_data.get('reviewer_email')
        if not reviewer_email:
            raise ValidationError("This field is required.")
        if not forms.EmailField().clean(reviewer_email):
            raise ValidationError("Enter a valid email address.")
        return reviewer_email

    def clean_review_title(self):
        """Cleaning and validating review title"""
        review_title = self.cleaned_data.get('review_title')
        if not review_title:
            raise ValidationError("This field is required.")
        return review_title

    def clean_review_description(self):
        """Cleaning and validating review description"""
        review_description = self.cleaned_data.get('review_description')
        if not review_description:
            raise ValidationError("This field is required.")
        return review_description
