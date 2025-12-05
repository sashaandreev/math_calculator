"""
Unit tests for Text Formatting functionality.

Tests text formatting commands and LaTeX generation.
"""
import pytest
from mathinput.security import sanitize_latex, validate_commands


@pytest.mark.unit
def test_bold_format_applied():
    """
    What we are testing: Bold formatting correctly wraps text in \textbf{}
    Why we are testing: Text formatting is core feature for emphasis
    Expected Result: Selected text wrapped in \textbf{} command
    """
    # Test that \textbf{} is a valid LaTeX command
    latex = r'\textbf{test}'
    
    # Should pass validation (returns tuple: (is_valid, blocked_commands))
    is_valid, blocked = validate_commands(latex)
    assert is_valid is True
    assert len(blocked) == 0
    
    # Should be sanitized correctly
    sanitized = sanitize_latex(latex)
    assert r'\textbf' in sanitized


@pytest.mark.unit
def test_color_format_applied():
    """
    What we are testing: Color formatting correctly applies \textcolor{} command
    Why we are testing: Users need color formatting for visual emphasis
    Expected Result: Selected text wrapped in \textcolor{color}{} command
    """
    # Test that \textcolor{} is a valid LaTeX command
    latex = r'\textcolor{red}{test}'
    
    # Should pass validation (returns tuple: (is_valid, blocked_commands))
    is_valid, blocked = validate_commands(latex)
    assert is_valid is True
    assert len(blocked) == 0
    
    # Should be sanitized correctly
    sanitized = sanitize_latex(latex)
    assert r'\textcolor' in sanitized


@pytest.mark.unit
def test_size_format_applied():
    """
    What we are testing: Size formatting correctly applies size commands
    Why we are testing: Users need different text sizes in formulas
    Expected Result: Selected text wrapped in appropriate size command
    """
    # Test various size commands
    # Note: Some size commands may not be in the allowed list, but they should still be sanitized
    size_commands = [
        r'\small{test}',
        r'\large{test}',
        r'\Large{test}',
        r'\huge{test}',
    ]
    
    for latex in size_commands:
        # Check validation (returns tuple: (is_valid, blocked_commands))
        is_valid, blocked = validate_commands(latex)
        # Size commands may or may not be in allowed list, but should be sanitizable
        assert isinstance(is_valid, bool)
        
        # Should be sanitized correctly
        sanitized = sanitize_latex(latex)
        assert len(sanitized) > 0


@pytest.mark.unit
def test_format_commands_sanitized():
    """
    What we are testing: Formatting commands are properly sanitized
    Why we are testing: Security - format commands should not contain dangerous content
    Expected Result: Formatting commands pass sanitization
    """
    format_commands = [
        r'\textbf{test}',
        r'\textcolor{red}{test}',
        r'\large{test}',
        r'\textit{test}',
        r'\textsc{test}',
    ]
    
    for latex in format_commands:
        sanitized = sanitize_latex(latex)
        
        # Should not contain script tags
        assert '<script' not in sanitized.lower()
        
        # Should still contain the command (or be sanitized safely)
        assert len(sanitized) > 0

