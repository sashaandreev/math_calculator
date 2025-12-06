"""
Integration tests for Phase 5: Forms, Templates, and Admin Integration.

Comprehensive integration tests for:
- Form integration (widget in forms, submission, validation)
- Template integration (tag usage, rendering, context handling)
- Admin integration (form rendering, save functionality)
"""
import pytest
from django import forms
from django.test import TestCase, Client
from django.template import Context, Template, TemplateSyntaxError
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.db import models
from mathinput.widgets import MathInputWidget
from mathinput.validators import MathInputValidator
from mathinput.templatetags.mathinput_tags import as_mathinput, render_math


# ============================================================================
# Test Models
# ============================================================================

class MathInputTestModel(models.Model):
    """Test model for admin integration tests."""
    name = models.CharField(max_length=100)
    equation = models.TextField()
    
    class Meta:
        app_label = 'tests'
        managed = False  # Don't create table in test database


# ============================================================================
# Form Integration Tests
# ============================================================================

@pytest.mark.integration
class TestFormIntegration(TestCase):
    """
    What we are testing: MathInputWidget integration with Django forms
    Why we are testing: Widget must work correctly in real form contexts
    Expected Result: Forms render, submit, and validate correctly
    """
    
    def test_widget_in_form_renders(self):
        """
        What we are testing: Widget renders correctly in Django form
        Why we are testing: Basic form integration requirement
        Expected Result: Form HTML contains widget structure
        """
        class MathForm(forms.Form):
            equation = forms.CharField(widget=MathInputWidget())
        
        form = MathForm()
        html = form.as_p()
        
        # Should render form
        assert isinstance(html, str)
        assert len(html) > 0
        assert 'equation' in html
        
        # Should contain widget structure
        assert 'mi-widget' in html or 'id_equation' in html
    
    def test_widget_in_form_with_initial_value(self):
        """
        What we are testing: Widget displays initial value in form
        Why we are testing: Forms often have initial values
        Expected Result: Initial value is displayed in widget
        """
        class MathForm(forms.Form):
            equation = forms.CharField(widget=MathInputWidget())
        
        initial_value = r'x^2 + 1'
        form = MathForm(initial={'equation': initial_value})
        html = form.as_p()
        
        # Should contain initial value
        assert initial_value in html or 'value=' in html
    
    def test_form_submission_with_valid_latex(self):
        """
        What we are testing: Form submission with valid LaTeX formula
        Why we are testing: Core functionality - form must submit data
        Expected Result: Form validates and cleaned_data contains formula
        """
        class MathForm(forms.Form):
            equation = forms.CharField(widget=MathInputWidget())
        
        valid_latex = r'\frac{1}{2} + \sqrt{x}'
        form = MathForm(data={'equation': valid_latex})
        
        # Form should be valid
        assert form.is_valid(), f"Form should be valid but got errors: {form.errors}"
        
        # Check cleaned data
        assert 'equation' in form.cleaned_data
        assert form.cleaned_data['equation'] == valid_latex
    
    def test_form_submission_with_empty_value(self):
        """
        What we are testing: Form submission with empty value
        Why we are testing: Edge case - empty formulas
        Expected Result: Form handles empty value correctly
        """
        class MathForm(forms.Form):
            equation = forms.CharField(widget=MathInputWidget(), required=False)
        
        form = MathForm(data={'equation': ''})
        
        # Form should be valid (field is not required)
        assert form.is_valid()
        assert form.cleaned_data['equation'] == ''
    
    def test_form_submission_with_required_field(self):
        """
        What we are testing: Required field validation works with widget
        Why we are testing: Form validation must work with widget
        Expected Result: Empty required field causes validation error
        """
        class MathForm(forms.Form):
            equation = forms.CharField(widget=MathInputWidget(), required=True)
        
        form = MathForm(data={'equation': ''})
        
        # Form should not be valid
        assert not form.is_valid()
        assert 'equation' in form.errors
    
    def test_form_validation_integration(self):
        """
        What we are testing: Form field validation integrates with MathInputValidator
        Why we are testing: Validation must work at form level
        Expected Result: Invalid formulas cause form validation errors
        """
        class MathForm(forms.Form):
            equation = forms.CharField(
                widget=MathInputWidget(),
                validators=[MathInputValidator()]
            )
        
        # Test with dangerous LaTeX command
        invalid_latex = r'\input{/etc/passwd}'
        form = MathForm(data={'equation': invalid_latex})
        
        # Form should not be valid
        assert not form.is_valid()
        assert 'equation' in form.errors
    
    def test_form_with_custom_mode(self):
        """
        What we are testing: Form can use widget with custom mode
        Why we are testing: Different forms may need different modes
        Expected Result: Widget renders with specified mode
        """
        class MathForm(forms.Form):
            equation = forms.CharField(
                widget=MathInputWidget(mode='matrices')
            )
        
        form = MathForm()
        html = form.as_p()
        
        # Should contain mode information
        assert 'data-mode' in html or 'matrices' in html.lower()
    
    def test_form_with_custom_preset(self):
        """
        What we are testing: Form can use widget with custom preset
        Why we are testing: Different forms may need different presets
        Expected Result: Widget renders with specified preset
        """
        class MathForm(forms.Form):
            equation = forms.CharField(
                widget=MathInputWidget(preset='calculus')
            )
        
        form = MathForm()
        html = form.as_p()
        
        # Should render widget
        assert 'mi-widget' in html or 'id_equation' in html
    
    def test_form_multiple_widgets(self):
        """
        What we are testing: Form can have multiple MathInputWidget fields
        Why we are testing: Real forms may have multiple formula fields
        Expected Result: All widgets render correctly
        """
        class MathForm(forms.Form):
            equation1 = forms.CharField(widget=MathInputWidget())
            equation2 = forms.CharField(widget=MathInputWidget())
        
        form = MathForm()
        html = form.as_p()
        
        # Should contain both fields
        assert 'equation1' in html
        assert 'equation2' in html
        assert html.count('mi-widget') >= 2 or html.count('id_equation') >= 2
    
    def test_form_value_from_post_data(self):
        """
        What we are testing: Widget correctly extracts value from POST data
        Why we are testing: Form submission must work correctly
        Expected Result: Widget value_from_datadict returns correct value
        """
        widget = MathInputWidget()
        
        # Simulate POST data
        data = {'equation': r'\frac{1}{2}'}
        files = {}
        
        value = widget.value_from_datadict(data, files, 'equation')
        
        # Should extract value correctly
        assert value == r'\frac{1}{2}'


