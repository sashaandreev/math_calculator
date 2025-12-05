## 1. HIGH-LEVEL ARCHITECTURE

```diagram
+----------------------+       +---------------------+
|   Django Templates   | <---> |   MathInputWidget   |
|   (forms, display)   |       |   (mode, preset)    |
+----------------------+       +---------------------+
|                                |
|                                v
|                    +-----------------------+
|                    |   Mode System         |
|                    |   (6 input modes)     |
|                    +-----------------------+
|                                |
|                                v
|                    +-----------------------+
|                    |   Preset System      |
|                    |   (6 domain presets)  |
|                    +-----------------------+
|                                |
v                                v
+---------------------+       +---------------------+
|   Vanilla JS Engine |       |   Visual Builder    |
|  (mathinput.js)     | <---> |   (AST, UI sync)    |
+---------------------+       +---------------------+
|                                |
|                                v
|                    +-----------------------+
|                    |   Live Preview        |
|                    |   (KaTeX rendering)   |
|                    +-----------------------+
|
+--------------------+---------------------+
|                    |                     |
+------+------+     +-------+------+      +--------+--------+
|   KaTeX      |     |  MathJax     |      | KaTeX Extensions |
| (default)    |     | (fallback)   |      | cancel, copy-tex |
+--------------+     +--------------+      +-----------------+
↑                    ↑                     ↑
+-------- Client Browser (100% frontend) ------+
```

**Zero server-side processing** – all rendering and interaction happens in the browser.

**Key Architectural Principles:**
- **Graphical Interface First:** All user interaction via visual buttons, not direct LaTeX typing
- **Mode-Based UI:** Different toolbar layouts for different math complexity levels
- **Preset Configuration:** Domain-specific optimizations (tab order, quick inserts)
- **Visual Builder:** Tree-based AST structure with linear visual representation
- **Bidirectional Sync:** Visual builder ↔ Source mode ↔ Hidden form field

---

## 2. COMPONENT BREAKDOWN

| Component              | Responsibility                                 | File Location                     |
|------------------------|------------------------------------------------|-----------------------------------|
| `MathInputWidget`      | Django form widget, injects HTML + Media, mode/preset support | `mathinput/widgets.py`            |
| `mathinput_tags`       | `{% as_mathinput %}`, `{% render_math %}` template filters | `mathinput/templatetags/mathinput_tags.py` |
| `widget.html`          | Main container, mode switcher, toolbar wrapper, visual builder area | `templates/mathinput/widget.html` |
| `toolbar_*.html`       | One file per tab (Text, Basic, Advanced, Calculus, Matrices, Trig, Symbols) | `templates/mathinput/toolbar_*.html` |
| `quick_insert.html`    | Dropdown with preset templates                 | `templates/mathinput/quick_insert.html` |
| `mathinput.js`         | Core editor logic: visual builder, AST, sync, insert, preview, modes, presets | `static/mathinput/js/mathinput.js` |
| `mathinput.css`        | Grid layout, responsive, dark mode, visual builder styles | `static/mathinput/css/mathinput.css` |
| `modes/*.py`           | Input mode configurations (6 modes)            | `mathinput/modes/`                |
| `presets/*.py`         | Domain preset configurations (6 presets)      | `mathinput/presets/`              |
| `security.py`          | LaTeX sanitization, validation, command whitelist | `mathinput/security.py`           |
| `validators.py`        | Formula validation, complexity checks         | `mathinput/validators.py`         |

---

## 3. MODE SYSTEM DESIGN

Input modes define UI/UX complexity and toolbar layouts. Each mode is a Python module:

```python
# mathinput/modes/integrals_differentials.py
def get_mode():
    return {
        "name": "Integrals/Differentials",
        "code": "integrals_differentials",
        "toolbars": {
            "visible": ["text", "calculus", "advanced", "basic"],
            "hidden": ["trig", "symbols", "matrices"],
            "priority": ["calculus", "advanced", "basic", "text"]
        },
        "button_layout": {
            "size": "large",  # For prominent calculus operations
            "grouping": "calculus_operations"
        },
        "quick_inserts": [
            ("Indefinite Integral", "\\int f(x) \\, dx"),
            ("Definite Integral", "\\int_{a}^{b} f(x) \\, dx"),
            ("Derivative", "\\frac{d}{dx}"),
        ]
    }
```

