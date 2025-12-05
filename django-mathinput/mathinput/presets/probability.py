"""
Probability preset configuration.

Domain: Probability theory, stochastic processes
Recommended Modes: statistics_probability
"""
from typing import Dict


def get_preset() -> Dict:
    """
    Get Probability preset configuration.
    
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
        "name": "Probability",
        "code": "probability",
        "tab_order": ["text", "advanced", "symbols", "basic", "calculus", "trig", "matrices"],
        "quick_inserts": [
            ("Conditional Probability", r"P(A|B) = \frac{P(A \cap B)}{P(B)}"),
            ("Bayes' Theorem", r"P(A|B) = \frac{P(B|A) P(A)}{P(B)}"),
            ("Expected Value", r"E[X] = \sum_{i=1}^{n} x_i P(x_i)"),
            ("Variance", r"\text{Var}(X) = E[X^2] - (E[X])^2"),
            ("Covariance", r"\text{Cov}(X, Y) = E[XY] - E[X]E[Y]"),
            ("Binomial Distribution", r"P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}"),
            ("Poisson Distribution", r"P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}"),
            ("Normal Distribution", r"f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}"),
        ],
        "highlight_buttons": ["P", "E", "∩", "∪", "|", "~", "λ", "μ", "σ"],
        "recommended_modes": ["statistics_probability"]
    }

