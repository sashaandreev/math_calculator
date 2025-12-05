## 1. PROJECT OVERVIEW

A pip-installable, open-source (MIT) Django package delivering a CKEditor-style math formula editor with:

• **Graphical button-based interface** - Visual toolbar with icon buttons for all math operations (like WolframAlpha's math input toolbar)
• **Visual formula builder** - Users click buttons to insert operations, see graphical representation as they build
• **Visual + Source modes** - Graphical editing mode with optional LaTeX source view
• **Live KaTeX preview** - Real-time rendering of formulas as they're constructed
• **7 tabbed toolbars** - Text, Basic, Advanced, Calculus, Matrices, Trigonometry, Symbols with graphical buttons
• **Multiple math input modes** - Regular Functions, Advanced Expressions, Integrals/Differentials, Matrices, etc.
• **6 domain presets** - Algebra, Calculus, Physics, ML, Statistics, Probability  
• **Flexible storage format** - Save as LaTeX, MathML, or other formats (interface is always graphical)
• Zero backend math, mobile-first, Django Admin ready
• Separate installable package for Django templates

---

## 2. BUSINESS OBJECTIVES

| Goal | KPI |
|------|-----|
| 70% faster formula input | User testing |
| 95% satisfaction | Survey |
| Full coverage: high school to PhD | Feature audit |
| <2 min setup | Install guide |
| 100% client-side | Architecture |

---

## 3. FUNCTIONAL REQUIREMENTS

| ID | Requirement |
|----|-------------|
| FR-01 | Render via `{{ form.field|as_mathinput }}` |
| FR-02 | **Graphical button-based interface** - All operations via clickable icon buttons |
| FR-03 | **Visual formula builder** - See math structure graphically as you build (not just LaTeX text) |
| FR-04 | Dual mode: Visual (graphical) + Source (LaTeX text) |
| FR-05 | Mode toggle: tabs + Ctrl+M |
| FR-06 | 7 tabs: Text, Basic, Adv, Calc, Mat, Trig, Sym - each with graphical button toolbar |
| FR-07 | Live KaTeX preview - shows rendered formula in real-time |
| FR-08 | Multiple math input modes: Regular, Advanced, Integrals/Differentials, Matrices |
| FR-09 | Mode-specific toolbars with graphical button layouts |
| FR-10 | Toolbar buttons show visual icons (∫, √, ∂, Σ, etc.) not just text |
| FR-11 | 6 presets with tab reorder + quick insert |
| FR-12 | Text formatting: bold, color, size (via graphical buttons) |
| FR-13 | Storage format: LaTeX (default), MathML, or configurable format |
| FR-14 | Display: `|render_math` - renders stored format to visual output |
| FR-15 | Django Admin compatible |
| FR-16 | CKEditor-style integration pattern |

---

## 4. USER STORIES WITH ACCEPTANCE CRITERIA (16)

### US-01: Insert Fraction
**As a Teacher**  
I want to insert a fraction  
So that I can write equations quickly

| AC | Description |
|----|-------------|
| AC-01 | Basic tab has fraction button with visual icon (/) |
| AC-02 | Click → inserts `\frac{}{}` template in visual builder |
| AC-03 | Cursor automatically placed in numerator placeholder |
| AC-04 | Preview shows: □/□ |
| AC-05 | Tab key moves cursor to denominator placeholder |
| AC-06 | Can type directly in placeholders or use buttons |

### US-02: Insert Integral
**As a Calculus Student**  
I want to insert an integral  
So that I can write calculus problems

| AC | Description |
|----|-------------|
| AC-01 | Calculus tab has integral button with ∫ icon |
| AC-02 | Click → inserts `\int_{}^{}` template |
| AC-03 | Visual builder shows: ∫□ d□ |
| AC-04 | Can click placeholders to fill limits and integrand |
| AC-05 | Definite integral button available for limits |
| AC-06 | Preview renders integral correctly in real-time |

### US-03: Insert Matrix
**As a Linear Algebra Student**  
I want to create a matrix  
So that I can work with linear algebra problems

| AC | Description |
|----|-------------|
| AC-01 | Matrices tab has matrix button with grid icon |
| AC-02 | Click → opens dialog to set rows and columns |
| AC-03 | Dialog creates interactive grid in visual builder |
| AC-04 | Can click cells to edit with formula builder |
| AC-05 | Can add/remove rows and columns |
| AC-06 | Preview renders matrix with proper formatting |

### US-04: Switch Between Visual and Source Modes
**As an Advanced User**  
I want to toggle between visual and LaTeX source views  
So that I can use the interface that suits my workflow

| AC | Description |
|----|-------------|
| AC-01 | Tabs "Visual" and "Source" visible at top |
| AC-02 | Click "Source" → shows LaTeX text editor |
| AC-03 | Click "Visual" → shows graphical builder |
| AC-04 | Keyboard shortcut Ctrl+M toggles modes |
| AC-05 | Changes sync bidirectionally in real-time |
| AC-06 | Current mode is visually indicated (highlighted tab) |

### US-05: Use Quick Insert Templates
**As a Teacher**  
I want to insert common formula templates quickly  
So that I can save time on repetitive formulas

| AC | Description |
|----|-------------|
| AC-01 | Quick Insert dropdown visible in toolbar |
| AC-02 | Dropdown shows preset-specific templates |
| AC-03 | Click template name → inserts LaTeX at cursor |
| AC-04 | Template converts to visual builder structure |
| AC-05 | Placeholders in template are editable |
| AC-06 | Templates organized by preset (e.g., Calculus, Algebra) |

### US-06: Format Text (Bold, Color, Size)
**As a Teacher**  
I want to format text in my formulas  
So that I can emphasize important parts

| AC | Description |
|----|-------------|
| AC-01 | Text tab has formatting buttons (Bold, Color, Size) |
| AC-02 | Select text → click Bold → text becomes bold |
| AC-03 | Select text → click Color → color picker appears |
| AC-04 | Select text → click Size → size dropdown appears |
| AC-05 | Formatting applies to selected portion |
| AC-06 | Preview shows formatted text correctly |

### US-07: Switch Input Modes
**As a User**  
I want to switch between different input modes  
So that I can use the interface optimized for my math type

| AC | Description |
|----|-------------|
| AC-01 | Can select mode via widget parameter or template filter |
| AC-02 | Mode change updates toolbar button layout |
| AC-03 | Current formula preserved when switching modes |
| AC-04 | Toolbar shows mode-appropriate buttons prominently |
| AC-05 | Warning shown if formula uses operations not prominent in new mode |
| AC-06 | All modes can edit any valid LaTeX (full compatibility) |

### US-08: Use Domain Presets
**As a Course Instructor**  
I want to use domain-specific presets  
So that my students see relevant tools for the subject

| AC | Description |
|----|-------------|
| AC-01 | Can select preset via widget parameter or template filter |
| AC-02 | Preset reorders toolbar tabs by priority |
| AC-03 | Preset provides domain-specific quick insert templates |
| AC-04 | Preset highlights commonly used buttons |
| AC-05 | Preset works with any mode (additive, not restrictive) |
| AC-06 | Default preset can be set in Django settings |

### US-09: Edit Existing Formula
**As a User**  
I want to edit a formula I've already created  
So that I can make corrections or modifications

| AC | Description |
|----|-------------|
| AC-01 | Click on any element in visual builder to edit |
| AC-02 | Selected element highlighted visually |
| AC-03 | Can type to replace or use buttons to modify |
| AC-04 | Arrow keys navigate between elements |
| AC-05 | Tab key moves between placeholders |
| AC-06 | Changes reflected immediately in preview |

### US-10: Copy and Paste Formulas
**As a User**  
I want to copy and paste formulas  
So that I can reuse formulas or import from other sources

| AC | Description |
|----|-------------|
| AC-01 | Can copy formula as LaTeX (Ctrl+C or right-click menu) |
| AC-02 | Can copy formula as image (PNG/SVG) via right-click |
| AC-03 | Can paste LaTeX code (Ctrl+V) in visual or source mode |
| AC-04 | Pasted LaTeX auto-converts to visual builder |
| AC-05 | Can paste from external sources (Word, Google Docs) |
| AC-06 | Paste attempts to parse and convert common formats |

### US-11: Undo and Redo Changes
**As a User**  
I want to undo and redo my changes  
So that I can correct mistakes easily

| AC | Description |
|----|-------------|
| AC-01 | Undo button visible in toolbar |
| AC-02 | Redo button visible in toolbar |
| AC-03 | Ctrl+Z undoes last change |
| AC-04 | Ctrl+Y or Ctrl+Shift+Z redoes change |
| AC-05 | 50-level undo/redo history maintained |
| AC-06 | History persists during session, cleared on form submit |

### US-12: Create Multi-line Equations
**As a User**  
I want to create multi-line equations  
So that I can write complex mathematical expressions

| AC | Description |
|----|-------------|
| AC-01 | "New line" button available in toolbar |
| AC-02 | Shift+Enter also creates new line |
| AC-03 | Multi-line shown with visual line separators |
| AC-04 | Alignment options available (left, center, right, aligned) |
| AC-05 | Preview shows proper LaTeX alignment |
| AC-06 | Each line can be edited independently |

### US-13: Use on Mobile Device
**As a Mobile User**  
I want to use the editor on my mobile device  
So that I can create formulas on the go

| AC | Description |
|----|-------------|
| AC-01 | Toolbar is horizontally scrollable on mobile |
| AC-02 | Buttons are touch-optimized (48×48px minimum) |
| AC-03 | Preview is collapsible (tap to expand/collapse) |
| AC-04 | Matrix builder uses bottom sheet on mobile |
| AC-05 | Swipe gestures can switch tabs |
| AC-06 | Interface adapts to small screen sizes |

### US-14: Navigate with Keyboard Only
**As an Accessibility User**  
I want to use the editor with only keyboard  
So that I can work efficiently without a mouse

| AC | Description |
|----|-------------|
| AC-01 | Tab key navigates through toolbar buttons |
| AC-02 | Enter key activates selected button |
| AC-03 | Arrow keys navigate within visual builder |
| AC-04 | Tab key moves between placeholders |
| AC-05 | All functions accessible via keyboard |
| AC-06 | Focus indicators visible on all interactive elements |

### US-15: Handle Errors Gracefully
**As a User**  
I want to see clear error messages when something goes wrong  
So that I can fix issues quickly

| AC | Description |
|----|-------------|
| AC-01 | Invalid LaTeX shows error message in preview area |
| AC-02 | Error tooltip appears on hover over invalid elements |
| AC-03 | Invalid elements highlighted with red border |
| AC-04 | Error messages are clear and non-technical |
| AC-05 | Can continue editing with errors (non-blocking) |
| AC-06 | Specific error shown (e.g., "Missing closing brace") |

### US-16: Display Stored Formulas
**As a Developer**  
I want to display stored formulas in my templates  
So that users can view formulas created with the editor

| AC | Description |
|----|-------------|
| AC-01 | `|render_math` filter available in templates |
| AC-02 | Filter detects stored format (LaTeX/MathML) automatically |
| AC-03 | Filter renders formula using configured renderer (KaTeX/MathJax) |
| AC-04 | Rendered output is safe (XSS protected) |
| AC-05 | Invalid formulas show error message instead of breaking |
| AC-06 | Can override renderer via filter parameter |

---

## 5. NON-FUNCTIONAL REQUIREMENTS

| Category | ID | Requirement |
|--------|----|-----------|
| Performance | NFR-01 | Preview update < 100ms |
| | NFR-02 | Initial load < 1.5s (3G) |
| Bundle Size | NFR-03 | JS + CSS < 150 KB (gzipped) |
| Compatibility | NFR-04 | Django 3.2+, Python 3.8+ |
| | NFR-05 | Browsers: Chrome, Firefox, Safari, Edge (latest 2) |
| Accessibility | NFR-06 | WCAG 2.1 AA compliant |
| Security | NFR-09 | No XSS: sanitize output |
| | NFR-10 | CSRF protection for form submissions |
| | NFR-11 | Input validation and sanitization |
| | NFR-12 | Content Security Policy (CSP) compliant |
| | NFR-13 | Secure LaTeX command whitelist |
| Scalability | NFR-14 | 100% client-side |
| Testing | NFR-17 | 90% unit test coverage |

---

## 6. TECHNICAL CONSTRAINTS

| ID | Constraint |
|----|----------|
| TC-01 | No backend math engine – all rendering client-side |
| TC-02 | No npm / Webpack – assets must be CDN or bundled |
| TC-03 | No external API calls – works offline |
| TC-04 | No jQuery – vanilla JS only |
| TC-05 | No database schema changes |
| TC-06 | No server-side LaTeX compilation |
| TC-07 | KaTeX as default renderer – MathJax optional |
| TC-08 | Django-only |

---

## 7. MOCKUPS

### 7.1 Desktop – Integrals/Differentials Mode (Graphical Toolbar)
```
┌────────────────────────────────────────────────────────────────────┐
│  [Visual] [Source]                        [Calc Quick ▼]          │
├────────────────────────────────────────────────────────────────────┤
│ [Text] [Calc] [Adv] [Basic] [Trig] [Sym] [Mat]                    │
│ ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐      │
│ │ / │ x²│ √ │ ∛ │ ⁿ√│d/dx│d²/dx│ ∫ │ ∫ │ Σ │lim│[ ]│ ⧉ │...│      │
│ │   │   │   │   │   │    │     │   │_^│   │   │   │   │   │      │
│ └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘      │
├────────────────────────────────────────────────────────────────────┤
│  [Live Preview Area - Rendered Formula]                            │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  ∫ 3x dx = (3x²)/2 + constant                              │   │
│  └────────────────────────────────────────────────────────────┘   │
│  [Formula Builder - Visual Structure]                               │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  [∫] [3] [x] [d] [x]  (clickable elements)                 │   │
│  └────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────┘
```

### 7.2 Desktop – Regular Functions Mode (Simplified Graphical Toolbar)
```
┌────────────────────────────────────────────────────────────────────┐
│  [Visual] [Source]                        [Algebra Quick ▼]        │
├────────────────────────────────────────────────────────────────────┤
│ [Text] [Basic] [Trig] [Adv] [Calc] [Mat] [Sym]                    │
│ ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐                    │
│ │ / │ x²│ √ │ + │ - │ × │ ÷ │ ( │ ) │ = │...│                    │
│ └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘                    │
├────────────────────────────────────────────────────────────────────┤
│  [Live Preview: f(x) = x² + 3x - 5]                                │
│  [Visual Builder: [f][(][x][)][=][x²][+][3][x][-][5]]              │
└────────────────────────────────────────────────────────────────────┘
```

**Key Design Principles:**
- **Graphical buttons** with visual icons (∫, √, ∂, Σ, etc.) - not text labels
- **Visual formula builder** shows structure as user clicks buttons
- **Live preview** renders formula in real-time using KaTeX
- **Button-based input** - users click to insert, not type LaTeX manually
- **Mode-specific toolbars** - different button sets for different complexity levels

*(All mockups show graphical button interface, not text-based input)*

---

## 8. MATH INPUT MODES

The package supports multiple input modes optimized for different mathematical complexity levels and use cases. Each mode provides a tailored interface with relevant toolbars and button layouts.

| Mode ID | Mode Name | Description | Primary Toolbars | Use Cases |
|---------|-----------|-------------|------------------|-----------|
| MODE-01 | Regular Functions | Basic algebraic expressions, simple functions | Text, Basic, Trig | High school algebra, basic functions like f(x) = x² + 1 |
| MODE-02 | Advanced Expressions | Complex equations, nested structures, multiple operations | Text, Basic, Advanced, Symbols | College-level algebra, complex equations with multiple terms |
| MODE-03 | Integrals/Differentials | Calculus operations, limits, derivatives, integrals | Text, Calculus, Advanced, Basic | Calculus courses, mathematical analysis, engineering math |
| MODE-04 | Matrices | Matrix operations, vectors, linear algebra | Text, Matrices, Advanced, Symbols | Linear algebra, ML notation, tensor operations |
| MODE-05 | Statistics & Probability | Statistical notation, probability symbols | Text, Advanced, Symbols, Basic | Statistics courses, probability theory, data science |
| MODE-06 | Physics & Engineering | Physics notation, tensor calculus, special symbols | Text, Calculus, Symbols, Advanced | Physics courses, engineering notation, tensor analysis |

### Mode Selection

Modes can be selected via:
- Widget parameter: `MathInputWidget(mode='integrals_differentials')`
- Template filter: `{{ form.field|as_mathinput mode="matrices" }}`
- Settings: `MATHINPUT_DEFAULT_MODE = 'regular_functions'`

### Mode Behavior

Each mode:
- Shows/hides relevant toolbar tabs based on complexity
- **Displays graphical button toolbars** with visual icons (not text)
- Prioritizes commonly used buttons for that mode
- Provides mode-specific quick insert templates
- Adapts button sizes and layouts for optimal UX
- **Visual formula builder** - shows math structure graphically as user clicks buttons
- **Live preview** - renders formula in real-time as it's built
- Maintains full LaTeX compatibility across all modes (storage format)

---

## 9. PRESETS (6)

Presets are domain-specific configurations that work in conjunction with input modes. They customize tab order, quick inserts, and button highlighting.

| Preset | Tab Priority | Quick Insert | Recommended Mode |
|--------|--------------|--------------|-------------------|
| Algebra | Text → Basic → Adv | x², √ | Regular Functions or Advanced Expressions |
| Calculus | Text → Calc → Basic | ∫, lim | Integrals/Differentials |
| Physics | Text → Calc → Sym | ∇·F, T^{ij} | Physics & Engineering |
| ML | Text → Mat → Adv | a^{[l]}, ∇_θ J | Matrices |
| Statistics | Text → Adv → Basic | μ, σ², H₀ | Statistics & Probability |
| Probability | Text → Adv → Sym | P(A|B), E[X] | Statistics & Probability |

---

## 10. REAL-WORLD EXAMPLES

```latex
// Algebra
\textbf{\large{Problem:}} \quad \colorbox{#fff2cc}{x^2 - 5x + 6 = 0}

// ML
a^{[l]} = \sigma(W^{[l]} a^{[l-1]} + b^{[l]})
```

---

## 11. DJANGO INTEGRATION

### Basic Usage (CKEditor-style)

```python
# your_app/forms.py (or math_calculator/forms.py)
from mathinput.widgets import MathInputWidget
from django import forms

class ProblemForm(forms.Form):
    # Using default mode and preset
    equation = forms.CharField(widget=MathInputWidget())
    
    # Specifying mode for integrals/differentials
    calculus_problem = forms.CharField(
        widget=MathInputWidget(mode='integrals_differentials', preset='calculus')
    )
    
    # Matrix operations
    matrix_equation = forms.CharField(
        widget=MathInputWidget(mode='matrices', preset='machine_learning')
    )
```

```django
{# In Django templates - similar to CKEditor usage #}
{% load mathinput_tags %}

{# Basic usage with default mode #}
{{ form.equation|as_mathinput }}

{# Specify mode and preset #}
{{ form.calculus_problem|as_mathinput mode="integrals_differentials" preset="calculus" }}

{# Advanced expressions mode #}
{{ form.complex_equation|as_mathinput mode="advanced_expressions" }}

{# Render stored LaTeX for display #}
{{ problem.equation|render_math }}
```

### Mode Examples by Use Case

```python
# Regular functions mode - for basic algebra
basic_math = forms.CharField(
    widget=MathInputWidget(mode='regular_functions')
)

# Advanced expressions - for complex equations
complex_math = forms.CharField(
    widget=MathInputWidget(mode='advanced_expressions')
)

# Integrals and differentials - for calculus
calculus_math = forms.CharField(
    widget=MathInputWidget(mode='integrals_differentials', preset='calculus')
)

# Matrices - for linear algebra
matrix_math = forms.CharField(
    widget=MathInputWidget(mode='matrices', preset='machine_learning')
)
```

---

## 12. CONFIGURATION

```python
# math_calculator/settings.py

# Default input mode (regular_functions, advanced_expressions, integrals_differentials, matrices, etc.)
MATHINPUT_DEFAULT_MODE = 'regular_functions'

# Default preset (algebra, calculus, physics, machine_learning, statistics, probability)
MATHINPUT_PRESET = 'algebra'

# Renderer selection
MATHINPUT_RENDERER = 'katex'  # or 'mathjax'

# Storage format (interface is always graphical, but storage can vary)
MATHINPUT_STORAGE_FORMAT = 'latex'  # 'latex', 'mathml', or 'both'

# Enable text formatting features
MATHINPUT_ENABLE_TEXT_FORMATTING = True

# KaTeX extensions to load
MATHINPUT_KATEX_EXTENSIONS = ['cancel', 'copy-tex']

# Graphical interface settings
MATHINPUT_SHOW_VISUAL_BUILDER = True  # Show visual structure as user builds
MATHINPUT_BUTTON_SIZE = 'medium'  # 'small', 'medium', 'large' for touch targets
MATHINPUT_TOOLBAR_STYLE = 'icons'  # 'icons' (default), 'icons-text', 'text'

# CDN URLs (optional - defaults to jsdelivr)
MATHINPUT_KATEX_CDN = 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/'
MATHINPUT_MATHJAX_CDN = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml.js'
```

---

## 13. PACKAGE STRUCTURE

### Package Structure (django-mathinput)

The installable package structure:

```
django-mathinput/                    # Package root (separate from project)
├── mathinput/                       # Django app package
│   ├── __init__.py
│   ├── apps.py
│   ├── widgets.py                   # MathInputWidget with mode support
│   ├── security.py                  # LaTeX sanitization, validation
│   ├── validators.py                # Formula validation, complexity checks
│   ├── modes/                       # Input mode configurations
│   │   ├── __init__.py
│   │   ├── regular_functions.py     # Regular functions mode
│   │   ├── advanced_expressions.py  # Advanced expressions mode
│   │   ├── integrals_differentials.py # Integrals/differentials mode
│   │   ├── matrices.py              # Matrices mode
│   │   ├── statistics_probability.py # Statistics & probability mode
│   │   └── physics_engineering.py  # Physics & engineering mode
│   ├── presets/                     # Domain presets (6 files)
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
│   │   ├── widget.html
│   │   ├── toolbar_*.html           # 7 toolbar templates
│   │   └── quick_insert.html
│   └── static/mathinput/
│       ├── css/mathinput.css
│       └── js/mathinput.js          # Core JS with mode support
├── tests/
├── README.md
├── setup.py
└── MANIFEST.in
```

### Project Structure (math_calculator)

The Django project structure:

```
math_calculator/                     # Project root
├── math_calculator/                 # Main Django app (settings.py here)
│   ├── __init__.py
│   ├── settings.py                  # Django settings
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

### Package Installation

```bash
# Install from PyPI (production)
pip install django-mathinput

# Or install from local source (development)
pip install -e ./django-mathinput
```

### Django Setup

```python
# math_calculator/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ...
    'mathinput',  # Add the package
]
```

---

## 14. SUCCESS METRICS

| KPI | Target |
|-----|--------|
| PyPI | 2,000+/mo |
| GitHub Stars | 400+ |
| Mobile Score | 95+ |
| Accessibility | 100% |

---

## 15. MATH INPUT MODE DETAILS

### MODE-01: Regular Functions
**Target Users:** High school students, basic math courses  
**Toolbar Focus:** Text formatting, Basic operations, Trigonometry  
**Graphical Interface:**
- **Toolbar buttons:** Visual icons for / (fraction), x² (square), √ (root), +, -, ×, ÷, etc.
- **Visual builder:** Shows formula structure as user clicks buttons (e.g., [f][(][x][)][=][x²][+][1])
- **Live preview:** Renders formula in real-time below builder
- **Button layout:** Larger icons (44×44px minimum) for touch-friendly educational use
**Key Features:**
- Simplified toolbar with essential graphical buttons
- Quick access via icons: fractions, exponents, roots, basic functions
- Optimized for: f(x) = x² + 1, sin(x), log(x), etc.
- Storage: LaTeX format (e.g., `f(x) = x^2 + 1`)

**Example LaTeX Output:**
```latex
f(x) = x^2 + 3x - 5
g(x) = \sin(x) + \cos(x)
```

### MODE-02: Advanced Expressions
**Target Users:** College students, advanced algebra  
**Toolbar Focus:** Text, Basic, Advanced, Symbols  
**Graphical Interface:**
- **Toolbar buttons:** Full set of visual icons for all operations (fractions, roots, sums, integrals, matrices, etc.)
- **Visual builder:** Shows complex nested structures with visual nesting indicators
- **Live preview:** Renders complex equations in real-time
- **Button layout:** All toolbars visible, organized by category
**Key Features:**
- Full toolbar access with nested structure support
- Complex equation templates
- Multi-line equation support
- Advanced symbol palette

**Example LaTeX Output:**
```latex
\frac{d}{dx}\left[\frac{x^2 + 3x - 5}{x - 1}\right] = \frac{(2x + 3)(x - 1) - (x^2 + 3x - 5)}{(x - 1)^2}
```

### MODE-03: Integrals/Differentials
**Target Users:** Calculus students, engineers, mathematicians  
**Toolbar Focus:** Calculus, Advanced, Basic, Text  
**Graphical Interface:**
- **Toolbar buttons:** Prominent visual icons for ∫ (integral), d/dx (derivative), d²/dx² (second derivative), ∫ with limits (definite integral), Σ (summation), lim (limit)
- **Visual builder:** Shows integral structure graphically (e.g., [∫][₀][∞][e][⁻][x²][dx])
- **Live preview:** Renders calculus expressions in real-time
- **Button layout:** Calculus operations prominently displayed with large, clear icons
**Key Features:**
- Prominent integral and derivative graphical buttons (like WolframAlpha's math input toolbar)
- Limit notation support via graphical button
- Definite/indefinite integral templates with visual placeholders
- Partial derivatives (∂/∂x), gradients (∇) via icon buttons
- Summation and product notation via graphical buttons

**Example LaTeX Output:**
```latex
\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
\lim_{n \to \infty} \sum_{i=1}^{n} \frac{1}{i^2} = \frac{\pi^2}{6}
\nabla \cdot \mathbf{F} = \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y}
```

### MODE-04: Matrices
**Target Users:** Linear algebra students, ML practitioners, data scientists  
**Toolbar Focus:** Matrices, Advanced, Symbols, Text  
**Graphical Interface:**
- **Toolbar buttons:** Visual icons for [ ] (matrix/vector), grid icon (matrix builder), transpose, inverse, determinant symbols
- **Visual builder:** Interactive matrix grid where users click to add rows/columns and fill cells
- **Live preview:** Renders matrices with proper formatting in real-time
- **Button layout:** Matrix-specific operations with clear visual indicators
**Key Features:**
- **Graphical matrix builder interface** - click to create grid, fill cells visually
- Vector notation via graphical button
- Tensor operations via icon buttons
- Matrix operations (transpose, inverse, determinant) via graphical buttons
- Special ML notation (superscript indices, etc.) via visual buttons

**Example LaTeX Output:**
```latex
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}^{-1} = \frac{1}{ad - bc}\begin{pmatrix}
d & -b \\
-c & a
\end{pmatrix}

