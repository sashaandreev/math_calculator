# Implementation Plan - Phase 1: Foundation

## Overview
Phase 1 establishes the project foundation: project structure, basic widget, and security infrastructure.

## Tasks

### ✅Task 1: Project Init + Setup.py + Folder Structure
**Owner:** Lead Dev  
**Duration:** 1 day  
**Dependencies:** None

**Implementation:**
- Create Django package structure in `math_calculator/django-mathinput/`
- Set up `setup.py` with package metadata
- Create `MANIFEST.in` for static files
- Set up basic folder structure:
  ```
  math_calculator/                    # Project root
  ├── math_calculator/                # Main Django app
  │   ├── settings.py
  │   └── ...
  └── django-mathinput/               # Package source (separate package)
      ├── mathinput/                  # Django app package
      │   ├── __init__.py
      │   ├── apps.py
      │   └── ...
      ├── tests/
      ├── README.md
      ├── setup.py
      └── MANIFEST.in
  ```
- Configure `setup.py` with:
  - Package metadata (name, version, description, license)
  - Dependencies (Django 3.2+)
  - Entry points
  - Package data (templates, static files)

**Deliverables:**
- Complete project structure
- Working `setup.py`
- Package installable via `pip install -e .`

---

### ✅Task 2: MathInputWidget + Basic Widget.html
**Owner:** Lead Dev  
**Duration:** 2 days  
**Dependencies:** Task 1

**Implementation:**
- Create `django-mathinput/mathinput/widgets.py`:
  ```python
  from django import forms
  from django.conf import settings
  from django.template.loader import render_to_string
  
  class MathInputWidget(forms.Widget):
      template_name = 'mathinput/widget.html'
      
      def __init__(self, mode=None, preset=None, attrs=None):
          self.mode = mode or getattr(settings, 'MATHINPUT_DEFAULT_MODE', 'regular_functions')
          self.preset = preset or getattr(settings, 'MATHINPUT_PRESET', 'algebra')
          super().__init__(attrs)
      
      class Media:
          css = {'all': ('mathinput/css/mathinput.css',)}
          js = ('mathinput/js/mathinput.js',)
      
      def render(self, name, value, attrs=None, renderer=None):
          # Render widget template
          context = {
              'name': name,
              'value': value or '',
              'mode': self.mode,
              'preset': self.preset,
          }
          return render_to_string(self.template_name, context)
  ```
- Create `django-mathinput/mathinput/templates/mathinput/widget.html`:
  - Basic container structure
  - Mode switcher (Visual/Source tabs)
  - Toolbar area placeholder
  - Visual builder area placeholder
  - Preview area placeholder
  - Hidden textarea for form submission

**Deliverables:**
- Functional `MathInputWidget` class
- Basic widget template
- Widget renders in Django forms

---

### ✅Task 3: Security Module (Sanitization, Validation)
**Owner:** Lead Dev  
**Duration:** 2 days  
**Dependencies:** Task 1

**Features:**
- Multi-layer defense:
    - Pattern-based removal of dangerous commands
    - Whitelist validation of allowed commands
    - Detection of dangerous patterns
- Protection against:
    - XSS (Cross-Site Scripting)
    - Command injection
    - File system access
    - System command execution
    - JavaScript injection
    - HTML/JS tag injection
- Comprehensive coverage:
    - 20+ dangerous patterns blocked
    - 100+ safe commands allowed
    - Case-insensitive matching
    - Regex-based pattern matching

**Module structure:**
```code
security.py
├── DANGEROUS_COMMANDS (list of regex patterns)
├── BLOCKED_COMMANDS (set of blocked command names)
├── ALLOWED_COMMANDS (set of allowed command names)
├── sanitize_latex() ✓
├── extract_commands() ✓
├── contains_dangerous_pattern() ✓
├── is_command_allowed() ✓
├── validate_commands() ✓
├── get_blocked_commands() ✓
└── get_allowed_commands() ✓
```

