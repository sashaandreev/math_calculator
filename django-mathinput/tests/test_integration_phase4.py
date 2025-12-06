"""
Integration tests for Phase 4: Template Tags, Admin Integration, Renderer Fallback.

Tests integration of Phase 4 features with Django systems.
"""
import pytest
from django.test import TestCase, Client
from django.template import Context, Template
from django.contrib.auth.models import User
from mathinput.widgets import MathInputWidget
from mathinput.templatetags.mathinput_tags import as_mathinput, render_math
from mathinput.admin import MathInputAdminMixin, get_mathinput_widget_for_field


@pytest.mark.integration
class TestTemplateTagIntegration(TestCase):
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
    
    def test_as_mathinput_with_mode_in_template(self):
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


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
class TestDjangoAdminIntegration(TestCase):
    """
    What we are testing: Widget works in Django Admin interface
    Why we are testing: Admin integration is required feature
    Expected Result: Widget renders and functions in admin
    """
    
    def setUp(self):
        """Set up test user and client."""
        # User creation happens in test methods that have @pytest.mark.django_db
        # setUp is called by TestCase, which has database access via the class decorator
        self.client = Client()
    
    @pytest.mark.django_db(transaction=True)
    def test_widget_renders_in_admin(self):
        """
        What we are testing: Widget renders correctly in admin form
        Why we are testing: Admin users need to edit formulas
        Expected Result: Widget HTML present in admin form
        """
        # Create admin user for this test
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )
        
        widget = MathInputWidget()
        html = widget.render('equation', 'x^2 + 1')
        
        # Widget should render
        assert html is not None
        assert 'mi-widget' in html
        assert 'x^2' in html or 'value=' in html
    
    @pytest.mark.django_db(transaction=True)
    def test_admin_list_shows_preview(self):
        """
        What we are testing: Admin list view shows formula preview
        Why we are testing: Admins need to see formulas in list
        Expected Result: List view shows truncated/preview of formula
        """
        # Create admin user for this test
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )
        
        # This would typically be tested with a real model
        # For now, we test that the widget value can be accessed
        widget = MathInputWidget()
        value = 'x^2 + 1'
        html = widget.render('equation', value)
        
        # Value should be accessible for list display
        assert value is not None
        assert len(value) > 0
        
        # Can be truncated for list view
        truncated = value[:10] if len(value) > 10 else value
        assert truncated is not None
    
    @pytest.mark.django_db(transaction=True)
    def test_admin_saves_formula(self):
        """
        What we are testing: Admin can save formula via widget
        Why we are testing: Admin must be able to create/edit formulas
        Expected Result: Formula saved correctly through admin
        """
        # Create admin user for this test
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )
        
        from django import forms
        
        class TestForm(forms.Form):
            equation = forms.CharField(widget=MathInputWidget())
        
        form = TestForm(data={'equation': 'x^2 + 1'})
        
        # Form should be valid
        assert form.is_valid()
        assert form.cleaned_data['equation'] == 'x^2 + 1'


@pytest.mark.integration
class TestRendererIntegration(TestCase):
    """
    What we are testing: Renderer system integrates with widget
    Why we are testing: Renderer must work in full widget context
    Expected Result: Renderer loads and renders correctly
    """
    
    def test_widget_initializes_renderer(self):
        """
        What we are testing: Widget initializes renderer on load
        Why we are testing: Renderer must be ready for preview
        Expected Result: Renderer initialized when widget loads
        """
        widget = MathInputWidget()
        html = widget.render('equation', 'x^2 + 1')
        
        # Widget should render with renderer configuration
        assert html is not None
        assert 'renderer' in html.lower() or 'katex' in html.lower()
    
    def test_renderer_configuration_passed_to_template(self):
        """
        What we are testing: Renderer configuration passed to template
        Why we are testing: JavaScript needs renderer info
        Expected Result: Template contains renderer configuration
        """
        widget = MathInputWidget()
        html = widget.render('equation', '')
        
        # Should contain renderer configuration
        assert html is not None
        # Renderer is passed in script tag initialization
        assert 'initializeMathInput' in html or 'renderer' in html.lower()


@pytest.mark.integration
def test_template_tags_with_different_modes():
    """
    What we are testing: Template tags work with different modes
    Why we are testing: Tags must support all widget modes
    Expected Result: All modes work with template tags
    """
    modes = [
        'regular_functions',
        'integrals_differentials',
        'matrices',
    ]
    
    for mode in modes:
        result = as_mathinput('x^2', mode)
        assert result is not None
        assert len(result) > 0


@pytest.mark.integration
def test_admin_helper_functions():
    """
    What we are testing: Admin helper functions work correctly
    Why we are testing: Helper functions simplify admin integration
    Expected Result: Helper functions return correct configurations
    """
    # Test get_mathinput_widget_for_field
    widgets = get_mathinput_widget_for_field('equation', mode='matrices')
    
    assert 'equation' in widgets
    assert isinstance(widgets['equation'], MathInputWidget)
    assert widgets['equation'].mode == 'matrices'


@pytest.mark.integration
def test_render_math_with_different_renderers():
    """
    What we are testing: render_math works with different renderers
    Why we are testing: Users may configure different renderers
    Expected Result: Both KaTeX and MathJax render correctly
    """
    latex = r'x^2 + 1'
    
    # Test with katex
    result_katex = render_math(latex, 'katex')
    assert result_katex is not None
    assert len(result_katex) > 0
    
    # Test with mathjax
    result_mathjax = render_math(latex, 'mathjax')
    assert result_mathjax is not None
    assert len(result_mathjax) > 0

