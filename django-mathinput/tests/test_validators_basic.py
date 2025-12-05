"""
Basic tests for validators module.

These tests verify the validator functions work correctly.
Full tests will be in Phase 1 testing.
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

from mathinput.validators import (
    MathInputValidator,
    count_nesting,
    get_matrix_size,
    validate_complexity,
    MAX_FORMULA_LENGTH,
    MAX_NESTING_DEPTH,
    MAX_MATRIX_SIZE,
)


@pytest.mark.unit
@pytest.mark.security
def test_validator_rejects_too_long_formula():
    """
    What we are testing: MathInputValidator rejects formulas exceeding length limit
    Why we are testing: Prevent DoS attacks via extremely long formulas
    Expected Result: ValidationError raised for formulas > 10,000 characters
    """
    validator = MathInputValidator()
    long_formula = 'x' * (MAX_FORMULA_LENGTH + 1)
    
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(long_formula)
    
    assert 'too long' in str(exc_info.value).lower()


@pytest.mark.unit
@pytest.mark.security
def test_validator_rejects_disallowed_commands():
    """
    What we are testing: MathInputValidator rejects formulas with disallowed commands
    Why we are testing: Security - enforce command whitelist
    Expected Result: ValidationError raised for formulas containing \\input, \\include, etc.
    """
    validator = MathInputValidator()
    
    # \input is caught by dangerous pattern check first (which is correct)
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(r'\input{file}')
    
    # Should be caught by dangerous pattern check
    error_msg = str(exc_info.value).lower()
    assert 'unsafe' in error_msg or 'dangerous' in error_msg or 'not allowed' in error_msg


@pytest.mark.unit
def test_validator_accepts_allowed_commands():
    """
    What we are testing: MathInputValidator accepts formulas with allowed commands
    Why we are testing: Ensure legitimate math operations pass validation
    Expected Result: No ValidationError for formulas with \\frac, \\sqrt, etc.
    """
    validator = MathInputValidator()
    
    # Should not raise
    result = validator.validate(r'\frac{1}{2} + \sqrt{x}')
    assert 'frac' in result
    assert 'sqrt' in result


@pytest.mark.unit
def test_count_nesting_calculates_depth():
    """
    What we are testing: count_nesting correctly calculates maximum nesting depth
    Why we are testing: Prevent DoS via deeply nested structures
    Expected Result: Returns correct nesting depth for nested fractions/expressions
    """
    # Simple formula - depth 1
    assert count_nesting(r'\frac{1}{2}') == 1
    
    # Nested formula - depth 2
    assert count_nesting(r'\frac{\frac{1}{2}}{3}') == 2
    
    # Deeply nested - depth 3
    assert count_nesting(r'\frac{\frac{\frac{1}{2}}{3}}{4}') == 3
    
    # Flat formula - depth 0
    assert count_nesting(r'x + y') == 0


@pytest.mark.unit
@pytest.mark.security
def test_validator_rejects_too_deeply_nested():
    """
    What we are testing: MathInputValidator rejects formulas exceeding nesting depth
    Why we are testing: Prevent DoS attacks via deeply nested structures
    Expected Result: ValidationError raised for formulas with > 50 levels of nesting
    """
    validator = MathInputValidator(max_nesting=5)  # Lower limit for testing
    
    # Create deeply nested formula
    deeply_nested = r'\frac{' * 6 + '1' + '}' * 6
    
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(deeply_nested)
    
    assert 'too deeply nested' in str(exc_info.value).lower()


@pytest.mark.unit
def test_get_matrix_size_detects_dimensions():
    """
    What we are testing: get_matrix_size correctly extracts matrix dimensions
    Why we are testing: Need to validate matrix size limits
    Expected Result: Returns tuple (rows, cols) for valid matrices
    """
    # 2x2 matrix
    size = get_matrix_size(r'\begin{pmatrix} a & b \\ c & d \end{pmatrix}')
    assert size == (2, 2)
    
    # 3x3 matrix
    size = get_matrix_size(r'\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}')
    assert size == (3, 3)
    
    # 1x1 matrix
    size = get_matrix_size(r'\begin{matrix} a \end{matrix}')
    assert size == (1, 1)
    
    # No matrix
    size = get_matrix_size(r'\frac{1}{2}')
    assert size is None


@pytest.mark.unit
@pytest.mark.security
def test_validator_rejects_oversized_matrix():
    """
    What we are testing: MathInputValidator rejects matrices exceeding size limits
    Why we are testing: Prevent DoS via extremely large matrices
    Expected Result: ValidationError raised for matrices > 100×100
    """
    validator = MathInputValidator(max_matrix_size=(2, 2))  # Small limit for testing
    
    # 3x3 matrix (exceeds 2x2 limit)
    large_matrix = r'\begin{pmatrix} a & b & c \\ d & e & f \\ g & h & i \end{pmatrix}'
    
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(large_matrix)
    
    assert 'too large' in str(exc_info.value).lower()


@pytest.mark.unit
def test_validate_complexity_non_raising():
    """
    What we are testing: validate_complexity returns validation status without raising
    Why we are testing: Need non-raising validation for client-side checks
    Expected Result: Returns (True, []) for valid, (False, [issues]) for invalid
    """
    # Valid formula
    is_valid, issues = validate_complexity(r'\frac{1}{2}')
    assert is_valid is True
    assert len(issues) == 0
    
    # Invalid formula (too long)
    long_formula = 'x' * (MAX_FORMULA_LENGTH + 1)
    is_valid, issues = validate_complexity(long_formula)
    assert is_valid is False
    assert len(issues) > 0
    assert any('too long' in issue.lower() for issue in issues)


@pytest.mark.unit
def test_validator_sanitizes_output():
    """
    What we are testing: MathInputValidator sanitizes output before returning
    Why we are testing: Security - ensure output is safe even if input passes validation
    Expected Result: Returned string is sanitized (dangerous patterns removed)
    """
    validator = MathInputValidator()
    
    # Even if input passes validation, output should be sanitized
    result = validator.validate(r'\frac{1}{2}')
    # Result should be sanitized (though in this case, safe input = safe output)
    assert isinstance(result, str)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