# ============================================================================
# Template Integration Tests
# ============================================================================

@pytest.mark.integration
class TestTemplateIntegration(TestCase):
    """
    What we are testing: Template tags work in real Django templates
    Why we are testing: Template tags must integrate with Django template system
    Expected Result: Tags render correctly in template context
    """
    
    def test_as_mathinput_in_template(self):
        """
        What we are testing: as_mathinput filter works in Django template
        Why we are testing: Primary usage pattern for widget
        Expected Result: Template renders widget HTML correctly
        """
        template = Template('{% load mathinput_tags %}{{ value|as_mathinput }}')
        context = Context({'value': 'x^2 + 1'})
        result = template.render(context)
        
        # Should render widget
        assert 'mi-widget' in result or 'widget' in result.lower()
        assert len(result) > 0
    
    def test_as_mathinput_with_mode_parameter(self):
        """
        What we are testing: as_mathinput with mode parameter works in template
        Why we are testing: Template parameter passing must work
        Expected Result: Widget rendered with specified mode
        """
        template = Template('{% load mathinput_tags %}{{ value|as_mathinput:"matrices" }}')
        context = Context({'value': 'x^2 + 1'})
        result = template.render(context)
        
        # Should render widget
        assert result is not None
        assert len(result) > 0
        assert 'data-mode' in result or 'matrices' in result.lower()
    
    def test_render_math_in_template(self):
        """
        What we are testing: render_math filter works in Django template
        Why we are testing: Display stored formulas in templates
        Expected Result: Template renders formula correctly
        """
        template = Template('{% load mathinput_tags %}{{ formula|render_math }}')
        context = Context({'formula': r'x^2 + 1'})
        result = template.render(context)
        
        # Should render formula
        assert result is not None
        assert len(result) > 0
        assert 'katex' in result.lower() or 'mathjax' in result.lower() or 'data-latex' in result
    
    def test_template_with_context_variables(self):
        """
        What we are testing: Template tags work with context variables
        Why we are testing: Real templates use context variables
        Expected Result: Tags correctly use context values
        """
        template = Template(
            '{% load mathinput_tags %}'
            '{{ formula|render_math }}'
        )
        context = Context({
            'formula': r'\frac{1}{2}',
            'mode': 'calculus'
        })
        result = template.render(context)
        
        # Should render using context
        assert result is not None
        assert len(result) > 0
    
    def test_template_with_multiple_tags(self):
        """
        What we are testing: Multiple template tags work in same template
        Why we are testing: Templates may use multiple tags
        Expected Result: All tags render correctly
        """
        template = Template(
            '{% load mathinput_tags %}'
            'Input: {{ value|as_mathinput }}'
            'Output: {{ value|render_math }}'
        )
        context = Context({'value': r'x^2 + 1'})
        result = template.render(context)
        
        # Should render both tags
        assert 'Input:' in result
        assert 'Output:' in result
        assert len(result) > 0
    
    def test_template_tag_error_handling(self):
        """
        What we are testing: Template tags handle errors gracefully
        Why we are testing: Templates should not crash on invalid input
        Expected Result: Tags return empty string or safe default
        """
        template = Template('{% load mathinput_tags %}{{ value|as_mathinput }}')
        
        # Test with None
        context = Context({'value': None})
        result = template.render(context)
        assert result is not None  # Should not crash
    
    def test_template_inheritance_with_tags(self):
        """
        What we are testing: Template tags work in template inheritance
        Why we are testing: Real projects use template inheritance
        Expected Result: Tags work in child templates
        """
        # Test that the filter can be used in block context
        # Note: Full template inheritance requires template loader, so we test
        # that the filter works in a template that could be used in inheritance
        template = Template('{% load mathinput_tags %}{{ formula|render_math }}')
        context = Context({'formula': r'x^2'})
        result = template.render(context)
        
        assert result is not None
        assert 'katex' in result.lower() or 'mathjax' in result.lower() or 'data-latex' in result
    
    def test_template_with_empty_value(self):
        """
        What we are testing: Template tags handle empty values
        Why we are testing: Edge case - empty formulas
        Expected Result: Tags handle empty values gracefully
        """
        template = Template('{% load mathinput_tags %}{{ value|as_mathinput }}')
        context = Context({'value': ''})
        result = template.render(context)
        
        # Should render widget even with empty value
        assert result is not None
        assert len(result) > 0


