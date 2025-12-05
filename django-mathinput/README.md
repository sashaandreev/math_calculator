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

## Installation

```bash
pip install django-mathinput
```

## Quick Start

1. Add `mathinput` to your `INSTALLED_APPS`:

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'mathinput',
]
```

2. Use the widget in your forms:

```python
# forms.py
from mathinput.widgets import MathInputWidget
from django import forms

class ProblemForm(forms.Form):
    equation = forms.CharField(widget=MathInputWidget())
```

3. Render in templates:

```django
{% load mathinput_tags %}

{{ form.equation|as_mathinput }}
```

## Documentation

Full documentation is available in the `docs/` directory.

## Development Status

**Version 0.1.0** - Alpha release

This package is currently in active development. See the implementation plan in `docs/implementation_phase*.md` for progress.

## License

MIT License

## Running Tests

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

## Contributing

Contributions are welcome! Please see the documentation for development guidelines.

