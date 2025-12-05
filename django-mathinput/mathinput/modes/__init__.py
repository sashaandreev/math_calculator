"""
Mode system for math input.

Provides configuration for different math input modes:
- regular_functions: Basic algebraic expressions
- advanced_expressions: Complex equations
- integrals_differentials: Calculus operations
- matrices: Matrix operations
- statistics_probability: Statistical notation
- physics_engineering: Physics and engineering notation
"""
from typing import Dict, Optional

# Import all mode modules
from .regular_functions import get_mode as get_regular_functions
from .advanced_expressions import get_mode as get_advanced_expressions
from .integrals_differentials import get_mode as get_integrals_differentials
from .matrices import get_mode as get_matrices
from .statistics_probability import get_mode as get_statistics_probability
from .physics_engineering import get_mode as get_physics_engineering

# Mode registry
_MODE_REGISTRY = {
    'regular_functions': get_regular_functions,
    'advanced_expressions': get_advanced_expressions,
    'integrals_differentials': get_integrals_differentials,
    'matrices': get_matrices,
    'statistics_probability': get_statistics_probability,
    'physics_engineering': get_physics_engineering,
}

# Valid mode codes
VALID_MODES = list(_MODE_REGISTRY.keys())


def load_mode(mode_code: str) -> Dict:
    """
    Load mode configuration by code.
    
    Args:
        mode_code: Mode identifier (e.g., 'regular_functions', 'matrices')
    
    Returns:
        Mode configuration dictionary
    
    Raises:
        ValueError: If mode_code is not valid
    
    Example:
        >>> mode = load_mode('regular_functions')
        >>> mode['name']
        'Regular Functions'
    """
    if mode_code not in _MODE_REGISTRY:
        raise ValueError(
            f"Invalid mode code: '{mode_code}'. "
            f"Valid modes: {', '.join(VALID_MODES)}"
        )
    
    return _MODE_REGISTRY[mode_code]()


def get_all_modes() -> Dict[str, Dict]:
    """
    Get all available mode configurations.
    
    Returns:
        Dictionary mapping mode codes to mode configurations
    
    Example:
        >>> all_modes = get_all_modes()
        >>> 'regular_functions' in all_modes
        True
    """
    return {code: load_mode(code) for code in VALID_MODES}


def is_valid_mode(mode_code: str) -> bool:
    """
    Check if a mode code is valid.
    
    Args:
        mode_code: Mode identifier to check
    
    Returns:
        True if mode code is valid, False otherwise
    
    Example:
        >>> is_valid_mode('regular_functions')
        True
        >>> is_valid_mode('invalid_mode')
        False
    """
    return mode_code in _MODE_REGISTRY