**Implementation:**
- Create `django-mathinput/mathinput/security.py`:
  ```python
  import re
  from django.conf import settings
  
  # Dangerous LaTeX commands to block
  DANGEROUS_COMMANDS = [
      r'\input', r'\include', r'\write18', r'\def', r'\newcommand',
      r'\verbatiminput', r'\lstinputlisting', r'\href.*javascript:',
      r'<script', r'</script>', r'javascript:', r'onerror=', r'onclick='
  ]
  
  # Allowed LaTeX commands (whitelist)
  ALLOWED_COMMANDS = [
      'frac', 'sqrt', 'root', 'sum', 'int', 'prod', 'lim',
      'sin', 'cos', 'tan', 'log', 'ln', 'exp',
      'mathbf', 'mathit', 'mathrm', 'text', 'textbf',
      'begin', 'end', 'matrix', 'pmatrix', 'bmatrix',
      'partial', 'nabla', 'cdot', 'times', 'div',
      # ... more commands
  ]
  
  def sanitize_latex(latex_string):
      """Remove dangerous LaTeX commands"""
      for pattern in DANGEROUS_COMMANDS:
          latex_string = re.sub(pattern, '', latex_string, flags=re.IGNORECASE)
      return latex_string
  
  def extract_commands(latex_string):
      """Extract all LaTeX commands from string"""
      # Implementation
      pass
  
  def contains_dangerous_pattern(latex_string):
      """Check if string contains dangerous patterns"""
      # Implementation
      pass
  ```

**Deliverables:**
- Security module with sanitization functions
- Command whitelist/blacklist
- Pattern detection functions

---

### ✅Task 4: Validators Module (Complexity Checks)
**Owner:** Lead Dev  
**Duration:** 2 days  
**Dependencies:** Task 1, Task 3

**Features:**
    - Length validation: prevents formulas exceeding MAX_FORMULA_LENGTH (10,000 chars)
    - Dangerous pattern detection: checks for unsafe content before other validations
    - Command whitelist validation: ensures only allowed commands are used
    - Nesting depth validation: prevents deeply nested structures (max 50 levels)
    - Matrix size validation: prevents oversized matrices (max 100×100)
    - Sanitization: returns sanitized output
    

**Implementation:**
- Create `django-mathinput/mathinput/validators.py`:
  ```python
  from django.core.exceptions import ValidationError
  from django.conf import settings
  from .security import sanitize_latex, extract_commands, ALLOWED_COMMANDS
  
  MAX_FORMULA_LENGTH = getattr(settings, 'MATHINPUT_MAX_FORMULA_LENGTH', 10000)
  MAX_NESTING_DEPTH = getattr(settings, 'MATHINPUT_MAX_NESTING_DEPTH', 50)
  MAX_MATRIX_SIZE = getattr(settings, 'MATHINPUT_MAX_MATRIX_SIZE', (100, 100))
  
  class MathInputValidator:
      def validate(self, latex_string):
          # Length check
          if len(latex_string) > MAX_FORMULA_LENGTH:
              raise ValidationError("Formula too long (max 10,000 chars)")
          
          # Command whitelist
          commands = extract_commands(latex_string)
          for cmd in commands:
              if cmd not in ALLOWED_COMMANDS:
                  raise ValidationError(f"Command '{cmd}' not allowed")
          
          # Complexity checks
          nesting_depth = count_nesting(latex_string)
          if nesting_depth > MAX_NESTING_DEPTH:
              raise ValidationError("Formula too deeply nested (max 50 levels)")
          
          matrix_size = get_matrix_size(latex_string)
          if matrix_size and (matrix_size[0] > MAX_MATRIX_SIZE[0] or 
                             matrix_size[1] > MAX_MATRIX_SIZE[1]):
              raise ValidationError(f"Matrix too large (max {MAX_MATRIX_SIZE[0]}×{MAX_MATRIX_SIZE[1]})")
          
          # Sanitize
          return sanitize_latex(latex_string)
  
  def count_nesting(latex_string):
      """Count maximum nesting depth"""
      # Implementation
      pass
  
  def get_matrix_size(latex_string):
      """Get matrix dimensions if present"""
      # Implementation
      pass
  ```