\mathbf{W}^{[l]} = \begin{bmatrix}
w_{11} & w_{12} & \cdots & w_{1n} \\
w_{21} & w_{22} & \cdots & w_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
w_{m1} & w_{m2} & \cdots & w_{mn}
\end{bmatrix}
```

### MODE-05: Statistics & Probability
**Target Users:** Statistics students, data analysts  
**Toolbar Focus:** Advanced, Symbols, Basic, Text  
**Graphical Interface:**
- **Toolbar buttons:** Visual icons for statistical symbols (μ, σ, χ², ∑, etc.), probability operators (P, E, Var, Cov), distribution notation
- **Visual builder:** Shows probability expressions and statistical formulas with proper notation
- **Live preview:** Renders statistical notation correctly in real-time
- **Button layout:** Statistics symbols prominently displayed, probability operators easily accessible
**Key Features:**
- Statistical notation (μ, σ, χ², etc.) via graphical buttons
- Probability operators (P, E, Var, Cov) via icon buttons
- Distribution notation via visual buttons
- Hypothesis testing symbols via toolbar

**Example LaTeX Output:**
```latex
P(A|B) = \frac{P(A \cap B)}{P(B)}
E[X] = \sum_{i=1}^{n} x_i P(x_i)
\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i
```

### MODE-06: Physics & Engineering
**Target Users:** Physics students, engineers  
**Toolbar Focus:** Calculus, Symbols, Advanced, Text  
**Graphical Interface:**
- **Toolbar buttons:** Visual icons for tensor notation (T^{μν}), vector calculus (∇, ×, ·), physics symbols (ℏ, c, etc.), engineering notation
- **Visual builder:** Shows tensor structures, vector operations, and physics equations with proper notation
- **Live preview:** Renders physics notation and tensor calculus correctly
- **Button layout:** Physics and engineering symbols prominently displayed, tensor operations easily accessible
**Key Features:**
- Tensor notation via graphical buttons
- Vector calculus operators (∇, ×, ·) via icon buttons
- Physics-specific symbols via visual buttons
- Engineering notation via toolbar
- Special relativity and quantum mechanics symbols via symbols toolbar

**Example LaTeX Output:**
```latex
\nabla \times \mathbf{F} = \begin{vmatrix}
\mathbf{i} & \mathbf{j} & \mathbf{k} \\
\frac{\partial}{\partial x} & \frac{\partial}{\partial y} & \frac{\partial}{\partial z} \\
F_x & F_y & F_z
\end{vmatrix}

