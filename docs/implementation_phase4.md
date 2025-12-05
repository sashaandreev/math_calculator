# Implementation Plan - Phase 4: Polish & Integration

## Overview
Phase 4 adds polish and integration features: mobile responsiveness, accessibility, template tags, Django Admin integration, and renderer fallback.

## Tasks

### ✅Task 14: Mobile Responsive + Touch Testing
**Owner:** UI Dev  
**Duration:** 3 days  
**Dependencies:** Task 7, Task 9

**Features:**
- Responsive design: adapts to mobile, tablet, and desktop
- Touch-optimized: 48×48px minimum touch targets
- Horizontal scrolling: toolbar scrolls on mobile
- Collapsible preview: saves screen space on mobile
- Swipe gestures: swipe to switch tabs
- Performance: passive event listeners, touch optimizations

**Implementation:**
- Responsive CSS in `django-mathinput/mathinput/static/mathinput/css/mathinput.css`:
  ```css
  /* Desktop layout */
  .mi-widget {
      display: grid;
      grid-template-columns: 1fr 1fr; /* Builder | Preview */
  }
  
  /* Mobile layout */
  @media (max-width: 768px) {
      .mi-widget {
          grid-template-columns: 1fr;
          grid-template-rows: auto auto;
      }
      
      .mi-toolbar {
          overflow-x: auto;
          -webkit-overflow-scrolling: touch;
      }
      
      .mi-button {
          min-width: 48px;
          min-height: 48px;
      }
      
      .mi-preview {
          max-height: 200px;
          overflow-y: auto;
      }
  }
  ```

- Touch-optimized interactions:
  - Swipe gestures for tab switching
  - Bottom sheet for matrix builder
  - Collapsible preview area
  - Larger touch targets (48×48px minimum)

**Deliverables:**
- Responsive CSS
- Mobile-optimized layouts
- Touch gesture support
- Mobile testing completed

---

### ✅Task 15: Accessibility (ARIA, Keyboard)
**Owner:** A11y Dev  
**Duration:** 3 days  
**Dependencies:** Task 7, Task 9

**Features:**
- Full keyboard navigation: all features accessible via keyboard
- Screen reader support: ARIA labels and live regions
- Focus indicators: visible on all interactive elements
- WCAG 2.1 AA compliance: keyboard navigation, focus indicators, ARIA labels
- Logical tab order: focus moves through elements in a logical sequence

**Keyboard shortcuts:**
- Tab: Navigate forward through buttons/placeholders
- Shift+Tab: Navigate backward
- Enter/Space: Activate button
- Arrow Left/Right: Navigate placeholders horizontally
- Arrow Up/Down: Navigate placeholders vertically
- Home: Jump to first placeholder
- End: Jump to last placeholder
- Ctrl+M: Toggle Visual/Source mode

**Implementation:**
- ARIA labels and roles:
  ```html
  <div class="mi-toolbar" role="toolbar" aria-label="Basic operations">
      <button type="button" 
              class="mi-button"
              aria-label="Insert fraction"
              aria-describedby="fraction-help">
          /
      </button>
      <span id="fraction-help" class="sr-only">
          Inserts fraction template. Use Tab to navigate placeholders.
      </span>
  </div>
  
  <div class="mi-preview" 
       role="region" 
       aria-live="polite"
       aria-label="Formula preview">
      <!-- Rendered formula -->
  </div>
  ```

- Keyboard navigation:
  ```javascript
  function setupKeyboardNavigation() {
      // Tab navigation through buttons
      document.addEventListener('keydown', (e) => {
          if (e.key === 'Tab') {
              // Handle tab navigation
          }
          if (e.key === 'Enter' && e.target.classList.contains('mi-button')) {
              // Activate button
          }
          if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
              // Navigate visual builder
          }
      });
  }
  ```

- Focus management
- Screen reader announcements

**Deliverables:**
- ARIA labels on all interactive elements
- Full keyboard navigation
- Screen reader support
- Focus indicators
- WCAG 2.1 AA compliance

---

### ✅Task 16: Template Tags (as_mathinput, render_math)
**Owner:** Lead Dev  
**Duration:** 2 days  
**Dependencies:** Task 2

