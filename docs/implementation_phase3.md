# Implementation Plan - Phase 3: User Interface

## Overview
Phase 3 implements the user interface features: Quick Insert dropdown, text formatting, mode switching UI, and source mode with bidirectional sync.

## Tasks

### ✅Task 10: Quick Insert Dropdown
**Owner:** UI Dev  
**Duration:** 2 days  
**Dependencies:** Task 6, Task 7

**Features:**
- Click to open/close dropdown
- Click menu item to insert template
- Keyboard navigation in menu
- Auto-close after selection
- Template insertion updates visual builder, preview, and hidden field

**Implementation:**
- Create `django-mathinput/mathinput/templates/mathinput/quick_insert.html`:
  ```html
  <div class="mi-quick-insert">
      <button type="button" 
              class="mi-quick-insert-toggle"
              aria-label="Quick insert templates"
              aria-haspopup="true"
              aria-expanded="false">
          [Preset Name] Quick ▼
      </button>
      <ul class="mi-quick-insert-menu" role="menu" hidden>
          <li role="menuitem">
              <button type="button" 
                      class="mi-quick-insert-item"
                      data-template="\\int f(x) \\, dx">
                  Indefinite Integral
              </button>
          </li>
          <!-- More items from preset config -->
      </ul>
  </div>
  ```

- JavaScript functionality:
  ```javascript
  function initializeQuickInsert(presetConfig) {
      const menu = document.querySelector('.mi-quick-insert-menu');
      presetConfig.quick_inserts.forEach(item => {
          const button = createQuickInsertButton(item);
          menu.appendChild(button);
      });
  }
  
  function handleQuickInsertClick(template) {
      insertTemplate(template);
      updateVisualBuilder();
      updatePreview();
  }
  ```

**Deliverables:**
- Quick insert dropdown template
- JavaScript handlers
- Preset-based template loading
- Keyboard navigation support

---

### ✅Task 11: Text Formatting (Bold, Color, Size)
**Owner:** UI/JS Dev  
**Duration:** 3 days  
**Dependencies:** Task 7, Task 9

**Features:**
- Bold formatting: Wraps next input in \textbf{}
- Color formatting: Wraps next input in \textcolor{color}{}
- Size formatting: Wraps next input in size commands
- Quick color buttons: One-click color application
- Custom colors: Hex color picker support
- Dropdown menus: Color picker and size menu with auto-close

**Implementation:**
- Text formatting buttons in `toolbar_text.html`:
  ```html
  <button type="button" 
          class="mi-button mi-button-bold"
          data-action="format"
          data-format="bold"
          aria-label="Bold">
      <strong>B</strong>
  </button>
  <button type="button" 
          class="mi-button mi-button-color"
          data-action="format"
          data-format="color"
          aria-label="Text color">
      A
  </button>
  <button type="button" 
          class="mi-button mi-button-size"
          data-action="format"
          data-format="size"
          aria-label="Text size">
      Size
  </button>
  ```

- Formatting handlers:
  ```javascript
  function handleFormatButton(formatType) {
      const selection = getSelection();
      if (selection) {
          applyFormat(selection, formatType);
      } else {
          // Apply to next input
          setNextInputFormat(formatType);
      }
      updateVisualBuilder();
      updatePreview();
  }
  
  function applyFormat(selection, formatType) {
      switch(formatType) {
          case 'bold':
              wrapSelection('\\textbf{', '}');
              break;
          case 'color':
              showColorPicker(selection);
              break;
          case 'size':
              showSizePicker(selection);
              break;
      }
  }
  ```

- Color picker component
- Size dropdown component

**Deliverables:**
- Text formatting buttons
- Format application logic
- Color picker UI
- Size selector UI
- Format persistence in AST

---

### ✅Task 12: Mode Switching UI
**Owner:** UI Dev  
**Duration:** 2 days  
**Dependencies:** Task 5, Task 7

**Implementation:**
- Mode selector in widget template:
  ```html
  <div class="mi-mode-selector">
      <label for="mode-select">Input Mode:</label>
      <select id="mode-select" 
              class="mi-mode-select"
              aria-label="Select input mode">
          <option value="regular_functions">Regular Functions</option>
          <option value="advanced_expressions">Advanced Expressions</option>
          <option value="integrals_differentials">Integrals/Differentials</option>
          <option value="matrices">Matrices</option>
          <option value="statistics_probability">Statistics & Probability</option>
          <option value="physics_engineering">Physics & Engineering</option>
      </select>
  </div>
  ```

