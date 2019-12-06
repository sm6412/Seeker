from django import template
register = template.Library()

@register.simple_tag
def define(val=None):
    url = "http://127.0.0.1:8000"+val
    return url