**as_mathinput template filter**
Purpose: Render a field value as a MathInput widget in templates.
Usage:
```
{% load mathinput_tags %}

{# Basic usage #}
{{ form.equation|as_mathinput }}

{# With mode shorthand #}
{{ form.equation|as_mathinput:"integrals_differentials" }}

{# With mode and preset #}
{{ form.equation|as_mathinput:"mode=integrals_differentials,preset=calculus" }}
```

***Features:***
- Parses mode and preset from argument string
- Supports shorthand (just mode name) or key=value format
- Creates MathInputWidget with specified mode/preset
- Returns safe HTML

**render_math template filter**
Purpose: Render stored LaTeX/MathML formulas for display.
Usage:
```
{% load mathinput_tags %}

{# Basic usage (uses default renderer from settings) #}
{{ formula|render_math }}

{# With specific renderer #}
{{ formula|render_math:"katex" }}
{{ formula|render_math:"mathjax" }}
```

***Features:***
- Auto-detects format (LaTeX vs MathML)
- Supports KaTeX and MathJax renderers
- Removes dollar signs if present
- Escapes HTML for safe output
- Handles empty values gracefully
- Returns safe HTML

**render_math_inline template filter**
Purpose: Render LaTeX as inline math (bonus feature).
Usage:
```
{% load mathinput_tags %}

{{ formula|render_math_inline }}
```

***Features:***
Renders as inline math (KaTeX inline or MathJax \(...\))
Same renderer support as render_math
Safe HTML output

**Usage example**
```
{% load mathinput_tags %}

{# Render widget in form #}
{{ form.equation|as_mathinput }}

{# Render widget with specific mode #}
{{ form.calculus_problem|as_mathinput:"mode=integrals_differentials,preset=calculus" }}

{# Display stored formula #}
{{ problem.equation|render_math }}

{# Display inline formula #}
The formula \({{ formula|render_math_inline }}\) is important.
```

**Implementation:**
- Create `django-mathinput/mathinput/templatetags/mathinput_tags.py`:
  ```python
  from django import template
  from mathinput.widgets import MathInputWidget
  
  register = template.Library()
  
  @register.filter(name='as_mathinput')
  def as_mathinput(value, mode=None, preset=None):
      """
      Template filter to render field as math input widget
      Usage: {{ form.equation|as_mathinput mode="integrals_differentials" }}
      """
      widget = MathInputWidget(mode=mode, preset=preset)
      return widget.render('field', value)
  
  @register.filter(name='render_math')
  def render_math(value, renderer=None):
      """
      Template filter to render stored LaTeX/MathML
      Usage: {{ formula|render_math }}
      """
      renderer = renderer or settings.MATHINPUT_RENDERER
      # Detect format (LaTeX vs MathML)
      # Render using KaTeX or MathJax
      # Return safe HTML
      pass
  ```

**Deliverables:**
- `as_mathinput` template filter
- `render_math` template filter
- Format auto-detection
- Safe HTML output

---

### ✅Task 17: Django Admin Integration
**Owner:** Lead Dev  
**Duration:** 2 days  
**Dependencies:** Task 2, Task 16

**Usage examples:**

1. Method 1: Using MathInputAdminMixin

```python
from mathinput.admin import MathInputAdminMixin
from django.contrib import admin

@admin.register(Problem)
class ProblemAdmin(MathInputAdminMixin, admin.ModelAdmin):
    mathinput_fields = {
        'equation': {'mode': 'regular_functions'},
        'calculus_problem': {'mode': 'integrals_differentials', 'preset': 'calculus'},
    }
```

2. Method 2: Using register_mathinput_admin

```python
from mathinput.admin import register_mathinput_admin

register_mathinput_admin(
    Problem,
    equation={'mode': 'regular_functions'},
    calculus_problem={'mode': 'integrals_differentials', 'preset': 'calculus'}
)
```

3. Method 3: Manual widget configuration

```python
from mathinput.admin import MathInputAdminForm, get_mathinput_widget_for_field

class ProblemAdmin(admin.ModelAdmin):
    form = MathInputAdminForm
    
    class Meta:
        widgets = get_mathinput_widget_for_field('equation', mode='matrices')
```

