# Implementation Plan - Phase 2: Core Functionality

## Overview
Phase 2 implements the core functionality: mode system, preset system, toolbar templates, visual builder AST engine, and JavaScript core functionality.

## Tasks

### Task 5: Mode System (6 Mode Modules)
**Owner:** Lead Dev  
**Duration:** 3 days  
**Dependencies:** Task 1

**Implementation:**
- Create `django-mathinput/mathinput/modes/` directory
- Implement 6 mode modules:
  - `regular_functions.py`
  - `advanced_expressions.py`
  - `integrals_differentials.py`
  - `matrices.py`
  - `statistics_probability.py`
  - `physics_engineering.py`

Each mode module structure:
```python
# django-mathinput/mathinput/modes/integrals_differentials.py
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
            "size": "large",
            "grouping": "calculus_operations"
        },
        "quick_inserts": [
            ("Indefinite Integral", "\\int f(x) \\, dx"),
            ("Definite Integral", "\\int_{a}^{b} f(x) \\, dx"),
            ("Derivative", "\\frac{d}{dx}"),
        ]
    }
```

- Create mode loader function in `mathinput/modes/__init__.py`

**Deliverables:**
- 6 mode configuration modules
- Mode loader function
- Mode validation

---

### Task 6: Preset System (6 Preset Modules)
**Owner:** Lead Dev  
**Duration:** 2 days  
**Dependencies:** Task 1

**Implementation:**
- Create preset modules in `django-mathinput/mathinput/presets/`:
  - `algebra.py`
  - `calculus.py`
  - `physics.py`
  - `machine_learning.py`
  - `statistics.py`
  - `probability.py`

Each preset module:
```python
# django-mathinput/mathinput/presets/machine_learning.py
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

- Create preset loader function

**Deliverables:**
- 6 preset configuration modules
- Preset loader function
- Preset validation

---

### Task 7: Toolbar Templates (7 Tabs)
**Owner:** UI Dev  
**Duration:** 4 days  
**Dependencies:** Task 2

**Implementation:**
- Create 7 toolbar template files in `django-mathinput/mathinput/templates/mathinput/`:
  - `toolbar_text.html` - Text formatting buttons
  - `toolbar_basic.html` - Basic operations (fractions, roots, powers)
  - `toolbar_advanced.html` - Advanced operations
  - `toolbar_calculus.html` - Calculus operations (integrals, derivatives)
  - `toolbar_matrices.html` - Matrix operations
  - `toolbar_trig.html` - Trigonometry functions
  - `toolbar_symbols.html` - Mathematical symbols

Each toolbar template:
```html
<!-- django-mathinput/mathinput/templates/mathinput/toolbar_basic.html -->
<div class="mi-toolbar mi-toolbar-basic" role="toolbar" aria-label="Basic operations">
    <button type="button" 
            class="mi-button mi-button-fraction" 
            data-action="insert"
            data-template="\\frac{}{}"
            aria-label="Insert fraction"
            title="Fraction (/)">
        /
    </button>
    <button type="button" 
            class="mi-button mi-button-square" 
            data-action="insert"
            data-template="^{2}"
            aria-label="Square"
            title="Square (x²)">
        x²
    </button>
    <!-- More buttons... -->
