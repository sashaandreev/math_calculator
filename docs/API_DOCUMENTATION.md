# MathInput Widget - API Documentation

Complete API reference for the MathInput widget.

## Table of Contents

1. [Widget API](#widget-api)
2. [Template Filters API](#template-filters-api)
3. [Validators API](#validators-api)
4. [Security API](#security-api)
5. [JavaScript API](#javascript-api)

---

## Widget API

### MathInputWidget

```python
from mathinput.widgets import MathInputWidget

widget = MathInputWidget(mode=None, preset=None, attrs=None)
```

#### Parameters

- **mode** (str, optional): Input mode name
  - Valid values: `'regular_functions'`, `'advanced_expressions'`, `'integrals_differentials'`, `'matrices'`, `'statistics_probability'`, `'physics_engineering'`
  - Default: `MATHINPUT_DEFAULT_MODE` setting or `'regular_functions'`

- **preset** (str, optional): Domain preset name
  - Valid values: `'algebra'`, `'calculus'`, `'physics'`, `'machine_learning'`, `'statistics'`, `'probability'`
  - Default: `MATHINPUT_PRESET` setting or `'algebra'`

- **attrs** (dict, optional): Additional HTML attributes
  - Example: `{'class': 'custom-class', 'data-theme': 'dark'}`

#### Methods

##### render(name, value, attrs=None, renderer=None)

Renders the widget HTML.

**Parameters:**
- `name` (str): Field name
- `value` (str): Initial value (LaTeX string)
- `attrs` (dict, optional): Additional HTML attributes
- `renderer` (TemplateRenderer, optional): Django template renderer

**Returns:**
- `str`: Rendered HTML string

**Example:**
```python
html = widget.render('equation', r'\frac{1}{2}')
```

##### value_from_datadict(data, files, name)

Extracts value from form data.

**Parameters:**
- `data` (QueryDict): Form data
- `files` (MultiValueDict): Uploaded files
- `name` (str): Field name

**Returns:**
- `str`: LaTeX string from form data

**Example:**
```python
latex = widget.value_from_datadict(request.POST, request.FILES, 'equation')
```

#### Media

The widget includes CSS and JavaScript:

```python
class Media:
    css = {
        'all': ('mathinput/css/mathinput.css',)
    }
    js = ('mathinput/js/mathinput.js',)
```

---

## Template Filters API

### as_mathinput

Renders a field value as a math input widget.

**Syntax:**
```django
{{ value|as_mathinput }}
{{ value|as_mathinput:"mode_name" }}
{{ value|as_mathinput:"mode=mode_name,preset=preset_name" }}
```

**Parameters:**
- `value` (str): Field value (LaTeX string)
- `arg` (str, optional): Mode name or `mode=value,preset=value` format

**Returns:**
- Safe HTML string containing the widget

**Examples:**
```django
{{ form.equation|as_mathinput }}
{{ form.equation|as_mathinput:"regular_functions" }}
{{ form.equation|as_mathinput:"mode=integrals_differentials,preset=calculus" }}
```

### render_math

Renders stored LaTeX/MathML formula for display.

**Syntax:**
```django
{{ value|render_math }}
{{ value|render_math:"renderer_name" }}
```

**Parameters:**
- `value` (str): LaTeX or MathML string
- `renderer` (str, optional): Renderer name (`'katex'` or `'mathjax'`)
  - Default: `MATHINPUT_RENDERER` setting or `'katex'`

**Returns:**
- Safe HTML string containing rendered formula

**Examples:**
```django
{{ formula|render_math }}
{{ formula|render_math:"katex" }}
{{ formula|render_math:"mathjax" }}
```

### render_math_inline

Renders LaTeX as inline math.

**Syntax:**
```django
{{ value|render_math_inline }}
{{ value|render_math_inline:"renderer_name" }}
```

**Parameters:**
- `value` (str): LaTeX string
- `renderer` (str, optional): Renderer name

**Returns:**
- Safe HTML string containing inline rendered formula

**Example:**
```django
<span>The formula {{ formula|render_math_inline }} is important.</span>
```

---

## Validators API

### MathInputValidator

```python
from mathinput.validators import MathInputValidator

validator = MathInputValidator(
    max_length=None,
    max_nesting=None,
    max_matrix_size=None
)
```

#### Parameters

- **max_length** (int, optional): Maximum formula length
  - Default: `MATHINPUT_MAX_FORMULA_LENGTH` setting or `10000`

- **max_nesting** (int, optional): Maximum nesting depth
  - Default: `MATHINPUT_MAX_NESTING_DEPTH` setting or `50`

- **max_matrix_size** (tuple, optional): Maximum matrix dimensions `(rows, cols)`
  - Default: `MATHINPUT_MAX_MATRIX_SIZE` setting or `(100, 100)`

#### Methods

##### validate(latex_string)

Validates and sanitizes LaTeX formula.

**Parameters:**
- `latex_string` (str): Input LaTeX string

**Returns:**
- `str`: Sanitized LaTeX string

**Raises:**
- `ValidationError`: If validation fails

**Example:**
```python
try:
    sanitized = validator.validate(r'\frac{1}{2}')
except ValidationError as e:
    print(f"Validation error: {e}")
```

##### __call__(value)

Makes validator callable for Django form validation.

**Parameters:**
- `value` (str): Input LaTeX string

**Returns:**
- `str`: Sanitized LaTeX string

**Raises:**
- `ValidationError`: If validation fails

**Example:**
```python
class MyForm(forms.Form):
    equation = forms.CharField(
        widget=MathInputWidget(),
        validators=[MathInputValidator()]
    )
```

#### Helper Functions

##### validate_complexity(latex_string)

Validates formula complexity without raising exceptions.

**Parameters:**
- `latex_string` (str): Input LaTeX string

**Returns:**
- `tuple`: `(is_valid, list_of_issues)`

**Example:**
```python
from mathinput.validators import validate_complexity

is_valid, issues = validate_complexity(r'\frac{1}{2}')
if not is_valid:
    for issue in issues:
        print(f"Issue: {issue}")
```

##### count_nesting(latex_string)

Counts maximum nesting depth in LaTeX formula.

**Parameters:**
- `latex_string` (str): Input LaTeX string

**Returns:**
- `int`: Maximum nesting depth

**Example:**
```python
from mathinput.validators import count_nesting

depth = count_nesting(r'\frac{\frac{1}{2}}{3}')  # Returns 2
```

##### get_matrix_size(latex_string)

Gets matrix dimensions if present.

**Parameters:**
- `latex_string` (str): Input LaTeX string

**Returns:**
- `tuple` or `None`: `(rows, cols)` if matrix found, `None` otherwise

**Example:**
```python
from mathinput.validators import get_matrix_size

size = get_matrix_size(r'\begin{pmatrix} a & b \\ c & d \end{pmatrix}')
# Returns (2, 2)
```

---

## Security API

### sanitize_latex(latex_string)

Removes dangerous patterns from LaTeX string.

**Parameters:**
- `latex_string` (str): Input LaTeX string

**Returns:**
- `str`: Sanitized LaTeX string

**Example:**
```python
from mathinput.security import sanitize_latex

safe = sanitize_latex(r'\frac{1}{2}<script>alert(1)</script>')
# Returns: '\frac{1}{2}'
```

### contains_dangerous_pattern(latex_string)

Checks if string contains dangerous patterns.

**Parameters:**
- `latex_string` (str): Input LaTeX string

**Returns:**
- `bool`: `True` if dangerous patterns found, `False` otherwise

**Example:**
```python
from mathinput.security import contains_dangerous_pattern

is_dangerous = contains_dangerous_pattern(r'\input{/etc/passwd}')
# Returns: True
```

### extract_commands(latex_string)

Extracts all LaTeX commands from string.

**Parameters:**
- `latex_string` (str): Input LaTeX string

**Returns:**
- `list`: List of command names (without backslash)

**Example:**
```python
from mathinput.security import extract_commands

commands = extract_commands(r'\frac{1}{2} + \sqrt{x}')
# Returns: ['frac', 'sqrt']
```

### is_command_allowed(command)

Checks if a LaTeX command is allowed.

**Parameters:**
- `command` (str): Command name (without backslash)

**Returns:**
- `bool`: `True` if allowed, `False` otherwise

**Example:**
```python
from mathinput.security import is_command_allowed

is_allowed = is_command_allowed('frac')  # Returns: True
is_blocked = is_command_allowed('input')  # Returns: False
```

### validate_commands(latex_string)

Validates that all commands are allowed.

**Parameters:**
- `latex_string` (str): Input LaTeX string

**Returns:**
- `tuple`: `(is_valid, list_of_blocked_commands)`

**Example:**
```python
from mathinput.security import validate_commands

is_valid, blocked = validate_commands(r'\frac{1}{2}\input{file}')
# Returns: (False, ['input'])
```

### Constants

#### DANGEROUS_COMMANDS

List of dangerous command patterns (regex).

#### BLOCKED_COMMANDS

Set of blocked command names.

#### ALLOWED_COMMANDS

Set of allowed command names.

---

## JavaScript API

### MathInput Class

```javascript
// Get widget instance
const mathInput = window.MathInput.getInstance(widgetId);

// Or access via DOM
const widget = document.querySelector('[data-widget-id="' + widgetId + '"]');
const mathInput = widget.mathInput;
```

#### Methods

##### getInstance(widgetId)

Gets widget instance by ID.

**Parameters:**
- `widgetId` (str): Widget ID

**Returns:**
- `MathInput`: Widget instance

##### getLatex()

Gets current LaTeX string.

**Returns:**
- `str`: LaTeX string

**Example:**
```javascript
const latex = mathInput.getLatex();
```

##### setLatex(latex)

Sets LaTeX string.

**Parameters:**
- `latex` (str): LaTeX string

**Example:**
```javascript
mathInput.setLatex('\\frac{1}{2}');
```

##### getAST()

Gets current AST (Abstract Syntax Tree).

**Returns:**
- `Object`: AST object

##### setAST(ast)

Sets AST.

**Parameters:**
- `ast` (Object): AST object

##### parseLatex(latex)

Parses LaTeX string to AST.

**Parameters:**
- `latex` (str): LaTeX string

**Returns:**
- `Object`: AST object

**Example:**
```javascript
const ast = mathInput.parseLatex('\\frac{1}{2}');
```

##### render()

Renders the visual builder.

**Example:**
```javascript
mathInput.render();
```

##### switchMode(mode)

Switches input mode.

**Parameters:**
- `mode` (str): Mode name

**Example:**
```javascript
mathInput.switchMode('integrals_differentials');
```

##### switchPreset(preset)

Switches domain preset.

**Parameters:**
- `preset` (str): Preset name

**Example:**
```javascript
mathInput.switchPreset('calculus');
```

#### Events

##### on(event, callback)

Registers event listener.

**Parameters:**
- `event` (str): Event name
- `callback` (Function): Callback function

**Available Events:**
- `formulaChange` - Formula changed
- `modeChange` - Mode changed
- `presetChange` - Preset changed
- `render` - Widget rendered

**Example:**
```javascript
mathInput.on('formulaChange', function(latex) {
    console.log('Formula changed:', latex);
});
```

##### off(event, callback)

Removes event listener.

**Parameters:**
- `event` (str): Event name
- `callback` (Function): Callback function

**Example:**
```javascript
mathInput.off('formulaChange', callback);
```

---

## Additional Resources

- **User Guide**: See `docs/USER_GUIDE.md`
- **Developer Guide**: See `docs/DEVELOPER_GUIDE.md`
- **Code Examples**: See `docs/CODE_EXAMPLES.md`