**Features:**
- Easy integration: Multiple ways to integrate with admin
- Automatic configuration: Mixin handles widget setup
- Flexible: Supports all widget modes and presets
- Admin-compatible: CSS ensures proper styling in admin
- Tested: Full test coverage for admin integration

**Implementation:**
- Admin widget registration:
  ```python
  # django-mathinput/mathinput/admin.py
  from django.contrib import admin
  from django import forms
  from .widgets import MathInputWidget
  
  class MathInputAdminForm(forms.ModelForm):
      class Meta:
          widgets = {
              'equation': MathInputWidget(mode='regular_functions'),
          }
  ```

- Admin list display customization:
  ```python
  @admin.register(Problem)
  class ProblemAdmin(admin.ModelAdmin):
      list_display = ('title', 'equation_preview', 'created')
      
      def equation_preview(self, obj):
          # Show truncated LaTeX or rendered preview
          return truncatewords(obj.equation, 10)
      equation_preview.short_description = 'Equation'
  ```

**Deliverables:**
- Widget works in Django Admin
- Admin list view shows formula preview
- Admin detail view shows full widget
- Admin CSS compatibility

---

### Task 18: KaTeX Extensions + MathJax Fallback
**Owner:** Frontend Dev  
**Duration:** 2 days  
**Dependencies:** Task 9

**Implementation:**
- KaTeX extensions loading:
  ```javascript
  function loadKaTeXExtensions(extensions) {
      extensions.forEach(ext => {
          const script = document.createElement('script');
          script.src = `https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/${ext}.min.js`;
          script.integrity = getSRIHash(ext); // SRI hash
          document.head.appendChild(script);
      });
  }
  ```

- MathJax fallback:
  ```javascript
  function initializeRenderer(rendererType) {
      if (rendererType === 'mathjax') {
          loadMathJax();
      } else {
          loadKaTeX();
          if (settings.katex_extensions) {
              loadKaTeXExtensions(settings.katex_extensions);
          }
      }
  }
  
  function loadMathJax() {
      const script = document.createElement('script');
      script.src = settings.mathjax_cdn;
      script.integrity = getSRIHash('mathjax');
      script.onerror = () => {
          console.warn('MathJax failed to load, falling back to KaTeX');
          loadKaTeX();
      };
      document.head.appendChild(script);
  }
  ```

- SRI (Subresource Integrity) hashes
- Error handling and fallback

**Deliverables:**
- KaTeX extensions support
- MathJax fallback mechanism
- SRI hash validation
- Error handling

---

## Phase 4 Testing Requirements

### Unit Tests

#### Test File: `tests/test_template_tags.py`

```python
import pytest
from django.template import Context, Template
from mathinput.templatetags.mathinput_tags import as_mathinput, render_math


@pytest.mark.unit
def test_as_mathinput_filter_renders_widget():
    """
    What we are testing: as_mathinput filter renders MathInputWidget
    Why we are testing: Template filter is primary integration point
    Expected Result: Filter returns widget HTML
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_as_mathinput_with_mode_parameter():
    """
    What we are testing: as_mathinput filter accepts mode parameter
    Why we are testing: Users need to specify modes in templates
    Expected Result: Widget rendered with specified mode
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_render_math_renders_latex():
    """
    What we are testing: render_math filter renders LaTeX to HTML
    Why we are testing: Display filter is core feature
    Expected Result: LaTeX string converted to rendered HTML
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_render_math_auto_detects_format():
    """
    What we are testing: render_math auto-detects LaTeX vs MathML
    Why we are testing: Support multiple storage formats
    Expected Result: Correct renderer used based on format
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_render_math_handles_invalid_input():
    """
    What we are testing: render_math handles invalid LaTeX gracefully
    Why we are testing: Users may have invalid stored formulas
    Expected Result: Error message shown instead of breaking
    """
    # Test implementation
    pass
```

### Integration Tests

#### Test File: `tests/test_integration_phase4.py`

