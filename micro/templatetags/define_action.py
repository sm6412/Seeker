from django import template
register = template.Library()

@register.simple_tag
def define(val=None):
    url = "http://35.202.78.214"+val
    return url