- Mode switching handler:
  ```javascript
  function handleModeChange(newMode) {
      // 1. Preserve current formula
      const currentLatex = getCurrentLatex();
      
      // 2. Load new mode config
      const modeConfig = loadModeConfig(newMode);
      
      // 3. Update toolbar visibility
      updateToolbarVisibility(modeConfig.toolbars);
      
      // 4. Update button layout
      updateButtonLayout(modeConfig.button_layout);
      
      // 5. Show warning if needed
      if (usesOperationsNotInMode(currentLatex, newMode)) {
          showModeWarning();
      }
      
      // 6. Re-render with new mode
      renderToolbars();
  }
  ```

**Deliverables:**
- Mode selector UI
- Mode switching logic
- Toolbar visibility updates
- Warning system for incompatible operations

**Features:**
- Mode switching: Dropdown to change input modes
- Toolbar visibility: Automatically shows/hides toolbars based on mode
- Formula preservation: Current formula is preserved when switching modes
- Warning system: Alerts users about incompatible operations
- Dynamic updates: Toolbars update immediately on mode change

---

### Task 13: Source Mode + Bidirectional Sync
**Owner:** Frontend Dev  
**Duration:** 4 days  
**Dependencies:** Task 9

**Implementation:**
- Source mode toggle in widget:
  ```html
  <div class="mi-mode-tabs">
      <button type="button" 
              class="mi-tab mi-tab-visual active"
              data-mode="visual"
              aria-label="Visual mode">
          Visual
      </button>
      <button type="button" 
              class="mi-tab mi-tab-source"
              data-mode="source"
              aria-label="Source mode">
          Source
      </button>
  </div>
  
  <div class="mi-visual-builder" data-mode="visual">
      <!-- Visual builder content -->
  </div>
  
  <div class="mi-source-editor" data-mode="source" hidden>
      <textarea class="mi-source-textarea"
                aria-label="LaTeX source code"></textarea>
  </div>
  ```

- Bidirectional sync:
  ```javascript
  class SyncManager {
      constructor(visualBuilder, sourceEditor) {
          this.visualBuilder = visualBuilder;
          this.sourceEditor = sourceEditor;
          this.syncing = false;
          this.lastEdit = {source: 'visual', timestamp: 0};
      }
      
      syncFromVisual() {
          if (this.syncing) return;
          this.syncing = true;
          
          const latex = this.visualBuilder.getLatex();
          this.sourceEditor.value = latex;
          
          this.lastEdit = {source: 'visual', timestamp: Date.now()};
          this.syncing = false;
      }
      
      syncFromSource() {
          if (this.syncing) return;
          this.syncing = true;
          
          const latex = this.sourceEditor.value;
          try {
              const ast = parseLatex(latex);
              this.visualBuilder.setAST(ast);
              this.visualBuilder.render();
          } catch (error) {
              showParseError(error);
          }
          
          this.lastEdit = {source: 'source', timestamp: Date.now()};
          this.syncing = false;
      }
  }
  
  // Debounced sync
  const debouncedSyncFromVisual = debounce(() => {
      syncManager.syncFromVisual();
  }, 300);
  
  const debouncedSyncFromSource = debounce(() => {
      syncManager.syncFromSource();
  }, 300);
  ```

- Keyboard shortcut (Ctrl+M) for mode toggle

**Deliverables:**
- Visual/Source mode tabs
- Source mode textarea
- Bidirectional sync system
- Conflict resolution (last edit wins)
- Sync indicators
- Keyboard shortcut support

---

## Phase 3 Testing Requirements

### Unit Tests

#### Test File: `tests/test_quick_insert.py`

```python
import pytest
from mathinput.presets import load_preset


@pytest.mark.unit
def test_quick_insert_templates_loaded():
    """
    What we are testing: Quick insert templates loaded from preset configuration
    Why we are testing: Quick insert must show preset-specific templates
    Expected Result: Templates list matches preset quick_inserts configuration
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_quick_insert_templates_valid_latex():
    """
    What we are testing: All quick insert templates are valid LaTeX
    Why we are testing: Templates must be insertable without errors
    Expected Result: All templates pass LaTeX validation
    """
    # Test implementation
    pass
```

