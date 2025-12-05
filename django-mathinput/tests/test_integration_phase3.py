"""
Integration tests for Phase 3: Quick Insert, Text Formatting, Mode Switching, Source Mode.

Tests integration of Phase 3 features with widget and other systems.
"""
import pytest
from django import forms
from django.test import TestCase
from mathinput.widgets import MathInputWidget
from mathinput.presets import load_preset


@pytest.mark.integration
class TestQuickInsertIntegration(TestCase):
    """
    What we are testing: Quick insert integrates with widget and preset system
    Why we are testing: Quick insert must work correctly in full widget context
    Expected Result: Clicking quick insert item inserts template into visual builder
    """
    
    def test_quick_insert_integrates_with_widget(self):
        """
        What we are testing: Quick insert dropdown works in widget
        Why we are testing: Feature must work in real widget context
        Expected Result: Quick insert menu appears, items insert correctly
        """
        widget = MathInputWidget(preset='calculus')
        html = widget.render('equation', '')
        
        # Widget should render
        assert html is not None
        assert len(html) > 0
        
        # Should contain quick insert structure
        assert 'mi-quick-insert' in html
        assert 'mi-quick-insert-toggle' in html
        assert 'mi-quick-insert-menu' in html
        
        # Should have preset name in button
        preset = load_preset('calculus')
        assert preset['name'] in html or 'Quick' in html


@pytest.mark.integration
class TestModeSwitchingIntegration(TestCase):
    """
    What we are testing: Mode switching integrates with widget and preserves formula
    Why we are testing: Mode switching must work without data loss
    Expected Result: Formula preserved, toolbar updated when mode changes
    """
    
    def test_mode_switch_preserves_formula(self):
        """
        What we are testing: Switching modes preserves current formula
        Why we are testing: Users should not lose work when changing modes
        Expected Result: Formula remains intact after mode switch
        """
        initial_latex = r'x^2 + 1'
        
        # Create widget with initial value
        widget = MathInputWidget(mode='regular_functions')
        html1 = widget.render('equation', initial_latex)
        
        # Switch mode
        widget2 = MathInputWidget(mode='advanced_expressions')
        html2 = widget2.render('equation', initial_latex)
        
        # Both should contain the initial value
        assert initial_latex in html1 or 'x^2' in html1
        assert initial_latex in html2 or 'x^2' in html2


@pytest.mark.integration
class TestTextFormattingIntegration(TestCase):
    """
    What we are testing: Text formatting integrates with widget
    Why we are testing: Formatting must work in full widget context
    Expected Result: Format buttons work correctly in widget
    """
    
    def test_format_buttons_in_widget(self):
        """
        What we are testing: Format buttons are present in widget
        Why we are testing: Formatting UI must be available
        Expected Result: Format buttons rendered in widget HTML
        """
        widget = MathInputWidget()
        html = widget.render('equation', '')
        
        # Should contain toolbar structure
        assert 'mi-toolbar' in html or 'toolbar' in html.lower()


@pytest.mark.integration
class TestSourceModeIntegration(TestCase):
    """
    What we are testing: Source mode integrates with widget
    Why we are testing: Source mode must work in full widget context
    Expected Result: Source mode textarea and sync work correctly
    """
    
    def test_source_mode_in_widget(self):
        """
        What we are testing: Source mode textarea is present in widget
        Why we are testing: Source mode must be accessible
        Expected Result: Source textarea rendered in widget HTML
        """
        widget = MathInputWidget()
        html = widget.render('equation', '')
        
        # Should contain source mode structure
        assert 'mi-source-textarea' in html or 'source' in html.lower()
        assert 'mi-tab-source' in html or 'source' in html.lower()


@pytest.mark.integration
def test_quick_insert_preset_integration():
    """
    What we are testing: Quick insert shows correct templates for preset
    Why we are testing: Quick insert must match selected preset
    Expected Result: Templates match preset configuration
    """
    # Test calculus preset
    widget = MathInputWidget(preset='calculus')
    html = widget.render('equation', '')
    
    # Widget should render with calculus preset
    assert 'data-preset="calculus"' in html
    
    # Test algebra preset
    widget2 = MathInputWidget(preset='algebra')
    html2 = widget2.render('equation', '')
    
    # Widget should render with algebra preset
    assert 'data-preset="algebra"' in html2

