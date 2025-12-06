"""
Compatibility tests for Phase 5.

Tests compatibility with different Django and Python versions.
"""
import pytest
import sys
import django
from django import forms
from django.test import TestCase

from mathinput.widgets import MathInputWidget
from mathinput.validators import MathInputValidator
from mathinput.security import sanitize_latex
from mathinput.templatetags.mathinput_tags import as_mathinput, render_math


@pytest.mark.compatibility
class TestDjangoVersionsCompatible:
    """
    What we are testing: Widget works with Django 3.2, 4.0, 4.1, 4.2
    Why we are testing: Compatibility requirement (NFR-04)
    Expected Result: Widget functions correctly on all supported Django versions
    """
    
    def test_django_version_detected(self):
        """
        What we are testing: Django version is detected correctly
        Why we are testing: Compatibility - need to know Django version
        Expected Result: Django version is accessible
        """
        django_version = django.get_version()
        assert django_version is not None
        assert len(django_version) > 0
        
        # Should be 3.2+ or 4.0+
        major, minor = map(int, django_version.split('.')[:2])
        assert (major == 3 and minor >= 2) or (major == 4 and minor >= 0), \
            f"Django version {django_version} should be 3.2+ or 4.0+"
    
    def test_widget_works_on_current_django(self):
        """
        What we are testing: Widget works on current Django version
        Why we are testing: Compatibility - basic functionality
        Expected Result: Widget renders correctly
        """
        widget = MathInputWidget()
        html = widget.render('equation', r'\frac{1}{2}')
        
        assert html is not None
        assert len(html) > 0
    
    def test_forms_integration_works(self):
        """
        What we are testing: Forms integration works on current Django
        Why we are testing: Compatibility - forms are core Django feature
        Expected Result: Widget works in Django forms
        """
        class TestForm(forms.Form):
            equation = forms.CharField(widget=MathInputWidget())
        
        form = TestForm()
        assert 'equation' in form.fields
        
        # Form should render
        html = str(form['equation'])
        assert html is not None
        assert len(html) > 0
    
    def test_validators_work_on_current_django(self):
        """
        What we are testing: Validators work on current Django
        Why we are testing: Compatibility - validators are core Django feature
        Expected Result: Validator works in Django forms
        """
        class TestForm(forms.Form):
            equation = forms.CharField(
                widget=MathInputWidget(),
                validators=[MathInputValidator()]
            )
        
        form = TestForm(data={'equation': r'\frac{1}{2}'})
        assert form.is_valid()
        
        form_invalid = TestForm(data={'equation': r'\input{/etc/passwd}'})
        assert not form_invalid.is_valid()


@pytest.mark.compatibility
class TestPythonVersionsCompatible:
    """
    What we are testing: Widget works with Python 3.8, 3.9, 3.10, 3.11, 3.12
    Why we are testing: Compatibility requirement (NFR-04)
    Expected Result: Widget functions correctly on all supported Python versions
    """
    
    def test_python_version_detected(self):
        """
        What we are testing: Python version is detected correctly
        Why we are testing: Compatibility - need to know Python version
        Expected Result: Python version is accessible
        """
        python_version = sys.version_info
        assert python_version.major == 3
        assert python_version.minor >= 8, \
            f"Python version {python_version.major}.{python_version.minor} should be 3.8+"
    
    def test_widget_works_on_current_python(self):
        """
        What we are testing: Widget works on current Python version
        Why we are testing: Compatibility - basic functionality
        Expected Result: Widget renders correctly
        """
        widget = MathInputWidget()
        html = widget.render('equation', r'\frac{1}{2}')
        
        assert html is not None
        assert len(html) > 0
    
    def test_type_hints_compatible(self):
        """
        What we are testing: Type hints work on current Python
        Why we are testing: Compatibility - type hints require Python 3.5+
        Expected Result: Type hints don't cause errors
        """
        # If we can import and use the modules, type hints are compatible
        from mathinput.widgets import MathInputWidget
        from mathinput.validators import MathInputValidator
        
        widget = MathInputWidget()
        validator = MathInputValidator()
        
        assert widget is not None
        assert validator is not None
    
    def test_f_strings_compatible(self):
        """
        What we are testing: f-strings work on current Python
        Why we are testing: Compatibility - f-strings require Python 3.6+
        Expected Result: f-strings work correctly
        """
        # Test f-string usage (requires Python 3.6+)
        value = "test"
        result = f"Value is {value}"
        assert result == "Value is test"


@pytest.mark.compatibility
class TestCrossVersionCompatibility:
    """
    What we are testing: Widget works across different version combinations
    Why we are testing: Compatibility - real-world usage
    Expected Result: Widget functions correctly
    """
    
    def test_basic_functionality_across_versions(self):
        """
        What we are testing: Basic functionality works across versions
        Why we are testing: Compatibility - core features should work
        Expected Result: All basic features work
        """
        # Widget creation
        widget = MathInputWidget()
        assert widget is not None
        
        # Widget rendering
        html = widget.render('equation', r'\frac{1}{2}')
        assert html is not None
        
        # Validation
        validator = MathInputValidator()
        result = validator.validate(r'\frac{1}{2}')
        assert result is not None
        
        # Sanitization
        sanitized = sanitize_latex(r'\frac{1}{2}')
        assert sanitized is not None
        
        # Template filters
        widget_html = as_mathinput(r'\frac{1}{2}')
        assert widget_html is not None
        
        display_html = render_math(r'\frac{1}{2}')
        assert display_html is not None
    
    def test_all_modes_work(self):
        """
        What we are testing: All modes work across versions
        Why we are testing: Compatibility - modes should work on all versions
        Expected Result: All modes render correctly
        """
        modes = [
            'regular_functions',
            'advanced_expressions',
            'integrals_differentials',
            'matrices',
            'statistics_probability',
            'physics_engineering',
        ]
        
        for mode in modes:
            widget = MathInputWidget(mode=mode)
            html = widget.render('equation', r'\frac{1}{2}')
            assert html is not None
    
    def test_all_presets_work(self):
        """
        What we are testing: All presets work across versions
        Why we are testing: Compatibility - presets should work on all versions
        Expected Result: All presets render correctly
        """
        presets = [
            'algebra',
            'calculus',
            'physics',
            'machine_learning',
            'statistics',
            'probability',
        ]
        
        for preset in presets:
            widget = MathInputWidget(preset=preset)
            html = widget.render('equation', r'\frac{1}{2}')
            assert html is not None

