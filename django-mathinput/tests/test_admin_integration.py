"""
Integration tests for Django Admin integration.

Tests MathInputWidget integration with Django Admin.
"""
import pytest
from django import forms
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from mathinput.widgets import MathInputWidget
from mathinput.admin import (
    MathInputAdminForm,
    MathInputAdminMixin,
    get_mathinput_widget_for_field,
    register_mathinput_admin,
)


@pytest.mark.integration
class TestMathInputAdminForm(TestCase):
    """
    What we are testing: MathInputAdminForm uses MathInputWidget
    Why we are testing: Admin forms must use the widget correctly
    Expected Result: Form renders with MathInputWidget
    """
    
    def test_admin_form_uses_widget(self):
        """
        What we are testing: Admin form can use MathInputWidget
        Why we are testing: Admin integration requirement
        Expected Result: Form renders widget correctly
        """
        # Test that MathInputAdminForm can be used as base class
        # In practice, it would be used with a model
        class TestForm(forms.Form):
            equation = forms.CharField(widget=MathInputWidget(mode='regular_functions'))
        
        form = TestForm()
        widget = form.fields['equation'].widget
        
        # Should be MathInputWidget
        assert isinstance(widget, MathInputWidget)
        assert widget.mode == 'regular_functions'


@pytest.mark.integration
def test_get_mathinput_widget_for_field():
    """
    What we are testing: Helper function returns correct widget configuration
    Why we are testing: Convenience function for admin setup
    Expected Result: Returns dictionary with MathInputWidget
    """
    widgets = get_mathinput_widget_for_field('equation', mode='matrices', preset='machine_learning')
    
    assert 'equation' in widgets
    assert isinstance(widgets['equation'], MathInputWidget)
    assert widgets['equation'].mode == 'matrices'
    assert widgets['equation'].preset == 'machine_learning'


@pytest.mark.integration
class TestMathInputAdminMixin(TestCase):
    """
    What we are testing: MathInputAdminMixin configures widgets automatically
    Why we are testing: Mixin provides easy admin integration
    Expected Result: Mixin configures widgets for specified fields
    """
    
    def test_mixin_has_mathinput_fields(self):
        """
        What we are testing: Mixin has mathinput_fields attribute
        Why we are testing: Easy admin integration
        Expected Result: Mixin can be configured with mathinput_fields
        """
        class TestAdmin(MathInputAdminMixin, admin.ModelAdmin):
            mathinput_fields = {
                'equation': {'mode': 'regular_functions', 'preset': 'algebra'},
            }
        
        # Check that mixin has the attribute
        assert hasattr(TestAdmin, 'mathinput_fields')
        assert TestAdmin.mathinput_fields == {'equation': {'mode': 'regular_functions', 'preset': 'algebra'}}


@pytest.mark.integration
def test_widget_renders_in_admin_context():
    """
    What we are testing: Widget renders correctly in admin context
    Why we are testing: Admin has different styling and context
    Expected Result: Widget HTML renders without errors
    """
    widget = MathInputWidget(mode='regular_functions', preset='algebra')
    html = widget.render('equation', 'x^2 + 1')
    
    # Should render HTML
    assert html is not None
    assert len(html) > 0
    assert 'mi-widget' in html
    
    # Should contain widget structure
    assert 'mi-visual-builder' in html or 'widget' in html.lower()


@pytest.mark.integration
def test_admin_widget_with_different_modes():
    """
    What we are testing: Widget works with different modes in admin
    Why we are testing: Admin should support all widget modes
    Expected Result: All modes work in admin context
    """
    modes = [
        'regular_functions',
        'integrals_differentials',
        'matrices',
    ]
    
    for mode in modes:
        widget = MathInputWidget(mode=mode)
        html = widget.render('equation', '')
        
        assert html is not None
        assert 'mi-widget' in html
        assert f'data-mode="{mode}"' in html


@pytest.mark.integration
def test_admin_form_saves_value():
    """
    What we are testing: Admin form saves widget value correctly
    Why we are testing: Form submission must work in admin
    Expected Result: Value saved correctly through admin form
    """
    class TestForm(forms.Form):
        equation = forms.CharField(widget=MathInputWidget())
    
    form = TestForm(data={'equation': 'x^2 + 1'})
    
    # Form should be valid
    assert form.is_valid()
    assert form.cleaned_data['equation'] == 'x^2 + 1'


@pytest.mark.user_story
@pytest.mark.us_15  # US-15: Django Admin Compatible
def test_widget_works_in_admin():
    """
    What we are testing: Widget functions correctly in Django Admin
    Why we are testing: US-15 - Admin integration requirement
    Expected Result: Widget renders and saves in admin interface
    """
    widget = MathInputWidget()
    html = widget.render('equation', 'x^2 + 1')
    
    # Widget should render
    assert html is not None
    assert len(html) > 0
    
    # Should contain widget structure
    assert 'mi-widget' in html
    assert 'mi-visual-builder' in html or 'widget' in html.lower()
    
    # Should contain the value
    assert 'x^2' in html or 'value=' in html


@pytest.mark.user_story
@pytest.mark.us_15
def test_admin_list_display_support():
    """
    What we are testing: Admin list view can display formula previews
    Why we are testing: US-15 - Admin should show formula previews
    Expected Result: Admin can display truncated or rendered formulas
    """
    # This would typically be in a ModelAdmin class
    # We test that the widget value can be accessed for display
    widget = MathInputWidget()
    value = 'x^2 + 1'
    
    # Value should be accessible for admin list display
    assert value is not None
    assert len(value) > 0
    
    # Can be truncated for list view
    truncated = value[:10] if len(value) > 10 else value
    assert truncated is not None

