"""
Validators module for formula complexity checks.

Provides validation functions to check formula length, nesting depth,
matrix size, and command whitelist to prevent DoS attacks and ensure
formulas are within acceptable complexity limits.
"""
import re
from typing import Optional, Tuple
from django.core.exceptions import ValidationError
from django.conf import settings

from .security import (
    sanitize_latex,
    extract_commands,
    contains_dangerous_pattern,
    is_command_allowed,
    ALLOWED_COMMANDS,
)

# Configuration constants (can be overridden in Django settings)
def _get_setting(name, default):
    """Get Django setting with fallback if not configured."""
    try:
        return getattr(settings, name, default)
    except Exception:
        return default

MAX_FORMULA_LENGTH = _get_setting('MATHINPUT_MAX_FORMULA_LENGTH', 10000)
MAX_NESTING_DEPTH = _get_setting('MATHINPUT_MAX_NESTING_DEPTH', 50)
MAX_MATRIX_SIZE = _get_setting('MATHINPUT_MAX_MATRIX_SIZE', (100, 100))


class MathInputValidator:
    """
    Validator for math input formulas.
    
    Performs comprehensive validation including:
    - Length checks
    - Command whitelist validation
    - Dangerous pattern detection
    - Complexity checks (nesting depth, matrix size)
    - Sanitization
    
    Usage:
        validator = MathInputValidator()
        try:
            sanitized = validator.validate(r'\\frac{1}{2}')
        except ValidationError as e:
            # Handle validation error
    """
    
    def __init__(self, max_length=None, max_nesting=None, max_matrix_size=None):
        """
        Initialize validator with optional custom limits.
        
        Args:
            max_length: Maximum formula length (defaults to MAX_FORMULA_LENGTH)
            max_nesting: Maximum nesting depth (defaults to MAX_NESTING_DEPTH)
            max_matrix_size: Maximum matrix size tuple (defaults to MAX_MATRIX_SIZE)
        """
        self.max_length = max_length or MAX_FORMULA_LENGTH
        self.max_nesting = max_nesting or MAX_NESTING_DEPTH
        self.max_matrix_size = max_matrix_size or MAX_MATRIX_SIZE
    
    def validate(self, latex_string: str) -> str:
        """
        Validate and sanitize LaTeX formula.
        
        Performs all validation checks and returns sanitized string.
        Raises ValidationError if validation fails.
        
        Args:
            latex_string: Input LaTeX string to validate
        
        Returns:
            Sanitized LaTeX string
        
        Raises:
            ValidationError: If validation fails
        
        Example:
            >>> validator = MathInputValidator()
            >>> validator.validate(r'\\frac{1}{2}')
            r'\\frac{1}{2}'  # doctest: +SKIP
            >>> validator.validate(r'\\input{file}')
            ValidationError: Formula contains unsafe content  # doctest: +SKIP
        """
        if not latex_string:
            return ''
        
        # 1. Length check
        if len(latex_string) > self.max_length:
            raise ValidationError(
                f"Formula too long (max {self.max_length:,} characters, "
                f"got {len(latex_string):,})"
            )
        
        # 2. Dangerous pattern check (before other checks)
        if contains_dangerous_pattern(latex_string):
            raise ValidationError(
                "Formula contains unsafe content. Dangerous patterns detected."
            )
        
        # 3. Command whitelist validation
        commands = extract_commands(latex_string)
        blocked_commands = []
        for cmd in commands:
            if not is_command_allowed(cmd):
                blocked_commands.append(cmd)
        
        if blocked_commands:
            raise ValidationError(
                f"Command(s) not allowed: {', '.join(blocked_commands)}"
            )
        
        # 4. Complexity checks
        nesting_depth = count_nesting(latex_string)
        if nesting_depth > self.max_nesting:
            raise ValidationError(
                f"Formula too deeply nested (max {self.max_nesting} levels, "
                f"got {nesting_depth})"
            )
        
        # 5. Matrix size check
        matrix_size = get_matrix_size(latex_string)
        if matrix_size:
            rows, cols = matrix_size
            max_rows, max_cols = self.max_matrix_size
            if rows > max_rows or cols > max_cols:
                raise ValidationError(
                    f"Matrix too large (max {max_rows}×{max_cols}, "
                    f"got {rows}×{cols})"
                )
        
        # 6. Sanitize and return
        return sanitize_latex(latex_string)
    
    def __call__(self, value):
        """
        Make validator callable for Django form validation.
        
        Django validators must be callable. This method allows
        MathInputValidator to be used directly in form field validators.
        
        Args:
            value: Input LaTeX string to validate
        
        Returns:
            Sanitized LaTeX string
        
        Raises:
            ValidationError: If validation fails
        """
        return self.validate(value)


