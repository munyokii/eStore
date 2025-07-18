""" Custom template filters for Django."""
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by key."""
    return dictionary.get(key, 0)
