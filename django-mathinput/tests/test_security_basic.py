"""
Basic tests for security module.

These tests verify the security functions work correctly.
Full tests will be in Phase 1 testing.
"""
import pytest
import sys
from pathlib import Path

# Add package to path
package_dir = Path(__file__).parent.parent
sys.path.insert(0, str(package_dir))

from mathinput.security import (
    sanitize_latex,
    extract_commands,
    contains_dangerous_pattern,
    is_command_allowed,
    validate_commands,
    DANGEROUS_COMMANDS,
    ALLOWED_COMMANDS,
    BLOCKED_COMMANDS,
)


@pytest.mark.unit
@pytest.mark.security
def test_sanitize_removes_dangerous_commands():
    """
    What we are testing: sanitize_latex function removes dangerous LaTeX commands
    Why we are testing: Security - prevent XSS and command injection attacks
    Expected Result: Dangerous commands are removed from input string
    """
    # Test file system access
    result = sanitize_latex(r'\input{file.tex}')
    assert 'input' not in result.lower(), "Should remove \\input command"
    
    # Test system command execution
    result = sanitize_latex(r'\write18{rm -rf /}')
    assert 'write18' not in result.lower(), "Should remove \\write18 command"
    
    # Test macro definition
    result = sanitize_latex(r'\def\test{hello}')
    assert 'def' not in result.lower(), "Should remove \\def command"


@pytest.mark.unit
@pytest.mark.security
def test_sanitize_preserves_safe_commands():
    """
    What we are testing: sanitize_latex preserves safe mathematical commands
    Why we are testing: Ensure legitimate math operations are not blocked
    Expected Result: Safe commands like \\frac, \\sqrt remain unchanged
    """
    safe_latex = r'\frac{1}{2} + \sqrt{x}'
    result = sanitize_latex(safe_latex)
    
    assert 'frac' in result, "Should preserve \\frac"
    assert 'sqrt' in result, "Should preserve \\sqrt"


@pytest.mark.unit
@pytest.mark.security
def test_extract_commands():
    """
    What we are testing: extract_commands correctly identifies all LaTeX commands
    Why we are testing: Need accurate command extraction for whitelist validation
    Expected Result: All commands in string are extracted as list
    """
    latex = r'\frac{1}{2} + \sqrt{x} - \int f(x) dx'
    commands = extract_commands(latex)
    
    assert 'frac' in commands, "Should extract frac"
    assert 'sqrt' in commands, "Should extract sqrt"
    assert 'int' in commands, "Should extract int"
    assert len(commands) == 3, f"Should extract 3 commands, got {len(commands)}"


@pytest.mark.unit
@pytest.mark.security
def test_contains_dangerous_pattern_detects_xss():
    """
    What we are testing: contains_dangerous_pattern detects XSS attempts
    Why we are testing: Security - prevent script injection
    Expected Result: Returns True for strings containing <script> tags
    """
    # Should detect script tags
    assert contains_dangerous_pattern(r'<script>alert("XSS")</script>'), "Should detect script tags"
    assert contains_dangerous_pattern(r'\input{file}'), "Should detect \\input"
    assert contains_dangerous_pattern(r'\write18{cmd}'), "Should detect \\write18"


@pytest.mark.unit
@pytest.mark.security
def test_contains_dangerous_pattern_detects_javascript():
    """
    What we are testing: contains_dangerous_pattern detects javascript: protocol
    Why we are testing: Security - prevent javascript execution in href
    Expected Result: Returns True for strings containing javascript: protocol
    """
    # Should detect javascript: protocol
    assert contains_dangerous_pattern(r'\href{javascript:alert("XSS")}{Click}'), "Should detect javascript:"
    assert contains_dangerous_pattern(r'javascript:void(0)'), "Should detect javascript: protocol"


@pytest.mark.unit
@pytest.mark.security
def test_contains_dangerous_pattern_safe_patterns():
    """
    What we are testing: contains_dangerous_pattern does not flag safe patterns
    Why we are testing: Ensure legitimate math operations are not blocked
    Expected Result: Returns False for safe LaTeX commands
    """
    # Should not detect safe patterns
    assert not contains_dangerous_pattern(r'\frac{1}{2}'), "Should not detect \\frac as dangerous"
    assert not contains_dangerous_pattern(r'\sqrt{x}'), "Should not detect \\sqrt as dangerous"


@pytest.mark.unit
@pytest.mark.security
def test_is_command_allowed():
    """
    What we are testing: is_command_allowed correctly checks command whitelist
    Why we are testing: Security - enforce command whitelist validation
    Expected Result: Returns True for allowed commands, False for blocked commands
    """
    # Allowed commands
    assert is_command_allowed('frac'), "frac should be allowed"
    assert is_command_allowed('sqrt'), "sqrt should be allowed"
    assert is_command_allowed('int'), "int should be allowed"
    
    # Blocked commands
    assert not is_command_allowed('input'), "input should be blocked"
    assert not is_command_allowed('write18'), "write18 should be blocked"
    assert not is_command_allowed('def'), "def should be blocked"


@pytest.mark.unit
@pytest.mark.security
def test_validate_commands():
    """
    What we are testing: validate_commands validates all commands in LaTeX string
    Why we are testing: Security - ensure all commands are whitelisted
    Expected Result: Returns (True, []) for valid commands, (False, [blocked]) for invalid
    """
    # Valid LaTeX
    is_valid, blocked = validate_commands(r'\frac{1}{2} + \sqrt{x}')
    assert is_valid, "Should be valid"
    assert len(blocked) == 0, "Should have no blocked commands"
    
    # Invalid LaTeX
    is_valid, blocked = validate_commands(r'\input{file} + \frac{1}{2}')
    assert not is_valid, "Should be invalid"
    assert 'input' in blocked, "Should detect input as blocked"