def count_nesting(latex_string: str) -> int:
    r"""
    Count maximum nesting depth in LaTeX formula.
    
    Calculates the maximum depth of nested structures like:
    - Braces: { }
    - Fractions: \frac{}{}
    - Environments: \begin{}...\end{}
    - Parentheses: ( )
    - Brackets: [ ]
    
    Args:
        latex_string: Input LaTeX string
    
    Returns:
        Maximum nesting depth (0 for flat formulas)
    
    Example:
        >>> count_nesting(r'\\frac{1}{2}')
        1  # doctest: +SKIP
        >>> count_nesting(r'\\frac{\\frac{1}{2}}{3}')
        2  # doctest: +SKIP
    """
    if not latex_string:
        return 0
    
    max_depth = 0
    current_depth = 0
    
    # Track different bracket types
    brace_stack = []
    
    i = 0
    while i < len(latex_string):
        char = latex_string[i]
        
        # Opening braces
        if char == '{':
            current_depth += 1
            brace_stack.append('{')
            max_depth = max(max_depth, current_depth)
        # Closing braces
        elif char == '}':
            if brace_stack and brace_stack[-1] == '{':
                current_depth -= 1
                brace_stack.pop()
            # If mismatched, don't decrement (syntax error, but count what we can)
        
        # Opening parentheses
        elif char == '(':
            current_depth += 1
            brace_stack.append('(')
            max_depth = max(max_depth, current_depth)
        # Closing parentheses
        elif char == ')':
            if brace_stack and brace_stack[-1] == '(':
                current_depth -= 1
                brace_stack.pop()
        
        # Opening brackets
        elif char == '[':
            current_depth += 1
            brace_stack.append('[')
            max_depth = max(max_depth, current_depth)
        # Closing brackets
        elif char == ']':
            if brace_stack and brace_stack[-1] == '[':
                current_depth -= 1
                brace_stack.pop()
        
        # Skip escaped characters
        elif char == '\\' and i + 1 < len(latex_string):
            i += 1  # Skip next character (escaped)
        
        i += 1
    
    return max_depth


def get_matrix_size(latex_string: str) -> Optional[Tuple[int, int]]:
    r"""
    Get matrix dimensions if present in LaTeX string.
    
    Detects matrix environments:
    - \begin{matrix}...\end{matrix}
    - \begin{pmatrix}...\end{pmatrix}
    - \begin{bmatrix}...\end{bmatrix}
    - \begin{Bmatrix}...\end{Bmatrix}
    - \begin{vmatrix}...\end{vmatrix}
    - \begin{Vmatrix}...\end{Vmatrix}
    - \begin{array}...\end{array}
    
    Args:
        latex_string: Input LaTeX string
    
    Returns:
        Tuple of (rows, columns) if matrix found, None otherwise
    
    Example:
        >>> get_matrix_size(r'\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}')
        (2, 2)  # doctest: +SKIP
        >>> get_matrix_size(r'\\frac{1}{2}')
        None  # doctest: +SKIP
    """
    if not latex_string:
        return None
    
    # Matrix environment patterns
    matrix_patterns = [
        r'\\begin\{matrix\}',
        r'\\begin\{pmatrix\}',
        r'\\begin\{bmatrix\}',
        r'\\begin\{Bmatrix\}',
        r'\\begin\{vmatrix\}',
        r'\\begin\{Vmatrix\}',
        r'\\begin\{array\}',
    ]
    
    for pattern in matrix_patterns:
        # Find matrix environment
        match = re.search(pattern, latex_string, re.IGNORECASE)
        if match:
            # Find corresponding \end
            start_pos = match.end()
            end_pattern = pattern.replace('\\begin', '\\end')
            end_match = re.search(end_pattern, latex_string[start_pos:], re.IGNORECASE)
            
            if end_match:
                # Extract matrix content
                matrix_content = latex_string[start_pos:start_pos + end_match.start()]
                
                # Count rows (separated by \\)
                rows = matrix_content.count('\\\\') + 1
                if not matrix_content.strip():
                    rows = 0
                
                # Count columns in first row (separated by &)
                first_row_end = matrix_content.find('\\\\')
                if first_row_end == -1:
                    first_row = matrix_content
                else:
                    first_row = matrix_content[:first_row_end]
                
                # Count & separators + 1 for columns
                cols = first_row.count('&') + 1
                if not first_row.strip():
                    cols = 0
                
                # Return dimensions
                if rows > 0 and cols > 0:
                    return (rows, cols)
    
    return None


def validate_complexity(latex_string: str) -> Tuple[bool, list]:
    """
    Validate formula complexity and return detailed results.
    
    This is a non-raising version that returns validation status
    and list of issues instead of raising exceptions.
    
    Args:
        latex_string: Input LaTeX string to validate
    
    Returns:
        Tuple of (is_valid, list_of_issues)
        issues is empty list if valid, contains error messages if invalid
    
    Example:
        >>> is_valid, issues = validate_complexity(r'\\frac{1}{2}')
        >>> is_valid
        True
        >>> issues
        []
    """
    issues = []
    
    if not latex_string:
        return (True, [])
    
    # Length check
    if len(latex_string) > MAX_FORMULA_LENGTH:
        issues.append(
            f"Formula too long (max {MAX_FORMULA_LENGTH:,} characters, "
            f"got {len(latex_string):,})"
        )
    
    # Dangerous pattern check
    if contains_dangerous_pattern(latex_string):
        issues.append("Formula contains unsafe content")
    
    # Command whitelist check
    commands = extract_commands(latex_string)
    blocked_commands = []
    for cmd in commands:
        if not is_command_allowed(cmd):
            blocked_commands.append(cmd)
    
    if blocked_commands:
        issues.append(f"Command(s) not allowed: {', '.join(blocked_commands)}")
    
    # Nesting depth check
    nesting_depth = count_nesting(latex_string)
    if nesting_depth > MAX_NESTING_DEPTH:
        issues.append(
            f"Formula too deeply nested (max {MAX_NESTING_DEPTH} levels, "
            f"got {nesting_depth})"
        )
    
    # Matrix size check
    matrix_size = get_matrix_size(latex_string)
    if matrix_size:
        rows, cols = matrix_size
        max_rows, max_cols = MAX_MATRIX_SIZE
        if rows > max_rows or cols > max_cols:
            issues.append(
                f"Matrix too large (max {max_rows}×{max_cols}, got {rows}×{cols})"
            )
    
    return (len(issues) == 0, issues)