```python
import pytest
from django.test import TestCase, Client
from django.contrib import admin
from django.contrib.auth.models import User


@pytest.mark.integration
class TestTemplateTagIntegration(TestCase):
    """
    What we are testing: Template tags work in real Django templates
    Why we are testing: Template tags must integrate with Django template system
    Expected Result: Tags render correctly in template context
    """
    
    def test_as_mathinput_in_template():
        """
        What we are testing: as_mathinput filter works in Django template
        Why we are testing: Primary usage pattern for widget
        Expected Result: Template renders widget HTML correctly
        """
        # Test implementation
        pass
    
    def test_render_math_in_template():
        """
        What we are testing: render_math filter works in Django template
        Why we are testing: Display stored formulas in templates
        Expected Result: Template renders formula correctly
        """
        # Test implementation
        pass


@pytest.mark.integration
class TestDjangoAdminIntegration(TestCase):
    """
    What we are testing: Widget works in Django Admin interface
    Why we are testing: Admin integration is required feature
    Expected Result: Widget renders and functions in admin
    """
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@test.com', password='testpass'
        )
        self.client = Client()
        self.client.login(username='admin', password='testpass')
    
    def test_widget_renders_in_admin():
        """
        What we are testing: Widget renders correctly in admin form
        Why we are testing: Admin users need to edit formulas
        Expected Result: Widget HTML present in admin form
        """
        # Test implementation
        pass
    
    def test_admin_list_shows_preview():
        """
        What we are testing: Admin list view shows formula preview
        Why we are testing: Admins need to see formulas in list
        Expected Result: List view shows truncated/preview of formula
        """
        # Test implementation
        pass
    
    def test_admin_saves_formula():
        """
        What we are testing: Admin can save formula via widget
        Why we are testing: Admin must be able to create/edit formulas
        Expected Result: Formula saved correctly through admin
        """
        # Test implementation
        pass
```

### Frontend Tests

#### Test File: `tests/test_frontend_phase4.js`

```javascript
describe('Mobile Responsiveness', () => {
    test('toolbar scrolls horizontally on mobile', () => {
        /**
         * What we are testing: Toolbar is horizontally scrollable on small screens
         * Why we are testing: Mobile users need access to all buttons
         * Expected Result: Toolbar scrolls horizontally when buttons overflow
         */
        // Test implementation
    });
    
    test('preview collapses on mobile', () => {
        /**
         * What we are testing: Preview area is collapsible on mobile
         * Why we are testing: Save screen space on small devices
         * Expected Result: Preview can be expanded/collapsed via tap
         */
        // Test implementation
    });
    
    test('buttons are touch-optimized size', () => {
        /**
         * What we are testing: Buttons meet minimum touch target size (48×48px)
         * Why we are testing: WCAG requirement for touch targets
         * Expected Result: All buttons are at least 48×48px on mobile
         */
        // Test implementation
    });
});

describe('Accessibility', () => {
    test('all buttons have ARIA labels', () => {
        /**
         * What we are testing: All interactive buttons have ARIA labels
         * Why we are testing: Screen reader accessibility requirement
         * Expected Result: Every button has aria-label attribute
         */
        // Test implementation
    });
    
    test('keyboard navigation works', () => {
        /**
         * What we are testing: Full keyboard navigation through widget
         * Why we are testing: WCAG requirement for keyboard accessibility
         * Expected Result: All features accessible via keyboard only
         */
        // Test implementation
    });
    
    test('focus indicators visible', () => {
        /**
         * What we are testing: Focus indicators visible on all interactive elements
         * Why we are testing: Users need to see keyboard focus
         * Expected Result: Focused elements have visible focus indicator
         */
        // Test implementation
    });
    
    test('screen reader announcements work', () => {
        /**
         * What we are testing: Screen reader announces formula changes
         * Why we are testing: Accessibility for visually impaired users
         * Expected Result: aria-live region announces preview updates
         */
        // Test implementation
    });
});

describe('Renderer Fallback', () => {
    test('KaTeX loads with extensions', () => {
        /**
         * What we are testing: KaTeX loads with configured extensions
         * Why we are testing: Extensions provide additional functionality
         * Expected Result: Extensions loaded and functional
         */
        // Test implementation
    });
    
    test('MathJax fallback works', () => {
        /**
         * What we are testing: MathJax loads when configured as renderer
         * Why we are testing: Users may prefer MathJax over KaTeX
         * Expected Result: MathJax renders formulas correctly
         */
        // Test implementation
    });
    
    test('CDN failure falls back gracefully', () => {
        /**
         * What we are testing: Widget handles CDN failure gracefully
         * Why we are testing: Network issues should not break widget
         * Expected Result: Error message shown, widget still functional
         */
        // Test implementation
    });
});
```

