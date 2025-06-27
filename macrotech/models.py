"""Application models for the Macrotech app."""
from django.db import models

# Create your models here.
class Product(models.Model):
    """Model representing a product."""
    product_image = models.ImageField(upload_to='products/')
    product_more_image = models.ImageField(upload_to='products/more/', blank=True, null=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    previous_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    more_detail_description = models.TextField()
    product_specification = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return str(self.product_name)
