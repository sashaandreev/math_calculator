"""
Unit tests for mode system.

Tests mode loading, validation, and configuration structure.
"""
import pytest
from mathinput.modes import (
    load_mode,
    get_all_modes,
    is_valid_mode,
    VALID_MODES,
)


@pytest.mark.unit
def test_get_mode_returns_valid_structure():
    """
    What we are testing: get_mode() returns valid mode configuration structure
    Why we are testing: Mode system must provide consistent configuration format
    Expected Result: Dictionary with required keys: name, code, toolbars, button_layout
    """
    from mathinput.modes.regular_functions import get_mode
    
    mode = get_mode()
    
    assert isinstance(mode, dict)
    assert 'name' in mode
    assert 'code' in mode
    assert 'toolbars' in mode
    assert 'button_layout' in mode
    assert isinstance(mode['name'], str)
    assert isinstance(mode['code'], str)
    assert isinstance(mode['toolbars'], dict)
    assert isinstance(mode['button_layout'], dict)


@pytest.mark.unit
def test_load_mode_loads_integrals_mode():
    """
    What we are testing: load_mode() correctly loads integrals_differentials mode
    Why we are testing: Mode loader must correctly retrieve mode configurations
    Expected Result: Returns mode config with calculus toolbar prioritized
    """
    mode = load_mode('integrals_differentials')
    
    assert mode['code'] == 'integrals_differentials'
    assert mode['name'] == 'Integrals/Differentials'
    assert 'calculus' in mode['toolbars']['visible']
    assert 'calculus' in mode['toolbars']['priority']


@pytest.mark.unit
def test_mode_toolbar_visibility():
    """
    What we are testing: Mode configuration correctly specifies visible/hidden toolbars
    Why we are testing: UI must show/hide toolbars based on mode
    Expected Result: Visible toolbars list matches mode requirements
    """
    mode = load_mode('regular_functions')
    
    assert 'visible' in mode['toolbars']
    assert 'hidden' in mode['toolbars']
    assert isinstance(mode['toolbars']['visible'], list)
    assert isinstance(mode['toolbars']['hidden'], list)
    assert len(mode['toolbars']['visible']) > 0


@pytest.mark.unit
def test_all_modes_have_valid_codes():
    """
    What we are testing: All 6 modes have valid, unique code identifiers
    Why we are testing: Mode codes used in settings and widget parameters
    Expected Result: All modes have valid codes matching naming convention
    """
    assert len(VALID_MODES) == 6
    
    expected_modes = {
        'regular_functions',
        'advanced_expressions',
        'integrals_differentials',
        'matrices',
        'statistics_probability',
        'physics_engineering',
    }
    
    assert set(VALID_MODES) == expected_modes
    
    # Verify all modes can be loaded
    for mode_code in VALID_MODES:
        mode = load_mode(mode_code)
        assert mode['code'] == mode_code


@pytest.mark.unit
def test_load_mode_raises_error_for_invalid_code():
    """
    What we are testing: load_mode() raises ValueError for invalid mode codes
    Why we are testing: Invalid mode codes should be rejected early
    Expected Result: ValueError raised with descriptive message
    """
    with pytest.raises(ValueError) as exc_info:
        load_mode('invalid_mode')
    
    assert 'invalid_mode' in str(exc_info.value)
    assert 'Valid modes' in str(exc_info.value)


@pytest.mark.unit
def test_is_valid_mode():
    """
    What we are testing: is_valid_mode() correctly identifies valid/invalid modes
    Why we are testing: Need to validate mode codes before loading
    Expected Result: Returns True for valid modes, False for invalid
    """
    assert is_valid_mode('regular_functions') is True
    assert is_valid_mode('matrices') is True
    assert is_valid_mode('invalid_mode') is False
    assert is_valid_mode('') is False


@pytest.mark.unit
def test_get_all_modes():
    """
    What we are testing: get_all_modes() returns all mode configurations
    Why we are testing: Need to retrieve all available modes
    Expected Result: Dictionary with all 6 modes, each with valid structure
    """
    all_modes = get_all_modes()
    
    assert isinstance(all_modes, dict)
    assert len(all_modes) == 6
    
    for mode_code, mode_config in all_modes.items():
        assert mode_code in VALID_MODES
        assert mode_config['code'] == mode_code
        assert 'name' in mode_config
        assert 'toolbars' in mode_config


@pytest.mark.unit
def test_mode_quick_inserts_structure():
    """
    What we are testing: Mode quick_inserts have correct structure
    Why we are testing: Quick inserts must be tuples of (label, LaTeX)
    Expected Result: All quick inserts are tuples with 2 elements
    """
    mode = load_mode('regular_functions')
    
    if 'quick_inserts' in mode:
        assert isinstance(mode['quick_inserts'], list)
        for insert in mode['quick_inserts']:
            assert isinstance(insert, (tuple, list))
            assert len(insert) == 2
            assert isinstance(insert[0], str)  # Label
            assert isinstance(insert[1], str)  # LaTeX template

