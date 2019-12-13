from django import template
register = template.Library()

@register.simple_tag
def define(val=None):
    url = "http://35.245.160.40:8000"+val
    return url