"""Quick test for security module."""
import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent))

from mathinput.security import (
    sanitize_latex,
    extract_commands,
    contains_dangerous_pattern,
    is_command_allowed,
    validate_commands,
)

print("Testing security module...\n")

# Test 1: sanitize_latex
result = sanitize_latex(r'\input{file}')
assert 'input' not in result.lower(), "Should remove \\input"
print("✓ sanitize_latex removes dangerous commands")

result = sanitize_latex(r'\frac{1}{2}')
assert 'frac' in result, "Should preserve \\frac"
print("✓ sanitize_latex preserves safe commands")

# Test 2: extract_commands
commands = extract_commands(r'\frac{1}{2} + \sqrt{x}')
assert 'frac' in commands and 'sqrt' in commands, "Should extract commands"
print("✓ extract_commands works")

# Test 3: contains_dangerous_pattern
assert contains_dangerous_pattern(r'\input{file}'), "Should detect dangerous"
assert not contains_dangerous_pattern(r'\frac{1}{2}'), "Should not detect safe"
print("✓ contains_dangerous_pattern works")

# Test 4: is_command_allowed
assert is_command_allowed('frac'), "frac should be allowed"
assert not is_command_allowed('input'), "input should be blocked"
print("✓ is_command_allowed works")

# Test 5: validate_commands
is_valid, blocked = validate_commands(r'\frac{1}{2}')
assert is_valid and len(blocked) == 0, "Should validate safe commands"
print("✓ validate_commands works")

is_valid, blocked = validate_commands(r'\input{file}')
assert not is_valid and 'input' in blocked, "Should block dangerous commands"
print("✓ validate_commands blocks dangerous commands")

print("\n✅ All security module tests passed!")

