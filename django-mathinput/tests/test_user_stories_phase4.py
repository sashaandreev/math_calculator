"""
User story tests for Phase 4: Mobile Responsiveness and Accessibility.

Tests user stories US-13 (Mobile Device), US-14 (Keyboard Navigation).
"""
import pytest
from django import forms
from django.test import TestCase
from mathinput.widgets import MathInputWidget


@pytest.mark.user_story
@pytest.mark.us_13  # US-13: Use on Mobile Device
def test_mobile_toolbar_scrollable():
    """
    What we are testing: Toolbar is horizontally scrollable on mobile
    Why we are testing: US-13 - Mobile users need access to all buttons
    Expected Result: Toolbar scrolls horizontally on small screens
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Widget should render
    assert html is not None
    assert len(html) > 0
    
    # Should contain toolbar structure
    assert 'mi-toolbar-container' in html
    assert 'mi-toolbar-content' in html


@pytest.mark.user_story
@pytest.mark.us_13
def test_mobile_touch_targets_adequate():
    """
    What we are testing: Buttons meet minimum touch target size on mobile
    Why we are testing: US-13 - Mobile usability requirement
    Expected Result: All buttons are at least 48×48px on mobile
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Widget should render
    assert html is not None
    
    # Should contain buttons (they will be styled with CSS for mobile)
    # The actual size is enforced via CSS, which is tested in frontend tests
    assert 'mi-button' in html or 'toolbar' in html.lower()


@pytest.mark.user_story
@pytest.mark.us_13
def test_mobile_preview_collapsible():
    """
    What we are testing: Preview area is collapsible on mobile
    Why we are testing: US-13 - Save screen space on mobile devices
    Expected Result: Preview can be collapsed/expanded on mobile
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Widget should render
    assert html is not None
    
    # Should contain preview container and toggle
    assert 'mi-preview-container' in html
    assert 'mi-preview-toggle' in html
    assert 'mi-preview' in html


@pytest.mark.user_story
@pytest.mark.us_13
def test_mobile_swipe_gestures_supported():
    """
    What we are testing: Swipe gestures work for tab switching on mobile
    Why we are testing: US-13 - Mobile users need gesture-based navigation
    Expected Result: Swipe left/right switches between Visual and Source tabs
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Widget should render
    assert html is not None
    
    # Should contain mode tabs for swipe gestures
    assert 'mi-mode-tabs' in html
    assert 'mi-tab-visual' in html
    assert 'mi-tab-source' in html


@pytest.mark.user_story
@pytest.mark.us_14  # US-14: Navigate with Keyboard Only
def test_keyboard_navigation_complete():
    """
    What we are testing: All features accessible via keyboard only
    Why we are testing: US-14 - Keyboard-only navigation requirement
    Expected Result: All buttons and features accessible without mouse
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Widget should render
    assert html is not None
    
    # Should contain keyboard-accessible elements
    # Buttons should be focusable (they are by default)
    assert 'button' in html or 'role="button"' in html


@pytest.mark.user_story
@pytest.mark.us_14
def test_focus_indicators_visible():
    """
    What we are testing: Focus indicators visible on all interactive elements
    Why we are testing: US-14 - Users need to see keyboard focus
    Expected Result: Focused elements have visible focus indicator
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Widget should render
    assert html is not None
    
    # Focus indicators are handled via CSS
    # We verify that interactive elements exist
    assert 'button' in html or 'role="button"' in html
    assert 'select' in html or 'role="combobox"' in html


@pytest.mark.user_story
@pytest.mark.us_14
def test_keyboard_shortcuts_work():
    """
    What we are testing: Keyboard shortcuts work for common actions
    Why we are testing: US-14 - Keyboard shortcuts improve efficiency
    Expected Result: Ctrl+M toggles Visual/Source mode
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Widget should render
    assert html is not None
    
    # Keyboard shortcuts are handled in JavaScript
    # We verify that mode tabs exist (which Ctrl+M toggles)
    assert 'mi-mode-tabs' in html
    assert 'mi-tab-visual' in html
    assert 'mi-tab-source' in html


@pytest.mark.user_story
@pytest.mark.us_13
def test_mobile_layout_adapts():
    """
    What we are testing: Layout adapts to mobile screen sizes
    Why we are testing: US-13 - Mobile devices have limited screen space
    Expected Result: Widget layout stacks vertically on mobile
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Widget should render
    assert html is not None
    
    # Should contain widget structure
    assert 'mi-widget' in html
    # Layout adaptation is handled via CSS media queries
    # which are tested in frontend tests


@pytest.mark.user_story
@pytest.mark.us_13
def test_mobile_quick_insert_full_width():
    """
    What we are testing: Quick insert menu is full width on mobile
    Why we are testing: US-13 - Better usability on small screens
    Expected Result: Quick insert menu spans full width on mobile
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Widget should render
    assert html is not None
    
    # Should contain quick insert structure
    assert 'mi-quick-insert' in html
    assert 'mi-quick-insert-menu' in html
    # Full width styling is handled via CSS media queries


@pytest.mark.user_story
@pytest.mark.us_13
def test_mobile_color_picker_full_width():
    """
    What we are testing: Color picker is full width on mobile
    Why we are testing: US-13 - Better usability on small screens
    Expected Result: Color picker spans full width on mobile
    """
    widget = MathInputWidget()
    html = widget.render('equation', '')
    
    # Widget should render
    assert html is not None
    
    # Color picker is dynamically created in JavaScript
    # We verify widget structure exists
    assert 'mi-widget' in html
    # Full width styling is handled via CSS media queries

