"""tags for sorting querysets. Used to sort default context variables within templates"""
from django import template
from django.utils.safestring import mark_safe
from django.utils.text import slugify

register = template.Library()

@register.filter(name='sort_by_season')
def cars_by_season(cars_queryset):
    """Returns the Wikipedia link for this object"""
    return sorted(cars_queryset, key=lambda c: c.earliest_season())