- Configuration:
    - Uses Django settings with fallbacks if not configured
    - Configurable limits via MATHINPUT_MAX_FORMULA_LENGTH, MATHINPUT_MAX_NESTING_DEPTH, MATHINPUT_MAX_MATRIX_SIZE

**Deliverables:**
- Validator class with complexity checks
- Nesting depth calculation
- Matrix size detection

---

## Phase 1 Testing Requirements

### Unit Tests

#### Test File: `tests/test_security.py`

```python
import pytest
from mathinput.security import (
    sanitize_latex,
    extract_commands,
    contains_dangerous_pattern,
    DANGEROUS_COMMANDS,
    ALLOWED_COMMANDS
)


@pytest.mark.unit
def test_sanitize_latex_removes_dangerous_commands():
    """
    What we are testing: sanitize_latex function removes dangerous LaTeX commands
    Why we are testing: Security - prevent XSS and command injection attacks
    Expected Result: Dangerous commands are removed from input string
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_sanitize_latex_preserves_safe_commands():
    """
    What we are testing: sanitize_latex preserves safe mathematical commands
    Why we are testing: Ensure legitimate math operations are not blocked
    Expected Result: Safe commands like \frac, \sqrt remain unchanged
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_extract_commands_finds_all_commands():
    """
    What we are testing: extract_commands correctly identifies all LaTeX commands
    Why we are testing: Need accurate command extraction for whitelist validation
    Expected Result: All commands in string are extracted as list
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_contains_dangerous_pattern_detects_xss():
    """
    What we are testing: contains_dangerous_pattern detects XSS attempts
    Why we are testing: Security - prevent script injection
    Expected Result: Returns True for strings containing <script> tags
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_contains_dangerous_pattern_detects_javascript():
    """
    What we are testing: contains_dangerous_pattern detects javascript: protocol
    Why we are testing: Security - prevent javascript execution in href
    Expected Result: Returns True for strings containing javascript: protocol
    """
    # Test implementation
    pass
```

#### Test File: `tests/test_validators.py`

```python
import pytest
from django.core.exceptions import ValidationError
from mathinput.validators import MathInputValidator, count_nesting, get_matrix_size


@pytest.mark.unit
def test_validator_rejects_too_long_formula():
    """
    What we are testing: MathInputValidator rejects formulas exceeding length limit
    Why we are testing: Prevent DoS attacks via extremely long formulas
    Expected Result: ValidationError raised for formulas > 10,000 characters
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_validator_rejects_disallowed_commands():
    """
    What we are testing: MathInputValidator rejects formulas with disallowed commands
    Why we are testing: Security - enforce command whitelist
    Expected Result: ValidationError raised for formulas containing \input, \include, etc.
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_validator_accepts_allowed_commands():
    """
    What we are testing: MathInputValidator accepts formulas with allowed commands
    Why we are testing: Ensure legitimate math operations pass validation
    Expected Result: No ValidationError for formulas with \frac, \sqrt, etc.
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_count_nesting_calculates_depth():
    """
    What we are testing: count_nesting correctly calculates maximum nesting depth
    Why we are testing: Prevent DoS via deeply nested structures
    Expected Result: Returns correct nesting depth for nested fractions/expressions
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_validator_rejects_too_deeply_nested():
    """
    What we are testing: MathInputValidator rejects formulas exceeding nesting depth
    Why we are testing: Prevent DoS attacks via deeply nested structures
    Expected Result: ValidationError raised for formulas with > 50 levels of nesting
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_get_matrix_size_detects_dimensions():
    """
    What we are testing: get_matrix_size correctly extracts matrix dimensions
    Why we are testing: Need to validate matrix size limits
    Expected Result: Returns tuple (rows, cols) for valid matrices
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_validator_rejects_oversized_matrix():
    """
    What we are testing: MathInputValidator rejects matrices exceeding size limits
    Why we are testing: Prevent DoS via extremely large matrices
    Expected Result: ValidationError raised for matrices > 100×100
    """
    # Test implementation
    pass
```

