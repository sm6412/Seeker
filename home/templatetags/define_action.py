from django import template
register = template.Library()

@register.simple_tag
def define(val=None):
    url = "http://35.186.174.20:8000"+val
    return url