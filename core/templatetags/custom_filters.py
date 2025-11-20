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


@register.filter
def payload(card, key):
    """
    Retrieve a value from a card's dynamic payload.
    Usage: {{ card|payload:"role" }}
    """
    if not card or not hasattr(card, 'get_payload_value'):
        return None
    return card.get_payload_value(key)


@register.filter
def payload_list(card, key):
    """
    Retrieve a list from a card's dynamic payload.
    """
    if not card or not hasattr(card, 'get_payload_list'):
        return []
    return card.get_payload_list(key)