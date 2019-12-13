from django import template
register = template.Library()

@register.simple_tag
def define(val=None):
    url = "http://35.222.145.173"+val
    return url