## 4. PRESET SYSTEM DESIGN

Presets work with modes to provide domain-specific configurations:

```python
# mathinput/presets/machine_learning.py
def get_preset():
    return {
        "name": "Machine Learning",
        "code": "machine_learning",
        "tab_order": ["text", "matrices", "advanced", "symbols", "calculus", "basic", "trig"],
        "quick_inserts": [
            ("Neural Layer", "a^{[l]} = \\sigma(W^{[l]} a^{[l-1]} + b^{[l]})"),
            ("Loss", "\\mathcal{L} = -\\sum y \\log \\hat{y}"),
            ("Gradient", "\\nabla_\\theta J(\\theta)"),
        ],
        "highlight_buttons": ["W", "σ", "𝔼", "θ", "⊙"],
        "recommended_modes": ["matrices", "advanced_expressions"]
    }
```

**Mode + Preset Interaction:**
- Mode determines which toolbars are visible and button layouts
- Preset customizes tab order within visible toolbars
- Preset provides domain-specific quick inserts
- Both work together: `mode='integrals_differentials'` + `preset='calculus'`

## 5. DATA FLOW

### 5.1 Visual Builder Flow

```code
User clicks button "∫" (graphical icon)
   ↓
JS → parseButtonClick("integral")
   ↓
JS → insertTemplate("\\int_{}^{}")
   ↓
Visual Builder → update AST (Abstract Syntax Tree)
   ↓
Visual Builder → render visual structure (□/□ with placeholders)
   ↓
JS → update hidden <textarea name="equation"> with LaTeX
   ↓
JS → sync Source mode (if visible)
   ↓
KaTeX → re-render .mi-preview (live preview)
   ↓
User fills placeholders → AST updated → LaTeX updated → Preview updated
   ↓
On form submit → raw LaTeX sent to server
   ↓
Server validates & sanitizes → saves to DB
   ↓
Frontend display → {{ content|render_math }} → KaTeX renders
```

### 5.2 Source Mode Flow

```code
User types in Source mode: "\int 3x dx"
   ↓
JS → parse LaTeX → build AST
   ↓
AST → convert to visual builder structure
   ↓
Visual Builder → render visual representation
   ↓
KaTeX → render preview
   ↓
Bidirectional sync: Source ↔ Visual ↔ Hidden field
```

### 5.3 Formula Loading Flow

```code
Form loads with existing value: "\int x^2 dx"
   ↓
Widget initialization → parse LaTeX
   ↓
Build AST from LaTeX
   ↓
Convert AST to visual builder structure
   ↓
Render visual builder with clickable elements
   ↓
Render preview with KaTeX
   ↓
User can edit in either Visual or Source mode
```

## 6. VISUAL BUILDER ARCHITECTURE

### 6.1 AST (Abstract Syntax Tree) Structure

The visual builder uses a tree-based AST internally:

```javascript
// Example: \frac{a}{b} + c
{
  type: "expression",
  operator: "+",
  left: {
    type: "fraction",
    numerator: { type: "variable", value: "a" },
    denominator: { type: "variable", value: "b" }
  },
  right: { type: "variable", value: "c" }
}
```

### 6.2 Visual Representation

AST is converted to linear visual structure with placeholders:

```
[Visual Builder Display]
┌─────────────────────────────────────┐
│ [a] / [b] + [c]                     │
│  ↑    ↑    ↑                        │
│ num  den  var                       │
└─────────────────────────────────────┘
```

### 6.3 Placeholder Navigation

- Click placeholder → activates inline editor
- Tab → next placeholder
- Shift+Tab → previous placeholder
- Arrow keys → navigate between elements

## 7. MEDIA & ASSET STRATEGY

```python
class MathInputWidget(forms.Widget):
    class Media:
        css = {
            "all": (
                "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css",  # Optional CDN
                "mathinput/css/mathinput.css",
            )
        }
        js = (
            "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js",  # CDN with SRI
            # Extensions loaded conditionally via settings
            "mathinput/js/mathinput.js",
        )
```