#### Test File: `tests/test_text_formatting.py`

```python
import pytest


@pytest.mark.unit
def test_bold_format_applied():
    """
    What we are testing: Bold formatting correctly wraps text in \textbf{}
    Why we are testing: Text formatting is core feature for emphasis
    Expected Result: Selected text wrapped in \textbf{} command
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_color_format_applied():
    """
    What we are testing: Color formatting correctly applies \color{} command
    Why we are testing: Users need color formatting for visual emphasis
    Expected Result: Selected text wrapped in \color{hex} command
    """
    # Test implementation
    pass


@pytest.mark.unit
def test_size_format_applied():
    """
    What we are testing: Size formatting correctly applies size commands
    Why we are testing: Users need different text sizes in formulas
    Expected Result: Selected text wrapped in appropriate size command
    """
    # Test implementation
    pass
```

### Integration Tests

#### Test File: `tests/test_integration_phase3.py`

```python
import pytest
from django.test import TestCase


@pytest.mark.integration
class TestQuickInsertIntegration(TestCase):
    """
    What we are testing: Quick insert integrates with widget and preset system
    Why we are testing: Quick insert must work correctly in full widget context
    Expected Result: Clicking quick insert item inserts template into visual builder
    """
    
    def test_quick_insert_integrates_with_widget():
        """
        What we are testing: Quick insert dropdown works in widget
        Why we are testing: Feature must work in real widget context
        Expected Result: Quick insert menu appears, items insert correctly
        """
        # Test implementation
        pass


@pytest.mark.integration
class TestModeSwitchingIntegration(TestCase):
    """
    What we are testing: Mode switching integrates with widget and preserves formula
    Why we are testing: Mode switching must work without data loss
    Expected Result: Formula preserved, toolbar updated when mode changes
    """
    
    def test_mode_switch_preserves_formula():
        """
        What we are testing: Switching modes preserves current formula
        Why we are testing: Users should not lose work when changing modes
        Expected Result: Formula remains intact after mode switch
        """
        # Test implementation
        pass
```

### Frontend Tests

#### Test File: `tests/test_frontend_phase3.js`

```javascript
describe('Quick Insert', () => {
    test('quick insert dropdown opens', () => {
        /**
         * What we are testing: Quick insert dropdown opens on button click
         * Why we are testing: Users need access to template menu
         * Expected Result: Dropdown menu becomes visible
         */
        // Test implementation
    });
    
    test('quick insert item inserts template', () => {
        /**
         * What we are testing: Clicking quick insert item inserts LaTeX template
         * Why we are testing: Core functionality - inserting pre-made templates
         * Expected Result: Template inserted into visual builder at cursor
         */
        // Test implementation
    });
    
    test('quick insert closes after selection', () => {
        /**
         * What we are testing: Quick insert menu closes after item selection
         * Why we are testing: UI should close menus after action
         * Expected Result: Dropdown hidden after template insertion
         */
        // Test implementation
    });
});

describe('Text Formatting', () => {
    test('bold button applies bold format', () => {
        /**
         * What we are testing: Bold button wraps selection in \textbf{}
         * Why we are testing: Text formatting is user-requested feature
         * Expected Result: Selected text wrapped in \textbf{} command
         */
        // Test implementation
    });
    
    test('color picker applies color format', () => {
        /**
         * What we are testing: Color picker applies \color{} command
         * Why we are testing: Users need color formatting capability
         * Expected Result: Selected text wrapped in \color{hex} command
         */
        // Test implementation
    });
    
    test('format applies to selection', () => {
        /**
         * What we are testing: Formatting applies to selected text only
         * Why we are testing: Users need precise formatting control
         * Expected Result: Only selected portion formatted, rest unchanged
         */
        // Test implementation
    });
});

describe('Mode Switching', () => {
    test('mode switch updates toolbar visibility', () => {
        /**
         * What we are testing: Switching modes shows/hides appropriate toolbars
         * Why we are testing: Mode system must control UI layout
         * Expected Result: Toolbar visibility matches new mode configuration
         */
        // Test implementation
    });
    
    test('mode switch preserves formula', () => {
        /**
         * What we are testing: Formula remains intact when switching modes
         * Why we are testing: Users should not lose work when changing modes
         * Expected Result: Formula LaTeX unchanged after mode switch
         */
        // Test implementation
    });
});

describe('Source Mode Sync', () => {
    test('visual to source sync updates textarea', () => {
        /**
         * What we are testing: Changes in visual builder sync to source mode
         * Why we are testing: Bidirectional sync is core feature
         * Expected Result: Source textarea updated when visual builder changes
         */
        // Test implementation
    });
    
    test('source to visual sync updates builder', () => {
        /**
         * What we are testing: Changes in source mode sync to visual builder
         * Why we are testing: Users editing LaTeX directly need visual update
         * Expected Result: Visual builder updated when source textarea changes
         */
        // Test implementation
    });
    
    test('sync handles parse errors gracefully', () => {
        /**
         * What we are testing: Sync handles invalid LaTeX in source mode
         * Why we are testing: Users may type invalid LaTeX, should see errors
         * Expected Result: Error message shown, visual builder not corrupted
         */
        // Test implementation
    });
    
    test('sync debouncing prevents excessive updates', () => {
        /**
         * What we are testing: Sync debouncing reduces update frequency
         * Why we are testing: Performance - prevent excessive re-rendering
         * Expected Result: Updates debounced to 300ms intervals
         */
        // Test implementation
    });
    
    test('Ctrl+M toggles visual/source mode', () => {
        /**
         * What we are testing: Keyboard shortcut toggles between modes
         * Why we are testing: Keyboard navigation improves efficiency
         * Expected Result: Ctrl+M switches between visual and source modes
         */
        // Test implementation
    });
});
```

