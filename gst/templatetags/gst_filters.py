"""Custom template filters for GST module."""
from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except (TypeError, ValueError):
        return 0


@register.filter(name="mul")
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return 0
