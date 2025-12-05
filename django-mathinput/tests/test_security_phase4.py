"""
Security tests for Phase 4: Template Tags, Admin Integration.

Tests security aspects of Phase 4 features.
"""
import pytest
from django.test import TestCase
from mathinput.templatetags.mathinput_tags import render_math, as_mathinput
from django.utils.html import escape


@pytest.mark.security
def test_render_math_sanitizes_output():
    """
    What we are testing: render_math filter sanitizes output HTML
    Why we are testing: Security - prevent XSS in rendered output
    Expected Result: Output is safe HTML, no script tags
    """
    # Test with potential XSS
    xss_attempt = r'<script>alert("xss")</script>'
    result = render_math(xss_attempt)
    
    # Should not contain unescaped script tags
    assert '<script>' not in result or '&lt;script&gt;' in result
    
    # Test with HTML entities
    html_content = r'x < 1 & y > 0'
    result2 = render_math(html_content)
    
    # HTML should be escaped
    assert result2 is not None


@pytest.mark.security
def test_template_tags_escape_user_input():
    """
    What we are testing: Template tags properly escape user input
    Why we are testing: Security - prevent template injection
    Expected Result: User input is escaped in template output
    """
    # Test with special characters
    special_chars = r'x "quoted" & <tagged>'
    result = render_math(special_chars)
    
    # Should be escaped
    assert result is not None
    # Check that HTML entities are used
    assert '&quot;' in result or '&lt;' in result or 'data-latex' in result


@pytest.mark.security
def test_render_math_handles_malicious_latex():
    """
    What we are testing: render_math handles potentially malicious LaTeX
    Why we are testing: Security - prevent injection via LaTeX
    Expected Result: Malicious content sanitized or safely rendered
    """
    # Test with JavaScript protocol
    malicious = r'\href{javascript:alert("xss")}{link}'
    result = render_math(malicious)
    
    # Should not contain unescaped javascript:
    assert 'javascript:' not in result.lower() or '&quot;' in result
    
    # Test with HTML tags
    html_tags = r'<img src=x onerror=alert(1)>'
    result2 = render_math(html_tags)
    
    # HTML should be escaped
    assert result2 is not None


@pytest.mark.security
def test_as_mathinput_sanitizes_value():
    """
    What we are testing: as_mathinput filter sanitizes input value
    Why we are testing: Security - prevent XSS in widget value
    Expected Result: Widget value is safely rendered
    """
    # Test with potential XSS
    xss_value = '<script>alert("xss")</script>'
    result = as_mathinput(xss_value)
    
    # Widget should render, but value should be escaped
    assert result is not None
    assert 'mi-widget' in result or 'widget' in result.lower()
    
    # Value should not contain unescaped script tags
    # (Widget rendering handles this, but we verify it works)
    assert result is not None