### Security Tests

#### Test File: `tests/test_security_phase3.py`

```python
import pytest


@pytest.mark.security
def test_quick_insert_templates_sanitized():
    """
    What we are testing: Quick insert templates are sanitized before insertion
    Why we are testing: Security - prevent injection via template system
    Expected Result: Templates do not contain dangerous commands
    """
    # Test implementation
    pass


@pytest.mark.security
def test_source_mode_input_sanitized():
    """
    What we are testing: Source mode input is sanitized before sync
    Why we are testing: Security - prevent XSS via direct LaTeX input
    Expected Result: Dangerous commands removed from source input
    """
    # Test implementation
    pass
```

### User Story Tests

#### Test File: `tests/test_user_stories_phase3.py`

```python
import pytest


@pytest.mark.user_story
@pytest.mark.us_05  # US-05: Use Quick Insert Templates
def test_quick_insert_dropdown_accessible():
    """
    What we are testing: Quick insert dropdown is accessible and functional
    Why we are testing: US-05 - Users need quick access to common templates
    Expected Result: Dropdown opens, shows templates, inserts on click
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_05
def test_quick_insert_shows_preset_templates():
    """
    What we are testing: Quick insert shows preset-specific templates
    Why we are testing: US-05 - Templates should match current preset
    Expected Result: Templates list matches preset quick_inserts configuration
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_06  # US-06: Format Text (Bold, Color, Size)
def test_text_formatting_buttons_available():
    """
    What we are testing: Text formatting buttons are available in Text toolbar
    Why we are testing: US-06 - Users need text formatting capabilities
    Expected Result: Bold, Color, Size buttons visible in Text toolbar
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_06
def test_bold_formatting_applies():
    """
    What we are testing: Bold button applies bold formatting to selection
    Why we are testing: US-06 - Core text formatting functionality
    Expected Result: Selected text wrapped in \textbf{} command
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_04  # US-04: Switch Between Visual and Source Modes
def test_mode_tabs_visible():
    """
    What we are testing: Visual and Source mode tabs are visible
    Why we are testing: US-04 - Users need to switch between modes
    Expected Result: Both tabs visible, active tab highlighted
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_04
def test_mode_toggle_switches_views():
    """
    What we are testing: Clicking mode tab switches between visual and source
    Why we are testing: US-04 - Core mode switching functionality
    Expected Result: Visual builder hidden when source active, vice versa
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_04
def test_ctrl_m_shortcut_toggles_mode():
    """
    What we are testing: Ctrl+M keyboard shortcut toggles modes
    Why we are testing: US-04 - Keyboard shortcuts improve efficiency
    Expected Result: Ctrl+M switches between visual and source modes
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_04
def test_bidirectional_sync_works():
    """
    What we are testing: Changes sync bidirectionally between visual and source
    Why we are testing: US-04 - Both modes must stay in sync
    Expected Result: Changes in one mode reflected in other mode
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_07  # US-07: Switch Input Modes
def test_mode_selector_available():
    """
    What we are testing: Mode selector dropdown is available
    Why we are testing: US-07 - Users need to switch input modes
    Expected Result: Mode selector visible with all 6 modes listed
    """
    # Test implementation
    pass


@pytest.mark.user_story
@pytest.mark.us_07
def test_mode_switch_updates_ui():
    """
    What we are testing: Mode switch updates toolbar layout
    Why we are testing: US-07 - Different modes need different UIs
    Expected Result: Toolbar visibility and layout match new mode
    """
    # Test implementation
    pass
```

