"""tags for sorting querysets. Used to sort default context variables within templates"""
from django import template
from django.utils.safestring import mark_safe
from django.utils.text import slugify

register = template.Library()

@register.filter(name='sort_by_season')
def sort_by_season(queryset):
    """Sort by season; Can be used for cars or engines or anything that has an earliest_season() method."""
    return sorted(queryset, key=lambda c: c.earliest_season())

