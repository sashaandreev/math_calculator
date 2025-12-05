"""
Security module for LaTeX sanitization and validation.

Provides functions to sanitize LaTeX input, extract commands,
and detect dangerous patterns to prevent XSS and command injection attacks.
"""
import re
from typing import List, Set, Optional


# Dangerous LaTeX commands to block
DANGEROUS_COMMANDS = [
    # File system access
    r'\\input\s*\{',
    r'\\include\s*\{',
    r'\\verbatiminput\s*\{',
    r'\\lstinputlisting\s*\{',
    # System command execution
    r'\\write18\s*\{',
    # Macro definition (potential DoS)
    r'\\def\s*',
    r'\\newcommand\s*\{',
    r'\\renewcommand\s*\{',
    r'\\providecommand\s*\{',
    # Package loading
    r'\\usepackage\s*\{',
    r'\\RequirePackage\s*\{',
    r'\\documentclass\s*\{',
    # Code execution
    r'\\catcode\s*',
    r'\\makeatletter',
    r'\\makeatother',
    # JavaScript injection
    r'\\href\s*\{[^}]*javascript:',
    r'javascript:',
    # HTML/JS tags
    r'<script',
    r'</script>',
    r'<iframe',
    r'onerror\s*=',
    r'onclick\s*=',
    r'onload\s*=',
    r'onmouseover\s*=',
]


# Blocked command names (for whitelist checking)
BLOCKED_COMMANDS = {
    'input', 'include', 'write18', 'def', 'newcommand', 'renewcommand',
    'providecommand', 'verbatiminput', 'lstinputlisting', 'catcode',
    'makeatletter', 'makeatother', 'usepackage', 'RequirePackage',
    'documentclass', 'href',  # href is blocked if contains javascript:
}


# Allowed LaTeX commands (whitelist)
# This is a comprehensive list of safe mathematical commands
ALLOWED_COMMANDS = {
    # Math operations
    'frac', 'sqrt', 'root', 'sum', 'int', 'prod', 'lim', 'inf',
    # Functions
    'sin', 'cos', 'tan', 'sec', 'csc', 'cot',
    'arcsin', 'arccos', 'arctan', 'arcsec', 'arccsc', 'arccot',
    'sinh', 'cosh', 'tanh', 'sech', 'csch', 'coth',
    'log', 'ln', 'exp', 'lg',
    # Formatting
    'mathbf', 'mathit', 'mathrm', 'mathsf', 'mathtt', 'mathcal',
    'mathbb', 'mathfrak', 'mathscr',
    'text', 'textbf', 'textit', 'textsf', 'texttt', 'textsc',
    'emph', 'underline', 'overline',
    # Structures
    'begin', 'end',
    'matrix', 'pmatrix', 'bmatrix', 'Bmatrix', 'vmatrix', 'Vmatrix',
    'array', 'cases', 'align', 'aligned', 'eqnarray', 'equation',
    'split', 'multline', 'gather', 'gathered',
    # Operators
    'partial', 'nabla', 'Delta', 'nabla',
    'cdot', 'times', 'div', 'pm', 'mp',
    'leq', 'geq', 'neq', 'approx', 'equiv', 'sim',
    'in', 'notin', 'subset', 'supset', 'subseteq', 'supseteq',
    'cup', 'cap', 'setminus', 'emptyset',
    'forall', 'exists', 'nexists',
    # Greek letters (common ones)
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'varepsilon',
    'zeta', 'eta', 'theta', 'vartheta', 'iota', 'kappa',
    'lambda', 'mu', 'nu', 'xi', 'pi', 'varpi', 'rho', 'varrho',
    'sigma', 'varsigma', 'tau', 'upsilon', 'phi', 'varphi',
    'chi', 'psi', 'omega',
    'Gamma', 'Delta', 'Theta', 'Lambda', 'Xi', 'Pi', 'Sigma',
    'Upsilon', 'Phi', 'Psi', 'Omega',
    # Symbols
    'infty', 'emptyset', 'varnothing',
    'ell', 'hbar', 'imath', 'jmath',
    # Superscripts and subscripts
    '^', '_',
    # Spacing
    'quad', 'qquad', 'hspace', 'vspace', 'thinspace', 'medspace',
    'thickspace', 'negthinspace', 'negmedspace', 'negthickspace',
    # Delimiters
    'left', 'right', 'big', 'Big', 'bigg', 'Bigg',
    # Accents
    'hat', 'check', 'breve', 'acute', 'grave', 'tilde', 'bar',
    'vec', 'dot', 'ddot', 'dddot', 'ddddot',
    # Colors (if enabled)
    'color', 'textcolor', 'colorbox', 'fcolorbox',
    # Other safe commands
    'label', 'ref', 'eqref', 'tag',
    'not', 'neg',
    'prime', 'backprime',
    'ldots', 'cdots', 'vdots', 'ddots',
    'angle', 'measuredangle', 'sphericalangle',
    'parallel', 'nparallel', 'perp',
    'propto', 'asymp',
}


