"""
Security tests for Phase 1.

Tests security features including XSS prevention, command injection prevention,
and DoS prevention mechanisms.
"""
import pytest
import os
import django
from django.conf import settings
from django.core.exceptions import ValidationError

# Configure Django settings for testing
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    django.setup()

from mathinput.security import sanitize_latex, contains_dangerous_pattern
from mathinput.validators import MathInputValidator


@pytest.mark.security
def test_xss_prevention_script_tags():
    """
    What we are testing: Security module prevents XSS via <script> tags
    Why we are testing: Critical security requirement - prevent script injection
    Expected Result: <script> tags are removed from input
    """
    malicious_input = r'<script>alert("XSS")</script>\frac{1}{2}'
    
    # Check that dangerous pattern is detected
    assert contains_dangerous_pattern(malicious_input), "Should detect script tags"
    
    # Check that script tags are removed
    sanitized = sanitize_latex(malicious_input)
    assert '<script>' not in sanitized.lower()
    assert '</script>' not in sanitized.lower()
    # Safe content should remain
    assert 'frac' in sanitized


@pytest.mark.security
def test_xss_prevention_javascript_protocol():
    """
    What we are testing: Security module prevents XSS via javascript: protocol
    Why we are testing: Prevent javascript execution in href attributes
    Expected Result: javascript: protocol is removed from input
    """
    malicious_input = r'\href{javascript:alert("XSS")}{Click}'
    
    # Check that dangerous pattern is detected
    assert contains_dangerous_pattern(malicious_input), "Should detect javascript: protocol"
    
    # Check that javascript: is removed
    sanitized = sanitize_latex(malicious_input)
    assert 'javascript:' not in sanitized.lower()
    
    # Validator should reject it
    validator = MathInputValidator()
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(malicious_input)
    
    assert 'unsafe' in str(exc_info.value).lower() or 'dangerous' in str(exc_info.value).lower()


@pytest.mark.security
def test_command_injection_prevention():
    r"""
    What we are testing: Validator prevents LaTeX command injection
    Why we are testing: Prevent file system access and system command execution
    Expected Result: Commands like \input, \write18 are rejected
    """
    validator = MathInputValidator()
    
    # Test file system access command
    malicious_input = r'\input{/etc/passwd}'
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(malicious_input)
    
    error_msg = str(exc_info.value).lower()
    assert 'unsafe' in error_msg or 'dangerous' in error_msg or 'not allowed' in error_msg
    
    # Test system command execution
    malicious_input = r'\write18{rm -rf /}'
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(malicious_input)
    
    error_msg = str(exc_info.value).lower()
    assert 'unsafe' in error_msg or 'dangerous' in error_msg or 'not allowed' in error_msg


@pytest.mark.security
def test_dos_prevention_long_formula():
    """
    What we are testing: Validator prevents DoS via extremely long formulas
    Why we are testing: Prevent resource exhaustion attacks
    Expected Result: Formulas > 10,000 characters are rejected
    """
    validator = MathInputValidator()
    
    # Create formula exceeding max length
    long_formula = 'x' * 10001  # Exceeds default 10,000 limit
    
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(long_formula)
    
    assert 'too long' in str(exc_info.value).lower()
    
    # Valid formula should pass
    valid_formula = 'x' * 1000  # Within limit
    result = validator.validate(valid_formula)
    assert isinstance(result, str)


@pytest.mark.security
def test_dos_prevention_deep_nesting():
    """
    What we are testing: Validator prevents DoS via deeply nested structures
    Why we are testing: Prevent CPU/memory exhaustion from complex parsing
    Expected Result: Formulas with > 50 nesting levels are rejected
    """
    validator = MathInputValidator(max_nesting=5)  # Lower limit for testing
    
    # Create deeply nested formula
    deeply_nested = r'\frac{' * 6 + '1' + '}' * 6  # 6 levels of nesting
    
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(deeply_nested)
    
    assert 'too deeply nested' in str(exc_info.value).lower()
    
    # Valid nesting should pass
    valid_nested = r'\frac{1}{2}'  # 1 level
    result = validator.validate(valid_nested)
    assert isinstance(result, str)


@pytest.mark.security
def test_dos_prevention_large_matrix():
    """
    What we are testing: Validator prevents DoS via extremely large matrices
    Why we are testing: Prevent memory exhaustion from large matrix rendering
    Expected Result: Matrices > 100×100 are rejected
    """
    validator = MathInputValidator(max_matrix_size=(2, 2))  # Small limit for testing
    
    # Create large matrix (3x3, exceeds 2x2 limit)
    large_matrix = r'\begin{pmatrix} a & b & c \\ d & e & f \\ g & h & i \end{pmatrix}'
    
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(large_matrix)
    
    assert 'too large' in str(exc_info.value).lower()
    
    # Valid matrix should pass
    valid_matrix = r'\begin{pmatrix} a & b \\ c & d \end{pmatrix}'  # 2x2
    result = validator.validate(valid_matrix)
    assert isinstance(result, str)

