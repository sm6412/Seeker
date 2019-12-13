from django import template
register = template.Library()

@register.simple_tag
def define(val=None):
    url = "http://134.209.168.171:8000"+val
    return url