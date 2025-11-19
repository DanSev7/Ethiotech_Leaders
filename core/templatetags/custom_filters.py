# core/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """
    Replaces all occurrences of a substring with another string.
    Usage: {{ value|replace:"old_text,new_text" }}
    """
    if not isinstance(value, str):
        return value
    
    try:
        # Expects 'old_text,new_text' format
        parts = arg.split(',', 1) 

        if len(parts) != 2:
            return value

        old, new = parts
        return value.replace(old, new)
    except Exception:
        return value