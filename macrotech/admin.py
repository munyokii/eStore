"""Application admin configuration for the Macrotech app."""
import logging
import smtplib

from django.contrib import admin
from django import forms
from django.core.mail import send_mail
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Widget

from macrotech.models import Category, EmailTemplate, NewsletterSubscriber, Product, Review, BlogPost


logger = logging.getLogger(__name__)
# Register your models here.
class EmailTemplateAdminForm(forms.ModelForm):
    """Email Template Admin"""
    class Meta:
        """Class meta"""
        model = EmailTemplate
        fields = '__all__'
        widgets = {
            'message': CKEditor5Widget(),
        }

class EmailTemplateAdmin(admin.ModelAdmin):
    """Admin template"""
    form = EmailTemplateAdminForm

    def save_related(self, request, form, formsets, change):
        """Save M2M and then send email"""
        super().save_related(request, form, formsets, change)

        obj = form.instance
        subject = obj.subject
        html_message = obj.message

        recipients = [subscriber.email for subscriber in obj.recipients.all()]
        from_email = settings.EMAIL_HOST_USER

        if recipients:
            try:
                send_mail(
                    subject,
                    "",
                    from_email,
                    recipients,
                    html_message=html_message,
                    fail_silently=False
                )
                logger.warning("Email sent successfully to: %s", recipients)
            except smtplib.SMTPException as e:
                logger.exception(
                    "Failed to send email to: %s. SMTP Error: %s", recipients, str(e))
        else:
            logger.warning("No recipients found. Email not sent.")

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(BlogPost)
admin.site.register(NewsletterSubscriber)
admin.site.register(EmailTemplate,  EmailTemplateAdmin)
