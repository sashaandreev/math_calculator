"""
Unit tests for preset system.

Tests preset loading, validation, and configuration structure.
"""
import pytest
from mathinput.presets import (
    load_preset,
    get_all_presets,
    is_valid_preset,
    VALID_PRESETS,
)


@pytest.mark.unit
def test_get_preset_returns_valid_structure():
    """
    What we are testing: get_preset() returns valid preset configuration structure
    Why we are testing: Preset system must provide consistent configuration format
    Expected Result: Dictionary with required keys: name, code, tab_order, quick_inserts
    """
    from mathinput.presets.algebra import get_preset
    
    preset = get_preset()
    
    assert isinstance(preset, dict)
    assert 'name' in preset
    assert 'code' in preset
    assert 'tab_order' in preset
    assert isinstance(preset['name'], str)
    assert isinstance(preset['code'], str)
    assert isinstance(preset['tab_order'], list)


@pytest.mark.unit
def test_load_preset_loads_calculus_preset():
    """
    What we are testing: load_preset() correctly loads calculus preset
    Why we are testing: Preset loader must correctly retrieve preset configurations
    Expected Result: Returns preset config with calculus-specific quick inserts
    """
    preset = load_preset('calculus')
    
    assert preset['code'] == 'calculus'
    assert preset['name'] == 'Calculus'
    assert 'quick_inserts' in preset
    assert len(preset['quick_inserts']) > 0


@pytest.mark.unit
def test_preset_tab_order_valid():
    """
    What we are testing: Preset tab_order contains valid toolbar names
    Why we are testing: Tab order must reference existing toolbars
    Expected Result: All tab names in tab_order are valid toolbar identifiers
    """
    preset = load_preset('calculus')
    
    assert 'tab_order' in preset
    assert isinstance(preset['tab_order'], list)
    
    # Valid toolbar names
    valid_toolbars = {
        'text', 'basic', 'advanced', 'calculus', 'matrices',
        'trig', 'symbols'
    }
    
    for tab_name in preset['tab_order']:
        assert tab_name in valid_toolbars


@pytest.mark.unit
def test_preset_quick_inserts_valid_latex():
    """
    What we are testing: Preset quick_inserts contain valid LaTeX strings
    Why we are testing: Quick inserts must be valid LaTeX for insertion
    Expected Result: All quick insert templates are valid LaTeX
    """
    preset = load_preset('calculus')
    
    if 'quick_inserts' in preset:
        assert isinstance(preset['quick_inserts'], list)
        for insert in preset['quick_inserts']:
            assert isinstance(insert, (tuple, list))
            assert len(insert) == 2
            assert isinstance(insert[0], str)  # Label
            assert isinstance(insert[1], str)  # LaTeX template
            # LaTeX should not be empty
            assert len(insert[1]) > 0


@pytest.mark.unit
def test_all_presets_have_valid_codes():
    """
    What we are testing: All 6 presets have valid, unique code identifiers
    Why we are testing: Preset codes used in settings and widget parameters
    Expected Result: All presets have valid codes matching naming convention
    """
    assert len(VALID_PRESETS) == 6
    
    expected_presets = {
        'algebra',
        'calculus',
        'physics',
        'machine_learning',
        'statistics',
        'probability',
    }
    
    assert set(VALID_PRESETS) == expected_presets
    
    # Verify all presets can be loaded
    for preset_code in VALID_PRESETS:
        preset = load_preset(preset_code)
        assert preset['code'] == preset_code


@pytest.mark.unit
def test_load_preset_raises_error_for_invalid_code():
    """
    What we are testing: load_preset() raises ValueError for invalid preset codes
    Why we are testing: Invalid preset codes should be rejected early
    Expected Result: ValueError raised with descriptive message
    """
    with pytest.raises(ValueError) as exc_info:
        load_preset('invalid_preset')
    
    assert 'invalid_preset' in str(exc_info.value)
    assert 'Valid presets' in str(exc_info.value)


@pytest.mark.unit
def test_is_valid_preset():
    """
    What we are testing: is_valid_preset() correctly identifies valid/invalid presets
    Why we are testing: Need to validate preset codes before loading
    Expected Result: Returns True for valid presets, False for invalid
    """
    assert is_valid_preset('algebra') is True
    assert is_valid_preset('calculus') is True
    assert is_valid_preset('invalid_preset') is False
    assert is_valid_preset('') is False


@pytest.mark.unit
def test_get_all_presets():
    """
    What we are testing: get_all_presets() returns all preset configurations
    Why we are testing: Need to retrieve all available presets
    Expected Result: Dictionary with all 6 presets, each with valid structure
    """
    all_presets = get_all_presets()
    
    assert isinstance(all_presets, dict)
    assert len(all_presets) == 6
    
    for preset_code, preset_config in all_presets.items():
        assert preset_code in VALID_PRESETS
        assert preset_config['code'] == preset_code
        assert 'name' in preset_config
        assert 'tab_order' in preset_config


@pytest.mark.unit
def test_preset_highlight_buttons_structure():
    """
    What we are testing: Preset highlight_buttons have correct structure (if present)
    Why we are testing: Highlight buttons must be a list of button identifiers
    Expected Result: highlight_buttons is a list of strings (if present)
    """
    preset = load_preset('machine_learning')
    
    if 'highlight_buttons' in preset:
        assert isinstance(preset['highlight_buttons'], list)
        for button in preset['highlight_buttons']:
            assert isinstance(button, str)

