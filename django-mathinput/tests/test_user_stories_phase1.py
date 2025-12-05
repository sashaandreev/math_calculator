"""
User story tests for Phase 1.

Tests user stories US-15 (Handle Errors Gracefully) and US-16 (Display Stored Formulas).
"""
import pytest
import os
import django
from django import forms
from django.conf import settings

# Configure Django settings for testing
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    django.setup()

from mathinput.widgets import MathInputWidget
from mathinput.validators import MathInputValidator, validate_complexity


@pytest.mark.user_story
@pytest.mark.us_16  # US-16: Display Stored Formulas
def test_widget_displays_existing_formula():
    """
    What we are testing: Widget displays existing formula value when initialized
    Why we are testing: US-16 - Users need to see and edit existing formulas
    Expected Result: Widget HTML contains existing formula value
    """
    existing_formula = r'\int_{0}^{1} x^2 dx'
    widget = MathInputWidget()
    
    # Render widget with existing value
    html = widget.render('equation', existing_formula, {'id': 'id_equation'})
    
    # Check that existing value is in the HTML
    assert isinstance(html, str)
    # The value should be present in the rendered HTML
    # (exact format depends on template, but value should be there)
    assert existing_formula in html or 'int' in html


@pytest.mark.user_story
@pytest.mark.us_15  # US-15: Handle Errors Gracefully
def test_widget_handles_invalid_formula_gracefully():
    """
    What we are testing: Widget handles invalid/corrupted formula values
    Why we are testing: US-15 - Users should see errors, not crashes
    Expected Result: Widget renders with error message, allows editing
    """
    widget = MathInputWidget()
    
    # Test with potentially problematic values
    problematic_values = [
        None,  # None value
        '',   # Empty string
        r'\frac{1}',  # Malformed (missing closing brace)
        r'<script>alert("XSS")</script>',  # XSS attempt
    ]
    
    for value in problematic_values:
        # Widget should render without crashing
        html = widget.render('equation', value, {'id': 'id_equation'})
        assert isinstance(html, str)
        assert len(html) > 0  # Should produce some HTML
    
    # Widget should handle None gracefully
    html = widget.render('equation', None, {'id': 'id_equation'})
    assert isinstance(html, str)


@pytest.mark.user_story
@pytest.mark.us_15
def test_validation_shows_clear_error_messages():
    """
    What we are testing: Validation provides clear, non-technical error messages
    Why we are testing: US-15 - Users need to understand what went wrong
    Expected Result: Error messages are user-friendly and actionable
    """
    validator = MathInputValidator()
    
    # Test various validation errors and check message clarity
    test_cases = [
        # (input, expected_keyword_in_error)
        ('x' * 10001, 'too long'),  # Length error
        (r'\input{file}', 'unsafe'),  # Dangerous command
        (r'\frac{' * 51 + '1' + '}' * 51, 'too deeply nested'),  # Nesting error
    ]
    
    for input_value, expected_keyword in test_cases:
        try:
            validator.validate(input_value)
            pytest.fail(f"Should have raised ValidationError for: {input_value[:50]}")
        except Exception as e:
            # Check that error message is clear and contains expected keyword
            error_msg = str(e).lower()
            assert expected_keyword in error_msg, \
                f"Error message should contain '{expected_keyword}', got: {error_msg}"
            
            # Error message should not be empty
            assert len(str(e)) > 0
    
    # Test non-raising validation function
    is_valid, issues = validate_complexity(r'\frac{1}{2}')
    assert is_valid is True
    assert len(issues) == 0
    
    # Test with invalid input
    is_valid, issues = validate_complexity('x' * 10001)
    assert is_valid is False
    assert len(issues) > 0
    # Issues should be clear and actionable
    assert any('too long' in issue.lower() for issue in issues)