### Security Tests

#### Test File: `tests/test_security_phase4.py`

```python
import pytest
from django.test import TestCase
from mathinput.templatetags.mathinput_tags import render_math


@pytest.mark.security
def test_render_math_sanitizes_output():
    """
    What we are testing: render_math filter sanitizes output HTML
    Why we are testing: Security - prevent XSS in rendered output
    Expected Result: Output is safe HTML, no script tags
    """
    # Test implementation
    pass


@pytest.mark.security
def test_template_tags_escape_user_input():
    """
    What we are testing: Template tags properly escape user input
    Why we are testing: Security - prevent template injection
    Expected Result: User input is escaped in template output
    """
    # Test implementation
    pass


@pytest.mark.security
def test_admin_integration_requires_permissions():
    """
    What we are testing: Admin integration respects Django permissions
    Why we are testing: Security - prevent unauthorized access
    Expected Result: Only authorized users can access admin features
    """
    # Test implementation
    pass
```

### User Story Tests

#### Test File: `tests/test_user_stories_phase4.py`

```python
import pytest
from django.test import TestCase


@pytest.mark.user_story
@pytest.mark.us_13  # US-13: Use on Mobile Device
def test_mobile_toolbar_scrollable():
    """
    What we are testing: Toolbar is horizontally scrollable on mobile
    Why we are testing: US-13 - Mobile users need access to all buttons
    Expected Result: Toolbar scrolls horizontally on small screens
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_13
def test_mobile_touch_targets_adequate():
    """
    What we are testing: Buttons meet minimum touch target size on mobile
    Why we are testing: US-13 - Mobile usability requirement
    Expected Result: All buttons are at least 48×48px on mobile
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_14  # US-14: Navigate with Keyboard Only
def test_keyboard_navigation_complete():
    """
    What we are testing: All features accessible via keyboard only
    Why we are testing: US-14 - Keyboard-only navigation requirement
    Expected Result: All buttons and features accessible without mouse
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_14
def test_focus_indicators_visible():
    """
    What we are testing: Focus indicators visible on all interactive elements
    Why we are testing: US-14 - Users need to see keyboard focus
    Expected Result: Focused elements have visible focus indicator
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_16  # US-16: Display Stored Formulas
def test_render_math_displays_formula():
    """
    What we are testing: render_math filter displays stored formulas
    Why we are testing: US-16 - Core display functionality
    Expected Result: Stored LaTeX rendered correctly in templates
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_16
def test_render_math_handles_errors():
    """
    What we are testing: render_math handles invalid formulas gracefully
    Why we are testing: US-16 - Users may have invalid stored formulas
    Expected Result: Error message shown instead of breaking page
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_15  # US-15: Django Admin Compatible
def test_widget_works_in_admin():
    """
    What we are testing: Widget functions correctly in Django Admin
    Why we are testing: US-15 - Admin integration requirement
    Expected Result: Widget renders and saves in admin interface
    """
    # Test implementation
    pass
```

---

## Phase 4 Completion Criteria

- [ ] Mobile responsive design implemented
- [ ] Touch-optimized interactions working
- [ ] Full keyboard navigation functional
- [ ] ARIA labels on all elements
- [ ] Screen reader support working
- [ ] WCAG 2.1 AA compliance verified
- [ ] Template tags implemented and tested
- [ ] Django Admin integration working
- [ ] KaTeX extensions support
- [ ] MathJax fallback mechanism
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] All frontend tests passing
- [ ] All security tests passing
- [ ] All user story tests passing
- [ ] Accessibility audit completed
- [ ] Mobile testing completed
- [ ] Code review completed
- [ ] Documentation updated

---

## Phase 4 Manual Testing Checklist

### Mobile Responsiveness Testing

**Test 4.1: Mobile Layout**
- [ ] Open widget on mobile device (or browser dev tools mobile view)
- [ ] Verify layout adapts to small screen
- [ ] Verify toolbar and preview stack vertically
- [ ] Verify no horizontal scrolling of main container
- **Expected Result:** Layout responsive on mobile

