from django import template
from django.utils.safestring import mark_safe
from django.utils.text import slugify

register = template.Library()

@register.filter(name="to_class_name")
def to_class_name(value):
    if value:
        return value.__class__.__name__
    return ''