#### Test File: `tests/test_widgets.py`

```python
import pytest
from django import forms
from mathinput.widgets import MathInputWidget


@pytest.mark.unit
def test_widget_initialization_with_defaults():
    """
    What we are testing: MathInputWidget initializes with default mode and preset
    Why we are testing: Ensure widget works without explicit configuration
    Expected Result: Widget created with default mode='regular_functions', preset='algebra'
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_widget_initialization_with_custom_mode():
    """
    What we are testing: MathInputWidget accepts custom mode parameter
    Why we are testing: Users need to specify input modes for different math types
    Expected Result: Widget created with specified mode
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_widget_media_includes_css():
    """
    What we are testing: Widget Media class includes CSS files
    Why we are testing: Ensure stylesheets are loaded for widget rendering
    Expected Result: CSS files listed in widget.Media.css
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_widget_media_includes_js():
    """
    What we are testing: Widget Media class includes JavaScript files
    Why we are testing: Ensure JavaScript is loaded for widget functionality
    Expected Result: JS files listed in widget.Media.js
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_widget_renders_basic_html():
    """
    What we are testing: Widget render method produces HTML output
    Why we are testing: Widget must render to be usable in forms
    Expected Result: HTML string returned with widget structure
    """
    # Test implementation
    pass
```

### Integration Tests

#### Test File: `tests/test_integration_phase1.py`

```python
import pytest
from django import forms
from django.test import TestCase
from mathinput.widgets import MathInputWidget
from mathinput.validators import MathInputValidator


@pytest.mark.integration
class TestWidgetFormIntegration(TestCase):
    """
    What we are testing: MathInputWidget integration with Django forms
    Why we are testing: Ensure widget works correctly in real form context
    Expected Result: Form renders with widget, submits correctly
    """
    
    def test_form_with_widget_renders(self):
        """
        What we are testing: Form with MathInputWidget renders without errors
        Why we are testing: Widget must integrate with Django form system
        Expected Result: Form HTML contains widget structure
        """
        # Test implementation
        pass
    
    def test_form_submission_with_valid_data(self):
        """
        What we are testing: Form submission with valid LaTeX formula
        Why we are testing: Ensure widget data is correctly submitted
        Expected Result: Form validates and processes valid formula
        """
        # Test implementation
        pass
    
    def test_form_validation_with_invalid_data(self):
        """
        What we are testing: Form validation rejects invalid formulas
        Why we are testing: Security - prevent malicious input
        Expected Result: Form validation fails with ValidationError
        """
        # Test implementation
        pass
```

### Security Tests

#### Test File: `tests/test_security_phase1.py`

```python
import pytest
from mathinput.security import sanitize_latex, contains_dangerous_pattern
from mathinput.validators import MathInputValidator


@pytest.mark.security
def test_xss_prevention_script_tags():
    """
    What we are testing: Security module prevents XSS via <script> tags
    Why we are testing: Critical security requirement - prevent script injection
    Expected Result: <script> tags are removed from input
    """
    # Test implementation
    pass


@pytest.mark.security
def test_xss_prevention_javascript_protocol():
    """
    What we are testing: Security module prevents XSS via javascript: protocol
    Why we are testing: Prevent javascript execution in href attributes
    Expected Result: javascript: protocol is removed from input
    """
    # Test implementation
    pass


@pytest.mark.security
def test_command_injection_prevention():
    """
    What we are testing: Validator prevents LaTeX command injection
    Why we are testing: Prevent file system access and system command execution
    Expected Result: Commands like \input, \write18 are rejected
    """
    # Test implementation
    pass


@pytest.mark.security
def test_dos_prevention_long_formula():
    """
    What we are testing: Validator prevents DoS via extremely long formulas
    Why we are testing: Prevent resource exhaustion attacks
    Expected Result: Formulas > 10,000 characters are rejected
    """
    # Test implementation
    pass


@pytest.mark.security
def test_dos_prevention_deep_nesting():
    """
    What we are testing: Validator prevents DoS via deeply nested structures
    Why we are testing: Prevent CPU/memory exhaustion from complex parsing
    Expected Result: Formulas with > 50 nesting levels are rejected
    """
    # Test implementation
    pass


@pytest.mark.security
def test_dos_prevention_large_matrix():
    """
    What we are testing: Validator prevents DoS via extremely large matrices
    Why we are testing: Prevent memory exhaustion from large matrix rendering
    Expected Result: Matrices > 100×100 are rejected
    """
    # Test implementation
    pass
```