**Test 4.2: Toolbar Horizontal Scroll**
- [ ] On mobile, verify toolbar scrolls horizontally
- [ ] Swipe left/right on toolbar
- [ ] Verify all buttons accessible via scroll
- [ ] Verify scroll is smooth
- **Expected Result:** Toolbar scrolls horizontally on mobile

**Test 4.3: Touch Target Sizes**
- [ ] On mobile, measure button sizes
- [ ] Verify buttons are at least 48×48px
- [ ] Verify buttons are easy to tap
- [ ] Verify no mis-clicks due to small targets
- **Expected Result:** All buttons meet touch target requirements

**Test 4.4: Preview Collapsible**
- [ ] On mobile, verify preview can be collapsed
- [ ] Tap to collapse preview
- [ ] Verify more screen space for builder
- [ ] Tap to expand preview
- [ ] Verify preview shows again
- **Expected Result:** Preview collapsible on mobile

**Test 4.5: Matrix Builder Bottom Sheet**
- [ ] On mobile, click matrix button
- [ ] Verify matrix builder opens as bottom sheet
- [ ] Verify sheet is easy to interact with
- [ ] Verify sheet can be dismissed
- **Expected Result:** Matrix builder uses mobile-friendly UI

**Test 4.6: Swipe Gestures**
- [ ] On mobile, swipe left/right on toolbar tabs
- [ ] Verify tabs switch via swipe
- [ ] Verify swipe is responsive
- **Expected Result:** Swipe gestures work for tab switching

### Accessibility Testing

**Test 4.7: Keyboard Navigation**
- [ ] Tab through all toolbar buttons
- [ ] Verify focus moves logically
- [ ] Press Enter on focused button
- [ ] Verify button activates
- **Expected Result:** Full keyboard navigation works

**Test 4.8: Arrow Key Navigation**
- [ ] In visual builder, use arrow keys
- [ ] Verify cursor moves between elements
- [ ] Verify focus visible on active element
- **Expected Result:** Arrow keys navigate visual builder

**Test 4.9: Tab Key Navigation**
- [ ] Insert fraction template
- [ ] Press Tab
- [ ] Verify cursor moves to next placeholder
- [ ] Press Shift+Tab
- [ ] Verify cursor moves to previous placeholder
- **Expected Result:** Tab navigation works between placeholders

**Test 4.10: Screen Reader Testing**
- [ ] Enable screen reader (NVDA/JAWS/VoiceOver)
- [ ] Navigate widget with screen reader
- [ ] Verify buttons announced correctly
- [ ] Verify preview updates announced
- **Expected Result:** Screen reader can navigate and understand widget

**Test 4.11: ARIA Labels**
- [ ] Inspect widget HTML
- [ ] Verify all buttons have `aria-label`
- [ ] Verify toolbars have `role="toolbar"`
- [ ] Verify preview has `aria-live="polite"`
- **Expected Result:** All ARIA attributes present and correct

**Test 4.12: Focus Indicators**
- [ ] Tab through widget
- [ ] Verify focus indicator visible on each element
- [ ] Verify focus indicator is clear and visible
- [ ] Test with high contrast mode
- **Expected Result:** Focus indicators visible and clear

**Test 4.13: Color Contrast**
- [ ] Check text color contrast
- [ ] Check button color contrast
- [ ] Verify WCAG AA contrast ratios met
- [ ] Test with color blindness simulators
- **Expected Result:** All text meets contrast requirements

### Template Tags Testing

**Test 4.14: as_mathinput Filter**
- [ ] Use `{{ form.equation|as_mathinput }}` in template
- [ ] Render template
- [ ] Verify widget appears
- [ ] Verify widget is functional
- **Expected Result:** Template filter renders widget

**Test 4.15: as_mathinput with Mode**
- [ ] Use `{{ form.equation|as_mathinput mode="integrals_differentials" }}`
- [ ] Verify widget uses specified mode
- [ ] Verify toolbar matches mode
- **Expected Result:** Mode parameter works in template

**Test 4.16: render_math Filter**
- [ ] Store formula in database: `\int x dx`
- [ ] Use `{{ formula|render_math }}` in template
- [ ] Verify formula renders correctly
- [ ] Verify no errors
- **Expected Result:** Stored formula renders correctly