**Asset Loading Strategy:**
- CDN for KaTeX (with SRI hashes for security)
- Bundled package JS/CSS
- Fallback to local bundled KaTeX if CDN unavailable
- No npm, no build step → works immediately after INSTALLED_APPS
- Assets can be bundled locally for offline use

## 8. FILE STRUCTURE (FINAL)		

### Package Structure (django-mathinput)

```code
django-mathinput/                    # Package root (separate installable package)
├── mathinput/                       # Django app package
│   ├── __init__.py
│   ├── apps.py
│   ├── widgets.py                   # MathInputWidget + Media
│   ├── security.py                  # LaTeX sanitization, validation
│   ├── validators.py                # Formula validation, complexity checks
│   ├── modes/                       # Input mode configurations
│   │   ├── __init__.py
│   │   ├── regular_functions.py      # Regular functions mode
│   │   ├── advanced_expressions.py  # Advanced expressions mode
│   │   ├── integrals_differentials.py # Integrals/differentials mode
│   │   ├── matrices.py              # Matrices mode
│   │   ├── statistics_probability.py # Statistics & probability mode
│   │   └── physics_engineering.py  # Physics & engineering mode
│   ├── presets/                     # Domain preset configurations
│   │   ├── __init__.py
│   │   ├── algebra.py
│   │   ├── calculus.py
│   │   ├── physics.py
│   │   ├── machine_learning.py
│   │   ├── statistics.py
│   │   └── probability.py
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── mathinput_tags.py        # as_mathinput, render_math filters
│   ├── templates/mathinput/
│   │   ├── widget.html              # Main widget container
│   │   ├── toolbar_text.html
│   │   ├── toolbar_basic.html
│   │   ├── toolbar_advanced.html
│   │   ├── toolbar_calculus.html
│   │   ├── toolbar_matrices.html
│   │   ├── toolbar_trig.html
│   │   ├── toolbar_symbols.html
│   │   └── quick_insert.html
│   └── static/mathinput/
│       ├── css/
│       │   └── mathinput.css        # Main stylesheet
│       └── js/
│           └── mathinput.js         # Core JavaScript engine
├── tests/
│   ├── test_widgets.py
│   ├── test_validators.py
│   ├── test_security.py
│   └── test_modes.py
├── README.md
├── setup.py
└── MANIFEST.in
```

### Project Structure (math_calculator)

```code
math_calculator/                     # Project root directory
├── math_calculator/                 # Main Django app (settings.py location)
│   ├── __init__.py
│   ├── settings.py                  # Django settings (INSTALLED_APPS here)
│   ├── urls.py                      # URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── django-mathinput/                # Package source (during development)
│   └── (package structure as above)
├── manage.py
└── docs/                            # Documentation
    ├── math_br.md
    ├── math_design.md
    └── implementation_phase*.md
```

**Note:** The `django-mathinput` package is separate from the `math_calculator` project. The package can be:
- Developed locally in `math_calculator/django-mathinput/`
- Installed from PyPI: `pip install django-mathinput`
- Installed from local source: `pip install -e ./django-mathinput`

## 9. RESPONSIVE & ACCESSIBILITY DESIGN

### 9.1 Layout System

- **Desktop:** CSS Grid layout with visual builder (left) and preview (right)
- **Mobile:** Stacked layout, collapsible preview, horizontal scrollable toolbar
- **Tablet:** Adaptive layout based on screen size

### 9.2 Touch Targets

- **Desktop:** Minimum 44×44px (WCAG AA)
- **Mobile:** Minimum 48×48px (touch-optimized)
- **Button spacing:** Adequate spacing to prevent mis-clicks

### 9.3 Accessibility Features

- **ARIA labels:** All buttons have descriptive labels
- **Role attributes:** `role="toolbar"`, `role="button"`, `role="textbox"`
- **Live regions:** `aria-live="polite"` on preview for screen readers
- **Keyboard navigation:** Full keyboard-only workflow
  - Tab: Navigate buttons
  - Enter: Activate button
  - Arrow keys: Navigate visual builder
  - Tab/Shift+Tab: Move between placeholders
