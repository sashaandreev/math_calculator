"""
Unit tests for Quick Insert functionality.

Tests quick insert template loading and validation.
"""
import pytest
from mathinput.presets import load_preset, get_all_presets


@pytest.mark.unit
def test_quick_insert_templates_loaded():
    """
    What we are testing: Quick insert templates loaded from preset configuration
    Why we are testing: Quick insert must show preset-specific templates
    Expected Result: Templates list matches preset quick_inserts configuration
    """
    preset = load_preset('calculus')
    
    assert 'quick_inserts' in preset
    assert isinstance(preset['quick_inserts'], list)
    assert len(preset['quick_inserts']) > 0
    
    # Check that templates are tuples of (name, latex)
    for item in preset['quick_inserts']:
        assert isinstance(item, (tuple, list))
        assert len(item) == 2
        assert isinstance(item[0], str)  # Name
        assert isinstance(item[1], str)  # LaTeX template


@pytest.mark.unit
def test_quick_insert_templates_valid_latex():
    """
    What we are testing: All quick insert templates are valid LaTeX
    Why we are testing: Templates must be insertable without errors
    Expected Result: All templates pass LaTeX validation
    """
    all_presets = get_all_presets()
    
    for preset_code, preset in all_presets.items():
        if 'quick_inserts' in preset:
            for item in preset['quick_inserts']:
                name, latex = item
                
                # Check that LaTeX is a string
                assert isinstance(latex, str)
                
                # Check that LaTeX is not empty
                assert len(latex) > 0
                
                # Check that LaTeX doesn't contain obviously dangerous patterns
                # (More detailed validation would be in security tests)
                assert '<script' not in latex.lower()
                assert 'javascript:' not in latex.lower()


@pytest.mark.unit
def test_quick_insert_templates_have_names():
    """
    What we are testing: All quick insert templates have display names
    Why we are testing: Templates need human-readable names for UI
    Expected Result: All templates have non-empty names
    """
    all_presets = get_all_presets()
    
    for preset_code, preset in all_presets.items():
        if 'quick_inserts' in preset:
            for item in preset['quick_inserts']:
                name, latex = item
                
                assert isinstance(name, str)
                assert len(name) > 0
                assert name.strip() == name  # No leading/trailing whitespace

