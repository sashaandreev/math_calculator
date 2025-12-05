"""
Algebra preset configuration.

Domain: Basic algebraic operations, polynomials, equations
Recommended Modes: regular_functions, advanced_expressions
"""
from typing import Dict


def get_preset() -> Dict:
    """
    Get Algebra preset configuration.
    
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
        "name": "Algebra",
        "code": "algebra",
        "tab_order": ["text", "basic", "advanced", "symbols", "trig", "calculus", "matrices"],
        "quick_inserts": [
            ("Quadratic Equation", r"ax^2 + bx + c = 0"),
            ("Polynomial", r"p(x) = a_n x^n + a_{n-1} x^{n-1} + \cdots + a_0"),
            ("Square", r"x^2"),
            ("Square Root", r"\sqrt{x}"),
            ("Fraction", r"\frac{a}{b}"),
            ("Absolute Value", r"|x|"),
            ("Factorial", r"n!"),
        ],
        "highlight_buttons": ["x²", "√", "/", "=", "+", "-", "×", "÷"],
        "recommended_modes": ["regular_functions", "advanced_expressions"]
    }