### User Story Tests

#### Test File: `tests/test_user_stories_phase1.py`

```python
import pytest
from django import forms
from mathinput.widgets import MathInputWidget


@pytest.mark.user_story
@pytest.mark.us_16  # US-16: Display Stored Formulas
def test_widget_displays_existing_formula():
    """
    What we are testing: Widget displays existing formula value when initialized
    Why we are testing: US-16 - Users need to see and edit existing formulas
    Expected Result: Widget HTML contains existing formula value
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_15  # US-15: Handle Errors Gracefully
def test_widget_handles_invalid_formula_gracefully():
    """
    What we are testing: Widget handles invalid/corrupted formula values
    Why we are testing: US-15 - Users should see errors, not crashes
    Expected Result: Widget renders with error message, allows editing
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_15
def test_validation_shows_clear_error_messages():
    """
    What we are testing: Validation provides clear, non-technical error messages
    Why we are testing: US-15 - Users need to understand what went wrong
    Expected Result: Error messages are user-friendly and actionable
    """
    # Test implementation
    pass
```

---

## Phase 1 Completion Criteria

- [ ] Project structure created and package installable
- [ ] MathInputWidget class implemented and renders in forms
- [ ] Security module with sanitization functions
- [ ] Validators module with complexity checks
- [ ] All unit tests passing (90%+ coverage)
- [ ] All integration tests passing
- [ ] All security tests passing
- [ ] All user story tests passing
- [ ] Code review completed
- [ ] Documentation updated

---

## Phase 1 Manual Testing Checklist

### Setup & Installation Testing

**Test 1.1: Package Installation**
- [ ] Create fresh virtual environment
- [ ] Install package via `pip install -e .`
- [ ] Verify package installs without errors
- [ ] Verify package appears in `pip list`
- **Expected Result:** Package installs successfully, no errors

**Test 1.2: Django Integration**
- [ ] Add `'mathinput'` to `INSTALLED_APPS` in `math_calculator/settings.py`
- [ ] Run `python manage.py check`
- [ ] Verify no errors or warnings
- **Expected Result:** Django recognizes package, no configuration errors

**Test 1.3: Static Files Collection**
- [ ] Run `python manage.py collectstatic`
- [ ] Verify CSS and JS files collected
- [ ] Check static files directory structure
- **Expected Result:** All static files collected correctly
[.venv](../.venv)
### Widget Rendering Testing

**Test 1.4: Basic Widget Rendering**
- [ ] Create Django form in `math_calculator` project with `MathInputWidget`
- [ ] Render form in template
- [ ] Verify widget HTML appears in page source
- [ ] Verify widget container structure exists
- **Expected Result:** Widget renders basic HTML structure

**Test 1.5: Widget with Default Mode**
- [ ] Create widget without parameters: `MathInputWidget()`
- [ ] Render widget
- [ ] Verify default mode applied (regular_functions)
- [ ] Verify default preset applied (algebra)
- **Expected Result:** Widget uses default mode and preset

**Test 1.6: Widget with Custom Mode**
- [ ] Create widget with mode: `MathInputWidget(mode='integrals_differentials')`
- [ ] Render widget
- [ ] Verify mode parameter accepted
- **Expected Result:** Widget accepts and stores mode parameter

**Test 1.7: Widget Media Loading**
- [ ] Render form with widget
- [ ] Check page source for CSS link
- [ ] Check page source for JS script tag
- [ ] Verify media files load (check browser Network tab)
- **Expected Result:** CSS and JS files load correctly

### Security Testing