</div>
```

**Deliverables:**
- 7 toolbar HTML templates
- All buttons with proper ARIA labels
- Icon buttons (Unicode/SVG)
- Responsive layout

---

### Task 8: Visual Builder AST Engine
**Owner:** Frontend Dev  
**Duration:** 5 days  
**Dependencies:** Task 2

**Implementation:**
- Create AST (Abstract Syntax Tree) engine in `django-mathinput/mathinput/static/mathinput/js/mathinput.js`:
  ```javascript
  // AST Node Types
  const NodeTypes = {
      VARIABLE: 'variable',
      NUMBER: 'number',
      OPERATOR: 'operator',
      FRACTION: 'fraction',
      ROOT: 'root',
      POWER: 'power',
      FUNCTION: 'function',
      INTEGRAL: 'integral',
      SUM: 'sum',
      MATRIX: 'matrix',
      EXPRESSION: 'expression'
  };
  
  // AST Node Class
  class ASTNode {
      constructor(type, value, children = []) {
          this.type = type;
          this.value = value;
          this.children = children;
          this.parent = null;
      }
  }
  
  // LaTeX Parser
  function parseLatex(latex) {
      // Parse LaTeX string into AST
  }
  
  // AST to LaTeX Converter
  function astToLatex(ast) {
      // Convert AST back to LaTeX string
  }
  
  // Visual Builder Renderer
  class VisualBuilder {
      constructor(container, ast) {
          this.container = container;
          this.ast = ast;
      }
      
      render() {
          // Render AST as visual structure with placeholders
      }
      
      updateAST(newAST) {
          this.ast = newAST;
          this.render();
      }
  }
  ```

**Deliverables:**
- AST node classes
- LaTeX parser (LaTeX → AST)
- AST to LaTeX converter (AST → LaTeX)
- Visual builder renderer
- Placeholder management

---

### Task 9: Vanilla JS Core (Insert, Sync, Preview)
**Owner:** Frontend Dev  
**Duration:** 5 days  
**Dependencies:** Task 8

**Implementation:**
- Button click handlers:
  ```javascript
  function handleButtonClick(buttonElement) {
      const template = buttonElement.dataset.template;
      const cursor = getCursorPosition();
      const newNode = createNodeFromTemplate(template);
      insertNode(cursor, newNode);
      updateVisualBuilder();
      updateLaTeX();
      syncSourceMode();
      renderPreview();
  }
  ```

- Preview rendering with KaTeX:
  ```javascript
  function renderPreview(latex) {
      const container = document.querySelector('.mi-preview');
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

- Hidden field sync:
  ```javascript
  function updateHiddenField(latex) {
      const hiddenField = document.querySelector('textarea[name="equation"]');
      hiddenField.value = latex;
  }
  ```

- Event listeners setup
- Debouncing for preview updates

**Deliverables:**
- Button click handlers
- Preview rendering with KaTeX
- Hidden field synchronization
- Event management
- Error handling

---

## Phase 2 Testing Requirements

### Unit Tests

#### Test File: `tests/test_modes.py`

```python
import pytest
from mathinput.modes import get_mode, load_mode


@pytest.mark.unit
def test_get_mode_returns_valid_structure():
    """
    What we are testing: get_mode() returns valid mode configuration structure
    Why we are testing: Mode system must provide consistent configuration format
    Expected Result: Dictionary with required keys: name, code, toolbars, button_layout
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_load_mode_loads_integrals_mode():
    """
    What we are testing: load_mode() correctly loads integrals_differentials mode
    Why we are testing: Mode loader must correctly retrieve mode configurations
    Expected Result: Returns mode config with calculus toolbar prioritized
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_mode_toolbar_visibility():
    """
    What we are testing: Mode configuration correctly specifies visible/hidden toolbars
    Why we are testing: UI must show/hide toolbars based on mode
    Expected Result: Visible toolbars list matches mode requirements
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_all_modes_have_valid_codes():
    """
    What we are testing: All 6 modes have valid, unique code identifiers
    Why we are testing: Mode codes used in settings and widget parameters
    Expected Result: All modes have valid codes matching naming convention
    """
    # Test implementation
    pass
```

#### Test File: `tests/test_presets.py`

```python
import pytest
from mathinput.presets import get_preset, load_preset


@pytest.mark.unit
def test_get_preset_returns_valid_structure():
    """
    What we are testing: get_preset() returns valid preset configuration structure
    Why we are testing: Preset system must provide consistent configuration format
    Expected Result: Dictionary with required keys: name, code, tab_order, quick_inserts
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_load_preset_loads_calculus_preset():
    """
    What we are testing: load_preset() correctly loads calculus preset
    Why we are testing: Preset loader must correctly retrieve preset configurations
    Expected Result: Returns preset config with calculus-specific quick inserts
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_preset_tab_order_valid():
    """
    What we are testing: Preset tab_order contains valid toolbar names
    Why we are testing: Tab order must reference existing toolbars
    Expected Result: All tab names in tab_order are valid toolbar identifiers
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_preset_quick_inserts_valid_latex():
    """
    What we are testing: Preset quick_inserts contain valid LaTeX strings
    Why we are testing: Quick inserts must be valid LaTeX for insertion
    Expected Result: All quick insert templates are valid LaTeX
    """
    # Test implementation
    pass
```

### Integration Tests

#### Test File: `tests/test_integration_phase2.py`

```python
import pytest
from django.test import TestCase
from mathinput.widgets import MathInputWidget
from mathinput.modes import load_mode
from mathinput.presets import load_preset


@pytest.mark.integration
class TestModePresetIntegration(TestCase):
    """
    What we are testing: Mode and preset systems work together in widget
    Why we are testing: Widget must correctly combine mode and preset configurations
    Expected Result: Widget renders with correct toolbar layout and quick inserts
    """
    
    def test_widget_with_mode_and_preset():
        """
        What we are testing: Widget correctly applies mode and preset together
        Why we are testing: Users specify both mode and preset for optimal UI
        Expected Result: Widget shows mode-appropriate toolbars with preset quick inserts
        """
        # Test implementation
        pass
    
    def test_mode_preset_config_merge():
        """
        What we are testing: Mode and preset configurations merge correctly
        Why we are testing: Both systems must work together without conflicts
        Expected Result: Merged config has mode toolbars + preset tab order
        """
        # Test implementation
        pass
```

### Frontend Tests

#### Test File: `tests/test_frontend_phase2.js` (Jest/Jasmine)

```javascript
// Note: These would be JavaScript tests, not Python
// Using Jest or similar framework

describe('AST Engine', () => {
    test('parseLatex creates valid AST', () => {
        /**
         * What we are testing: parseLatex correctly parses LaTeX into AST
         * Why we are testing: AST is core data structure for visual builder
         * Expected Result: Valid AST structure created from LaTeX input
         */
        // Test implementation
    });
    
    test('astToLatex converts AST back to LaTeX', () => {
        /**
         * What we are testing: astToLatex correctly converts AST to LaTeX string
         * Why we are testing: Need bidirectional conversion for sync
         * Expected Result: LaTeX string matches original (or equivalent)
         */
        // Test implementation
    });
    
    test('VisualBuilder renders AST structure', () => {
        /**
         * What we are testing: VisualBuilder renders AST as visual elements
         * Why we are testing: Users must see visual representation of formula
         * Expected Result: DOM contains visual elements matching AST structure
         */
        // Test implementation
    });
    
    test('PlaceholderManager extracts placeholders', () => {
        /**
         * What we are testing: PlaceholderManager finds all placeholder positions
         * Why we are testing: Users need to navigate between placeholders
         * Expected Result: All empty slots in AST identified as placeholders
         */
        // Test implementation
    });
});

describe('Button Click Handlers', () => {
    test('button click inserts template', () => {
        /**
         * What we are testing: Button click inserts LaTeX template into AST
         * Why we are testing: Core user interaction - inserting operations
         * Expected Result: AST updated with new node, visual builder updated
         */
        // Test implementation
    });
    
    test('button click updates preview', () => {
        /**
         * What we are testing: Button click triggers preview update
         * Why we are testing: Users need immediate feedback on changes
         * Expected Result: Preview area shows rendered formula after button click
         */
        // Test implementation
    });
});

describe('Preview Rendering', () => {
    test('KaTeX renders valid LaTeX', () => {
        /**
         * What we are testing: KaTeX successfully renders valid LaTeX
         * Why we are testing: Preview must show correct mathematical rendering
         * Expected Result: Preview shows rendered formula without errors
         */
        // Test implementation
    });
    
    test('render error displayed for invalid LaTeX', () => {
        /**
         * What we are testing: Error message shown when KaTeX fails
         * Why we are testing: Users need feedback on invalid formulas
         * Expected Result: Error message displayed in preview area
         */
        // Test implementation
    });
});
```

### Security Tests

#### Test File: `tests/test_security_phase2.py`

```python
import pytest
from mathinput.widgets import MathInputWidget


@pytest.mark.security
def test_mode_config_injection_prevention():
    """
    What we are testing: Widget prevents injection via mode parameter
    Why we are testing: Security - prevent code injection through mode selection
    Expected Result: Invalid mode values are rejected or sanitized
    """
    # Test implementation
    pass


@pytest.mark.security
def test_preset_config_injection_prevention():
    """
    What we are testing: Widget prevents injection via preset parameter
    Why we are testing: Security - prevent code injection through preset selection
    Expected Result: Invalid preset values are rejected or sanitized
    """
    # Test implementation
    pass
```

### User Story Tests

#### Test File: `tests/test_user_stories_phase2.py`

```python
import pytest
from django import forms
from mathinput.widgets import MathInputWidget


@pytest.mark.user_story
@pytest.mark.us_07  # US-07: Switch Input Modes
def test_widget_switches_modes():
    """
    What we are testing: Widget correctly switches between input modes
    Why we are testing: US-07 - Users need different UI for different math types
    Expected Result: Toolbar layout changes when mode changes
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_08  # US-08: Use Domain Presets
def test_widget_applies_preset():
    """
    What we are testing: Widget correctly applies domain presets
    Why we are testing: US-08 - Users need domain-specific tool configurations
    Expected Result: Quick inserts and tab order match preset configuration
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_01  # US-01: Insert Fraction
def test_fraction_button_inserts_template():
    """
    What we are testing: Fraction button inserts fraction template
    Why we are testing: US-01 - Core user story for inserting fractions
    Expected Result: Clicking fraction button inserts \frac{}{} template
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_02  # US-02: Insert Integral
def test_integral_button_inserts_template():
    """
    What we are testing: Integral button inserts integral template
    Why we are testing: US-02 - Core user story for inserting integrals
    Expected Result: Clicking integral button inserts \int_{}^{} template
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_03  # US-03: Insert Matrix
def test_matrix_button_opens_dialog():
    """
    What we are testing: Matrix button opens matrix creation dialog
    Why we are testing: US-03 - Core user story for creating matrices
    Expected Result: Clicking matrix button opens dialog for dimensions
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_07
def test_mode_switch_preserves_formula():
    """
    What we are testing: Switching modes preserves current formula
    Why we are testing: US-07 - Users should not lose work when switching modes
    Expected Result: Formula remains intact when mode changes
    """
    # Test implementation
    pass
```

---

## Phase 2 Completion Criteria

- [ ] All 6 mode modules implemented
- [ ] All 6 preset modules implemented
- [ ] All 7 toolbar templates created
- [ ] AST engine fully functional
- [ ] LaTeX parser working (LaTeX → AST)
- [ ] AST to LaTeX converter working (AST → LaTeX)
- [ ] Visual builder renders AST
- [ ] Button click handlers functional
- [ ] Preview rendering with KaTeX working
- [ ] Hidden field sync working
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] All frontend tests passing
- [ ] All security tests passing
- [ ] All user story tests passing
- [ ] Code review completed
- [ ] Documentation updated

