from django import template
from django.utils.text import slugify

register = template.Library()

@register.filter(name="to_class_name")
def to_class_name(value):
    """Print the class of the default object passed to the template, for use as a CSS class"""
    if value:
        return value.__class__.__name__
    return ''