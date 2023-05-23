from django import template
from django.utils.safestring import mark_safe
from django.utils.text import slugify

register = template.Library()

@register.filter(name='wikipedia')
def wikipedia(obj):
    """Returns the Wikipedia link for this object"""
    return f"https://en.wikipedia.org/wiki/{obj}"

@register.filter(name='wikipedia_season')
def wikipedia_season(obj):
    """Returns the Wikipedia link for this Formula 1 Season"""
    this_year = obj.year
    return f"https://en.wikipedia.org/wiki/{this_year}_Formula_One_World_Championship"
    
@register.filter(name='statsf1')
def statsf1(car):
    """StatsF1 replaces slashes with dashes, unlike Wikipedia"""
    slug = slugify(str(car).replace('/', ' '))
    return f"https://www.statsf1.com/en/{slug}.aspx"

@register.filter(name='statsf1_engine_maker')
def statsf1_engine_maker(maker):
    return f"https://www.statsf1.com/en/moteur-{maker}.aspx"

# https://djangosnippets.org/snippets/2842/
@register.filter(name="nbhyphen")
def nbsp(value):
    return mark_safe("&#8209;".join(str(value).split('-')))

@register.filter(name="to_class_name")
def to_class_name(value):
    return value.__class__.__name__