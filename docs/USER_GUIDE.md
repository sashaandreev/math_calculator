# MathInput Widget - User Guide

Complete guide for using the MathInput widget in your Django applications.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Using the Widget](#using-the-widget)
3. [Mode Selection Guide](#mode-selection-guide)
4. [Preset Selection Guide](#preset-selection-guide)
5. [Keyboard Shortcuts](#keyboard-shortcuts)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Installation

```bash
pip install django-mathinput
```

### Basic Setup

1. Add `mathinput` to `INSTALLED_APPS` in `settings.py`
2. Use `MathInputWidget` in your forms
3. Load `mathinput_tags` in your templates

### Quick Example

```python
# forms.py
from mathinput.widgets import MathInputWidget
from django import forms

class MathForm(forms.Form):
    equation = forms.CharField(widget=MathInputWidget())
```

```django
<!-- template.html -->
{% load mathinput_tags %}
{{ form.equation|as_mathinput }}
```

---

## Using the Widget

### Visual Mode vs Source Mode

The widget has two modes:

**Visual Mode (Default):**
- Graphical button-based interface
- Click buttons to insert operations
- See visual representation as you build
- Best for most users

**Source Mode:**
- Direct LaTeX editing
- See raw LaTeX code
- Best for advanced users
- Toggle with `Ctrl+M` / `Cmd+M`

### Building a Formula

1. **Click toolbar buttons** to insert operations
2. **Click placeholders** (□) to fill in values
3. **Type directly** in placeholders or source mode
4. **See live preview** of rendered formula
5. **Formula is saved** as LaTeX in the form field

### Example: Building a Fraction

1. Click the **Fraction** button (or type `\frac`)
2. Visual builder shows: `\frac{□}{□}`
3. Click first placeholder, type `1`
4. Click second placeholder, type `2`
5. Result: `\frac{1}{2}`

### Example: Building an Integral

1. Click the **Integral** button (∫)
2. Visual builder shows: `∫ □ d□`
3. Click first placeholder, type `3x`
4. Click second placeholder, type `x`
5. Result: `\int 3x \, dx`

---

## Mode Selection Guide

Modes control which toolbars are visible and the complexity of the interface.

### Regular Functions Mode

**Best for:** Basic math, algebra, simple equations

**Features:**
- Basic operations (+, -, ×, ÷)
- Fractions, roots, powers
- Simple functions (sin, cos, log)
- Text formatting

**Use when:**
- Teaching basic math
- Simple algebraic equations
- General purpose math input

```python
widget = MathInputWidget(mode='regular_functions')
```

### Advanced Expressions Mode

**Best for:** Complex expressions, nested structures

**Features:**
- All basic operations
- Complex nesting
- Advanced functions
- Multiple levels of parentheses

**Use when:**
- Complex mathematical expressions
- Nested fractions and roots
- Advanced algebra

```python
widget = MathInputWidget(mode='advanced_expressions')
```

### Integrals/Differentials Mode

**Best for:** Calculus, integrals, derivatives

**Features:**
- Integral symbols (∫, ∮, ∬)
- Derivative notation (∂, ∇)
- Limits (lim)
- Summation (∑, ∏)
- Calculus-specific toolbars

**Use when:**
- Calculus courses
- Integration problems
- Differential equations

```python
widget = MathInputWidget(mode='integrals_differentials')
```

### Matrices Mode

**Best for:** Linear algebra, matrices, vectors

**Features:**
- Matrix creation tools
- Vector notation
- Matrix operations
- Determinants, traces

**Use when:**
- Linear algebra courses
- Machine learning (feature vectors)
- Matrix calculations

```python
widget = MathInputWidget(mode='matrices')
```

### Statistics/Probability Mode

**Best for:** Statistics, probability, data analysis

**Features:**
- Statistical functions (mean, median, std)
- Probability notation (P, E, Var)
- Distribution functions
- Statistical symbols

**Use when:**
- Statistics courses
- Probability problems
- Data analysis

```python
widget = MathInputWidget(mode='statistics_probability')
```

### Physics/Engineering Mode

**Best for:** Physics, engineering, scientific formulas

**Features:**
- Physics constants
- Engineering notation
- Scientific units
- Physics-specific symbols

**Use when:**
- Physics courses
- Engineering calculations
- Scientific formulas

```python
widget = MathInputWidget(mode='physics_engineering')
```

---

## Preset Selection Guide

Presets optimize the interface for specific domains by:
- Reordering toolbars
- Highlighting common buttons
- Providing domain-specific quick inserts

### Algebra Preset

**Best for:** General algebra, equations

**Optimizations:**
- Basic operations prioritized
- Equation solving tools highlighted
- Common algebraic templates

```python
widget = MathInputWidget(preset='algebra')
```

### Calculus Preset

**Best for:** Calculus courses, derivatives, integrals

**Optimizations:**
- Calculus toolbar prioritized
- Common integral templates
- Derivative notation highlighted

```python
widget = MathInputWidget(mode='integrals_differentials', preset='calculus')
```

### Physics Preset

**Best for:** Physics courses, scientific formulas

**Optimizations:**
- Physics constants available
- Scientific notation prioritized
- Common physics formulas

```python
widget = MathInputWidget(mode='physics_engineering', preset='physics')
```

### Machine Learning Preset

**Best for:** ML courses, feature vectors, matrices

**Optimizations:**
- Matrix operations prioritized
- Vector notation highlighted
- ML-specific templates

```python
widget = MathInputWidget(mode='matrices', preset='machine_learning')
```

### Statistics Preset

**Best for:** Statistics courses, data analysis

**Optimizations:**
- Statistical functions prioritized
- Probability notation highlighted
- Common statistical templates

```python
widget = MathInputWidget(mode='statistics_probability', preset='statistics')
```

### Probability Preset

**Best for:** Probability theory, random variables

**Optimizations:**
- Probability notation prioritized
- Distribution functions highlighted
- Common probability templates

```python
widget = MathInputWidget(mode='statistics_probability', preset='probability')
```

---

## Keyboard Shortcuts

### Mode Switching

- `Ctrl+M` / `Cmd+M` - Toggle Visual/Source mode

### Navigation

- `Tab` - Move to next placeholder
- `Shift+Tab` - Move to previous placeholder
- `Arrow Keys` - Navigate formula structure
- `Esc` - Close dialogs/popups

### Editing

- `Enter` - Insert new line (source mode)
- `Backspace` / `Delete` - Remove selected elements
- `Ctrl+Z` / `Cmd+Z` - Undo (if implemented)
- `Ctrl+Y` / `Cmd+Y` - Redo (if implemented)

### Quick Insert

- Type `\frac` - Insert fraction
- Type `\sqrt` - Insert square root
- Type `\int` - Insert integral
- Type `\sum` - Insert summation

---

## Troubleshooting

### Widget Not Appearing

**Problem:** Widget doesn't render in template

**Solutions:**
1. Check that `mathinput` is in `INSTALLED_APPS`
2. Verify `{% load mathinput_tags %}` is in template
3. Check browser console for JavaScript errors
4. Ensure static files are collected: `python manage.py collectstatic`

### Formula Not Saving

**Problem:** Formula doesn't save when form is submitted

**Solutions:**
1. Check form field name matches widget name
2. Verify form method is POST
3. Check CSRF token is included
4. Check form validation errors

### Preview Not Updating

**Problem:** Live preview doesn't update

**Solutions:**
1. Check browser console for JavaScript errors
2. Verify KaTeX/MathJax is loading
3. Check network tab for failed resource loads
4. Try refreshing the page

### Mode/Preset Not Working

**Problem:** Selected mode or preset doesn't apply

**Solutions:**
1. Verify mode/preset names are correct (case-sensitive)
2. Check widget initialization in form
3. Check browser console for errors
4. Try default mode/preset first

### Mobile Issues

**Problem:** Widget doesn't work well on mobile

**Solutions:**
1. Ensure responsive CSS is loaded
2. Check viewport meta tag: `<meta name="viewport" content="width=device-width, initial-scale=1">`
3. Test on actual device (not just browser dev tools)
4. Check touch event handling

### Security Validation Errors

**Problem:** Valid formulas are rejected

**Solutions:**
1. Check formula length (max 10,000 characters)
2. Check nesting depth (max 50 levels)
3. Check for blocked commands (see security docs)
4. Verify formula doesn't contain dangerous patterns

### Performance Issues

**Problem:** Widget is slow with large formulas

**Solutions:**
1. Reduce formula complexity
2. Use appropriate mode (simpler modes are faster)
3. Check browser performance (disable extensions)
4. Consider server-side validation limits

---

## Best Practices

### Choosing the Right Mode

- **Simple math**: Use `regular_functions`
- **Calculus**: Use `integrals_differentials` with `calculus` preset
- **Matrices**: Use `matrices` mode
- **Statistics**: Use `statistics_probability` with `statistics` preset

### Form Design

- Provide clear labels and help text
- Show example formulas
- Use appropriate mode for your use case
- Validate input on server side

### User Experience

- Start with Visual mode for most users
- Provide Source mode for advanced users
- Show live preview
- Provide keyboard shortcuts documentation

### Security

- Always validate input on server side
- Use security limits (length, nesting, matrix size)
- Sanitize output when displaying
- Keep widget updated

---

## Additional Resources

- **API Documentation**: See `docs/API_DOCUMENTATION.md`
- **Code Examples**: See `docs/CODE_EXAMPLES.md`
- **Developer Guide**: See `docs/DEVELOPER_GUIDE.md`
- **Security Report**: See `docs/SECURITY_AUDIT_REPORT.md`

