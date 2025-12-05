"""
Calculus preset configuration.

Domain: Calculus, derivatives, integrals, limits
Recommended Modes: integrals_differentials
"""
from typing import Dict


def get_preset() -> Dict:
    """
    Get Calculus preset configuration.
    
    Returns:
        Preset configuration dictionary with:
        - name: Display name
        - code: Preset identifier
        - tab_order: Toolbar tab priority order
        - quick_inserts: Common formula templates
        - highlight_buttons: Buttons to highlight
        - recommended_modes: Compatible mode codes
    """
    return {
        "name": "Calculus",
        "code": "calculus",
        "tab_order": ["text", "calculus", "basic", "advanced", "symbols", "trig", "matrices"],
        "quick_inserts": [
            ("Indefinite Integral", r"\int f(x) \, dx"),
            ("Definite Integral", r"\int_{a}^{b} f(x) \, dx"),
            ("Derivative", r"\frac{d}{dx}"),
            ("Partial Derivative", r"\frac{\partial}{\partial x}"),
            ("Limit", r"\lim_{x \to a} f(x)"),
            ("Second Derivative", r"\frac{d^2}{dx^2}"),
            ("Chain Rule", r"\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)"),
            ("Fundamental Theorem", r"\int_{a}^{b} f'(x) \, dx = f(b) - f(a)"),
        ],
        "highlight_buttons": ["∫", "d/dx", "∂/∂x", "lim", "∑", "∏"],
        "recommended_modes": ["integrals_differentials"]
    }

