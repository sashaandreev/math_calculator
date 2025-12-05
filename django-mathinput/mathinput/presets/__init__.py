"""
Preset system for math input.

Provides domain-specific configurations that work with modes:
- algebra: Basic algebraic operations
- calculus: Calculus and analysis
- physics: Physics and engineering
- machine_learning: Machine learning notation
- statistics: Statistical analysis
- probability: Probability theory
"""
from typing import Dict

# Import all preset modules
from .algebra import get_preset as get_algebra
from .calculus import get_preset as get_calculus
from .physics import get_preset as get_physics
from .machine_learning import get_preset as get_machine_learning
from .statistics import get_preset as get_statistics
from .probability import get_preset as get_probability

# Preset registry
_PRESET_REGISTRY = {
    'algebra': get_algebra,
    'calculus': get_calculus,
    'physics': get_physics,
    'machine_learning': get_machine_learning,
    'statistics': get_statistics,
    'probability': get_probability,
}

# Valid preset codes
VALID_PRESETS = list(_PRESET_REGISTRY.keys())


def load_preset(preset_code: str) -> Dict:
    """
    Load preset configuration by code.
    
    Args:
        preset_code: Preset identifier (e.g., 'algebra', 'calculus')
    
    Returns:
        Preset configuration dictionary
    
    Raises:
        ValueError: If preset_code is not valid
    
    Example:
        >>> preset = load_preset('algebra')
        >>> preset['name']
        'Algebra'
    """
    if preset_code not in _PRESET_REGISTRY:
        raise ValueError(
            f"Invalid preset code: '{preset_code}'. "
            f"Valid presets: {', '.join(VALID_PRESETS)}"
        )
    
    return _PRESET_REGISTRY[preset_code]()


def get_all_presets() -> Dict[str, Dict]:
    """
    Get all available preset configurations.
    
    Returns:
        Dictionary mapping preset codes to preset configurations
    
    Example:
        >>> all_presets = get_all_presets()
        >>> 'algebra' in all_presets
        True
    """
    return {code: load_preset(code) for code in VALID_PRESETS}


def is_valid_preset(preset_code: str) -> bool:
    """
    Check if a preset code is valid.
    
    Args:
        preset_code: Preset identifier to check
    
    Returns:
        True if preset code is valid, False otherwise
    
    Example:
        >>> is_valid_preset('algebra')
        True
        >>> is_valid_preset('invalid_preset')
        False
    """
    return preset_code in _PRESET_REGISTRY