---

## Phase 2 Manual Testing Checklist

### Mode System Testing

**Test 2.1: Mode Loading**
- [ ] Load each of the 6 modes programmatically
- [ ] Verify mode configuration structure is valid
- [ ] Verify each mode has required keys (name, code, toolbars, etc.)
- **Expected Result:** All modes load correctly with valid structure

**Test 2.2: Mode Toolbar Visibility**
- [ ] Set widget to `regular_functions` mode
- [ ] Verify only Text, Basic, Trig toolbars visible
- [ ] Set widget to `integrals_differentials` mode
- [ ] Verify Calculus toolbar prominently displayed
- **Expected Result:** Toolbar visibility matches mode configuration

**Test 2.3: Mode Button Layout**
- [ ] Switch between different modes
- [ ] Verify button sizes change appropriately
- [ ] Verify button grouping changes
- **Expected Result:** Button layout adapts to mode

### Preset System Testing

**Test 2.4: Preset Loading**
- [ ] Load each of the 6 presets programmatically
- [ ] Verify preset configuration structure is valid
- [ ] Verify each preset has required keys
- **Expected Result:** All presets load correctly

**Test 2.5: Preset Tab Order**
- [ ] Set widget with `calculus` preset
- [ ] Verify tab order: Text → Calc → Basic
- [ ] Set widget with `machine_learning` preset
- [ ] Verify tab order: Text → Mat → Adv
- **Expected Result:** Tab order matches preset configuration