**Test 4.17: render_math with Invalid Formula**
- [ ] Store invalid formula: `\frac{1}` (missing brace)
- [ ] Use `{{ formula|render_math }}` in template
- [ ] Verify error message shown (not page break)
- **Expected Result:** Invalid formulas handled gracefully

**Test 4.18: render_math Format Detection**
- [ ] Store LaTeX: `x^2 + 1`
- [ ] Store MathML: `<math>...</math>`
- [ ] Verify render_math detects format correctly
- [ ] Verify correct renderer used
- **Expected Result:** Format auto-detection works

### Django Admin Testing

**Test 4.19: Widget in Admin Form**
- [ ] Open Django Admin
- [ ] Navigate to model with math field
- [ ] Click "Add" or "Change"
- [ ] Verify widget appears in admin form
- [ ] Verify widget is functional
- **Expected Result:** Widget works in admin

**Test 4.20: Admin List View**
- [ ] View admin list for model with math field
- [ ] Verify formula preview shown (truncated)
- [ ] Verify preview is readable
- [ ] Click "View" link if available
- **Expected Result:** Admin list shows formula preview

**Test 4.21: Admin Save Functionality**
- [ ] In admin, create new record
- [ ] Enter formula in widget
- [ ] Click Save
- [ ] Verify formula saved
- [ ] Edit record
- [ ] Verify formula loads correctly
- **Expected Result:** Admin save/load works correctly

**Test 4.22: Admin CSS Compatibility**
- [ ] Check widget appearance in admin
- [ ] Verify no CSS conflicts
- [ ] Verify widget styled correctly
- [ ] Test with different admin themes
- **Expected Result:** Widget looks good in admin

### Renderer Testing

**Test 4.23: KaTeX Rendering**
- [ ] Set renderer to 'katex'
- [ ] Enter formula: `\frac{1}{2}`
- [ ] Verify KaTeX renders correctly
- [ ] Verify rendering is fast
- **Expected Result:** KaTeX renders formulas correctly

**Test 4.24: KaTeX Extensions**
- [ ] Enable extensions: ['cancel', 'copy-tex']
- [ ] Use cancel command: `\cancel{x}`
- [ ] Verify extension works
- **Expected Result:** KaTeX extensions load and work

**Test 4.25: MathJax Fallback**
- [ ] Set renderer to 'mathjax'
- [ ] Enter formula: `\int x dx`
- [ ] Verify MathJax loads
- [ ] Verify MathJax renders correctly
- **Expected Result:** MathJax works as alternative renderer

**Test 4.26: CDN Failure Handling**
- [ ] Simulate CDN failure (block CDN in dev tools)
- [ ] Load widget
- [ ] Verify fallback mechanism works
- [ ] Verify error message shown if no fallback
- **Expected Result:** CDN failure handled gracefully

**Test 4.27: SRI Hash Validation**
- [ ] Check script tags for integrity attributes
- [ ] Verify SRI hashes present
- [ ] Verify hashes are correct
- **Expected Result:** SRI hashes protect against CDN compromise

### Cross-Browser Testing

**Test 4.28: Chrome Compatibility**
- [ ] Test widget in Chrome (latest 2 versions)
- [ ] Verify all features work
- [ ] Verify no console errors
- **Expected Result:** Widget works in Chrome

**Test 4.29: Firefox Compatibility**
- [ ] Test widget in Firefox (latest 2 versions)
- [ ] Verify all features work
- [ ] Verify no console errors
- **Expected Result:** Widget works in Firefox

**Test 4.30: Safari Compatibility**
- [ ] Test widget in Safari (latest 2 versions)
- [ ] Verify all features work
- [ ] Verify no console errors
- **Expected Result:** Widget works in Safari

**Test 4.31: Edge Compatibility**
- [ ] Test widget in Edge (latest 2 versions)
- [ ] Verify all features work
- [ ] Verify no console errors
- **Expected Result:** Widget works in Edge

---

## Notes

- Accessibility is critical - ensure WCAG 2.1 AA compliance
- Mobile testing on real devices recommended
- Template tags must be safe (auto-escaping)
- Admin integration should be seamless
- **Manual Testing:** Complete all manual tests in checklist before marking phase complete

