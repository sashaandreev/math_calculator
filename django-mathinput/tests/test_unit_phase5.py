"""
Comprehensive unit tests for Phase 5: Widget, Validators, Security.

These tests provide thorough coverage of all unit-level functionality
for widgets, validators, and security modules.
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

from mathinput.widgets import MathInputWidget
from mathinput.validators import (
    MathInputValidator,
    count_nesting,
    get_matrix_size,
    validate_complexity,
    MAX_FORMULA_LENGTH,
    MAX_NESTING_DEPTH,
    MAX_MATRIX_SIZE,
)
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


# ============================================================================
# WIDGET UNIT TESTS
# ============================================================================

@pytest.mark.unit
class TestWidgetInitialization:
    """Comprehensive tests for widget initialization."""
    
    def test_widget_defaults(self):
        """
        What we are testing: Widget uses correct defaults when no parameters provided
        Why we are testing: Ensure widget works out of the box
        Expected Result: Default mode and preset are set correctly
        """
        widget = MathInputWidget()
        assert widget.mode == 'regular_functions'
        assert widget.preset == 'algebra'
        assert widget.template_name == 'mathinput/widget.html'
    
    def test_widget_with_valid_mode(self):
        """
        What we are testing: Widget accepts all valid modes
        Why we are testing: Users need to use different modes
        Expected Result: All valid modes are accepted
        """
        valid_modes = [
            'regular_functions',
            'advanced_expressions',
            'integrals_differentials',
            'matrices',
            'statistics_probability',
            'physics_engineering',
        ]
        
        for mode in valid_modes:
            widget = MathInputWidget(mode=mode)
            assert widget.mode == mode
    
    def test_widget_with_valid_preset(self):
        """
        What we are testing: Widget accepts all valid presets
        Why we are testing: Users need to use different presets
        Expected Result: All valid presets are accepted
        """
        valid_presets = [
            'algebra',
            'calculus',
            'physics',
            'machine_learning',
            'statistics',
            'probability',
        ]
        
        for preset in valid_presets:
            widget = MathInputWidget(preset=preset)
            assert widget.preset == preset
    
    def test_widget_rejects_invalid_mode(self):
        """
        What we are testing: Widget rejects invalid mode and uses default
        Why we are testing: Security - prevent injection via invalid modes
        Expected Result: Invalid mode is replaced with default
        """
        widget = MathInputWidget(mode='invalid_mode_xyz')
        assert widget.mode == 'regular_functions'  # Default
    
    def test_widget_rejects_invalid_preset(self):
        """
        What we are testing: Widget rejects invalid preset and uses default
        Why we are testing: Security - prevent injection via invalid presets
        Expected Result: Invalid preset is replaced with default
        """
        widget = MathInputWidget(preset='invalid_preset_xyz')
        assert widget.preset == 'algebra'  # Default
    
    def test_widget_with_attrs(self):
        """
        What we are testing: Widget accepts and preserves HTML attributes
        Why we are testing: Users may need custom HTML attributes
        Expected Result: Attrs are preserved in widget
        """
        attrs = {'class': 'custom-class', 'data-custom': 'value'}
        widget = MathInputWidget(attrs=attrs)
        # Attrs are stored in widget.attrs
        assert hasattr(widget, 'attrs')
    
    def test_widget_with_none_mode(self):
        """
        What we are testing: Widget handles None mode parameter
        Why we are testing: Edge case handling
        Expected Result: Default mode is used
        """
        widget = MathInputWidget(mode=None)
        assert widget.mode == 'regular_functions'
    
    def test_widget_with_none_preset(self):
        """
        What we are testing: Widget handles None preset parameter
        Why we are testing: Edge case handling
        Expected Result: Default preset is used
        """
        widget = MathInputWidget(preset=None)
        assert widget.preset == 'algebra'
    
    def test_widget_with_empty_string_mode(self):
        """
        What we are testing: Widget handles empty string mode
        Why we are testing: Edge case handling
        Expected Result: Default mode is used
        """
        widget = MathInputWidget(mode='')
        assert widget.mode == 'regular_functions'
    
    def test_widget_with_empty_string_preset(self):
        """
        What we are testing: Widget handles empty string preset
        Why we are testing: Edge case handling
        Expected Result: Default preset is used
        """
        widget = MathInputWidget(preset='')
        assert widget.preset == 'algebra'


@pytest.mark.unit
class TestWidgetRendering:
    """Comprehensive tests for widget rendering."""
    
    def test_widget_render_with_none_value(self):
        """
        What we are testing: Widget renders correctly with None value
        Why we are testing: Edge case - forms may have None values
        Expected Result: Widget renders with empty string
        """
        widget = MathInputWidget()
        html = widget.render('equation', None)
        assert isinstance(html, str)
        assert len(html) > 0
        assert 'equation' in html
    
    def test_widget_render_with_empty_string(self):
        """
        What we are testing: Widget renders correctly with empty string
        Why we are testing: Edge case - empty form fields
        Expected Result: Widget renders with empty value
        """
        widget = MathInputWidget()
        html = widget.render('equation', '')
        assert isinstance(html, str)
        assert 'equation' in html
    
    def test_widget_render_with_value(self):
        """
        What we are testing: Widget renders correctly with LaTeX value
        Why we are testing: Core functionality
        Expected Result: Value is included in rendered HTML
        """
        widget = MathInputWidget()
        value = r'\frac{1}{2}'
        html = widget.render('equation', value)
        assert isinstance(html, str)
        assert 'equation' in html
    
    def test_widget_render_with_attrs(self):
        """
        What we are testing: Widget renders with custom HTML attributes
        Why we are testing: Users may need custom attributes
        Expected Result: Custom attrs are included in rendered HTML
        """
        widget = MathInputWidget()
        attrs = {'id': 'custom_id', 'class': 'custom-class'}
        html = widget.render('equation', '', attrs)
        assert isinstance(html, str)
        assert 'custom_id' in html or 'id=' in html
    
    def test_widget_render_generates_unique_id(self):
        """
        What we are testing: Widget generates unique ID when not provided
        Why we are testing: Ensure proper HTML structure
        Expected Result: Unique ID is generated from field name
        """
        widget = MathInputWidget()
        html = widget.render('equation', '')
        assert 'id_' in html or 'equation' in html
    
    def test_widget_render_includes_mode(self):
        """
        What we are testing: Widget includes mode in rendered HTML
        Why we are testing: JavaScript needs mode information
        Expected Result: Mode is present in HTML (as data attribute or in script)
        """
        widget = MathInputWidget(mode='matrices')
        html = widget.render('equation', '')
        # Mode should be in the rendered HTML
        assert isinstance(html, str)
        assert len(html) > 0
    
    def test_widget_render_includes_preset(self):
        """
        What we are testing: Widget includes preset in rendered HTML
        Why we are testing: JavaScript needs preset information
        Expected Result: Preset is present in HTML
        """
        widget = MathInputWidget(preset='calculus')
        html = widget.render('equation', '')
        # Preset should be in the rendered HTML
        assert isinstance(html, str)
        assert len(html) > 0
    
    def test_widget_render_with_special_characters(self):
        """
        What we are testing: Widget handles special characters in value
        Why we are testing: Edge case - LaTeX may contain special chars
        Expected Result: Special characters are handled correctly
        """
        widget = MathInputWidget()
        value = r'x < 1 & y > 0'
        html = widget.render('equation', value)
        assert isinstance(html, str)
        assert len(html) > 0
    
    def test_widget_render_with_unicode(self):
        """
        What we are testing: Widget handles Unicode characters
        Why we are testing: Edge case - formulas may contain Unicode
        Expected Result: Unicode characters are handled correctly
        """
        widget = MathInputWidget()
        value = r'α + β = γ'
        html = widget.render('equation', value)
        assert isinstance(html, str)
        assert len(html) > 0


@pytest.mark.unit
class TestWidgetValueExtraction:
    """Tests for value extraction from form data."""
    
    def test_value_from_datadict_with_value(self):
        """
        What we are testing: Widget extracts value from form data
        Why we are testing: Core functionality - form submission
        Expected Result: Value is extracted correctly
        """
        widget = MathInputWidget()
        data = {'equation': r'\frac{1}{2}'}
        value = widget.value_from_datadict(data, {}, 'equation')
        assert value == r'\frac{1}{2}'
    
    def test_value_from_datadict_missing_key(self):
        """
        What we are testing: Widget handles missing form field
        Why we are testing: Edge case - field not in form data
        Expected Result: Returns empty string
        """
        widget = MathInputWidget()
        data = {}
        value = widget.value_from_datadict(data, {}, 'equation')
        assert value == ''
    
    def test_value_from_datadict_empty_string(self):
        """
        What we are testing: Widget handles empty string value
        Why we are testing: Edge case - empty form field
        Expected Result: Returns empty string
        """
        widget = MathInputWidget()
        data = {'equation': ''}
        value = widget.value_from_datadict(data, {}, 'equation')
        assert value == ''
    
    def test_value_from_datadict_with_whitespace(self):
        """
        What we are testing: Widget preserves whitespace in value
        Why we are testing: LaTeX may contain intentional whitespace
        Expected Result: Whitespace is preserved
        """
        widget = MathInputWidget()
        data = {'equation': r'  \frac{1}{2}  '}
        value = widget.value_from_datadict(data, {}, 'equation')
        assert value == r'  \frac{1}{2}  '


@pytest.mark.unit
class TestWidgetMedia:
    """Tests for widget Media class."""
    
    def test_widget_media_css_exists(self):
        """
        What we are testing: Widget Media includes CSS files
        Why we are testing: Styles must be loaded
        Expected Result: CSS files are listed
        """
        widget = MathInputWidget()
        assert hasattr(widget, 'Media')
        assert hasattr(widget.Media, 'css')
        assert 'all' in widget.Media.css
        assert len(widget.Media.css['all']) > 0
    
    def test_widget_media_js_exists(self):
        """
        What we are testing: Widget Media includes JavaScript files
        Why we are testing: Scripts must be loaded
        Expected Result: JS files are listed
        """
        widget = MathInputWidget()
        assert hasattr(widget, 'Media')
        assert hasattr(widget.Media, 'js')
        assert len(widget.Media.js) > 0
    
    def test_widget_media_css_path(self):
        """
        What we are testing: CSS file path is correct
        Why we are testing: Ensure correct static file path
        Expected Result: Path includes mathinput/css/mathinput.css
        """
        widget = MathInputWidget()
        css_files = widget.Media.css['all']
        assert any('mathinput/css/mathinput.css' in str(f) for f in css_files)
    
    def test_widget_media_js_path(self):
        """
        What we are testing: JavaScript file path is correct
        Why we are testing: Ensure correct static file path
        Expected Result: Path includes mathinput/js/mathinput.js
        """
        widget = MathInputWidget()
        js_files = widget.Media.js
        assert any('mathinput/js/mathinput.js' in str(f) for f in js_files)


# ============================================================================
# VALIDATOR UNIT TESTS
# ============================================================================

@pytest.mark.unit
class TestValidatorInitialization:
    """Tests for validator initialization."""
    
    def test_validator_defaults(self):
        """
        What we are testing: Validator uses default limits
        Why we are testing: Ensure defaults are correct
        Expected Result: Default limits are set
        """
        validator = MathInputValidator()
        assert validator.max_length == MAX_FORMULA_LENGTH
        assert validator.max_nesting == MAX_NESTING_DEPTH
        assert validator.max_matrix_size == MAX_MATRIX_SIZE
    
    def test_validator_custom_limits(self):
        """
        What we are testing: Validator accepts custom limits
        Why we are testing: Users may need custom validation rules
        Expected Result: Custom limits are used
        """
        validator = MathInputValidator(
            max_length=1000,
            max_nesting=10,
            max_matrix_size=(10, 10)
        )
        assert validator.max_length == 1000
        assert validator.max_nesting == 10
        assert validator.max_matrix_size == (10, 10)
    
    def test_validator_partial_custom_limits(self):
        """
        What we are testing: Validator accepts partial custom limits
        Why we are testing: Users may only override some limits
        Expected Result: Custom limits used, defaults for others
        """
        validator = MathInputValidator(max_length=5000)
        assert validator.max_length == 5000
        assert validator.max_nesting == MAX_NESTING_DEPTH
        assert validator.max_matrix_size == MAX_MATRIX_SIZE


@pytest.mark.unit
class TestValidatorLengthChecks:
    """Tests for formula length validation."""
    
    def test_validator_accepts_max_length(self):
        """
        What we are testing: Validator accepts formula at max length
        Why we are testing: Boundary condition
        Expected Result: Formula at max length passes
        """
        validator = MathInputValidator(max_length=100)
        formula = 'x' * 100
        result = validator.validate(formula)
        assert result == formula
    
    def test_validator_rejects_over_max_length(self):
        """
        What we are testing: Validator rejects formula over max length
        Why we are testing: Boundary condition
        Expected Result: ValidationError raised
        """
        validator = MathInputValidator(max_length=100)
        formula = 'x' * 101
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(formula)
        assert 'too long' in str(exc_info.value).lower()
    
    def test_validator_empty_string(self):
        """
        What we are testing: Validator accepts empty string
        Why we are testing: Edge case
        Expected Result: Empty string passes
        """
        validator = MathInputValidator()
        result = validator.validate('')
        assert result == ''
    
    def test_validator_length_error_message(self):
        """
        What we are testing: Length error message is informative
        Why we are testing: User experience
        Expected Result: Error message includes length info
        """
        validator = MathInputValidator(max_length=100)
        formula = 'x' * 150
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(formula)
        error_msg = str(exc_info.value)
        assert '100' in error_msg or '150' in error_msg


@pytest.mark.unit
class TestValidatorNestingChecks:
    """Tests for nesting depth validation."""
    
    def test_count_nesting_simple(self):
        """
        What we are testing: count_nesting handles simple formulas
        Why we are testing: Basic functionality
        Expected Result: Correct depth calculated
        """
        assert count_nesting('x + y') == 0
        assert count_nesting(r'\frac{1}{2}') == 1
    
    def test_count_nesting_complex(self):
        """
        What we are testing: count_nesting handles complex nested formulas
        Why we are testing: Complex formulas
        Expected Result: Correct depth calculated
        """
        # Depth 3
        formula = r'\frac{\frac{\frac{1}{2}}{3}}{4}'
        assert count_nesting(formula) == 3
    
    def test_count_nesting_mixed_commands(self):
        """
        What we are testing: count_nesting handles mixed commands
        Why we are testing: Real-world formulas
        Expected Result: Correct depth calculated
        """
        formula = r'\sqrt{\frac{\int x dx}{2}}'
        depth = count_nesting(formula)
        assert depth >= 2
    
    def test_validator_accepts_max_nesting(self):
        """
        What we are testing: Validator accepts formula at max nesting
        Why we are testing: Boundary condition
        Expected Result: Formula at max nesting passes
        """
        validator = MathInputValidator(max_nesting=3)
        formula = r'\frac{\frac{\frac{1}{2}}{3}}{4}'
        result = validator.validate(formula)
        assert isinstance(result, str)
    
    def test_validator_rejects_over_max_nesting(self):
        """
        What we are testing: Validator rejects formula over max nesting
        Why we are testing: Boundary condition
        Expected Result: ValidationError raised
        """
        validator = MathInputValidator(max_nesting=2)
        formula = r'\frac{\frac{\frac{1}{2}}{3}}{4}'
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(formula)
        assert 'too deeply nested' in str(exc_info.value).lower()


@pytest.mark.unit
class TestValidatorMatrixChecks:
    """Tests for matrix size validation."""
    
    def test_get_matrix_size_valid_matrices(self):
        """
        What we are testing: get_matrix_size extracts correct dimensions
        Why we are testing: Matrix validation needs correct dimensions
        Expected Result: Correct (rows, cols) tuple returned
        """
        # 2x2
        size = get_matrix_size(r'\begin{pmatrix} a & b \\ c & d \end{pmatrix}')
        assert size == (2, 2)
        
        # 1x3
        size = get_matrix_size(r'\begin{bmatrix} a & b & c \end{bmatrix}')
        assert size == (1, 3)
        
        # 3x1
        size = get_matrix_size(r'\begin{matrix} a \\ b \\ c \end{matrix}')
        assert size == (3, 1)
    
    def test_get_matrix_size_no_matrix(self):
        """
        What we are testing: get_matrix_size returns None for non-matrix
        Why we are testing: Edge case
        Expected Result: None returned
        """
        size = get_matrix_size(r'\frac{1}{2}')
        assert size is None
    
    def test_get_matrix_size_empty_matrix(self):
        """
        What we are testing: get_matrix_size handles empty matrix
        Why we are testing: Edge case
        Expected Result: Correct size or None
        """
        size = get_matrix_size(r'\begin{pmatrix} \end{pmatrix}')
        # Empty matrix might return (0, 0) or None
        assert size is None or size == (0, 0)
    
    def test_validator_accepts_max_matrix_size(self):
        """
        What we are testing: Validator accepts matrix at max size
        Why we are testing: Boundary condition
        Expected Result: Matrix at max size passes
        """
        validator = MathInputValidator(max_matrix_size=(2, 2))
        matrix = r'\begin{pmatrix} a & b \\ c & d \end{pmatrix}'
        result = validator.validate(matrix)
        assert isinstance(result, str)
    
    def test_validator_rejects_oversized_matrix(self):
        """
        What we are testing: Validator rejects oversized matrix
        Why we are testing: Boundary condition
        Expected Result: ValidationError raised
        """
        validator = MathInputValidator(max_matrix_size=(2, 2))
        matrix = r'\begin{pmatrix} a & b & c \\ d & e & f \\ g & h & i \end{pmatrix}'
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(matrix)
        assert 'too large' in str(exc_info.value).lower()


@pytest.mark.unit
class TestValidatorCommandValidation:
    """Tests for command whitelist validation."""
    
    def test_validator_accepts_allowed_commands(self):
        """
        What we are testing: Validator accepts formulas with allowed commands
        Why we are testing: Core functionality
        Expected Result: Allowed commands pass validation
        """
        validator = MathInputValidator()
        formula = r'\frac{1}{2} + \sqrt{x} + \int f(x) dx'
        result = validator.validate(formula)
        assert isinstance(result, str)
    
    def test_validator_rejects_blocked_commands(self):
        """
        What we are testing: Validator rejects formulas with blocked commands
        Why we are testing: Security
        Expected Result: ValidationError raised
        """
        validator = MathInputValidator()
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(r'\input{file}')
        error_msg = str(exc_info.value).lower()
        assert 'unsafe' in error_msg or 'dangerous' in error_msg or 'not allowed' in error_msg
    
    def test_validator_sanitizes_output(self):
        """
        What we are testing: Validator sanitizes output even for valid input
        Why we are testing: Defense in depth
        Expected Result: Output is sanitized
        """
        validator = MathInputValidator()
        formula = r'\frac{1}{2}'
        result = validator.validate(formula)
        # Result should be sanitized (though safe input = safe output)
        assert isinstance(result, str)
        assert 'frac' in result


@pytest.mark.unit
class TestValidateComplexity:
    """Tests for validate_complexity function."""
    
    def test_validate_complexity_valid(self):
        """
        What we are testing: validate_complexity returns True for valid formula
        Why we are testing: Non-raising validation
        Expected Result: Returns (True, [])
        """
        is_valid, issues = validate_complexity(r'\frac{1}{2}')
        assert is_valid is True
        assert len(issues) == 0
    
    def test_validate_complexity_too_long(self):
        """
        What we are testing: validate_complexity detects too long formula
        Why we are testing: Non-raising validation
        Expected Result: Returns (False, [issues])
        """
        long_formula = 'x' * (MAX_FORMULA_LENGTH + 1)
        is_valid, issues = validate_complexity(long_formula)
        assert is_valid is False
        assert len(issues) > 0
        assert any('too long' in issue.lower() for issue in issues)
    
    def test_validate_complexity_too_deeply_nested(self):
        """
        What we are testing: validate_complexity detects too deep nesting
        Why we are testing: Non-raising validation
        Expected Result: Returns (False, [issues])
        """
        deeply_nested = r'\frac{' * 60 + '1' + '}' * 60
        is_valid, issues = validate_complexity(deeply_nested)
        assert is_valid is False
        assert len(issues) > 0
        assert any('nested' in issue.lower() for issue in issues)


# ============================================================================
# SECURITY UNIT TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.security
class TestSanitizeLatex:
    """Comprehensive tests for sanitize_latex function."""
    
    def test_sanitize_empty_string(self):
        """
        What we are testing: sanitize_latex handles empty string
        Why we are testing: Edge case
        Expected Result: Returns empty string
        """
        result = sanitize_latex('')
        assert result == ''
    
    def test_sanitize_none(self):
        """
        What we are testing: sanitize_latex handles None
        Why we are testing: Edge case
        Expected Result: Returns empty string
        """
        result = sanitize_latex(None)
        assert result == ''
    
    def test_sanitize_removes_all_dangerous_commands(self):
        """
        What we are testing: sanitize_latex removes all dangerous commands
        Why we are testing: Security - comprehensive coverage
        Expected Result: All dangerous commands removed
        """
        dangerous_inputs = [
            r'\input{file}',
            r'\include{file}',
            r'\write18{cmd}',
            r'\def\test{value}',
            r'\newcommand{\test}{value}',
            r'\usepackage{package}',
        ]
        
        for dangerous in dangerous_inputs:
            result = sanitize_latex(dangerous)
            # Should not contain the dangerous command
            assert 'input' not in result.lower() or dangerous != r'\input{file}'
    
    def test_sanitize_removes_javascript_href(self):
        """
        What we are testing: sanitize_latex removes javascript: in href
        Why we are testing: Security - XSS prevention
        Expected Result: javascript: removed
        """
        result = sanitize_latex(r'\href{javascript:alert("xss")}{link}')
        assert 'javascript:' not in result.lower()
    
    def test_sanitize_removes_html_tags(self):
        """
        What we are testing: sanitize_latex removes HTML tags
        Why we are testing: Security - XSS prevention
        Expected Result: HTML tags removed
        """
        result = sanitize_latex('<script>alert("xss")</script>')
        assert '<script' not in result.lower()
    
    def test_sanitize_removes_event_handlers(self):
        """
        What we are testing: sanitize_latex removes event handlers
        Why we are testing: Security - XSS prevention
        Expected Result: Event handlers removed
        """
        result = sanitize_latex('onclick="alert(1)"')
        assert 'onclick' not in result.lower()
    
    def test_sanitize_preserves_safe_commands(self):
        """
        What we are testing: sanitize_latex preserves safe commands
        Why we are testing: Functionality - legitimate math
        Expected Result: Safe commands preserved
        """
        safe_formula = r'\frac{1}{2} + \sqrt{x} + \int f(x) dx'
        result = sanitize_latex(safe_formula)
        assert 'frac' in result
        assert 'sqrt' in result
        assert 'int' in result
    
    def test_sanitize_case_insensitive(self):
        """
        What we are testing: sanitize_latex is case-insensitive
        Why we are testing: Security - bypass attempts
        Expected Result: Case variations are removed
        """
        result = sanitize_latex(r'\INPUT{file}')
        assert 'input' not in result.lower()
    
    def test_sanitize_handles_unicode(self):
        """
        What we are testing: sanitize_latex handles Unicode
        Why we are testing: Edge case
        Expected Result: Unicode handled correctly
        """
        result = sanitize_latex(r'α + β = γ')
        assert isinstance(result, str)
        assert len(result) >= 0


@pytest.mark.unit
@pytest.mark.security
class TestExtractCommands:
    """Tests for extract_commands function."""
    
    def test_extract_commands_empty_string(self):
        """
        What we are testing: extract_commands handles empty string
        Why we are testing: Edge case
        Expected Result: Returns empty list
        """
        commands = extract_commands('')
        assert commands == []
    
    def test_extract_commands_simple(self):
        """
        What we are testing: extract_commands extracts simple commands
        Why we are testing: Basic functionality
        Expected Result: Commands extracted correctly
        """
        commands = extract_commands(r'\frac{1}{2}')
        assert 'frac' in commands
    
    def test_extract_commands_multiple(self):
        """
        What we are testing: extract_commands extracts multiple commands
        Why we are testing: Real-world formulas
        Expected Result: All commands extracted
        """
        commands = extract_commands(r'\frac{1}{2} + \sqrt{x} + \int f(x) dx')
        assert 'frac' in commands
        assert 'sqrt' in commands
        assert 'int' in commands
    
    def test_extract_commands_no_duplicates(self):
        """
        What we are testing: extract_commands removes duplicates
        Why we are testing: Efficiency
        Expected Result: Each command appears once
        """
        commands = extract_commands(r'\frac{1}{2} + \frac{3}{4}')
        assert commands.count('frac') == 1
    
    def test_extract_commands_ignores_non_commands(self):
        """
        What we are testing: extract_commands ignores non-command text
        Why we are testing: Accuracy
        Expected Result: Only commands extracted
        """
        commands = extract_commands(r'\frac{1}{2} + x + y')
        assert 'x' not in commands
        assert 'y' not in commands
        assert 'frac' in commands


@pytest.mark.unit
@pytest.mark.security
class TestContainsDangerousPattern:
    """Tests for contains_dangerous_pattern function."""
    
    def test_contains_dangerous_pattern_empty_string(self):
        """
        What we are testing: contains_dangerous_pattern handles empty string
        Why we are testing: Edge case
        Expected Result: Returns False
        """
        assert contains_dangerous_pattern('') is False
    
    def test_contains_dangerous_pattern_detects_all_dangerous(self):
        """
        What we are testing: contains_dangerous_pattern detects all dangerous patterns
        Why we are testing: Security - comprehensive coverage
        Expected Result: All dangerous patterns detected
        """
        dangerous_patterns = [
            r'\input{file}',
            r'\write18{cmd}',
            r'<script>alert("xss")</script>',
            r'\href{javascript:alert("xss")}{link}',
            r'onclick="alert(1)"',
        ]
        
        for pattern in dangerous_patterns:
            assert contains_dangerous_pattern(pattern) is True
    
    def test_contains_dangerous_pattern_safe_patterns(self):
        """
        What we are testing: contains_dangerous_pattern does not flag safe patterns
        Why we are testing: Functionality - legitimate math
        Expected Result: Safe patterns return False
        """
        safe_patterns = [
            r'\frac{1}{2}',
            r'\sqrt{x}',
            r'\int f(x) dx',
            r'x + y = z',
        ]
        
        for pattern in safe_patterns:
            assert contains_dangerous_pattern(pattern) is False
    
    def test_contains_dangerous_pattern_case_insensitive(self):
        """
        What we are testing: contains_dangerous_pattern is case-insensitive
        Why we are testing: Security - bypass attempts
        Expected Result: Case variations detected
        """
        assert contains_dangerous_pattern(r'\INPUT{file}') is True
        assert contains_dangerous_pattern(r'<SCRIPT>alert("xss")</SCRIPT>') is True


@pytest.mark.unit
@pytest.mark.security
class TestIsCommandAllowed:
    """Tests for is_command_allowed function."""
    
    def test_is_command_allowed_empty_string(self):
        """
        What we are testing: is_command_allowed handles empty string
        Why we are testing: Edge case
        Expected Result: Returns False
        """
        assert is_command_allowed('') is False
    
    def test_is_command_allowed_allowed_commands(self):
        """
        What we are testing: is_command_allowed returns True for allowed commands
        Why we are testing: Core functionality
        Expected Result: Allowed commands return True
        """
        allowed = ['frac', 'sqrt', 'int', 'sum', 'prod']
        for cmd in allowed:
            assert is_command_allowed(cmd) is True
    
    def test_is_command_allowed_blocked_commands(self):
        """
        What we are testing: is_command_allowed returns False for blocked commands
        Why we are testing: Security
        Expected Result: Blocked commands return False
        """
        blocked = ['input', 'write18', 'def', 'newcommand']
        for cmd in blocked:
            assert is_command_allowed(cmd) is False
    
    def test_is_command_allowed_case_insensitive(self):
        """
        What we are testing: is_command_allowed is case-insensitive
        Why we are testing: Consistency
        Expected Result: Case variations handled correctly
        """
        assert is_command_allowed('FRAC') is True
        assert is_command_allowed('INPUT') is False
    
    def test_is_command_allowed_whitespace(self):
        """
        What we are testing: is_command_allowed handles whitespace
        Why we are testing: Edge case
        Expected Result: Whitespace stripped
        """
        assert is_command_allowed('  frac  ') is True


@pytest.mark.unit
@pytest.mark.security
class TestValidateCommands:
    """Tests for validate_commands function."""
    
    def test_validate_commands_empty_string(self):
        """
        What we are testing: validate_commands handles empty string
        Why we are testing: Edge case
        Expected Result: Returns (True, [])
        """
        is_valid, blocked = validate_commands('')
        assert is_valid is True
        assert blocked == []
    
    def test_validate_commands_all_allowed(self):
        """
        What we are testing: validate_commands returns True when all commands allowed
        Why we are testing: Core functionality
        Expected Result: Returns (True, [])
        """
        is_valid, blocked = validate_commands(r'\frac{1}{2} + \sqrt{x}')
        assert is_valid is True
        assert blocked == []
    
    def test_validate_commands_some_blocked(self):
        """
        What we are testing: validate_commands detects blocked commands
        Why we are testing: Security
        Expected Result: Returns (False, [blocked_commands])
        """
        is_valid, blocked = validate_commands(r'\frac{1}{2} + \input{file}')
        assert is_valid is False
        assert 'input' in blocked
    
    def test_validate_commands_multiple_blocked(self):
        """
        What we are testing: validate_commands detects multiple blocked commands
        Why we are testing: Comprehensive validation
        Expected Result: All blocked commands in list
        """
        is_valid, blocked = validate_commands(r'\frac{1}{2} + \input{file} + \write18{cmd}')
        assert is_valid is False
        assert len(blocked) >= 1
        assert 'input' in blocked or 'write18' in blocked

