"""Application admin configuration for the Macrotech app."""
from django.contrib import admin

from macrotech.models import Category, Product, Review

# Register your models here.
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Category)