T^{\mu\nu} = \begin{pmatrix}
T^{00} & T^{01} & T^{02} & T^{03} \\
T^{10} & T^{11} & T^{12} & T^{13} \\
T^{20} & T^{21} & T^{22} & T^{23} \\
T^{30} & T^{31} & T^{32} & T^{33}
\end{pmatrix}
```

---

## 16. CLARIFICATIONS & MISSING DETAILS

### 16.1 User Input Methods

**Clarification Needed:**
- **Keyboard input:** Can users type numbers, variables (x, y, a, b), and operators directly, or must they use buttons?
- **Hybrid approach:** Recommended - buttons for complex operations (∫, √, fractions), keyboard for simple input (numbers, variables, +, -, =)
- **Auto-completion:** Should typing "frac" suggest fraction button? Or typing "int" suggest integral?

**Decision:** 
- Users can type directly for numbers, variables, and basic operators
- Buttons required for complex structures (fractions, integrals, matrices)
- Optional auto-suggest for LaTeX commands

### 16.2 Visual Formula Builder Details

**Clarification Needed:**
- **Structure:** Is it a tree/graph structure, linear sequence, or both?
- **Editing:** How do users edit existing parts? Click to select, then replace?
- **Navigation:** Arrow keys to move between elements? Tab to move between placeholders?
- **Placeholders:** Visual representation of empty slots (□, _, or actual LaTeX structure)?

**Decision:**
- Linear structure with visual placeholders (e.g., `□/□` for fraction)
- Click on any element to edit it
- Tab/Arrow keys navigate between placeholders and elements
- Placeholders shown as visual boxes with labels

### 16.3 Matrix Builder Interface

**Clarification Needed:**
- **Grid creation:** Click button → popup dialog to set dimensions? Or drag to resize?
- **Cell editing:** Click cell → inline editor? Or separate input field?
- **Operations:** How are transpose, inverse, determinant accessed? Separate buttons or context menu?

**Decision:**
- Click matrix button → dialog: "Rows: [2] Columns: [2]" → creates grid
- Click cell → inline editing with visual formula builder
- Matrix operations via toolbar buttons (transpose, inverse, det icons)

### 16.4 Error Handling & Validation

**Missing Details:**
- **Invalid LaTeX:** How are syntax errors displayed? Red underline? Error message below preview?
- **Real-time validation:** Validate as user types or on blur?
- **Error recovery:** Can users continue editing with errors, or must they fix first?

**Decision:**
- Real-time validation with visual indicators (red border on invalid elements)
- Error tooltip on hover showing specific issue
- Users can continue editing; errors shown but don't block input
- Preview shows error message if LaTeX invalid

### 16.5 Mobile Experience Details

**Missing Details:**
- **Toolbar layout:** Horizontal scroll? Collapsible sections? Bottom sheet?
- **Touch gestures:** Swipe to switch tabs? Pinch to zoom formula?
- **Screen space:** How to show toolbar + builder + preview on small screens?

**Decision:**
- Horizontal scrollable toolbar with tab indicators
- Bottom sheet for matrix builder and complex dialogs
- Collapsible preview (tap to expand/collapse)
- Touch-optimized button sizes (48×48px minimum on mobile)

### 16.6 Accessibility Details

**Missing Details:**
- **Screen readers:** How are formulas announced? Full LaTeX? Natural language description?
- **Keyboard navigation:** Full keyboard-only workflow documented?
- **Focus management:** How is focus handled when switching modes?

**Decision:**
- Screen readers: Announce button labels + LaTeX code
- Full keyboard navigation: Tab through buttons, Enter to activate, Arrow keys in builder
- Focus visible indicator on all interactive elements
- ARIA labels for all buttons and operations

### 16.7 Storage Format Details

**Clarification Needed:**
- **"both" format:** If `MATHINPUT_STORAGE_FORMAT = 'both'`, how is it stored? Two fields? JSON with both?
- **Migration:** Can users switch storage format for existing data?
- **Display:** If stored as MathML, how does `|render_math` work?

**Decision:**
- "both" format: Store as JSON `{"latex": "...", "mathml": "..."}`
- Single field in database (JSON or LaTeX string)
- `|render_math` detects format automatically or uses configured renderer
- Migration tool provided for format conversion

### 16.8 Mode Switching Behavior

**Missing Details:**
- **Active formula:** If user switches mode mid-edit, what happens to current formula?
- **Compatibility:** Can formulas created in one mode be edited in another?
- **Conversion:** Does mode switch convert formula structure?

**Decision:**
- Mode switch preserves current formula (no data loss)
- All modes can edit any valid LaTeX (full compatibility)
- Toolbar changes but formula remains editable
- Warning shown if current formula uses operations not prominent in new mode

### 16.9 Undo/Redo Functionality

**Missing Details:**
- **History depth:** How many undo levels?
- **Scope:** Per-formula or global?
- **Keyboard shortcuts:** Ctrl+Z / Ctrl+Y support?

**Decision:**
- 50-level undo/redo stack per formula
- Standard shortcuts: Ctrl+Z (undo), Ctrl+Y (redo), Ctrl+Shift+Z (redo alternative)
- Visual undo/redo buttons in toolbar
- History persists during session, cleared on form submit

### 16.10 Copy/Paste Operations

**Missing Details:**
- **Paste LaTeX:** Can users paste LaTeX code directly? Auto-convert to visual?
- **Copy format:** What format when copying? LaTeX? Image? Both?
- **External paste:** Paste from other editors (Word, Google Docs)?

**Decision:**
- Paste LaTeX: Supported, auto-converts to visual builder
- Copy: LaTeX text to clipboard (Ctrl+C)
- Copy as image: Right-click → "Copy as image" (PNG/SVG)
- External paste: Attempts to parse and convert common formats

### 16.11 Multi-line Equations

**Missing Details:**
- **Visual representation:** How are multi-line equations shown in builder?
- **Line breaks:** How do users add line breaks? Button? Shift+Enter?
- **Alignment:** Support for aligned equations (align environment)?

**Decision:**
- Multi-line shown with visual line separators
- "New line" button or Shift+Enter
- Alignment options via button (left, center, right, aligned)
- Live preview shows proper LaTeX alignment

### 16.12 Custom Buttons/Templates

**Missing Details:**
- **User-defined:** Can end-users create custom buttons?
- **Admin-defined:** Can admins add domain-specific buttons?
- **Template library:** Shared templates across users?

**Decision:**
- Phase 1: Admin-defined custom buttons via settings
- Phase 2: User-defined templates (saved per user)
- Custom buttons stored in database or config file
- Template library: Future feature (not in MVP)

### 16.13 Performance Considerations

**Clarification Needed:**
- **Complex formulas:** 100ms preview update - is this for all formulas or simple ones?
- **Debouncing:** Is preview update debounced to avoid excessive rendering?
- **Large matrices:** Performance with 10×10 or larger matrices?

**Decision:**
- 100ms target for formulas up to 50 operations
- Preview update debounced (300ms delay after last input)
- Complex formulas (>100 operations): Show "Rendering..." indicator
- Large matrices: Virtual scrolling or pagination for display

### 16.14 Icon Sources & Licensing

**Missing Details:**
- **Icon library:** Which icon set? Font Awesome? Custom SVG? Unicode?
- **Licensing:** Are icon licenses compatible with MIT package license?
- **Customization:** Can users/admins replace icons?

**Decision:**
- Primary: Unicode math symbols (no licensing issues)
- Secondary: Custom SVG icons for complex operations
- Fallback: Font-based icons (MathJax fonts)
- Icons bundled in package (no external dependencies)
- Customization: CSS variables for icon replacement

### 16.15 Visual Builder vs Live Preview

**Clarification Needed:**
- **Distinction:** Are these two separate areas or the same?
- **Relationship:** How do they interact?

**Decision:**
- **Visual Builder:** Interactive editing area (clickable elements, placeholders)
- **Live Preview:** Read-only rendered output (KaTeX rendering)
- Both shown simultaneously (builder on left, preview on right, or stacked on mobile)
- Preview updates automatically as builder changes

### 16.16 Source Mode Sync Details

**Missing Details:**
- **Bidirectional:** How exactly does sync work? Real-time? On blur?
- **Conflict resolution:** If user edits both simultaneously, which takes precedence?
- **Format preservation:** Does source mode preserve formatting/comments?

**Decision:**
- Real-time bidirectional sync (debounced, 300ms)
- Last edit wins (timestamp-based)
- Source mode: Pure LaTeX (no visual formatting)
- Visual mode: Enhanced with visual structure
- Sync indicator shows when syncing

### 16.17 Django Admin Integration Details

**Missing Details:**
- **Widget rendering:** How does widget appear in admin? Full interface or simplified?
- **List display:** How are formulas shown in admin list view? LaTeX code or rendered?
- **Permissions:** Any admin-specific permissions needed?

**Decision:**
- Full widget interface in admin (same as frontend)
- List view: Truncated LaTeX preview (first 50 chars) + "View" link
- Detail view: Full rendered formula
- No special permissions required
- Admin CSS may need adjustment (documented in setup)

### 16.18 Formula Validation & Sanitization

**Missing Details:**
- **XSS prevention:** How is LaTeX sanitized? Whitelist approach?
- **Malicious code:** Protection against script injection in LaTeX?
- **Size limits:** Maximum formula length?

**Decision:**
- LaTeX sanitization: Whitelist of allowed commands
- Strip dangerous commands (\input, \include, \write18, etc.)
- Size limit: 10,000 characters per formula (configurable)
- Server-side validation on form submit
- Client-side validation for immediate feedback

---

## 17. SECURITY CONSIDERATIONS

### 17.1 Threat Model

The package handles user-generated mathematical content that is:
- Stored in database (LaTeX/MathML strings)
- Rendered client-side (KaTeX/MathJax)
- Displayed to other users (via `|render_math` filter)
- Editable by users (visual builder + source mode)

**Potential Attack Vectors:**
1. XSS via LaTeX injection
2. LaTeX command injection
3. CSRF attacks
4. DoS via complex formulas
5. Dependency vulnerabilities
6. Content Security Policy violations
7. Data exfiltration

### 17.2 Cross-Site Scripting (XSS) Protection

**Risk:** Malicious LaTeX code could inject JavaScript when rendered.

**Attack Examples:**
```latex
% Dangerous: KaTeX doesn't execute JS, but custom rendering might
\href{javascript:alert('XSS')}{Click}
\text{<script>alert('XSS')</script>}
```

**Mitigation:**
- **Whitelist LaTeX commands** - Only allow safe mathematical commands
- **Strip dangerous commands:**
  - `\href` with javascript: protocol
  - `\input`, `\include`, `\write18` (file system access)
  - `\def`, `\newcommand` (macro definition - potential DoS)
  - `\verbatiminput`, `\lstinputlisting` (file reading)
- **Output encoding** - All rendered output HTML-escaped
- **CSP headers** - Content Security Policy prevents inline scripts
- **KaTeX sanitization** - KaTeX has built-in XSS protection, but we add extra layer

**Implementation:**
```python
# django-mathinput/mathinput/security.py
DANGEROUS_COMMANDS = [
    r'\input', r'\include', r'\write18', r'\def', r'\newcommand',
    r'\verbatiminput', r'\lstinputlisting', r'\href.*javascript:',
    r'<script', r'</script>', r'javascript:', r'onerror=', r'onclick='
]