**Test 2.6: Preset Quick Inserts**
- [ ] Set widget with `calculus` preset
- [ ] Verify quick insert shows calculus templates
- [ ] Set widget with `machine_learning` preset
- [ ] Verify quick insert shows ML templates
- **Expected Result:** Quick inserts match preset configuration

### Toolbar Testing

**Test 2.7: Toolbar Rendering**
- [ ] Render widget with all 7 toolbars
- [ ] Verify each toolbar renders correctly
- [ ] Verify toolbar buttons are visible
- [ ] Check toolbar HTML structure
- **Expected Result:** All toolbars render with proper structure

**Test 2.8: Toolbar Button Icons**
- [ ] Check each toolbar for icon buttons
- [ ] Verify icons are visible (not broken images)
- [ ] Verify icons are appropriate (∫ for integral, √ for root, etc.)
- **Expected Result:** All buttons show correct visual icons

**Test 2.9: Toolbar Accessibility**
- [ ] Check each button has `aria-label` attribute
- [ ] Check toolbar has `role="toolbar"` attribute
- [ ] Test with screen reader (if available)
- **Expected Result:** All toolbars accessible

### Visual Builder Testing

**Test 2.10: AST Creation**
- [ ] Click fraction button
- [ ] Verify AST structure created
- [ ] Check AST has fraction node with placeholders
- **Expected Result:** AST correctly represents formula structure