**Test 1.8: Dangerous Command Blocking**
- [ ] Try to submit form with `\input{/etc/passwd}`
- [ ] Verify command is blocked/rejected
- [ ] Try `\write18{rm -rf /}`
- [ ] Verify command is blocked/rejected
- **Expected Result:** Dangerous commands rejected with validation error

**Test 1.9: XSS Prevention**
- [ ] Try to submit form with `<script>alert('XSS')</script>`
- [ ] Verify script tags are removed
- [ ] Try `\href{javascript:alert('XSS')}{Click}`
- [ ] Verify javascript: protocol is blocked
- **Expected Result:** XSS attempts blocked, no script execution

**Test 1.10: Command Whitelist**
- [ ] Submit form with allowed command: `\frac{1}{2}`
- [ ] Verify command accepted
- [ ] Submit form with disallowed command: `\input{file}`
- [ ] Verify command rejected
- **Expected Result:** Only whitelisted commands accepted

### Validation Testing

**Test 1.11: Length Validation**
- [ ] Submit form with formula > 10,000 characters
- [ ] Verify validation error shown
- [ ] Submit form with formula < 10,000 characters
- [ ] Verify validation passes
- **Expected Result:** Length validation works correctly

**Test 1.12: Nesting Depth Validation**
- [ ] Create deeply nested formula (> 50 levels)
- [ ] Submit form
- [ ] Verify nesting depth error shown
- [ ] Create formula with < 50 nesting levels
- [ ] Verify validation passes
- **Expected Result:** Nesting depth validation works correctly

**Test 1.13: Matrix Size Validation**
- [ ] Create matrix > 100×100
- [ ] Submit form
- [ ] Verify matrix size error shown
- [ ] Create matrix < 100×100
- [ ] Verify validation passes
- **Expected Result:** Matrix size validation works correctly

### Form Integration Testing

**Test 1.14: Form Submission**
- [ ] Fill widget with valid LaTeX: `x^2 + 1`
- [ ] Submit form
- [ ] Verify form submits successfully
- [ ] Check submitted data in view
- **Expected Result:** Form submits, data received correctly

**Test 1.15: Form Validation Integration**
- [ ] Submit form with invalid LaTeX
- [ ] Verify Django form validation errors shown
- [ ] Verify errors displayed below widget
- [ ] Verify form does not submit
- **Expected Result:** Form validation integrated correctly

**Test 1.16: Widget with Existing Value**
- [ ] Create form with initial value: `\int x dx`
- [ ] Render form
- [ ] Verify initial value appears in widget
- **Expected Result:** Widget displays existing value

### Error Handling Testing

**Test 1.17: Invalid Formula Handling**
- [ ] Submit form with malformed LaTeX: `\frac{1}` (missing closing brace)
- [ ] Verify error message shown
- [ ] Verify error message is clear and helpful
- **Expected Result:** Clear error message, form does not submit

**Test 1.18: Empty Form Handling**
- [ ] Submit form with empty widget
- [ ] If field is required, verify required error
- [ ] If field is optional, verify form submits
- **Expected Result:** Empty form handled according to field requirements

### Browser Compatibility Testing

**Test 1.19: Browser Compatibility**
- [ ] Test widget in Chrome (latest 2 versions)
- [ ] Test widget in Firefox (latest 2 versions)
- [ ] Test widget in Safari (latest 2 versions)
- [ ] Test widget in Edge (latest 2 versions)
- [ ] Verify widget renders in all browsers
- **Expected Result:** Widget works in all supported browsers

---

## Notes

- All tests must include docstrings with:
  - **What we are testing:** Clear description of the test
  - **Why we are testing:** Justification for the test
  - **Expected Result:** What should happen when test passes

- Use pytest markers:
  - `@pytest.mark.unit` for unit tests
  - `@pytest.mark.integration` for integration tests
  - `@pytest.mark.security` for security tests
  - `@pytest.mark.user_story` for user story tests
  - `@pytest.mark.us_XX` for specific user story (e.g., `@pytest.mark.us_16`)

- Test coverage target: 90%+ for Phase 1 modules

- **Manual Testing:** Complete all manual tests in checklist before marking phase complete