- **Focus indicators:** Visible focus on all interactive elements
- **Screen reader support:** Announce button labels + LaTeX code

### 9.4 Dark Mode

- CSS variables for colors, sizes, spacing
- Automatic detection of system preference
- Manual toggle option (future)
- High contrast mode support

## 10. RENDERER FALLBACK LOGIC (JS)

```javascript
// Renderer initialization
function initializeRenderer(settings) {
if (settings.renderer === 'mathjax') {
        loadScript('https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml.js', {
            integrity: 'sha384-...',  // SRI hash
            onError: () => fallbackToKaTeX()
        });
    } else {
        // KaTeX (default)
        loadKaTeX(settings.katex_cdn, {
            extensions: settings.katex_extensions || ['cancel', 'copy-tex'],
            onError: () => showError('Failed to load KaTeX')
        });
    }
}

// Preview rendering with error handling
function renderPreview(latex, container) {
    try {
        katex.render(latex, container, {
            throwOnError: true,
            errorColor: '#cc0000'
        });
    } catch (error) {
        showRenderError(container, error.message);
    }
}
```

## 11. SECURITY ARCHITECTURE

### 11.1 Input Validation Pipeline

```python
# django-mathinput/mathinput/validators.py
class MathInputValidator:
    def validate(self, latex_string):
        # 1. Length check
        if len(latex_string) > settings.MAX_FORMULA_LENGTH:
            raise ValidationError("Formula too long")
        
        # 2. Command whitelist
        commands = extract_commands(latex_string)
        for cmd in commands:
            if cmd not in ALLOWED_COMMANDS:
                raise ValidationError(f"Command '{cmd}' not allowed")
        
        # 3. Dangerous pattern check
        if contains_dangerous_pattern(latex_string):
            raise ValidationError("Formula contains unsafe content")
        
        # 4. Complexity check
        if exceeds_complexity_limits(latex_string):
            raise ValidationError("Formula too complex")
        
        # 5. Sanitize
        return sanitize_latex(latex_string)
```

### 11.2 Sanitization

```python
# django-mathinput/mathinput/security.py
def sanitize_latex(latex_string):
    """Remove dangerous LaTeX commands"""
    for pattern in DANGEROUS_COMMANDS:
        latex_string = re.sub(pattern, '', latex_string, flags=re.IGNORECASE)
    return latex_string
```

### 11.3 Multi-Layer Defense

1. **Client-side (real-time):** Validate as user types, show warnings
2. **Client-side (on submit):** Full validation before form submission
3. **Server-side (required):** Re-validate all input, sanitize before storage

## 12. IMPLEMENTATION PLAN

