"""
Integrals/Differentials mode configuration.

Target Users: Calculus students, engineers, mathematicians
Toolbar Focus: Calculus, Advanced, Basic, Text
"""
from typing import Dict


def get_mode() -> Dict:
    """
    Get Integrals/Differentials mode configuration.
    
    Returns:
        Mode configuration dictionary with:
        - name: Display name
        - code: Mode identifier
        - toolbars: Toolbar visibility and priority
        - button_layout: Button size and grouping
        - quick_inserts: Common formula templates
    """
    return {
        "name": "Integrals/Differentials",
        "code": "integrals_differentials",
        "toolbars": {
            "visible": ["text", "calculus", "advanced", "basic"],
            "hidden": ["trig", "symbols", "matrices"],
            "priority": ["calculus", "advanced", "basic", "text"]
        },
        "button_layout": {
            "size": "large",  # Prominent calculus operations
            "grouping": "calculus_operations"
        },
        "quick_inserts": [
            ("Indefinite Integral", r"\int f(x) \, dx"),
            ("Definite Integral", r"\int_{a}^{b} f(x) \, dx"),
            ("Derivative", r"\frac{d}{dx}"),
            ("Partial Derivative", r"\frac{\partial}{\partial x}"),
            ("Gradient", r"\nabla f"),
            ("Divergence", r"\nabla \cdot \mathbf{F}"),
            ("Curl", r"\nabla \times \mathbf{F}"),
            ("Limit", r"\lim_{x \to a} f(x)"),
            ("Summation", r"\sum_{i=1}^{n} a_i"),
            ("Product", r"\prod_{i=1}^{n} a_i"),
        ]
    }