def sanitize_latex(latex_string):
    """Remove dangerous LaTeX commands"""
    for pattern in DANGEROUS_COMMANDS:
        latex_string = re.sub(pattern, '', latex_string, flags=re.IGNORECASE)
    return latex_string
```

### 17.3 LaTeX Command Injection

**Risk:** Malicious users could inject arbitrary LaTeX commands to:
- Access file system (`\input{/etc/passwd}`)
- Execute system commands (`\write18{rm -rf /}`)
- Consume resources (infinite loops, large files)

**Mitigation:**
- **Command whitelist** - Only allow mathematical commands
- **Blocked commands:**
  ```python
  BLOCKED_COMMANDS = [
      'input', 'include', 'write18', 'def', 'newcommand',
      'verbatiminput', 'lstinputlisting', 'catcode', 'makeatletter',
      'usepackage', 'RequirePackage', 'documentclass'
  ]
  ```
- **Server-side validation** - Validate on form submit
- **Client-side validation** - Real-time feedback (non-blocking)

**Allowed Commands (Sample):**
```python
ALLOWED_COMMANDS = [
    # Math operations
    'frac', 'sqrt', 'root', 'sum', 'int', 'prod', 'lim',
    # Functions
    'sin', 'cos', 'tan', 'log', 'ln', 'exp',
    # Formatting
    'mathbf', 'mathit', 'mathrm', 'text', 'textbf',
    # Structures
    'begin', 'end', 'matrix', 'pmatrix', 'bmatrix',
    # Operators
    'partial', 'nabla', 'cdot', 'times', 'div'
]
```

### 17.4 Cross-Site Request Forgery (CSRF)

**Risk:** Malicious sites could submit formulas on behalf of authenticated users.

**Mitigation:**
- **Django CSRF protection** - Use `{% csrf_token %}` in forms
- **CSRF middleware** - Django's built-in CSRF middleware enabled
- **SameSite cookies** - Configure cookies with SameSite attribute
- **Origin validation** - Verify request origin (if needed)

**Implementation:**
```django
{# widget.html #}
<form method="post">
    {% csrf_token %}
    {{ widget }}
</form>
```

### 17.5 Denial of Service (DoS) Protection

**Risk:** Complex formulas could:
- Consume excessive CPU/memory during rendering
- Cause browser to freeze
- Exhaust server resources (if server-side validation)

**Attack Examples:**
```latex
% Deeply nested structures
\frac{\frac{\frac{\frac{1}{2}}{3}}{4}}{5}... (1000 levels)

% Large matrices
\begin{pmatrix}
a_{11} & a_{12} & \cdots & a_{1,10000} \\
\vdots & \vdots & \ddots & \vdots \\
a_{10000,1} & \cdots & \cdots & a_{10000,10000}
\end{pmatrix}

% Infinite recursion via macros (if allowed)
\def\a{\a\a}\a
```

**Mitigation:**
- **Formula complexity limits:**
  - Maximum nesting depth: 50 levels
  - Maximum matrix size: 100×100
  - Maximum formula length: 10,000 characters (configurable)
  - Maximum operations: 500 per formula
- **Rendering timeout:** 5 seconds max for preview
- **Client-side limits:** Enforce before submission
- **Server-side validation:** Reject overly complex formulas
- **Rate limiting:** Limit formula submissions per user/IP

**Implementation:**
```python
def validate_complexity(latex_string):
    """Check formula complexity"""
    if len(latex_string) > 10000:
        raise ValidationError("Formula too long (max 10,000 chars)")
    
    nesting_depth = count_nesting(latex_string)
    if nesting_depth > 50:
        raise ValidationError("Formula too deeply nested (max 50 levels)")
    
    matrix_size = get_matrix_size(latex_string)
    if matrix_size and (matrix_size[0] > 100 or matrix_size[1] > 100):
        raise ValidationError("Matrix too large (max 100×100)")
```

### 17.6 Content Security Policy (CSP)

**Risk:** Inline scripts or unsafe eval could be exploited.

**Mitigation:**
- **CSP headers** - Configure strict CSP
- **No inline scripts** - All JS in external files
- **No eval()** - Avoid dynamic code execution
- **CDN whitelist** - Only allow trusted CDNs (jsdelivr.net)

**Recommended CSP:**
```
Content-Security-Policy: 
    default-src 'self';
    script-src 'self' https://cdn.jsdelivr.net;
    style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline';
    font-src 'self' https://cdn.jsdelivr.net;
    img-src 'self' data:;
```

### 17.7 Dependency Security

**Risk:** Vulnerabilities in KaTeX, MathJax, or other dependencies.

**Mitigation:**
- **Version pinning** - Pin exact versions in requirements
- **Regular updates** - Monitor for security advisories
- **Dependency scanning** - Use tools like `safety` or `pip-audit`
- **CDN integrity** - Use SRI (Subresource Integrity) hashes
- **Fallback strategy** - Have fallback if CDN compromised

**Implementation:**
```html
<script 
    src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"
    integrity="sha384-XjKyOOlGwcjNTAIQHIpgOno0Hl1YQqzUOEleOLALmuqehneUG+vnGctmUb0ZY0l8"
    crossorigin="anonymous">
</script>
```

### 17.8 Input Validation & Sanitization

**Multi-Layer Defense:**

1. **Client-Side (Real-time)**
   - Validate as user types
   - Show warnings for dangerous patterns
   - Non-blocking (user can continue)

2. **Client-Side (On Submit)**
   - Full validation before form submission
   - Block submission if invalid
   - Show clear error messages

3. **Server-Side (Required)**
   - Never trust client-side validation
   - Re-validate all input on server
   - Sanitize before storage
   - Log suspicious patterns

**Validation Rules:**
```python
class MathInputValidator:
    def validate(self, latex_string):
        # Length check
        if len(latex_string) > 10000:
            raise ValidationError("Formula too long")
        
        # Command whitelist
        commands = extract_commands(latex_string)
        for cmd in commands:
            if cmd not in ALLOWED_COMMANDS:
                raise ValidationError(f"Command '{cmd}' not allowed")
        
        # Dangerous pattern check
        if contains_dangerous_pattern(latex_string):
            raise ValidationError("Formula contains unsafe content")
        
        # Complexity check
        if exceeds_complexity_limits(latex_string):
            raise ValidationError("Formula too complex")
        
        return sanitize_latex(latex_string)
```

### 17.9 Output Encoding

**Risk:** Stored LaTeX could contain HTML/JS that executes when displayed.

**Mitigation:**
- **Template auto-escaping** - Django templates auto-escape by default
- **Explicit encoding** - Use `|escape` filter when needed
- **Safe rendering** - `|render_math` filter uses safe rendering context
- **No raw HTML** - Never output user content as raw HTML

**Implementation:**
```django
{# Safe rendering #}
{{ formula|render_math|safe }}  {# Safe only after render_math sanitizes #}

{# Never do this #}
{{ formula|safe }}  {# UNSAFE - could contain XSS #}
```

### 17.10 Data Privacy & Confidentiality

**Risk:** Mathematical formulas might contain sensitive information.

**Considerations:**
- **Data encryption** - Encrypt sensitive formulas at rest (if required)
- **Access control** - Who can view/edit formulas?
- **Audit logging** - Log access to sensitive formulas
- **Data retention** - Define retention policies
- **GDPR compliance** - Right to deletion, data export

**Implementation:**
- Use Django's permission system for access control
- Encrypt database fields if storing sensitive data
- Implement audit logging for sensitive operations

### 17.11 Authentication & Authorization

**Risk:** Unauthorized users modifying/viewing formulas.

**Mitigation:**
- **Django authentication** - Use Django's built-in auth
- **Permission checks** - Verify user permissions before edit/view
- **Form-level security** - Validate user can submit to form
- **Admin security** - Django Admin permission system

**Implementation:**
```python
@login_required
@permission_required('mathinput.edit_formula')
def edit_formula(request, formula_id):
    # Permission check ensures only authorized users
    pass
```

### 17.12 Rate Limiting

**Risk:** Abuse via excessive submissions or rendering requests.

**Mitigation:**
- **Submission limits** - Max N formulas per minute per user
- **Rendering limits** - Max preview updates per second
- **IP-based limiting** - Prevent IP-based abuse
- **User-based limiting** - Per-user quotas

**Implementation:**
- Use Django's rate limiting middleware
- Or Django REST Framework throttling
- Or custom middleware for preview requests

### 17.13 Security Configuration

**Settings:**
```python
# math_calculator/settings.py

# Security settings
MATHINPUT_MAX_FORMULA_LENGTH = 10000
MATHINPUT_MAX_NESTING_DEPTH = 50
MATHINPUT_MAX_MATRIX_SIZE = (100, 100)
MATHINPUT_ALLOWED_COMMANDS = [...]  # Whitelist
MATHINPUT_BLOCKED_COMMANDS = [...]  # Blacklist
MATHINPUT_ENABLE_STRICT_VALIDATION = True
MATHINPUT_SANITIZE_ON_SAVE = True
MATHINPUT_RATE_LIMIT_ENABLED = True
MATHINPUT_RATE_LIMIT_PER_MINUTE = 60
```

### 17.14 Security Testing Requirements

**Testing Checklist:**
- [ ] XSS injection attempts blocked
- [ ] LaTeX command injection prevented
- [ ] CSRF protection verified
- [ ] DoS protection (complexity limits) tested
- [ ] Input validation (client + server) tested
- [ ] Output encoding verified
- [ ] Dependency vulnerabilities scanned
- [ ] CSP compliance verified
- [ ] Rate limiting functional
- [ ] Authentication/authorization tested

### 17.15 Security Incident Response

**Procedure:**
1. **Detection** - Monitor for suspicious patterns
2. **Containment** - Block malicious input immediately
3. **Investigation** - Analyze attack vector
4. **Remediation** - Patch vulnerability
5. **Notification** - Inform affected users (if data breach)
6. **Documentation** - Document incident and fix

**Monitoring:**
- Log all validation failures
- Alert on suspicious patterns (e.g., many blocked commands)
- Monitor error rates
- Track formula complexity distribution

---

## 18. ADDITIONAL CLARIFICATIONS & EDGE CASES

### 18.1 Quick Insert Functionality

**Missing Details:**
- **UI/UX:** How is quick insert accessed? Dropdown menu? Popup dialog? Sidebar?
- **Templates:** What format are templates stored in? LaTeX strings? JSON?
- **Organization:** How are templates organized? By preset? By category?
- **User templates:** Can users save their own quick inserts? (mentioned as Phase 2, but needs detail)

**Clarification:**
- Quick insert accessed via dropdown button in toolbar (e.g., "[Calc Quick ▼]")
- Dropdown shows list of template names (e.g., "Indefinite Integral", "Definite Integral with Limits")
- Clicking template inserts LaTeX into visual builder at cursor position
- Templates stored as LaTeX strings in preset configuration files
- User-defined templates: Phase 2 feature, stored per-user in database or user settings

### 18.2 Text Formatting Details

**Missing Details:**
- **Color selection:** How do users pick colors? Color picker? Preset palette? Hex input?
- **Size options:** What sizes are available? Small, Normal, Large, Huge? Or numeric?
- **Scope:** Does formatting apply to entire formula or selected parts?
- **Formatting buttons:** Where are formatting buttons located? Text tab? Separate formatting toolbar?

**Clarification:**
- Color: Preset palette (10-15 common colors) + custom hex input
- Size: Preset sizes (tiny, small, normal, large, huge) matching LaTeX sizes
- Scope: Formatting applies to selected portion (if selection) or next input (if no selection)
- Formatting buttons: Located in Text tab toolbar, grouped together visually

### 18.3 Mode Name Standardization

**Inconsistency:** Mode names appear as:
- "Regular Functions" (descriptive)
- "regular" (lowercase, in code)
- "Regular" (capitalized)

**Clarification:**
- **Display names:** Use full descriptive names (e.g., "Regular Functions", "Integrals/Differentials")
- **Code identifiers:** Use lowercase with underscores (e.g., `mode='regular_functions'`, `mode='integrals_differentials'`)
- **Settings:** Use code identifiers in settings (e.g., `MATHINPUT_DEFAULT_MODE = 'regular_functions'`)

### 18.4 Preset-Mode Relationship

**Unclear:**
- Can presets be used without specifying a mode?
- What happens if preset and mode are incompatible?
- What's the default if neither is specified?

**Clarification:**
- Mode is required (defaults to `MATHINPUT_DEFAULT_MODE` if not specified)
- Preset is optional (defaults to `MATHINPUT_PRESET` if not specified)
- Presets work with any mode (they just customize tab order and quick inserts)
- No incompatibility - presets are additive, not restrictive
- Example: `mode='regular_functions'` with `preset='calculus'` is valid (shows calculus quick inserts in regular mode)

### 18.5 Visual Builder Implementation

**Unclear:**
- Is it a tree/graph structure internally?
- How are nested structures represented visually?
- Can users drag and drop to reorder?
- How are placeholders filled?

**Clarification:**
- Internal structure: Tree-based (AST - Abstract Syntax Tree)
- Visual representation: Linear with visual nesting indicators (indentation, brackets, boxes)
- Drag and drop: Not in MVP, future enhancement
- Placeholder filling: Click placeholder → activates inline editor → type or click buttons
- Navigation: Tab moves to next placeholder, Shift+Tab moves to previous

### 18.6 Button Click Behavior

**Unclear:**
- Where does inserted content go? At cursor? Replace selection? Always append?
- What if cursor is in middle of existing formula?
- What if user has text selected?

**Clarification:**
- Insert at cursor position (if no selection)
- Replace selection (if text is selected)
- If cursor in middle: Insert at cursor, push existing content right
- If cursor in placeholder: Insert into placeholder
- Selection is cleared after insertion

### 18.7 Empty State & Initialization

**Missing:**
- What does editor look like when empty?
- Is there placeholder text?
- How is initial value loaded?
- What if existing formula is loaded?

**Clarification:**
- Empty state: Shows placeholder text "Click buttons or type to start building formula"
- Placeholder disappears on first input
- Initial value: Loaded from form field value (if exists)
- Existing formula: Parsed and converted to visual builder structure
- Auto-detection: Detects LaTeX vs MathML format automatically

### 18.8 Browser Compatibility Details

**Vague:** "latest 2" versions is unclear

**Clarification:**
- Chrome: Last 2 major versions (e.g., 120, 121)
- Firefox: Last 2 major versions (e.g., 120, 121)
- Safari: Last 2 major versions (e.g., 17, 18)
- Edge: Last 2 major versions (Chromium-based, same as Chrome)
- Mobile: iOS Safari 15+, Chrome Android (last 2 versions)
- Graceful degradation: Show warning for older browsers, but attempt to work

### 18.9 Offline Functionality

**Unclear:** TC-03 says "works offline" but how?

**Clarification:**
- Assets (JS, CSS) can be bundled locally (not just CDN)
- KaTeX/MathJax can be bundled or loaded from CDN (with offline fallback)
- No server requests needed for editing/rendering
- Form submission requires network (but that's Django, not this package)
- Service worker: Optional, not required for basic offline editing

### 18.10 Internationalization (i18n)

**Missing:** No mention of non-English support

**Clarification:**
- Button labels: Support i18n via Django's translation system
- Error messages: Translatable
- Tooltips: Translatable
- LaTeX commands: Language-agnostic (same across languages)
- UI text: All user-facing text in translation files
- Default: English, with translation support for common languages

### 18.11 Formula Loading & Parsing

**Missing:**
- How are existing formulas loaded into editor?
- What if formula is invalid/corrupted?
- What if formula uses unsupported commands?
- Can formulas be imported from other formats?

**Clarification:**
- Loading: Parse stored LaTeX/MathML → convert to visual builder structure
- Invalid formula: Show error message, allow editing in source mode
- Unsupported commands: Show warning, allow in source mode, strip on save (if strict mode)
- Import: Support paste from Word, Google Docs, other LaTeX editors (parse and convert)
- Export: Copy as LaTeX, MathML, or image (PNG/SVG)

### 18.12 Error Messages & User Guidance

**Missing:**
- What error messages are shown?
- How are errors communicated to users?
- Is there help/documentation built-in?
- Tooltips for learning?

**Clarification:**
- Error messages: Clear, non-technical language
- Display: Inline below preview area, with icon and message
- Validation errors: Show specific issue (e.g., "Command '\input' is not allowed")
- Help: Tooltips on all buttons showing LaTeX code
- Documentation: Link to help page in toolbar (optional, configurable)
- Keyboard shortcuts: Shown in tooltip or help menu

### 18.13 Package Versioning & Compatibility

**Missing:**
- Versioning strategy (semantic versioning?)
- Backward compatibility policy
- Migration path for breaking changes
- Django version compatibility matrix

**Clarification:**
- Versioning: Semantic versioning (MAJOR.MINOR.PATCH)
- Backward compatibility: Maintained within major version
- Breaking changes: Only in major versions, with migration guide
- Django compatibility: Tested with Django 3.2, 4.0, 4.1, 4.2 (latest 2 LTS + latest)
- Python compatibility: Python 3.8, 3.9, 3.10, 3.11, 3.12 (latest 2 + LTS)

### 18.14 Performance Metrics Details

**Unclear:**
- "Preview update < 100ms" - under what conditions?
- What about complex formulas?
- What about slow devices?

**Clarification:**
- 100ms target: For formulas with <50 operations, on modern desktop browser
- Complex formulas (>100 operations): Up to 500ms acceptable
- Slow devices: Up to 1s acceptable with loading indicator
- Debouncing: 300ms delay prevents excessive rendering
- Progressive rendering: Show partial results for very complex formulas

### 18.15 Accessibility Keyboard Shortcuts

**Missing:**
- Complete list of keyboard shortcuts
- How are shortcuts discovered?
- Conflict resolution with browser shortcuts?

**Clarification:**
- Shortcuts documented in help menu
- Common shortcuts:
  - Ctrl+M: Toggle Visual/Source mode
  - Ctrl+Z/Y: Undo/Redo
  - Tab: Next placeholder
  - Shift+Tab: Previous placeholder
  - Ctrl+B: Bold (if in text mode)
  - Escape: Close dialogs, cancel operations
- Conflicts: Use Ctrl+Shift+Alt for shortcuts that conflict with browser
- Discovery: Tooltip shows shortcut on hover, help menu lists all

### 18.16 Formula Validation Feedback

**Unclear:**
- When is validation performed?
- How are validation results shown?
- Can users disable validation?

**Clarification:**
- Real-time: As user types (debounced, 500ms delay)
- On blur: When leaving input field
- On submit: Before form submission (blocks if invalid)
- Display: Inline errors below preview, with icon and message
- Disable: Can disable client-side validation (not recommended), server-side always enabled
- Warnings vs Errors: Warnings (yellow) don't block, Errors (red) block submission

### 18.17 Multi-Instance Support

**Missing:**
- Can multiple editors exist on same page?
- Do they share state?
- How are they identified?

**Clarification:**
- Multiple instances: Supported, each with unique ID
- State: Independent per instance
- Identification: Via widget ID or form field name
- Conflicts: None, each instance is isolated
- Performance: Each instance loads its own KaTeX renderer (shared if possible)

### 18.18 Customization & Theming

**Missing:**
- Can users/admins customize appearance?
- Dark mode support?
- Custom CSS?

**Clarification:**
- Theming: CSS variables for colors, sizes, spacing
- Dark mode: Built-in support via CSS variables
- Custom CSS: Can override styles via custom CSS file
- Configuration: Theme selection via settings or user preference
- Branding: Logo, colors customizable via settings

---

## 19. FINAL CLARIFICATIONS & EDGE CASES

### 19.1 Widget Initialization & Existing Values

**Missing Details:**
- What happens when widget is initialized with existing LaTeX value?
- How is existing value parsed and converted to visual builder?
- What if existing value is invalid/corrupted?
- What if existing value uses unsupported commands?

**Clarification:**
- Widget initialization: If form field has value, parse and convert to visual builder structure
- Parsing: Attempt to parse LaTeX → build AST → convert to visual structure
- Invalid value: Show error in preview, allow editing in source mode
- Unsupported commands: Show warning, allow in source mode, may be stripped on save (if strict mode)
- Empty value: Show placeholder text, ready for input

### 19.2 Widget Attributes & Form Integration

**Missing Details:**
- How do Django form field attributes (required, disabled, readonly) affect widget?
- Can widget be disabled/readonly?
- How does widget integrate with Django form validation?
- What about field-level validation errors?

**Clarification:**
- Required: Widget shows required indicator, blocks submission if empty
- Disabled: Widget is non-interactive, shows value but no editing
- Readonly: Similar to disabled, but may allow viewing
- Form validation: Widget integrates with Django's form validation system
- Field errors: Display validation errors below widget, highlight invalid fields
- Custom validators: Support Django's field validators, widget validates before form submission

### 19.3 Static Files & Asset Management

**Missing Details:**
- How are static files collected in production?
- What about collectstatic command?
- CDN vs bundled assets - how to choose?
- What if CDN is unavailable?

**Clarification:**
- Static files: Use Django's static files framework
- collectstatic: Required for production, collects all static files
- CDN vs bundled: Configurable via settings (default: CDN for KaTeX, bundled for package JS/CSS)
- CDN fallback: If CDN unavailable, attempt to load from local bundled version
- Offline mode: Can bundle all assets locally for offline use
- Asset versioning: Use cache-busting for updates

### 19.4 Template Tag Parameters

**Missing Details:**
- What parameters does `|as_mathinput` filter accept?
- What parameters does `|render_math` filter accept?
- Can parameters be combined?
- What are default values?

**Clarification:**
- `|as_mathinput` parameters:
  - `mode`: Input mode (e.g., `mode="integrals"`)
  - `preset`: Domain preset (e.g., `preset="calculus"`)
  - `button_size`: Button size (`small`, `medium`, `large`)
  - `show_preview`: Show/hide preview (`true`, `false`)
- `|render_math` parameters:
  - `renderer`: Override renderer (`katex`, `mathjax`)
  - `display`: Display mode (`inline`, `block`)
  - `error_message`: Custom error message if rendering fails
- Combined: All parameters can be combined
- Defaults: Use settings defaults if not specified

### 19.5 Render Failures & Error Handling

**Missing Details:**
- What happens if KaTeX fails to render a formula?
- What if formula is syntactically invalid?
- How are rendering errors displayed?
- Can users continue editing with rendering errors?

**Clarification:**
- Render failure: Show error message in preview area with icon
- Invalid syntax: Highlight invalid parts, show error tooltip
- Error display: Red border around preview, error message below
- Continue editing: Yes, errors don't block editing (only block submission if critical)
- Error types:
  - Syntax errors: Show specific error (e.g., "Missing closing brace")
  - Command errors: Show "Unknown command: \xyz"
  - Complexity errors: Show "Formula too complex to render"

### 19.6 Widget State & Persistence

**Missing Details:**
- Does widget state persist across page reloads?
- What about browser back/forward?
- How is undo/redo state managed?
- What happens on form reset?

**Clarification:**
- Page reload: State lost unless form has initial value
- Browser navigation: State lost (standard browser behavior)
- Undo/redo: Per-session, cleared on form submit/reset
- Form reset: Widget resets to initial value or empty
- Auto-save: Optional feature (future), can save draft to localStorage
- Session persistence: Not built-in, can be added via custom implementation

### 19.7 Widget ID Generation & Multiple Instances

**Missing Details:**
- How are widget IDs generated?
- What if multiple widgets on same page?
- Can widgets share state?
- How to identify specific widget in JavaScript?

**Clarification:**
- ID generation: Django's widget ID generation (based on field name)
- Multiple instances: Each widget has unique ID, independent state
- Shared state: No, each widget is isolated
- JavaScript access: Use widget ID or data attributes
- Naming: IDs follow Django convention: `id_<field_name>`

### 19.8 Media Loading & Dependencies

**Missing Details:**
- What's the loading order of CSS/JS?
- What if KaTeX fails to load?
- How are dependencies managed?
- What about async/defer loading?

**Clarification:**
- Loading order:
  1. KaTeX CSS (if CDN)
  2. Package CSS
  3. KaTeX JS (if CDN)
  4. Package JS
- KaTeX failure: Show error, attempt fallback to MathJax (if configured)
- Dependencies: KaTeX must load before package JS
- Async/defer: KaTeX can be async, package JS must wait for KaTeX
- Loading indicator: Show spinner while assets load

### 19.9 Testing Requirements & Coverage

**Missing Details:**
- What types of tests are required?
- What's the testing strategy?
- How to test visual builder?
- How to test rendering?

**Clarification:**
- Unit tests: Widget rendering, validation, sanitization (90% coverage target)
- Integration tests: Form submission, template tags, Django admin
- JavaScript tests: Use Jest or similar, test core functionality
- Visual tests: Manual testing for visual builder (automated visual regression future)
- Browser tests: Test in all supported browsers
- Accessibility tests: Automated a11y testing tools
- Performance tests: Load testing for complex formulas

### 19.10 Deployment & Production Considerations

**Missing Details:**
- What are production requirements?
- How to configure for production?
- What about caching?
- CDN configuration?

**Clarification:**
- Requirements: Django 3.2+, Python 3.8+, static files configured
- Configuration: Set `DEBUG=False`, configure static files, set CDN URLs
- Caching: Cache static assets, cache rendered formulas (optional)
- CDN: Configure CDN for KaTeX/MathJax, or bundle locally
- Security: Enable CSP headers, configure CSRF, enable rate limiting
- Monitoring: Log errors, monitor performance, track usage

### 19.11 Widget Cleanup & Memory Management

**Missing Details:**
- How is widget cleaned up when removed from DOM?
- What about memory leaks?
- Event listener cleanup?
- KaTeX instance cleanup?

**Clarification:**
- DOM removal: Cleanup event listeners, remove KaTeX instances
- Memory leaks: Proper cleanup prevents leaks
- Event listeners: Remove all listeners on widget destroy
- KaTeX instances: Destroy KaTeX renderers on cleanup
- Best practices: Follow JavaScript best practices for cleanup

### 19.12 Mode Name Standardization (Code vs Display)

**Inconsistency Found:**
- Display: "Regular Functions", "Integrals/Differentials"
- Code: Sometimes `'regular'`, sometimes `'regular_functions'`
- Settings: Mixed usage

**Standardization:**
- **Display names:** Full descriptive (e.g., "Regular Functions", "Integrals/Differentials")
- **Code identifiers:** Lowercase with underscores:
  - `regular_functions`
  - `advanced_expressions`
  - `integrals_differentials`
  - `matrices`
  - `statistics_probability`
  - `physics_engineering`
- **Settings:** Always use code identifiers
- **Widget parameters:** Use code identifiers
- **Template filters:** Use code identifiers

### 19.13 Preset Name Standardization

**Inconsistency Found:**
- Code examples show: `'calculus'`, `'ml'`, `'algebra'`
- Need standardization

**Standardization:**
- **Code identifiers:** Lowercase, no spaces:
  - `algebra`
  - `calculus`
  - `physics`
  - `machine_learning` (not `ml`)
  - `statistics`
  - `probability`

### 19.14 Widget Media Class Details

**Missing Details:**
- What CSS/JS files are included?
- What's the order?
- Can developers override/extend?

**Clarification:**
- CSS files:
  1. KaTeX CSS (if CDN)
  2. `mathinput/css/mathinput.css`
- JS files:
  1. KaTeX JS (if CDN)
  2. `mathinput/js/mathinput.js`
- Override: Developers can extend Media class to add custom CSS/JS
- Order: Dependencies loaded first, package files last

### 19.15 Formula Export Formats

**Missing Details:**
- What formats can formulas be exported to?
- How to export?
- What about images?

**Clarification:**
- Export formats:
  - LaTeX (text)
  - MathML (XML)
  - Image (PNG/SVG)
  - Copy to clipboard
- Export methods:
  - Right-click menu: "Copy as LaTeX", "Copy as Image"
  - Toolbar button: Export dropdown
  - Keyboard: Ctrl+Shift+C (copy as LaTeX)
- Images: Generated client-side using canvas or SVG

### 19.16 Formula Import Formats

**Missing Details:**
- What formats can be imported?
- How to import?
- What about paste from other editors?

**Clarification:**
- Import formats:
  - LaTeX (paste text)
  - MathML (paste XML)
  - Word/Google Docs (attempt to parse)
- Import methods:
  - Paste (Ctrl+V) in visual builder or source mode
  - File upload (future feature)
  - Drag and drop (future feature)
- Parsing: Attempt to detect format and convert to visual builder

### 19.17 Widget Customization & Extension

**Missing Details:**
- Can developers customize widget appearance?
- Can developers add custom buttons?
- Can developers extend functionality?

**Clarification:**
- Appearance: CSS customization via custom CSS or CSS variables
- Custom buttons: Phase 1 (admin-defined), Phase 2 (developer-defined)
- Extension: JavaScript API for extending functionality (future)
- Hooks: Event hooks for custom behavior (future)
- Plugins: Plugin system for advanced customization (future)

### 19.18 Documentation Requirements

**Missing Details:**
- What documentation is required?
- Where is documentation located?
- What about examples?

**Clarification:**
- Required documentation:
  - README.md (installation, quick start)
  - User guide (how to use widget)
  - Developer guide (customization, extension)
  - API documentation (if exposing API)
  - Examples (common use cases)
- Location: Package docs/ directory, GitHub wiki, or separate docs site
- Examples: Include in package, showcase common scenarios

---

## 20. APPROVAL

| Role | Name | Date |
|------|------|------|
| Product Owner | [You] | 16 Nov 2025 |

---

**END OF DOCUMENT**

---

## 19. GRAPHICAL INTERFACE DESIGN

### Core Principle: Button-Based Visual Input

The interface is **graphical and button-based**, similar to WolframAlpha's math input toolbar. Users interact with visual icon buttons, not by typing LaTeX directly.

### Interface Components

1. **Graphical Toolbar**
   - Icon buttons for all operations (∫, √, ∂, Σ, etc.)
   - Visual representation, not text labels
   - Mode-specific button sets
   - Responsive button sizes (touch-friendly on mobile)

2. **Visual Formula Builder**
   - Shows formula structure as user clicks buttons
   - Visual placeholders for empty slots (e.g., `□/□` for fraction)
   - Clickable elements that can be edited
   - Visual nesting indicators for complex structures

3. **Live Preview Area**
   - Real-time KaTeX rendering
   - Updates as user builds formula
   - Shows final rendered output
   - Scrollable for long formulas

4. **Source Mode (Optional)**
   - Toggle to LaTeX text view
   - For advanced users who prefer direct LaTeX editing
   - Bidirectional sync with visual builder

### Storage vs. Interface

- **Interface:** Always graphical/visual (button-based)
- **Storage:** Flexible format (LaTeX default, MathML optional)
- **Display:** Renders stored format to visual output

### Button Design Standards

- **Icon-based:** Use Unicode symbols or SVG icons (∫, √, ∂, Σ, etc.)
- **Size:** Minimum 44×44px for touch targets (WCAG)
- **Grouping:** Related operations grouped visually
- **Tooltips:** Show LaTeX code on hover for learning
- **Active state:** Highlight when formula contains that operation

### Example: Building an Integral

1. User clicks **∫** button → Visual builder shows `∫ □ d□`
2. User clicks in first placeholder → Types "3x"
3. User clicks in second placeholder → Types "x"
4. Live preview shows: `∫ 3x dx = (3x²)/2 + constant`
5. Storage saves: `\int 3x \, dx` (LaTeX format)

---

## 20. APPENDIX: MODE VS PRESET CLARIFICATION

**Input Modes** define the UI/UX complexity and toolbar layout:
- Control which toolbars are visible and prioritized
- Determine button sizes and layouts
- Optimize for specific mathematical operation types
- Example: "Integrals mode" shows calculus toolbar prominently

**Presets** define domain-specific configurations:
- Customize tab order within a mode
- Provide domain-specific quick insert templates
- Highlight commonly used buttons for that domain
- Example: "Calculus preset" prioritizes ∫ and lim buttons

**Usage Pattern:**
- Mode = "What type of math are you writing?" (UI complexity)
- Preset = "What domain/subject?" (Content optimization)

Both can be used together:
```python
# Calculus course with integrals mode
widget=MathInputWidget(mode='integrals_differentials', preset='calculus')

# ML course with matrices mode
widget=MathInputWidget(mode='matrices', preset='machine_learning')
```

### CKEditor-Style Integration

The package follows CKEditor's integration pattern:
- **Widget-based:** Use `MathInputWidget` in Django forms
- **Template filter:** Use `|as_mathinput` filter in templates
- **Display filter:** Use `|render_math` to render stored format
- **Graphical interface:** Button-based visual editor (like CKEditor's toolbar)
- **Separate package:** Installable via pip, works across Django projects
- **No database changes:** Pure frontend solution with Django integration
- **Storage flexibility:** Save as LaTeX, MathML, or other formats (interface is always graphical)

---

**WORD FILE READY**  
**Next Step:** **SYSTEM DESIGN DOCUMENT (SDD)**

Type: **"Proceed to Design Document"**