| Phase | Task                                      | Owner     | Status | Dependencies |
|-------|-------------------------------------------|-----------|--------|--------------|
| **Phase 1: Foundation** |
| 1   | Project init + setup.py + folder structure  | Lead Dev  | Pending | - |
| 2   | MathInputWidget + basic widget.html         | Lead Dev  | Pending | 1 |
| 3   | Security module (sanitization, validation)  | Lead Dev  | Pending | 1 |
| 4   | Validators module (complexity checks)       | Lead Dev  | Pending | 1 |
| **Phase 2: Core Functionality** |
| 5   | Mode system (6 mode modules)              | Lead Dev  | Pending | 1 |
| 6   | Preset system (6 preset modules)          | Lead Dev  | Pending | 1 |
| 7   | Toolbar templates (7 tabs)                 | UI Dev    | Pending | 2 |
| 8   | Visual builder AST engine                  | Frontend  | Pending | 2 |
| 9   | Vanilla JS core (insert, sync, preview)    | Frontend  | Pending | 8 |
| **Phase 3: User Interface** |
| 10  | Quick Insert dropdown                       | UI Dev    | Pending | 6, 7 |
| 11  | Text formatting (bold, color, size)        | UI/JS    | Pending | 7, 9 |
| 12  | Mode switching UI                          | UI Dev    | Pending | 5, 7 |
| 13  | Source mode + bidirectional sync           | Frontend  | Pending | 9 |
| **Phase 4: Polish & Integration** |
| 14  | Mobile responsive + touch testing            | UI Dev    | Pending | 7, 9 |
| 15  | Accessibility (ARIA, keyboard)              | A11y     | Pending | 7, 9 |
| 16  | Template tags (as_mathinput, render_math)   | Lead Dev  | Pending | 2 |
| 17  | Django Admin integration                    | Lead Dev  | Pending | 2, 16 |
| 18  | KaTeX extensions + MathJax fallback         | Frontend  | Pending | 9 |
| **Phase 5: Testing & Documentation** |
| 19  | Unit tests (widget, validators, security)   | QA       | Pending | 3, 4, 16 |
| 20  | JavaScript tests (visual builder, sync)     | QA       | Pending | 8, 9 |
| 21  | Integration tests (forms, templates)        | QA       | Pending | 16, 17 |
| 22  | Security testing (XSS, injection)          | Security | Pending | 3 |
| 23  | Documentation + README examples            | Lead Dev  | Pending | All |
| **Phase 6: Release** |
| 24  | PyPI package preparation                    | Lead Dev  | Pending | 23 |
| 25  | Release candidate                           | Lead Dev  | Pending | 24 |
| 26  | Production release                          | Lead Dev  | Pending | 25 |

**Estimated Timeline:** 6-8 weeks for MVP, 10-12 weeks for full release

---

## 13. VISUAL BUILDER IMPLEMENTATION DETAILS

### 13.1 AST Node Types

```javascript
// Node type definitions
const NodeTypes = {
    VARIABLE: 'variable',        // x, y, a, b
    NUMBER: 'number',            // 1, 2, 3.14
    OPERATOR: 'operator',        // +, -, ×, ÷
    FRACTION: 'fraction',        // \frac{}{}
    ROOT: 'root',                // \sqrt{}
    POWER: 'power',              // x^2
    FUNCTION: 'function',        // \sin, \cos
    INTEGRAL: 'integral',        // \int
    SUM: 'sum',                  // \sum
    MATRIX: 'matrix',            // \begin{pmatrix}...\end{pmatrix}
    EXPRESSION: 'expression'     // Compound expressions
};
```

### 13.2 Button Click Handler

```javascript
function handleButtonClick(buttonType, buttonData) {
    // 1. Get current cursor position in AST
    const cursor = getCursorPosition();
    
    // 2. Create new node based on button type
    const newNode = createNode(buttonType, buttonData);
    
    // 3. Insert node into AST at cursor
    insertNode(cursor, newNode);
    
    // 4. Update visual builder display
    renderVisualBuilder();
    
    // 5. Update LaTeX string
    const latex = astToLatex(ast);
    updateHiddenField(latex);
    
    // 6. Sync source mode (if visible)
    syncSourceMode(latex);
    
    // 7. Render preview
    renderPreview(latex);
    
    // 8. Move cursor to first placeholder
    moveCursorToPlaceholder(newNode);
}
```

### 13.3 Placeholder Management

```javascript
class PlaceholderManager {
    constructor(ast) {
        this.placeholders = this.extractPlaceholders(ast);
        this.currentIndex = 0;
    }
    
    extractPlaceholders(node) {
        // Recursively find all placeholder positions
        // Return array of {node, path, type}
    }
    
    moveToNext() {
        this.currentIndex = (this.currentIndex + 1) % this.placeholders.length;
        this.activatePlaceholder(this.placeholders[this.currentIndex]);
    }
    
    moveToPrevious() {
        this.currentIndex = (this.currentIndex - 1 + this.placeholders.length) % this.placeholders.length;
        this.activatePlaceholder(this.placeholders[this.currentIndex]);
    }
}
```

## 14. WIDGET INITIALIZATION

### 14.1 Widget Rendering Flow

