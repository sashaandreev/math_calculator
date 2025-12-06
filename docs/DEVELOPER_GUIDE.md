# MathInput Widget - Developer Guide

Complete guide for developers working with or extending the MathInput widget.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Customization Guide](#customization-guide)
3. [Extension Points](#extension-points)
4. [Contributing Guidelines](#contributing-guidelines)

---

## Architecture Overview

### Component Structure

```
mathinput/
├── widgets.py              # Django form widget
├── templatetags/
│   └── mathinput_tags.py   # Template filters
├── modes/                  # Input mode configurations
│   ├── regular_functions.py
│   ├── advanced_expressions.py
│   ├── integrals_differentials.py
│   ├── matrices.py
│   ├── statistics_probability.py
│   └── physics_engineering.py
├── presets/                # Domain preset configurations
│   ├── algebra.py
│   ├── calculus.py
│   ├── physics.py
│   ├── machine_learning.py
│   ├── statistics.py
│   └── probability.py
├── security.py             # Security and sanitization
├── validators.py           # Formula validation
├── static/
│   └── mathinput/
│       ├── css/
│       │   └── mathinput.css
│       └── js/
│           └── mathinput.js
└── templates/
    └── mathinput/
        ├── widget.html
        ├── toolbar_*.html
        └── quick_insert.html
```

### Data Flow

1. **User Input** → Visual Builder (JavaScript)
2. **Visual Builder** → AST (Abstract Syntax Tree)
3. **AST** → LaTeX (via parser)
4. **LaTeX** → Hidden Form Field
5. **Form Submission** → Server-side Validation
6. **Validated LaTeX** → Database Storage
7. **Display** → Template Filter → Rendered Math

### Key Components

#### MathInputWidget (Python)

- Django form widget
- Handles mode/preset configuration
- Renders widget HTML
- Manages media (CSS/JS)

#### Visual Builder (JavaScript)

- Interactive formula construction
- AST management
- Placeholder tracking
- Mode/preset handling
- LaTeX generation

#### Security Module (Python)

- Input sanitization
- Pattern detection
- Command whitelist/blacklist
- Validation

#### Validators (Python)

- Formula complexity checks
- Length validation
- Nesting depth validation
- Matrix size validation

---

## Customization Guide

### Creating Custom Modes

Create a new file in `mathinput/modes/`:

```python
# mathinput/modes/custom_mode.py

def get_mode_config():
    """
    Return mode configuration dictionary.
    """
    return {
        'name': 'custom_mode',
        'display_name': 'Custom Mode',
        'description': 'Description of custom mode',
        'toolbars': ['text', 'basic', 'custom'],  # Which toolbars to show
        'default_toolbar': 'basic',  # Default active toolbar
        'toolbar_order': ['text', 'basic', 'custom'],  # Toolbar order
        'features': {
            'visual_builder': True,
            'source_mode': True,
            'live_preview': True,
        }
    }
```

Register in `mathinput/modes/__init__.py`:

```python
from .custom_mode import get_mode_config

MODES = {
    # ... existing modes
    'custom_mode': get_mode_config,
}
```

### Creating Custom Presets

Create a new file in `mathinput/presets/`:

```python
# mathinput/presets/custom_preset.py

def get_preset_config():
    """
    Return preset configuration dictionary.
    """
    return {
        'name': 'custom_preset',
        'display_name': 'Custom Preset',
        'description': 'Description of custom preset',
        'toolbar_order': ['basic', 'advanced'],  # Reordered toolbars
        'highlighted_buttons': ['frac', 'sqrt', 'sum'],  # Highlighted buttons
        'quick_inserts': [
            {
                'label': 'Common Formula',
                'latex': r'\frac{a}{b} = c'
            },
            # ... more templates
        ]
    }
```

Register in `mathinput/presets/__init__.py`:

```python
from .custom_preset import get_preset_config

PRESETS = {
    # ... existing presets
    'custom_preset': get_preset_config,
}
```

### Customizing Toolbars

Edit toolbar templates in `templates/mathinput/toolbar_*.html`:

```django
<!-- templates/mathinput/toolbar_custom.html -->
<div class="mi-toolbar" data-toolbar="custom">
    <button class="mi-button" data-command="\custom{arg}">
        <span class="mi-icon">Custom</span>
        <span class="mi-tooltip">Custom Command</span>
    </button>
    <!-- More buttons -->
</div>
```

### Customizing Styles

Override CSS in your project:

```css
/* static/css/mathinput_custom.css */

.mi-widget {
    /* Custom widget styles */
}

.mi-toolbar {
    /* Custom toolbar styles */
}

.mi-button {
    /* Custom button styles */
}
```

Include in your template:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/mathinput_custom.css' %}">
```

### Customizing JavaScript

Extend the JavaScript API:

```javascript
// static/js/mathinput_custom.js

(function() {
    'use strict';
    
    // Wait for widget to initialize
    document.addEventListener('DOMContentLoaded', function() {
        // Access widget instance
        const widgets = document.querySelectorAll('.mi-widget');
        
        widgets.forEach(function(widget) {
            // Custom initialization
            const widgetId = widget.dataset.widgetId;
            const mathInput = window.MathInput.getInstance(widgetId);
            
            // Add custom event listeners
            mathInput.on('formulaChange', function(latex) {
                console.log('Formula changed:', latex);
            });
        });
    });
})();
```

---

## Extension Points

### 1. Custom Validators

Create custom validation:

```python
# myapp/validators.py
from django.core.exceptions import ValidationError
from mathinput.validators import MathInputValidator

class CustomMathValidator(MathInputValidator):
    def validate(self, latex_string: str) -> str:
        # Custom validation logic
        if 'custom_check' in latex_string:
            raise ValidationError("Custom validation failed")
        
        # Call parent validation
        return super().validate(latex_string)
```

Use in forms:

```python
from myapp.validators import CustomMathValidator

class MyForm(forms.Form):
    equation = forms.CharField(
        widget=MathInputWidget(),
        validators=[CustomMathValidator()]
    )
```

### 2. Custom Template Filters

Create custom filters:

```python
# myapp/templatetags/my_math_tags.py
from django import template
from mathinput.templatetags.mathinput_tags import render_math

register = template.Library()

@register.filter
def render_math_with_style(value, style='display'):
    """Render math with custom styling."""
    result = render_math(value)
    return f'<div class="math-{style}">{result}</div>'
```

### 3. Custom Widget Subclass

Extend the widget:

```python
# myapp/widgets.py
from mathinput.widgets import MathInputWidget

class CustomMathInputWidget(MathInputWidget):
    def __init__(self, *args, **kwargs):
        # Custom initialization
        self.custom_option = kwargs.pop('custom_option', None)
        super().__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None, renderer=None):
        # Custom rendering logic
        html = super().render(name, value, attrs, renderer)
        # Add custom HTML
        return html + f'<div class="custom-info">{self.custom_option}</div>'
```

### 4. JavaScript Event Hooks

Hook into JavaScript events:

```javascript
// Listen for widget events
document.addEventListener('mathinput:ready', function(event) {
    const widgetId = event.detail.widgetId;
    const mathInput = window.MathInput.getInstance(widgetId);
    
    // Custom event handlers
    mathInput.on('formulaChange', function(latex) {
        // Custom logic
    });
    
    mathInput.on('modeChange', function(mode) {
        // Custom logic
    });
});
```

### 5. Custom Security Rules

Extend security module:

```python
# myapp/security.py
from mathinput.security import DANGEROUS_COMMANDS, contains_dangerous_pattern

# Add custom dangerous patterns
CUSTOM_DANGEROUS_PATTERNS = [
    r'\\customdangerous\s*\{',
]

def custom_contains_dangerous_pattern(latex_string: str) -> bool:
    """Check for dangerous patterns including custom ones."""
    if contains_dangerous_pattern(latex_string):
        return True
    
    # Check custom patterns
    for pattern in CUSTOM_DANGEROUS_PATTERNS:
        if re.search(pattern, latex_string, re.IGNORECASE):
            return True
    
    return False
```

---

## Contributing Guidelines

### Development Setup

1. **Clone repository**
```bash
git clone <repository-url>
cd django-mathinput
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements-dev.txt
npm install
```

4. **Run tests**
```bash
# Python tests
python -m pytest tests/ -v

# Frontend tests
npm run test:frontend
```

### Code Style

- **Python**: Follow PEP 8
- **JavaScript**: Follow ESLint rules
- **Documentation**: Use docstrings and comments

### Testing Requirements

- All new features must have tests
- Tests must pass before submitting PR
- Include both unit and integration tests
- Update test documentation

### Pull Request Process

1. **Create feature branch**
```bash
git checkout -b feature/my-feature
```

2. **Make changes**
   - Write code
   - Write tests
   - Update documentation

3. **Run tests**
```bash
python -m pytest tests/ -v
npm run test:frontend
```

4. **Commit changes**
```bash
git add .
git commit -m "Add feature: description"
```

5. **Push and create PR**
```bash
git push origin feature/my-feature
```

### Documentation Requirements

- Update README if needed
- Add docstrings to new functions/classes
- Update API documentation
- Add code examples if applicable

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] Security considerations addressed
- [ ] Performance implications considered
- [ ] Backward compatibility maintained

---

## Additional Resources

- **API Documentation**: See `docs/API_DOCUMENTATION.md`
- **Code Examples**: See `docs/CODE_EXAMPLES.md`
- **User Guide**: See `docs/USER_GUIDE.md`
- **Security Report**: See `docs/SECURITY_AUDIT_REPORT.md`

