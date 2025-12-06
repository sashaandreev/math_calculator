# django-mathinput

A CKEditor-style math formula editor for Django templates. Supports multiple input modes, domain presets, and graphical formula building.

## Features

- **Graphical Interface**: Button-based formula building (like WolframAlpha)
- **Multiple Input Modes**: Regular functions, advanced expressions, integrals/differentials, matrices, statistics, physics
- **Domain Presets**: Algebra, calculus, physics, machine learning, statistics, probability
- **Visual Builder**: Interactive formula construction with live preview
- **LaTeX Storage**: Flexible storage format (LaTeX, MathML, or both)
- **Accessible**: WCAG 2.1 AA compliant with full keyboard navigation
- **Mobile Responsive**: Touch-optimized interface for mobile devices
- **Security**: Comprehensive XSS and injection protection

## Installation

### Basic Installation

```bash
pip install django-mathinput
```

### Requirements

- Django 3.2+ or 4.0+
- Python 3.8+
- Modern web browser with JavaScript enabled

## Quick Start

### 1. Add to INSTALLED_APPS

```python
# settings.py
INSTALLED_APPS = [
    # ... your other apps
    'mathinput',
]
```

### 2. Use in Forms

```python
# forms.py
from mathinput.widgets import MathInputWidget
from django import forms

class ProblemForm(forms.Form):
    equation = forms.CharField(widget=MathInputWidget())
```

### 3. Render in Templates

```django
{% load mathinput_tags %}

<form method="post">
    {% csrf_token %}
    {{ form.equation|as_mathinput }}
    <button type="submit">Submit</button>
</form>
```

### 4. Display Stored Formulas

```django
{% load mathinput_tags %}

<div class="formula-display">
    {{ problem.equation|render_math }}
</div>
```

That's it! The widget is now ready to use.

## Basic Usage Examples

### Example 1: Simple Math Form

```python
# forms.py
from mathinput.widgets import MathInputWidget
from django import forms

class MathForm(forms.Form):
    equation = forms.CharField(
        label="Enter your equation",
        widget=MathInputWidget(),
        help_text="Use the toolbar to build your formula"
    )
```

```django
<!-- template.html -->
{% load mathinput_tags %}

<form method="post">
    {% csrf_token %}
    <div class="form-group">
        {{ form.equation.label_tag }}
        {{ form.equation|as_mathinput }}
        {% if form.equation.help_text %}
            <small class="form-text text-muted">{{ form.equation.help_text }}</small>
        {% endif %}
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### Example 2: Calculus Problem with Preset

```python
# forms.py
from mathinput.widgets import MathInputWidget
from django import forms

class CalculusForm(forms.Form):
    integral = forms.CharField(
        widget=MathInputWidget(
            mode='integrals_differentials',
            preset='calculus'
        )
    )
```

### Example 3: Multiple Widgets with Different Modes

```python
# forms.py
from mathinput.widgets import MathInputWidget
from django import forms

class AdvancedMathForm(forms.Form):
    basic_equation = forms.CharField(
        widget=MathInputWidget(mode='regular_functions')
    )
    matrix = forms.CharField(
        widget=MathInputWidget(mode='matrices', preset='machine_learning')
    )
    physics_formula = forms.CharField(
        widget=MathInputWidget(mode='physics_engineering', preset='physics')
    )
```

### Example 4: Using Template Filters

```django
{% load mathinput_tags %}

<!-- Render widget with mode -->
{{ form.equation|as_mathinput:"regular_functions" }}

<!-- Render widget with mode and preset -->
{{ form.equation|as_mathinput:"mode=integrals_differentials,preset=calculus" }}

<!-- Display stored formula -->
<div class="formula">
    {{ stored_formula|render_math }}
</div>

<!-- Display inline formula -->
<span>{{ formula|render_math_inline }}</span>
```

### Example 5: Django Admin Integration

```python
# admin.py
from django.contrib import admin
from mathinput.widgets import MathInputWidget
from .models import Problem

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': MathInputWidget()},
    }
```

## Configuration Options

### Django Settings

Add these to your `settings.py` to customize behavior:

```python
# settings.py

# Default input mode (optional)
MATHINPUT_DEFAULT_MODE = 'regular_functions'  # or 'advanced_expressions', etc.

# Default domain preset (optional)
MATHINPUT_PRESET = 'algebra'  # or 'calculus', 'physics', etc.

# Math renderer (KaTeX or MathJax)
MATHINPUT_RENDERER = 'katex'  # or 'mathjax'

# KaTeX extensions (optional)
MATHINPUT_KATEX_EXTENSIONS = ['ams', 'color', 'cancel']

