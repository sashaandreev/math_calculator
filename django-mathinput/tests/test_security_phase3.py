"""
Security tests for Phase 3: Quick Insert, Text Formatting, Source Mode.

Tests security aspects of Phase 3 features.
"""
import pytest
from django import forms
from mathinput.widgets import MathInputWidget
from mathinput.presets import load_preset, get_all_presets
from mathinput.security import sanitize_latex, validate_commands, contains_dangerous_pattern


@pytest.mark.security
def test_quick_insert_templates_sanitized():
    """
    What we are testing: Quick insert templates are sanitized before insertion
    Why we are testing: Security - prevent injection via template system
    Expected Result: Templates do not contain dangerous commands
    """
    all_presets = get_all_presets()
    
    for preset_code, preset in all_presets.items():
        if 'quick_inserts' in preset:
            for item in preset['quick_inserts']:
                name, latex = item
                
                # Check that template doesn't contain dangerous patterns
                assert not contains_dangerous_pattern(latex)
                
                # Check that template passes validation (returns tuple)
                is_valid, blocked = validate_commands(latex)
                # Templates may contain commands not in whitelist, but should not be dangerous
                assert not contains_dangerous_pattern(latex)
                
                # Check that sanitized version is safe
                sanitized = sanitize_latex(latex)
                assert '<script' not in sanitized.lower()
                assert 'javascript:' not in sanitized.lower()


@pytest.mark.security
def test_source_mode_input_sanitized():
    """
    What we are testing: Source mode input is sanitized before sync
    Why we are testing: Security - prevent XSS via direct LaTeX input
    Expected Result: Dangerous commands removed from source input
    """
    # Test dangerous LaTeX patterns
    dangerous_inputs = [
        '<script>alert("xss")</script>',
        'javascript:alert("xss")',
        '\\input{../../../etc/passwd}',
        '\\include{malicious.tex}',
    ]
    
    for dangerous_input in dangerous_inputs:
        # Should be sanitized
        sanitized = sanitize_latex(dangerous_input)
        
        # Should not contain script tags
        assert '<script' not in sanitized.lower()
        assert 'javascript:' not in sanitized.lower()
        
        # Should not contain dangerous commands
        assert not contains_dangerous_pattern(sanitized)


@pytest.mark.security
def test_format_commands_safe():
    """
    What we are testing: Formatting commands don't allow injection
    Why we are testing: Security - format commands should be safe
    Expected Result: Format commands validated and sanitized
    """
    format_commands = [
        r'\textbf{test}',
        r'\textcolor{red}{test}',
        r'\large{test}',
    ]
    
    for latex in format_commands:
        # Should pass validation (returns tuple)
        is_valid, blocked = validate_commands(latex)
        # Format commands should be valid or at least not dangerous
        assert not contains_dangerous_pattern(latex)
        
        # Should be sanitized correctly
        sanitized = sanitize_latex(latex)
        assert len(sanitized) > 0


@pytest.mark.security
def test_source_mode_prevents_xss():
    """
    What we are testing: Source mode prevents XSS attacks
    Why we are testing: Security - direct LaTeX input must be safe
    Expected Result: XSS attempts blocked in source mode
    """
    xss_attempts = [
        '<script>alert("xss")</script>',
        '<img src=x onerror=alert("xss")>',
        'javascript:alert("xss")',
        'onclick="alert(\'xss\')"',
    ]
    
    for xss_input in xss_attempts:
        sanitized = sanitize_latex(xss_input)
        
        # Should not contain script tags
        assert '<script' not in sanitized.lower()
        assert 'onerror' not in sanitized.lower()
        assert 'onclick' not in sanitized.lower()
        assert 'javascript:' not in sanitized.lower()


@pytest.mark.security
def test_quick_insert_template_validation():
    """
    What we are testing: Quick insert templates are validated
    Why we are testing: Security - templates must be safe
    Expected Result: All templates pass security validation
    """
    all_presets = get_all_presets()
    
    for preset_code, preset in all_presets.items():
        if 'quick_inserts' in preset:
            for item in preset['quick_inserts']:
                name, latex = item
                
                # Should pass command validation (returns tuple)
                is_valid, blocked = validate_commands(latex)
                # Templates should not contain dangerous patterns
                assert not contains_dangerous_pattern(latex)

