from django import template

register = template.Library()

@register.simple_tag
def func(a1, a2):
    return a1+a2

@register.filter
def func2(a1, a2):
    return a1+a2