# Security limits
MATHINPUT_MAX_FORMULA_LENGTH = 10000  # Maximum formula length
MATHINPUT_MAX_NESTING_DEPTH = 50      # Maximum nesting depth
MATHINPUT_MAX_MATRIX_SIZE = (100, 100)  # Maximum matrix dimensions
```

### Available Modes

- `regular_functions` - Basic math operations (default)
- `advanced_expressions` - Complex expressions with nesting
- `integrals_differentials` - Calculus operations
- `matrices` - Matrix operations
- `statistics_probability` - Statistical functions
- `physics_engineering` - Physics and engineering formulas

### Available Presets

- `algebra` - Algebra-focused (default)
- `calculus` - Calculus-focused
- `physics` - Physics-focused
- `machine_learning` - ML-focused
- `statistics` - Statistics-focused
- `probability` - Probability-focused

## API Reference

### MathInputWidget

```python
from mathinput.widgets import MathInputWidget

widget = MathInputWidget(mode=None, preset=None, attrs=None)
```

**Parameters:**
- `mode` (str, optional): Input mode name. Defaults to `MATHINPUT_DEFAULT_MODE` or `'regular_functions'`
- `preset` (str, optional): Domain preset name. Defaults to `MATHINPUT_PRESET` or `'algebra'`
- `attrs` (dict, optional): Additional HTML attributes

**Example:**
```python
widget = MathInputWidget(
    mode='integrals_differentials',
    preset='calculus',
    attrs={'class': 'math-input-widget', 'data-theme': 'dark'}
)
```

### Template Filters

#### `as_mathinput`

Renders a field value as a math input widget.

```django
{{ form.equation|as_mathinput }}
{{ form.equation|as_mathinput:"regular_functions" }}
{{ form.equation|as_mathinput:"mode=integrals_differentials,preset=calculus" }}
```

**Parameters:**
- `value`: Field value (LaTeX string)
- `arg` (optional): Mode name or `mode=value,preset=value` format

#### `render_math`

Renders stored LaTeX/MathML formula for display.

```django
{{ formula|render_math }}
{{ formula|render_math:"katex" }}
{{ formula|render_math:"mathjax" }}
```

**Parameters:**
- `value`: LaTeX or MathML string
- `renderer` (optional): Renderer name ('katex' or 'mathjax')

#### `render_math_inline`

Renders LaTeX as inline math.

```django
<span>{{ formula|render_math_inline }}</span>
```

### Validators

```python
from mathinput.validators import MathInputValidator

validator = MathInputValidator(
    max_length=10000,
    max_nesting=50,
    max_matrix_size=(100, 100)
)

try:
    sanitized = validator.validate(latex_string)
except ValidationError as e:
    # Handle validation error
    print(e)
```

**Parameters:**
- `max_length` (int): Maximum formula length
- `max_nesting` (int): Maximum nesting depth
- `max_matrix_size` (tuple): Maximum matrix dimensions (rows, cols)

## Keyboard Shortcuts

- `Ctrl+M` / `Cmd+M` - Toggle between Visual and Source modes
- `Tab` - Navigate between placeholders
- `Enter` - Insert new line (in source mode)
- `Esc` - Close dialogs/popups
- Arrow keys - Navigate formula structure

## Security

The widget includes comprehensive security measures:

- **XSS Protection**: All script tags and JavaScript protocols blocked
- **Command Injection Protection**: Dangerous LaTeX commands blocked
- **DoS Protection**: Length, nesting depth, and matrix size limits
- **Input Sanitization**: All input sanitized before processing

See `docs/SECURITY_AUDIT_REPORT.md` for detailed security information.

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Documentation

- **User Guide**: See `docs/USER_GUIDE.md`
- **Developer Guide**: See `docs/DEVELOPER_GUIDE.md`
- **API Documentation**: See `docs/API_DOCUMENTATION.md`
- **Code Examples**: See `docs/CODE_EXAMPLES.md`
- **Security Report**: See `docs/SECURITY_AUDIT_REPORT.md`

## Development Status

**Version 0.1.0** - Alpha release

This package is currently in active development. See the implementation plan in `docs/implementation_phase*.md` for progress.

## Running Tests

### Python Tests

Tests should be run from the `django-mathinput` directory:

```bash
cd django-mathinput
python -m pytest tests/ -v
```

Or run specific test categories:

```bash
# Unit tests only
python -m pytest tests/ -m unit -v

# Security tests only
python -m pytest tests/ -m security -v

# Integration tests only
python -m pytest tests/ -m integration -v

# User story tests only
python -m pytest tests/ -m user_story -v
```

**Note:** Running tests from the root directory may cause pytest marker warnings. Always run tests from the `django-mathinput` directory.

### Frontend Tests (JavaScript)

Frontend tests require Node.js and Jest. See `tests/FRONTEND_TESTING.md` for detailed setup instructions.

**Quick Setup:**

```bash
cd django-mathinput
npm install --save-dev jest @jest/globals jsdom jest-environment-jsdom
npm run test:frontend
```

**Available Commands:**

```bash
# Run all frontend tests
npm run test:frontend

# Run tests in watch mode (for development)
npm run test:frontend:watch

# Run tests with coverage report
npm run test:frontend:coverage
```

## Contributing

Contributions are welcome! Please see `docs/DEVELOPER_GUIDE.md` for development guidelines and `docs/CONTRIBUTING.md` for contribution guidelines.

## License

MIT License

## Support

For issues, questions, or contributions, please see the project repository.
