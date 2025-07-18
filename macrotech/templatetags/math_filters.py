"""Custom template tags for mathematical operations."""
from django import template

register = template.Library()

@register.filter
def mod(value, arg):
    """Return the modulus of value and arg."""
    return value % arg