---

## Phase 3 Completion Criteria

- [ ] Quick insert dropdown functional
- [ ] Text formatting (bold, color, size) working
- [ ] Mode switching UI implemented
- [ ] Source mode with textarea functional
- [ ] Bidirectional sync working
- [ ] Sync debouncing implemented
- [ ] Keyboard shortcuts working (Ctrl+M)
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] All frontend tests passing
- [ ] All security tests passing
- [ ] All user story tests passing
- [ ] Code review completed
- [ ] Documentation updated

---

## Phase 3 Manual Testing Checklist

### Quick Insert Testing

**Test 3.1: Quick Insert Dropdown**
- [ ] Click quick insert button (e.g., "[Calc Quick ▼]")
- [ ] Verify dropdown menu opens
- [ ] Verify menu shows preset-specific templates
- [ ] Verify menu is keyboard accessible
- **Expected Result:** Dropdown opens and shows templates

**Test 3.2: Quick Insert Template Selection**
- [ ] Open quick insert dropdown
- [ ] Click on a template (e.g., "Indefinite Integral")
- [ ] Verify template inserted into visual builder
- [ ] Verify template converted to visual structure
- **Expected Result:** Template inserted correctly

**Test 3.3: Quick Insert with Different Presets**
- [ ] Set preset to `calculus`
- [ ] Verify quick insert shows calculus templates
- [ ] Set preset to `machine_learning`
- [ ] Verify quick insert shows ML templates
- **Expected Result:** Quick insert templates match preset

**Test 3.4: Quick Insert Keyboard Navigation**
- [ ] Open quick insert dropdown
- [ ] Use arrow keys to navigate
- [ ] Press Enter to select
- [ ] Verify template inserted
- **Expected Result:** Keyboard navigation works

### Text Formatting Testing

**Test 3.5: Bold Formatting**
- [ ] Type text: "Problem"
- [ ] Select text
- [ ] Click Bold button
- [ ] Verify text wrapped in `\textbf{}`
- [ ] Verify preview shows bold text
- **Expected Result:** Bold formatting applied correctly

**Test 3.6: Color Formatting**
- [ ] Type text: "Important"
- [ ] Select text
- [ ] Click Color button
- [ ] Select color from picker
- [ ] Verify text wrapped in `\color{}`
- [ ] Verify preview shows colored text
- **Expected Result:** Color formatting applied correctly

**Test 3.7: Size Formatting**
- [ ] Type text: "Title"
- [ ] Select text
- [ ] Click Size button
- [ ] Select size (e.g., "Large")
- [ ] Verify size command applied
- [ ] Verify preview shows correct size
- **Expected Result:** Size formatting applied correctly

**Test 3.8: Formatting Without Selection**
- [ ] Click Bold button without text selection
- [ ] Type text
- [ ] Verify text is bold
- **Expected Result:** Formatting applies to next input

### Mode Switching UI Testing

**Test 3.9: Mode Selector Dropdown**
- [ ] Locate mode selector in widget
- [ ] Verify all 6 modes listed
- [ ] Select different mode
- [ ] Verify mode changes
- **Expected Result:** Mode selector works correctly

