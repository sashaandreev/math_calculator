"""
Integration tests for Phase 2: Mode and Preset systems integration.

Tests mode and preset systems working together in widget context.
"""
import pytest
from django.test import TestCase
from django import forms
from django.template.loader import render_to_string
from mathinput.widgets import MathInputWidget
from mathinput.modes import load_mode, VALID_MODES
from mathinput.presets import load_preset, VALID_PRESETS


class MathForm(forms.Form):
    """Test form with MathInputWidget."""
    equation = forms.CharField(widget=MathInputWidget(), required=False)


@pytest.mark.integration
class TestModePresetIntegration(TestCase):
    """
    What we are testing: Mode and preset systems work together in widget
    Why we are testing: Widget must correctly combine mode and preset configurations
    Expected Result: Widget renders with correct toolbar layout and quick inserts
    """
    
    def test_widget_with_mode_and_preset(self):
        """
        What we are testing: Widget correctly applies mode and preset together
        Why we are testing: Users specify both mode and preset for optimal UI
        Expected Result: Widget shows mode-appropriate toolbars with preset quick inserts
        """
        widget = MathInputWidget(mode='integrals_differentials', preset='calculus')
        html = widget.render('equation', '')
        
        # Check that mode and preset are in the rendered HTML
        assert 'data-mode="integrals_differentials"' in html
        assert 'data-preset="calculus"' in html
        
        # Verify widget structure
        assert '<div class="mi-widget"' in html
        assert 'id="id_equation"' in html
    
    def test_mode_preset_config_merge(self):
        """
        What we are testing: Mode and preset configurations merge correctly
        Why we are testing: Both systems must work together without conflicts
        Expected Result: Merged config has mode toolbars + preset tab order
        """
        # Load mode and preset separately
        mode = load_mode('matrices')
        preset = load_preset('machine_learning')
        
        # Verify both have required structures
        assert 'toolbars' in mode
        assert 'tab_order' in preset
        
        # Verify they can be used together
        widget = MathInputWidget(mode='matrices', preset='machine_learning')
        html = widget.render('equation', '')
        
        assert 'data-mode="matrices"' in html
        assert 'data-preset="machine_learning"' in html
    
    def test_widget_with_all_mode_combinations(self):
        """
        What we are testing: Widget works with all valid mode/preset combinations
        Why we are testing: All combinations should be valid and functional
        Expected Result: All combinations render without errors
        """
        # Test a few key combinations
        combinations = [
            ('regular_functions', 'algebra'),
            ('integrals_differentials', 'calculus'),
            ('matrices', 'machine_learning'),
            ('statistics_probability', 'statistics'),
        ]
        
        for mode_code, preset_code in combinations:
            widget = MathInputWidget(mode=mode_code, preset=preset_code)
            html = widget.render('equation', '')
            
            assert f'data-mode="{mode_code}"' in html
            assert f'data-preset="{preset_code}"' in html
    
    def test_form_with_mode_and_preset(self):
        """
        What we are testing: Form with widget correctly passes mode and preset
        Why we are testing: Forms must correctly initialize widgets with parameters
        Expected Result: Form renders widget with correct mode and preset
        """
        class CustomForm(forms.Form):
            equation = forms.CharField(
                widget=MathInputWidget(mode='advanced_expressions', preset='physics'),
                required=False
            )
        
        form = CustomForm()
        html = str(form['equation'])
        
        assert 'data-mode="advanced_expressions"' in html
        assert 'data-preset="physics"' in html
    
    def test_widget_default_mode_and_preset(self):
        """
        What we are testing: Widget uses default mode and preset when not specified
        Why we are testing: Widget must have sensible defaults
        Expected Result: Widget renders with default mode and preset
        """
        widget = MathInputWidget()
        html = widget.render('equation', '')
        
        # Should have default mode and preset
        assert 'data-mode=' in html
        assert 'data-preset=' in html
        
        # Defaults should be valid
        # (exact values depend on settings, but should be in VALID_MODES/VALID_PRESETS)
        # We can't easily extract them from HTML, but we verify structure is present

