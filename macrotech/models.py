"""Application models for the Macrotech app."""
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Product(models.Model):
    """Model representing a product."""
    product_image = models.ImageField(upload_to='products/')
    product_more_image = models.ImageField(upload_to='products/more/', blank=True, null=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    more_detail_description = CKEditor5Field()
    product_specification = CKEditor5Field()

    objects = models.Manager()

    def __str__(self):
        return str(self.product_name)

class Review(models.Model):
    """Model representing a product review."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    reviewer_name = models.CharField(max_length=255)
    reviewer_email = models.EmailField()
    review_title = models.CharField(max_length=255)
    review_description = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return f"{self.product} - {self.review_title}"


class ContactMessage(models.Model):
    """Contact Messages Model"""
    name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=False)
    subject = models.CharField(max_length=255,blank=True)
    message = models.CharField(max_length=1000, blank=False)
    send_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        if self.name is None:
            return "No name provided (None)"
        return self.name
