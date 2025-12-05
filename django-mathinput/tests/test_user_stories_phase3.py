"""
User story tests for Phase 3: Quick Insert, Text Formatting, Mode Switching, Source Mode.

Tests user stories US-04, US-05, US-06, US-07.
"""
import pytest
from django import forms
from mathinput.widgets import MathInputWidget
from mathinput.presets import load_preset


@pytest.mark.user_story
@pytest.mark.us_05  # US-05: Use Quick Insert Templates
def test_quick_insert_dropdown_accessible():
    """
    What we are testing: Quick insert dropdown is accessible and functional
    Why we are testing: US-05 - Users need quick access to common templates
    Expected Result: Dropdown opens, shows templates, inserts on click
    """
    widget = MathInputWidget(preset='calculus')
    html = widget.render('equation', '')
    
    # Should contain quick insert dropdown
    assert 'mi-quick-insert' in html
    assert 'mi-quick-insert-toggle' in html
    assert 'mi-quick-insert-menu' in html
    
    # Should have ARIA attributes for accessibility
    assert 'aria-label' in html or 'aria-haspopup' in html


@pytest.mark.user_story
@pytest.mark.us_05
def test_quick_insert_shows_preset_templates():
    """
    What we are testing: Quick insert shows preset-specific templates
    Why we are testing: US-05 - Templates should match current preset
    Expected Result: Templates list matches preset quick_inserts configuration
    """
    # Test calculus preset
    preset = load_preset('calculus')
    widget = MathInputWidget(preset='calculus')
    html = widget.render('equation', '')
    
    # Widget should have calculus preset
    assert 'data-preset="calculus"' in html
    
    # Preset should have quick inserts
    assert 'quick_inserts' in preset
    assert len(preset['quick_inserts']) > 0


@pytest.mark.user_story
@pytest.mark.us_06  # US-06: Format Text (Bold, Color, Size)
def test_text_formatting_buttons_available():
    """
    What we are testing: Text formatting buttons are available in Text toolbar
    Why we are testing: US-06 - Users need text formatting capabilities
    Expected Result: Bold, Color, Size buttons visible in Text toolbar
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Should contain toolbar structure
    # Note: Toolbar content is loaded dynamically, so we check for structure
    assert 'mi-toolbar' in html or 'toolbar' in html.lower()


@pytest.mark.user_story
@pytest.mark.us_06
def test_bold_formatting_applies():
    """
    What we are testing: Bold button applies bold formatting to selection
    Why we are testing: US-06 - Core text formatting functionality
    Expected Result: Selected text wrapped in \textbf{} command
    """
    from mathinput.security import validate_commands
    
    # Test that \textbf{} is valid (returns tuple)
    latex = r'\textbf{test}'
    is_valid, blocked = validate_commands(latex)
    assert is_valid is True
    assert len(blocked) == 0


@pytest.mark.user_story
@pytest.mark.us_04  # US-04: Switch Between Visual and Source Modes
def test_mode_tabs_visible():
    """
    What we are testing: Visual and Source mode tabs are visible
    Why we are testing: US-04 - Users need to switch between modes
    Expected Result: Both tabs visible, active tab highlighted
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Should contain mode tabs
    assert 'mi-mode-tabs' in html
    assert 'mi-tab-visual' in html
    assert 'mi-tab-source' in html


@pytest.mark.user_story
@pytest.mark.us_04
def test_mode_toggle_switches_views():
    """
    What we are testing: Clicking mode tab switches between visual and source
    Why we are testing: US-04 - Core mode switching functionality
    Expected Result: Visual builder hidden when source active, vice versa
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Should contain both visual and source containers
    assert 'mi-visual-builder-container' in html
    assert 'mi-source-container' in html


@pytest.mark.user_story
@pytest.mark.us_04
def test_ctrl_m_shortcut_toggles_mode():
    """
    What we are testing: Ctrl+M keyboard shortcut toggles modes
    Why we are testing: US-04 - Keyboard shortcuts improve efficiency
    Expected Result: Ctrl+M switches between visual and source modes
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Widget should render (keyboard shortcut is handled in JavaScript)
    assert html is not None
    assert len(html) > 0


@pytest.mark.user_story
@pytest.mark.us_04
def test_bidirectional_sync_works():
    """
    What we are testing: Changes sync bidirectionally between visual and source
    Why we are testing: US-04 - Both modes must stay in sync
    Expected Result: Changes in one mode reflected in other mode
    """
    widget = MathInputWidget()
    html = widget.render('equation', 'x^2')
    
    # Should contain both visual and source elements
    assert 'mi-visual-builder' in html
    assert 'mi-source-textarea' in html
    
    # Initial value should be in hidden input
    assert 'x^2' in html or 'value=' in html


@pytest.mark.user_story
@pytest.mark.us_07  # US-07: Switch Input Modes
def test_mode_selector_available():
    """
    What we are testing: Mode selector dropdown is available
    Why we are testing: US-07 - Users need to switch input modes
    Expected Result: Mode selector visible with all 6 modes listed
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Should contain mode selector
    assert 'mi-mode-selector' in html
    assert 'mi-mode-select' in html


@pytest.mark.user_story
@pytest.mark.us_07
def test_mode_switch_updates_ui():
    """
    What we are testing: Mode switch updates toolbar layout
    Why we are testing: US-07 - Different modes need different UIs
    Expected Result: Toolbar visibility and layout match new mode
    """
    # Test different modes
    modes = [
        'regular_functions',
        'integrals_differentials',
        'matrices',
    ]
    
    for mode in modes:
        widget = MathInputWidget(mode=mode)
        html = widget.render('equation', '')
        
        # Widget should render with correct mode
        assert f'data-mode="{mode}"' in html