**Test 3.10: Mode Switch Updates Toolbar**
- [ ] Start in `regular_functions` mode
- [ ] Note visible toolbars
- [ ] Switch to `integrals_differentials` mode
- [ ] Verify toolbar visibility changes
- [ ] Verify Calculus toolbar now visible
- **Expected Result:** Toolbar updates when mode changes

**Test 3.11: Mode Switch Warning**
- [ ] Create formula with integral in `regular_functions` mode
- [ ] Switch to `regular_functions` mode (no calculus toolbar)
- [ ] Verify warning shown (if implemented)
- **Expected Result:** Warning shown for incompatible operations

### Source Mode Testing

**Test 3.12: Visual/Source Mode Tabs**
- [ ] Locate Visual and Source tabs
- [ ] Verify Visual tab is active by default
- [ ] Click Source tab
- [ ] Verify source textarea appears
- [ ] Verify visual builder hidden
- **Expected Result:** Mode tabs switch views correctly

**Test 3.13: Source Mode LaTeX Editing**
- [ ] Switch to Source mode
- [ ] Type LaTeX directly: `\frac{1}{2} + x^2`
- [ ] Verify textarea accepts input
- [ ] Verify no syntax errors shown
- **Expected Result:** Source mode allows direct LaTeX editing

**Test 3.14: Visual to Source Sync**
- [ ] In Visual mode, insert fraction
- [ ] Fill numerator: "1"
- [ ] Fill denominator: "2"
- [ ] Switch to Source mode
- [ ] Verify textarea shows: `\frac{1}{2}`
- **Expected Result:** Visual changes sync to source

**Test 3.15: Source to Visual Sync**
- [ ] Switch to Source mode
- [ ] Type LaTeX: `\int x dx`
- [ ] Wait for sync (300ms debounce)
- [ ] Switch to Visual mode
- [ ] Verify visual builder shows integral structure
- **Expected Result:** Source changes sync to visual

**Test 3.16: Bidirectional Sync Real-time**
- [ ] Keep both modes visible (if possible) or switch rapidly
- [ ] Make change in Visual mode
- [ ] Verify Source mode updates
- [ ] Make change in Source mode
- [ ] Verify Visual mode updates
- **Expected Result:** Changes sync bidirectionally

**Test 3.17: Sync Conflict Resolution**
- [ ] Make change in Visual mode
- [ ] Immediately make change in Source mode
- [ ] Verify last edit wins (timestamp-based)
- **Expected Result:** No data loss, last edit preserved

**Test 3.18: Sync Error Handling**
- [ ] Switch to Source mode
- [ ] Type invalid LaTeX: `\frac{1}` (missing brace)
- [ ] Verify error shown
- [ ] Verify Visual mode not corrupted
- [ ] Fix LaTeX
- [ ] Verify sync resumes
- **Expected Result:** Invalid LaTeX handled gracefully

**Test 3.19: Ctrl+M Keyboard Shortcut**
- [ ] Press Ctrl+M
- [ ] Verify mode switches (Visual ↔ Source)
- [ ] Press Ctrl+M again
- [ ] Verify mode switches back
- **Expected Result:** Keyboard shortcut works

**Test 3.20: Sync Indicator**
- [ ] Make change in Visual mode
- [ ] Verify sync indicator appears (if implemented)
- [ ] Wait for sync to complete
- [ ] Verify indicator disappears
- **Expected Result:** Sync status visible to user

### Combined Feature Testing

**Test 3.21: Quick Insert + Formatting**
- [ ] Insert template from quick insert
- [ ] Select portion of template
- [ ] Apply bold formatting
- [ ] Verify formatting persists
- **Expected Result:** Quick insert and formatting work together

**Test 3.22: Mode Switch + Source Mode**
- [ ] Create formula in Visual mode
- [ ] Switch to Source mode
- [ ] Change mode via mode selector
- [ ] Verify source mode still works
- [ ] Verify formula preserved
- **Expected Result:** Mode switching works with source mode

---

## Notes

- Bidirectional sync is critical - ensure no data loss
- Source mode must handle invalid LaTeX gracefully
- Formatting must persist correctly in AST
- Quick insert should be keyboard accessible
- **Manual Testing:** Complete all manual tests in checklist before marking phase complete

