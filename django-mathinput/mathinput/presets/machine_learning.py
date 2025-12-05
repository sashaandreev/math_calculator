"""
Machine Learning preset configuration.

Domain: Neural networks, optimization, linear algebra
Recommended Modes: matrices, advanced_expressions
"""
from typing import Dict


def get_preset() -> Dict:
    """
    Get Machine Learning preset configuration.
    
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
        "name": "Machine Learning",
        "code": "machine_learning",
        "tab_order": ["text", "matrices", "advanced", "symbols", "calculus", "basic", "trig"],
        "quick_inserts": [
            ("Neural Layer", r"a^{[l]} = \sigma(W^{[l]} a^{[l-1]} + b^{[l]})"),
            ("Loss Function", r"\mathcal{L} = -\sum_{i=1}^{m} y^{(i)} \log(\hat{y}^{(i)})"),
            ("Gradient", r"\nabla_\theta J(\theta)"),
            ("Matrix Product", r"W \mathbf{x} + \mathbf{b}"),
            ("Activation Function", r"\sigma(z) = \frac{1}{1 + e^{-z}}"),
            ("Backpropagation", r"\frac{\partial \mathcal{L}}{\partial W^{[l]}}"),
            ("Regularization", r"J(\theta) = \frac{1}{m}\sum L(\hat{y}, y) + \frac{\lambda}{2m}\sum \theta^2"),
        ],
        "highlight_buttons": ["W", "σ", "𝔼", "θ", "⊙", "[l]", "∇"],
        "recommended_modes": ["matrices", "advanced_expressions"]
    }

