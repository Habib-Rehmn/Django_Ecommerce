from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(int(value))

@register.filter
def empty_star_count(value):
    return 5 - int(value)
