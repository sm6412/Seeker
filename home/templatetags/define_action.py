from django import template
register = template.Library()

@register.simple_tag
def define(val=None):
    url = "http://167.172.237.157:8000"+val
    return url