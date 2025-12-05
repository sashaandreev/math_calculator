"""
Physics & Engineering mode configuration.

Target Users: Physics students, engineers
Toolbar Focus: Calculus, Symbols, Advanced, Text
"""
from typing import Dict


def get_mode() -> Dict:
    """
    Get Physics & Engineering mode configuration.
    
    Returns:
        Mode configuration dictionary with:
        - name: Display name
        - code: Mode identifier
        - toolbars: Toolbar visibility and priority
        - button_layout: Button size and grouping
        - quick_inserts: Common formula templates
    """
    return {
        "name": "Physics & Engineering",
        "code": "physics_engineering",
        "toolbars": {
            "visible": ["text", "calculus", "symbols", "advanced"],
            "hidden": ["basic", "trig", "matrices"],
            "priority": ["calculus", "symbols", "advanced", "text"]
        },
        "button_layout": {
            "size": "medium",
            "grouping": "physics_operations"
        },
        "quick_inserts": [
            ("Curl", r"\nabla \times \mathbf{F}"),
            ("Divergence", r"\nabla \cdot \mathbf{F}"),
            ("Gradient", r"\nabla f"),
            ("Laplacian", r"\nabla^2 f"),
            ("Tensor", r"T^{\mu\nu}"),
            ("4-Vector", r"x^\mu = (ct, x, y, z)"),
            ("Planck Constant", r"\hbar"),
            ("Speed of Light", r"c"),
            ("Schrödinger Equation", r"i\hbar\frac{\partial}{\partial t}\psi = \hat{H}\psi"),
        ]
    }

