"""
Django Admin integration for MathInput widget.

Provides admin form classes and utilities for using MathInputWidget in Django Admin.
"""
from django import forms
from django.contrib import admin
from mathinput.widgets import MathInputWidget


class MathInputAdminForm(forms.ModelForm):
    """
    Admin form class that uses MathInputWidget for math formula fields.
    
    Usage:
        from mathinput.admin import MathInputAdminForm
        
        @admin.register(Problem)
        class ProblemAdmin(admin.ModelAdmin):
            form = MathInputAdminForm
            
            class Meta:
                widgets = {
                    'equation': MathInputWidget(mode='regular_functions'),
                }
    """
    pass


def get_mathinput_widget_for_field(field_name, mode=None, preset=None):
    """
    Helper function to get MathInputWidget configured for a specific field.
    
    Args:
        field_name: Name of the field to configure
        mode: Optional input mode
        preset: Optional domain preset
    
    Returns:
        Dictionary suitable for use in Meta.widgets
    """
    return {
        field_name: MathInputWidget(mode=mode, preset=preset)
    }


class MathInputAdminMixin:
    """
    Mixin class for ModelAdmin to easily add MathInputWidget support.
    
    Usage:
        from mathinput.admin import MathInputAdminMixin
        
        @admin.register(Problem)
        class ProblemAdmin(MathInputAdminMixin, admin.ModelAdmin):
            mathinput_fields = {
                'equation': {'mode': 'regular_functions', 'preset': 'algebra'},
                'calculus_problem': {'mode': 'integrals_differentials', 'preset': 'calculus'},
            }
    """
    
    # Override this in your ModelAdmin to specify which fields use MathInputWidget
    mathinput_fields = {}
    
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        
        # Configure widgets for math input fields
        if self.mathinput_fields:
            if not hasattr(self, 'form') or self.form is None:
                # Create a form class dynamically if none exists
                class MathInputForm(forms.ModelForm):
                    class Meta:
                        model = model
                        fields = '__all__'
                        widgets = {}
                
                # Add widgets for math input fields
                for field_name, config in self.mathinput_fields.items():
                    mode = config.get('mode')
                    preset = config.get('preset')
                    MathInputForm.Meta.widgets[field_name] = MathInputWidget(
                        mode=mode,
                        preset=preset
                    )
                
                self.form = MathInputForm
            else:
                # Add widgets to existing form
                if not hasattr(self.form.Meta, 'widgets'):
                    self.form.Meta.widgets = {}
                
                for field_name, config in self.mathinput_fields.items():
                    mode = config.get('mode')
                    preset = config.get('preset')
                    self.form.Meta.widgets[field_name] = MathInputWidget(
                        mode=mode,
                        preset=preset
                    )


# Convenience function for registering admin with math input
def register_mathinput_admin(model_class, admin_class=None, **kwargs):
    """
    Register a model with admin and configure MathInputWidget for specified fields.
    
    Args:
        model_class: The model class to register
        admin_class: Optional custom admin class (defaults to ModelAdmin)
        **kwargs: Field configurations in format field_name={'mode': ..., 'preset': ...}
    
    Usage:
        from mathinput.admin import register_mathinput_admin
        
        register_mathinput_admin(
            Problem,
            equation={'mode': 'regular_functions'},
            calculus_problem={'mode': 'integrals_differentials', 'preset': 'calculus'}
        )
    """
    if admin_class is None:
        admin_class = admin.ModelAdmin
    
    # Create admin class with math input fields
    class MathInputAdmin(MathInputAdminMixin, admin_class):
        mathinput_fields = kwargs
    
    admin.site.register(model_class, MathInputAdmin)
    return MathInputAdmin