```python
# django-mathinput/mathinput/widgets.py
from django import forms
from django.conf import settings
from django.template.loader import render_to_string

class MathInputWidget(forms.Widget):
    def __init__(self, mode=None, preset=None, attrs=None):
        self.mode = mode or getattr(settings, 'MATHINPUT_DEFAULT_MODE', 'regular_functions')
        self.preset = preset or getattr(settings, 'MATHINPUT_PRESET', 'algebra')
        super().__init__(attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        # 1. Load mode configuration
        mode_config = load_mode(self.mode)
        
        # 2. Load preset configuration
        preset_config = load_preset(self.preset)
        
        # 3. Merge configurations
        config = merge_configs(mode_config, preset_config)
        
        # 4. Render widget template
        context = {
            'name': name,
            'value': value or '',
            'mode': self.mode,
            'preset': self.preset,
            'config': config,
            'widget_id': attrs.get('id', f'id_{name}'),
        }
        return render_to_string('mathinput/widget.html', context)
```

### 14.2 JavaScript Initialization

```javascript
function initializeMathInput(widgetId, config) {
    // 1. Create widget instance
    const widget = new MathInputWidget(widgetId, config);
    
    // 2. Initialize visual builder
    if (config.value) {
        // Parse existing LaTeX
        const ast = parseLatex(config.value);
        widget.setAST(ast);
} else {
        // Empty state
        widget.setAST(createEmptyAST());
    }
    
    // 3. Render initial state
    widget.renderVisualBuilder();
    widget.renderPreview();
    
    // 4. Set up event listeners
    widget.setupEventListeners();
    
    // 5. Initialize mode-specific UI
    widget.applyModeConfig(config.mode);
    
    // 6. Initialize preset-specific UI
    widget.applyPresetConfig(config.preset);
    
    return widget;
}
```

## 15. ERROR HANDLING & VALIDATION

### 15.1 Client-Side Validation

```javascript
function validateFormula(latex) {
    const errors = [];
    
    // Length check
    if (latex.length > MAX_FORMULA_LENGTH) {
        errors.push({type: 'length', message: 'Formula too long'});
    }
    
    // Syntax check
    try {
        parseLatex(latex);
    } catch (error) {
        errors.push({type: 'syntax', message: error.message, position: error.position});
    }
    
    // Command whitelist check
    const commands = extractCommands(latex);
    for (const cmd of commands) {
        if (!ALLOWED_COMMANDS.includes(cmd)) {
            errors.push({type: 'command', message: `Command '${cmd}' not allowed`});
        }
    }
    
    // Complexity check
    if (exceedsComplexityLimits(latex)) {
        errors.push({type: 'complexity', message: 'Formula too complex'});
    }
    
    return errors;
}
```

### 15.2 Error Display

```javascript
function displayErrors(errors, container) {
    container.innerHTML = '';
    
    errors.forEach(error => {
        const errorElement = document.createElement('div');
        errorElement.className = `error error-${error.type}`;
        errorElement.textContent = error.message;
        
        if (error.position) {
            highlightError(error.position);
        }
        
        container.appendChild(errorElement);
    });
}
```

## 16. PERFORMANCE OPTIMIZATION

### 16.1 Debouncing

```javascript
// Debounce preview updates
const debouncedRenderPreview = debounce((latex) => {
    renderPreview(latex);
}, 300); // 300ms delay

// Debounce validation
const debouncedValidate = debounce((latex) => {
    const errors = validateFormula(latex);
    displayErrors(errors, errorContainer);
}, 500); // 500ms delay
```

### 16.2 Virtual Scrolling (Large Matrices)

```javascript
function renderLargeMatrix(matrix, container) {
    if (matrix.rows > 10 || matrix.cols > 10) {
        // Use virtual scrolling
        return renderVirtualMatrix(matrix, container);
    } else {
        // Render normally
        return renderMatrix(matrix, container);
    }
}
```

### 16.3 Lazy Loading

```javascript
// Load toolbars on demand
function loadToolbar(toolbarName) {
    if (!loadedToolbars.has(toolbarName)) {
        fetch(`/static/mathinput/toolbars/${toolbarName}.html`)
            .then(response => response.text())
            .then(html => {
                loadedToolbars.set(toolbarName, html);
                renderToolbar(toolbarName, html);
            });
    }
}
```
