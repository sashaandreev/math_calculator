"""
Physics preset configuration.

Domain: Physics, engineering, tensor calculus
Recommended Modes: physics_engineering
"""
from typing import Dict


def get_preset() -> Dict:
    """
    Get Physics preset configuration.
    
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
        "name": "Physics",
        "code": "physics",
        "tab_order": ["text", "calculus", "symbols", "advanced", "basic", "trig", "matrices"],
        "quick_inserts": [
            ("Gradient", r"\nabla f"),
            ("Divergence", r"\nabla \cdot \mathbf{F}"),
            ("Curl", r"\nabla \times \mathbf{F}"),
            ("Laplacian", r"\nabla^2 f"),
            ("Tensor", r"T^{\mu\nu}"),
            ("4-Vector", r"x^\mu = (ct, x, y, z)"),
            ("Planck Constant", r"\hbar"),
            ("Schrödinger Equation", r"i\hbar\frac{\partial}{\partial t}\psi = \hat{H}\psi"),
            ("Maxwell Equations", r"\nabla \cdot \mathbf{E} = \frac{\rho}{\epsilon_0}"),
        ],
        "highlight_buttons": ["∇", "∂", "ℏ", "c", "×", "·", "μ", "ν"],
        "recommended_modes": ["physics_engineering"]
    }

