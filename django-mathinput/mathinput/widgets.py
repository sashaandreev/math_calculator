"""
Django form widget for math input.

Provides a CKEditor-style math formula editor with graphical interface,
multiple input modes, and domain presets.
"""
from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from mathinput.modes import is_valid_mode
from mathinput.presets import is_valid_preset


class MathInputWidget(forms.Widget):
    """
    Widget for math formula input with graphical interface.
    
    Supports multiple input modes (regular_functions, advanced_expressions,
    integrals_differentials, matrices, statistics_probability, physics_engineering)
    and domain presets (algebra, calculus, physics, machine_learning,
    statistics, probability).
    
    Usage:
        from mathinput.widgets import MathInputWidget
        
        class ProblemForm(forms.Form):
            equation = forms.CharField(widget=MathInputWidget())
            calculus_problem = forms.CharField(
                widget=MathInputWidget(mode='integrals_differentials', preset='calculus')
            )
    """
    
    template_name = 'mathinput/widget.html'
    
    def __init__(self, mode=None, preset=None, attrs=None):
        """
        Initialize the widget.
        
        Args:
            mode: Input mode ('regular_functions', 'advanced_expressions', etc.)
                  Defaults to MATHINPUT_DEFAULT_MODE setting or 'regular_functions'
            preset: Domain preset ('algebra', 'calculus', etc.)
                    Defaults to MATHINPUT_PRESET setting or 'algebra'
            attrs: Additional HTML attributes for the widget
        """
        super().__init__(attrs)
        
        # Get mode from parameter, settings, or default
        try:
            default_mode = getattr(settings, 'MATHINPUT_DEFAULT_MODE', 'regular_functions')
        except Exception:
            # Django settings not configured (e.g., during import)
            default_mode = 'regular_functions'
        
        # Validate mode - use default if invalid
        if mode and is_valid_mode(mode):
            self.mode = mode
        else:
            self.mode = default_mode
        
        # Get preset from parameter, settings, or default
        try:
            default_preset = getattr(settings, 'MATHINPUT_PRESET', 'algebra')
        except Exception:
            # Django settings not configured (e.g., during import)
            default_preset = 'algebra'
        
        # Validate preset - use default if invalid
        if preset and is_valid_preset(preset):
            self.preset = preset
        else:
            self.preset = default_preset
    
    class Media:
        """CSS and JavaScript files for the widget."""
        css = {
            'all': ('mathinput/css/mathinput.css',)
        }
        js = ('mathinput/js/mathinput.js',)
    
    def render(self, name, value, attrs=None, renderer=None):
        """
        Render the widget HTML.
        
        Args:
            name: Field name
            value: Initial value (LaTeX string)
            attrs: Additional HTML attributes
            renderer: Template renderer (Django 1.11+)
        
        Returns:
            Rendered HTML string
        """
        if attrs is None:
            attrs = {}
        
        # Generate unique widget ID
        widget_id = attrs.get('id') or f'id_{name}'
        attrs['id'] = widget_id
        
        # Get renderer from settings
        try:
            renderer_type = getattr(settings, 'MATHINPUT_RENDERER', 'katex')
        except Exception:
            renderer_type = 'katex'
        
        # Get extensions from settings
        try:
            extensions = getattr(settings, 'MATHINPUT_KATEX_EXTENSIONS', [])
            if isinstance(extensions, str):
                # If string, convert to list
                extensions = [ext.strip() for ext in extensions.split(',') if ext.strip()]
        except Exception:
            extensions = []
        
        # Convert extensions to JSON string for template
        import json
        extensions_json = json.dumps(extensions)
        
        # Prepare template context
        context = {
            'name': name,
            'value': value or '',
            'mode': self.mode,
            'preset': self.preset,
            'widget_id': widget_id,
            'attrs': attrs,
            'renderer': renderer_type,
            'extensions': extensions_json,
        }
        
        return render_to_string(self.template_name, context)
    
    def value_from_datadict(self, data, files, name):
        """
        Extract value from form data.
        
        Args:
            data: Form data dictionary
            files: Uploaded files dictionary
            name: Field name
        
        Returns:
            LaTeX string from form submission
        """
        return data.get(name, '')

