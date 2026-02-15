from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def styled_field(field):
    """
    Renders a form field with the specific Nexus Admin styling applied.
    Usage: {% styled_field field %}
    """
    # 1. Determine the CSS class based on widget type
    widget_type = getattr(field.field.widget, 'input_type', None)
    
    if widget_type == 'checkbox':
        css_class = "w-4 h-4 rounded bg-gray-900 border-gray-700 text-cyan-500 focus:ring-cyan-500 focus:ring-offset-gray-900"
    elif widget_type == 'file':
        # File inputs might need different styling, but let's stick to base for now or adjust
        css_class = "w-full bg-black/30 border rounded-md py-2 px-3 text-white placeholder-gray-500 focus:outline-none focus:ring-1 sm:text-sm file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-cyan-500/10 file:text-cyan-400 hover:file:bg-cyan-500/20"
        if field.errors:
            css_class += " border-red-500 focus:border-red-500 focus:ring-red-500"
        else:
            css_class += " border-white/10 focus:border-cyan-500 focus:ring-cyan-500"
    else:
        # Default text-like inputs (text, email, password, etc.)
        css_class = "w-full bg-black/30 border rounded-md py-2 px-3 text-white placeholder-gray-500 focus:outline-none focus:ring-1 sm:text-sm"
        if field.errors:
            css_class += " border-red-500 focus:border-red-500 focus:ring-red-500"
        else:
            css_class += " border-white/10 focus:border-cyan-500 focus:ring-cyan-500"

    # 2. Check for CKEditor or other special widgets
    widget_class_name = field.field.widget.__class__.__name__
    
    if 'CKEditor' in widget_class_name:
        # CKEditor handles its own styling, applying classes to the hidden textarea can cause issues
        rendered_widget = field.as_widget()
    else:
        # Render standard inputs with our custom classes
        rendered_widget = field.as_widget(attrs={'class': css_class})
    
    # 3. Append errors if any exist
    if field.errors:
        error_items = "".join([f'<p class="text-[10px] text-red-500 mt-1"><i class="fas fa-exclamation-circle mr-1"></i>{error}</p>' for error in field.errors])
        # Use placeholders to avoid conflicts with curly braces in widget HTML (e.g., CKEditor config)
        return format_html('{}{}', rendered_widget, format_html('<div class="mt-1">{}</div>', format_html(error_items)))
        
    return format_html('{}', rendered_widget)
