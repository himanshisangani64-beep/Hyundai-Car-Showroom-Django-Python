from django import template
register = template.Library()

@register.filter
def mul(value, arg):
    try:
        return value * arg
    except:
        return 0
