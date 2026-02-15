from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Adds a CSS class to a form field widget.
    Usage: {{ field|add_class:"my-class" }}
    """
    if hasattr(value, 'as_widget'):
        return value.as_widget(attrs={'class': arg})
    return value
