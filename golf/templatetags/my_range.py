from django import template

register = template.Library()

@register.filter(name='my_range')
def my_range(value):
    value = int(value)
    return range(1, value)