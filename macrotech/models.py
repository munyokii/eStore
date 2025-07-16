"""Application models for the Macrotech app."""
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Category(models.Model):
    """Model representing a product category."""
    CATEGORY_CHOICES = [
        ("Accessories", "Accessories"),
        ("Laptops", "Laptops"),
        ("Desktops", "Desktops"),
        ("Smartphones", "Smartphones"),
    ]
    category_image = models.ImageField(upload_to='categories/', blank=True, null=True)
    category_name = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    category_description = models.TextField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        """Meta class for Category model."""
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return str(self.category_name)


class Product(models.Model):
    """Model representing a product."""
    product_image = models.ImageField(upload_to='products/')
    product_more_image = models.ImageField(upload_to='products/more/', blank=True, null=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    more_detail_description = CKEditor5Field()
    product_specification = CKEditor5Field()
    uploaded_at = models.DateTimeField(auto_now_add=True)


    objects = models.Manager()

    def has_discount(self):
        """Check if the product has a discount."""
        return self.old_price and self.old_price > self.current_price

    def discount(self):
        """Calculate product discount percentage if old price exists."""
        if self.has_discount():
            try:
                product_discount = ((self.old_price - self.current_price) / self.old_price) * 100
                return int(product_discount)
            except (ZeroDivisionError, TypeError):
                return 0
        return 0


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