def sanitize_latex(latex_string: str) -> str:
    """
    Remove dangerous LaTeX commands from input string.
    
    This function removes patterns that could be used for:
    - File system access (\\input, \\include)
    - System command execution (\\write18)
    - Macro definition attacks (\\def, \\newcommand)
    - JavaScript injection (\\href{javascript:...})
    - HTML/JS tags (<script>, onclick=, etc.)
    
    Args:
        latex_string: Input LaTeX string to sanitize
    
    Returns:
        Sanitized LaTeX string with dangerous patterns removed
    
    Example:
        >>> sanitize_latex(r'\\input{file.tex}')
        ''
        >>> sanitize_latex(r'\\frac{1}{2}')
        r'\\frac{1}{2}'  # doctest: +SKIP
    """
    if not latex_string:
        return ''
    
    result = latex_string
    
    # Remove dangerous command patterns
    for pattern in DANGEROUS_COMMANDS:
        result = re.sub(pattern, '', result, flags=re.IGNORECASE)
    
    # Remove any remaining href with javascript: (case-insensitive)
    result = re.sub(
        r'\\href\s*\{[^}]*javascript:[^}]*\}',
        '',
        result,
        flags=re.IGNORECASE
    )
    
    # Remove any HTML tags
    result = re.sub(r'<[^>]+>', '', result)
    
    # Remove any remaining event handlers
    result = re.sub(
        r'\s*(on\w+)\s*=\s*["\'][^"\']*["\']',
        '',
        result,
        flags=re.IGNORECASE
    )
    
    return result


def extract_commands(latex_string: str) -> List[str]:
    """
    Extract all LaTeX commands from a string.
    
    LaTeX commands are identified by backslash followed by letters,
    e.g., \\frac, \\sqrt, \\int, etc.
    
    Args:
        latex_string: Input LaTeX string
    
    Returns:
        List of command names (without backslash)
    
    Example:
        >>> extract_commands(r'\\frac{1}{2} + \\sqrt{x}')
        ['frac', 'sqrt']  # doctest: +SKIP
    """
    if not latex_string:
        return []
    
    # Pattern: backslash followed by one or more letters
    pattern = r'\\([a-zA-Z]+)'
    matches = re.findall(pattern, latex_string)
    
    # Remove duplicates and return
    return list(set(matches))


def contains_dangerous_pattern(latex_string: str) -> bool:
    """
    Check if string contains dangerous patterns.
    
    This function checks for:
    - Dangerous LaTeX commands
    - JavaScript injection attempts
    - HTML/JS tags
    - Event handlers
    
    Args:
        latex_string: Input LaTeX string to check
    
    Returns:
        True if dangerous patterns found, False otherwise
    
    Example:
        >>> contains_dangerous_pattern(r'\\input{file}')
        True
        >>> contains_dangerous_pattern(r'\\frac{1}{2}')
        False
    """
    if not latex_string:
        return False
    
    # Check for dangerous command patterns
    for pattern in DANGEROUS_COMMANDS:
        if re.search(pattern, latex_string, re.IGNORECASE):
            return True
    
    # Check for javascript: in href
    if re.search(r'\\href\s*\{[^}]*javascript:', latex_string, re.IGNORECASE):
        return True
    
    # Check for HTML tags
    if re.search(r'<[^>]+>', latex_string):
        return True
    
    # Check for event handlers
    if re.search(r'\s*(on\w+)\s*=', latex_string, re.IGNORECASE):
        return True
    
    return False


def is_command_allowed(command: str) -> bool:
    """
    Check if a LaTeX command is in the allowed whitelist.
    
    Args:
        command: Command name (without backslash)
    
    Returns:
        True if command is allowed, False otherwise
    
    Example:
        >>> is_command_allowed('frac')
        True
        >>> is_command_allowed('input')
        False
    """
    if not command:
        return False
    
    # Normalize command name (lowercase, strip whitespace)
    command = command.lower().strip()
    
    # Check if blocked
    if command in BLOCKED_COMMANDS:
        return False
    
    # Check if allowed
    return command in ALLOWED_COMMANDS


def validate_commands(latex_string: str) -> tuple[bool, List[str]]:
    """
    Validate that all commands in LaTeX string are allowed.
    
    Args:
        latex_string: Input LaTeX string to validate
    
    Returns:
        Tuple of (is_valid, list_of_blocked_commands)
    
    Example:
        >>> validate_commands(r'\\frac{1}{2}')
        (True, [])
        >>> validate_commands(r'\\input{file}')
        (False, ['input'])
    """
    commands = extract_commands(latex_string)
    blocked = []
    
    for cmd in commands:
        if not is_command_allowed(cmd):
            blocked.append(cmd)
    
    return (len(blocked) == 0, blocked)


def get_blocked_commands() -> Set[str]:
    """
    Get set of blocked command names.
    
    Returns:
        Set of blocked command names
    """
    return BLOCKED_COMMANDS.copy()


def get_allowed_commands() -> Set[str]:
    """
    Get set of allowed command names.
    
    Returns:
        Set of allowed command names
    """
    return ALLOWED_COMMANDS.copy()

