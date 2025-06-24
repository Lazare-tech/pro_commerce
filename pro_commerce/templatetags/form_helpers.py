# myapp/templatetags/form_helpers.py

from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    """Add a class to a form field."""
    if isinstance(value, template.Variable):
        value = value.resolve(None)
    return value.as_widget(attrs={'class': arg})
#