**Test 2.11: Visual Builder Rendering**
- [ ] Insert fraction template
- [ ] Verify visual builder shows fraction structure
- [ ] Verify placeholders are visible (□/□)
- [ ] Verify placeholders are clickable
- **Expected Result:** Visual builder renders AST correctly

**Test 2.12: LaTeX Parsing**
- [ ] Enter LaTeX in source mode: `\frac{1}{2}`
- [ ] Verify LaTeX parsed into AST
- [ ] Verify AST structure is correct
- **Expected Result:** LaTeX correctly parsed to AST

**Test 2.13: AST to LaTeX Conversion**
- [ ] Build formula in visual builder
- [ ] Verify hidden field contains LaTeX
- [ ] Verify LaTeX matches visual structure
- **Expected Result:** AST correctly converts to LaTeX

### Button Click Testing

**Test 2.14: Fraction Button**
- [ ] Click fraction button (/) in Basic toolbar
- [ ] Verify `\frac{}{}` template inserted
- [ ] Verify cursor in numerator placeholder
- [ ] Verify preview shows fraction structure
- **Expected Result:** Fraction button inserts template correctly

**Test 2.15: Integral Button**
- [ ] Switch to Calculus toolbar
- [ ] Click integral button (∫)
- [ ] Verify `\int_{}^{}` template inserted
- [ ] Verify placeholders for limits and integrand
- **Expected Result:** Integral button inserts template correctly

**Test 2.16: Square Button**
- [ ] Click square button (x²)
- [ ] Verify `^{2}` inserted
- [ ] Type "x" before clicking
- [ ] Verify "x²" created
- **Expected Result:** Square button inserts power correctly

**Test 2.17: Root Button**
- [ ] Click square root button (√)
- [ ] Verify `\sqrt{}` template inserted
- [ ] Verify placeholder for radicand
- **Expected Result:** Root button inserts template correctly

### Preview Rendering Testing

**Test 2.18: KaTeX Preview**
- [ ] Enter simple formula: `x^2 + 1`
- [ ] Verify preview renders correctly
- [ ] Verify preview updates in real-time
- **Expected Result:** Preview shows rendered formula

**Test 2.19: Preview Error Handling**
- [ ] Enter invalid LaTeX: `\frac{1}` (missing closing brace)
- [ ] Verify error message shown in preview
- [ ] Verify error is clear and helpful
- **Expected Result:** Preview shows error for invalid LaTeX

**Test 2.20: Preview Update Performance**
- [ ] Type formula quickly
- [ ] Verify preview updates smoothly
- [ ] Check preview update delay (should be debounced)
- **Expected Result:** Preview updates within 100ms (after debounce)

### Mode + Preset Combination Testing

**Test 2.21: Mode and Preset Together**
- [ ] Set mode to `integrals_differentials`
- [ ] Set preset to `calculus`
- [ ] Verify calculus toolbar visible (from mode)
- [ ] Verify calculus quick inserts available (from preset)
- **Expected Result:** Mode and preset work together correctly

**Test 2.22: Mode Switch Preserves Formula**
- [ ] Create formula in `regular_functions` mode
- [ ] Switch to `integrals_differentials` mode
- [ ] Verify formula still visible and editable
- **Expected Result:** Formula preserved when switching modes

### Placeholder Navigation Testing

**Test 2.23: Placeholder Tab Navigation**
- [ ] Insert fraction template
- [ ] Press Tab key
- [ ] Verify cursor moves to denominator
- [ ] Press Shift+Tab
- [ ] Verify cursor moves back to numerator
- **Expected Result:** Tab navigation works between placeholders

**Test 2.24: Placeholder Click Navigation**
- [ ] Insert fraction template
- [ ] Click on denominator placeholder
- [ ] Verify cursor moves to denominator
- [ ] Type in denominator
- **Expected Result:** Click navigation works correctly

---

## Notes

- Frontend tests require JavaScript testing framework (Jest recommended)
- AST engine is critical - ensure thorough testing
- Mode and preset systems must be flexible for future extensions
- Toolbar templates must be accessible (ARIA labels required)
- **Manual Testing:** Complete all manual tests in checklist before marking phase complete

