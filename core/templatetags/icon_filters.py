# core/templatetags/icon_filters.py
import re
from django import template

register = template.Library()

@register.filter
def to_kebab_case(value):
    """
    Convert PascalCase or camelCase string to kebab-case.
    Examples:
    - 'BriefcaseConveyorBelt' -> 'briefcase-conveyor-belt'
    - 'HousePlus' -> 'house-plus'
    - 'TrendingUp' -> 'trending-up'
    """
    if not value:
        return value
    
    # Convert PascalCase/camelCase to kebab-case
    # Insert hyphens before uppercase letters (except the first one)
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', str(value))
    # Handle cases like 'HTMLParser' -> 'html-parser'
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1)
    # Convert to lowercase
    return s2.lower()