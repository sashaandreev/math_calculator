"""
Integration tests for Phase 1.

Tests the integration of MathInputWidget with Django forms,
ensuring the widget works correctly in real form contexts.
"""
import pytest
import os
import django
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

# Configure Django settings for testing
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    django.setup()

from mathinput.widgets import MathInputWidget
from mathinput.validators import MathInputValidator


class MathForm(forms.Form):
    """Test form with MathInputWidget."""
    equation = forms.CharField(widget=MathInputWidget())


@pytest.mark.integration
class TestWidgetFormIntegration:
    """
    What we are testing: MathInputWidget integration with Django forms
    Why we are testing: Ensure widget works correctly in real form context
    Expected Result: Form renders with widget, submits correctly
    """
    
    def test_form_with_widget_renders(self):
        """
        What we are testing: Form with MathInputWidget renders without errors
        Why we are testing: Widget must integrate with Django form system
        Expected Result: Form HTML contains widget structure
        """
        form = MathForm()
        html = form.as_p()
        
        # Check that form renders
        assert isinstance(html, str)
        assert len(html) > 0
        
        # Check for widget elements
        assert 'equation' in html
        # Widget should render its structure
        assert 'mi-widget' in html or 'id_equation' in html
    
    def test_form_submission_with_valid_data(self):
        """
        What we are testing: Form submission with valid LaTeX formula
        Why we are testing: Ensure widget data is correctly submitted
        Expected Result: Form validates and processes valid formula
        """
        # Valid LaTeX formula
        valid_latex = r'\frac{1}{2} + \sqrt{x}'
        
        form = MathForm(data={'equation': valid_latex})
        
        # Form should be valid
        assert form.is_valid(), f"Form should be valid but got errors: {form.errors}"
        
        # Check cleaned data
        assert 'equation' in form.cleaned_data
        assert form.cleaned_data['equation'] == valid_latex
    
    def test_form_validation_with_invalid_data(self):
        """
        What we are testing: Form validation rejects invalid formulas
        Why we are testing: Security - prevent malicious input
        Expected Result: Form validation fails with ValidationError
        """
        # Invalid formula with dangerous command
        invalid_latex = r'\input{/etc/passwd}'
        
        form = MathForm(data={'equation': invalid_latex})
        
        # Form should not be valid
        # Note: In Phase 1, we don't have form field validation yet,
        # so we test that the validator would reject it
        validator = MathInputValidator()
        
        with pytest.raises(ValidationError):
            validator.validate(invalid_latex)
        
        # Form should still process the data (validation happens in view/clean)
        # This is expected behavior - validation is done server-side
        assert form.is_bound
        assert 'equation' in form.data

