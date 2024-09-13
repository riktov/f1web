"""tags for sorting querysets. Used to sort default context variables within templates"""
from django import template
from django.utils.safestring import mark_safe
from django.utils.text import slugify

register = template.Library()

@register.filter(name='sort_by_season')
def sort_by_season(queryset):
    """Sort by season; Can be used for cars or engines or anything that has an earliest_season() method."""
    #Unlike earliest_season, where we can discard None items, here we need to deal with them first
    #filter out any item with no earliest season, since they can not be sorted
    unsortables = []
    sortables = []
    for i in queryset:
        if i.earliest_season() is None :
            unsortables.append(i)
        else:
            sortables.append(i)

    return unsortables + sorted(sortables, key=lambda c: c.earliest_season())