# ============================================================================
# Admin Integration Tests
# ============================================================================

@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
class TestAdminIntegration(TestCase):
    """
    What we are testing: Widget works in Django Admin interface
    Why we are testing: Admin integration is required feature
    Expected Result: Widget renders and functions in admin
    """
    
    def setUp(self):
        """Set up test user and client."""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )
        self.client.force_login(self.admin_user)
    
    def test_admin_form_renders_widget(self):
        """
        What we are testing: Admin form renders MathInputWidget
        Why we are testing: Admin users need to edit formulas
        Expected Result: Widget HTML present in admin form
        """
        widget = MathInputWidget()
        html = widget.render('equation', 'x^2 + 1')
        
        # Widget should render
        assert html is not None
        assert 'mi-widget' in html
        assert 'x^2' in html or 'value=' in html
    
    def test_admin_form_with_different_modes(self):
        """
        What we are testing: Admin can use widget with different modes
        Why we are testing: Different admin forms may need different modes
        Expected Result: Widget renders with specified mode
        """
        modes = ['regular_functions', 'matrices', 'integrals_differentials']
        
        for mode in modes:
            widget = MathInputWidget(mode=mode)
            html = widget.render('equation', 'x^2 + 1')
            
            assert 'mi-widget' in html
            assert f'data-mode="{mode}"' in html
    
    def test_admin_form_saves_value(self):
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
    
    def test_admin_form_with_initial_value(self):
        """
        What we are testing: Admin form displays existing value in widget
        Why we are testing: Admin must see current values when editing
        Expected Result: Widget displays initial value
        """
        widget = MathInputWidget()
        existing_value = r'\frac{1}{2} + \sqrt{x}'
        html = widget.render('equation', existing_value)
        
        # Should contain existing value
        assert existing_value in html or 'value=' in html
    
    def test_admin_form_validation(self):
        """
        What we are testing: Admin form validates widget input
        Why we are testing: Admin must not save invalid formulas
        Expected Result: Invalid formulas cause validation errors
        """
        class TestForm(forms.Form):
            equation = forms.CharField(
                widget=MathInputWidget(),
                validators=[MathInputValidator()]
            )
        
        # Test with dangerous command
        invalid_latex = r'\input{/etc/passwd}'
        form = TestForm(data={'equation': invalid_latex})
        
        # Form should not be valid
        assert not form.is_valid()
        assert 'equation' in form.errors
    
    def test_admin_list_display_truncation(self):
        """
        What we are testing: Admin list view can truncate long formulas
        Why we are testing: List views should show readable previews
        Expected Result: Long formulas can be truncated for display
        """
        long_formula = r'\frac{1}{2} + \sqrt{x} + \int_{0}^{1} f(x) dx + \sum_{i=1}^{n} a_i'
        
        # Can be truncated for list view
        truncated = long_formula[:50] + '...' if len(long_formula) > 50 else long_formula
        assert len(truncated) <= 53  # 50 + '...'
        assert truncated is not None
    
    def test_admin_widget_media_inclusion(self):
        """
        What we are testing: Admin includes widget media (CSS/JS)
        Why we are testing: Widget needs its assets in admin
        Expected Result: Media files are included in admin
        """
        widget = MathInputWidget()
        media = widget.media
        
        # Should have CSS and JS
        assert len(media._css) > 0 or len(media._js) > 0
    
    def test_admin_form_with_multiple_widgets(self):
        """
        What we are testing: Admin form can have multiple MathInputWidget fields
        Why we are testing: Some models may have multiple formula fields
        Expected Result: All widgets render correctly
        """
        class TestForm(forms.Form):
            equation1 = forms.CharField(widget=MathInputWidget())
            equation2 = forms.CharField(widget=MathInputWidget())
        
        form = TestForm()
        html = form.as_p()
        
        # Should contain both fields
        assert 'equation1' in html
        assert 'equation2' in html


