from django import template

register = template.Library()

@register.filter(name='numRound')
def _numRound(_min, _max):
    _max = int(_max)
    return range(_min+1, _max+1)