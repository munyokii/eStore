"""Email notification handling in the Macrotech application."""
from datetime import datetime

import cloudinary
import cloudinary.api

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

class EmailContactNotification:
    """Handles sending contact email notifications."""

    def __init__(self, context):
        self.context = context
        self.sender = settings.EMAIL_SENDER
        self.receiver = settings.ADMIN_EMAIL
        self.public_id = settings.PUBLIC_ID
        self.current_year = datetime.now().year

    def get_cloudinary_url(self):
        """Retrieve secure Cloudinary image URL based on PUBLIC_ID."""
        if not self.public_id:
            print("Error: PUBLIC_ID environment variable is not set.")
            return None

        try:
            result = cloudinary.api.resource(self.public_id)
            return result.get("secure_url", "")
        except Exception as e:
            print(f"Cloudinary error: {e}")
            return None

    def build_email(self):
        """Build the HTML email content."""
        cloudinary_url = self.get_cloudinary_url()
        if not cloudinary_url:
            return None

        message = (
            f"You have a new message from {self.context['name']}, "
            f"Email: {self.context['email']} about {self.context['subject'].upper()}. "
            f"The message is: {self.context['message']}"
        )

        return render_to_string('email/contact.html', {
            'subject': self.context["subject"],
            'message': message,
            'current_year': self.current_year,
            'image_url': cloudinary_url
        })

    def send(self):
        """Send the email and return success status."""
        html_content = self.build_email()
        if not html_content:
            return False

        try:
            msg = EmailMultiAlternatives(
                self.context["subject"], None, self.sender, [self.receiver]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