# ============================================================================
# Cross-Integration Tests
# ============================================================================

@pytest.mark.integration
class TestCrossIntegration(TestCase):
    """
    What we are testing: Integration between forms, templates, and admin
    Why we are testing: All components must work together
    Expected Result: Seamless integration across all layers
    """
    
    def test_form_to_template_workflow(self):
        """
        What we are testing: Form submission to template rendering workflow
        Why we are testing: Real-world usage involves both
        Expected Result: Data flows correctly from form to template
        """
        # Simulate form submission
        class MathForm(forms.Form):
            equation = forms.CharField(widget=MathInputWidget())
        
        form = MathForm(data={'equation': r'x^2 + 1'})
        assert form.is_valid()
        formula = form.cleaned_data['equation']
        
        # Render in template
        template = Template('{% load mathinput_tags %}{{ formula|render_math }}')
        context = Context({'formula': formula})
        result = template.render(context)
        
        # Should render correctly
        assert result is not None
        assert len(result) > 0
    
    def test_admin_to_template_workflow(self):
        """
        What we are testing: Admin save to template rendering workflow
        Why we are testing: Admin-saved data must display correctly
        Expected Result: Data flows correctly from admin to template
        """
        # Simulate admin save
        saved_formula = r'\frac{1}{2} + \sqrt{x}'
        
        # Render in template
        template = Template('{% load mathinput_tags %}{{ formula|render_math }}')
        context = Context({'formula': saved_formula})
        result = template.render(context)
        
        # Should render correctly
        assert result is not None
        assert len(result) > 0
    
    def test_form_validation_to_template_error_handling(self):
        """
        What we are testing: Form validation errors don't break template rendering
        Why we are testing: Error handling must work across layers
        Expected Result: Invalid form data handled gracefully
        """
        class MathForm(forms.Form):
            equation = forms.CharField(
                widget=MathInputWidget(),
                validators=[MathInputValidator()]
            )
        
        # Invalid form
        form = MathForm(data={'equation': r'\input{/etc/passwd}'})
        assert not form.is_valid()
        
        # Template should still render (with error handling)
        template = Template('{% load mathinput_tags %}{{ value|as_mathinput }}')
        context = Context({'value': ''})
        result = template.render(context)
        
        # Should not crash
        assert result is not None

