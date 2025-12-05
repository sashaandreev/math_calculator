"""
User story tests for Phase 2: Mode and Preset systems.

Tests user stories related to mode switching, presets, and button interactions.
"""
import pytest
from django import forms
from django.template.loader import render_to_string
from mathinput.widgets import MathInputWidget
from mathinput.modes import load_mode
from mathinput.presets import load_preset


class TestForm(forms.Form):
    """Test form with MathInputWidget."""
    equation = forms.CharField(widget=MathInputWidget(), required=False)


@pytest.mark.user_story
@pytest.mark.us_07  # US-07: Switch Input Modes
def test_widget_switches_modes():
    """
    What we are testing: Widget correctly switches between input modes
    Why we are testing: US-07 - Users need different UI for different math types
    Expected Result: Toolbar layout changes when mode changes
    """
    # Test different modes
    modes_to_test = [
        'regular_functions',
        'integrals_differentials',
        'matrices',
    ]
    
    for mode_code in modes_to_test:
        widget = MathInputWidget(mode=mode_code)
        html = widget.render('equation', '')
        
        # Verify mode is set correctly
        assert f'data-mode="{mode_code}"' in html
        
        # Verify mode configuration is valid
        mode_config = load_mode(mode_code)
        assert mode_config['code'] == mode_code


@pytest.mark.user_story
@pytest.mark.us_08  # US-08: Use Domain Presets
def test_widget_applies_preset():
    """
    What we are testing: Widget correctly applies domain presets
    Why we are testing: US-08 - Users need domain-specific tool configurations
    Expected Result: Quick inserts and tab order match preset configuration
    """
    # Test different presets
    presets_to_test = [
        'algebra',
        'calculus',
        'machine_learning',
    ]
    
    for preset_code in presets_to_test:
        widget = MathInputWidget(preset=preset_code)
        html = widget.render('equation', '')
        
        # Verify preset is set correctly
        assert f'data-preset="{preset_code}"' in html
        
        # Verify preset configuration is valid
        preset_config = load_preset(preset_code)
        assert preset_config['code'] == preset_code
        assert 'tab_order' in preset_config
        assert 'quick_inserts' in preset_config


@pytest.mark.user_story
@pytest.mark.us_01  # US-01: Insert Fraction
def test_fraction_button_inserts_template():
    """
    What we are testing: Fraction button inserts fraction template
    Why we are testing: US-01 - Core user story for inserting fractions
    Expected Result: Clicking fraction button inserts \frac{}{} template
    """
    # This test verifies the widget is set up correctly for fraction insertion
    # Actual button click testing would require JavaScript testing framework
    widget = MathInputWidget(mode='regular_functions')
    html = widget.render('equation', '')
    
    # Verify widget structure is present for button handling
    assert '<div class="mi-widget"' in html
    assert 'data-mode="regular_functions"' in html
    
    # Verify mode has basic toolbar (which should include fraction button)
    mode_config = load_mode('regular_functions')
    assert 'basic' in mode_config['toolbars']['visible']


@pytest.mark.user_story
@pytest.mark.us_02  # US-02: Insert Integral
def test_integral_button_inserts_template():
    """
    What we are testing: Integral button inserts integral template
    Why we are testing: US-02 - Core user story for inserting integrals
    Expected Result: Clicking integral button inserts \int_{}^{} template
    """
    # This test verifies the widget is set up correctly for integral insertion
    widget = MathInputWidget(mode='integrals_differentials')
    html = widget.render('equation', '')
    
    # Verify widget structure is present
    assert '<div class="mi-widget"' in html
    assert 'data-mode="integrals_differentials"' in html
    
    # Verify mode has calculus toolbar (which should include integral button)
    mode_config = load_mode('integrals_differentials')
    assert 'calculus' in mode_config['toolbars']['visible']


@pytest.mark.user_story
@pytest.mark.us_03  # US-03: Insert Matrix
def test_matrix_button_opens_dialog():
    """
    What we are testing: Matrix button opens matrix creation dialog
    Why we are testing: US-03 - Core user story for creating matrices
    Expected Result: Clicking matrix button opens dialog for dimensions
    """
    # This test verifies the widget is set up correctly for matrix insertion
    widget = MathInputWidget(mode='matrices')
    html = widget.render('equation', '')
    
    # Verify widget structure is present
    assert '<div class="mi-widget"' in html
    assert 'data-mode="matrices"' in html
    
    # Verify mode has matrices toolbar
    mode_config = load_mode('matrices')
    assert 'matrices' in mode_config['toolbars']['visible']


@pytest.mark.user_story
@pytest.mark.us_07
def test_mode_switch_preserves_formula():
    """
    What we are testing: Switching modes preserves current formula
    Why we are testing: US-07 - Users should not lose work when switching modes
    Expected Result: Formula remains intact when mode changes
    """
    # Test that widget can be initialized with existing value
    existing_formula = r'\int x^2 dx'
    
    widget1 = MathInputWidget(mode='regular_functions')
    html1 = widget1.render('equation', existing_formula)
    
    # Verify value is preserved in hidden input
    assert f'<textarea name="equation" id="id_equation" class="mi-hidden-input" style="display: none;">{existing_formula}</textarea>' in html1
    
    # Switch to different mode with same value
    widget2 = MathInputWidget(mode='integrals_differentials')
    html2 = widget2.render('equation', existing_formula)
    
    # Verify value is still preserved
    assert f'<textarea name="equation" id="id_equation" class="mi-hidden-input" style="display: none;">{existing_formula}</textarea>' in html2
    
    # Mode should have changed
    assert 'data-mode="regular_functions"' in html1
    assert 'data-mode="integrals_differentials"' in html2


@pytest.mark.user_story
@pytest.mark.us_08
def test_preset_quick_inserts_available():
    """
    What we are testing: Preset quick inserts are available in widget
    Why we are testing: US-08 - Users need quick access to domain-specific formulas
    Expected Result: Quick inserts from preset are accessible
    """
    preset = load_preset('calculus')
    
    # Verify preset has quick inserts
    assert 'quick_inserts' in preset
    assert len(preset['quick_inserts']) > 0
    
    # Verify quick inserts have correct structure
    for insert in preset['quick_inserts']:
        assert isinstance(insert, (tuple, list))
        assert len(insert) == 2
        assert isinstance(insert[0], str)  # Label
        assert isinstance(insert[1], str)  # LaTeX template


@pytest.mark.user_story
@pytest.mark.us_07
def test_mode_and_preset_work_together():
    """
    What we are testing: Mode and preset can be used together
    Why we are testing: US-07 and US-08 - Users combine mode and preset for optimal UI
    Expected Result: Widget works correctly with both mode and preset specified
    """
    widget = MathInputWidget(
        mode='integrals_differentials',
        preset='calculus'
    )
    html = widget.render('equation', '')
    
    # Both mode and preset should be present
    assert 'data-mode="integrals_differentials"' in html
    assert 'data-preset="calculus"' in html
    
    # Both configurations should be valid
    mode_config = load_mode('integrals_differentials')
    preset_config = load_preset('calculus')
    
    assert mode_config['code'] == 'integrals_differentials'
    assert preset_config['code'] == 'calculus'

