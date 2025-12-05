"""
Statistics & Probability mode configuration.

Target Users: Statistics students, data analysts
Toolbar Focus: Advanced, Symbols, Basic, Text
"""
from typing import Dict


def get_mode() -> Dict:
    """
    Get Statistics & Probability mode configuration.
    
    Returns:
        Mode configuration dictionary with:
        - name: Display name
        - code: Mode identifier
        - toolbars: Toolbar visibility and priority
        - button_layout: Button size and grouping
        - quick_inserts: Common formula templates
    """
    return {
        "name": "Statistics & Probability",
        "code": "statistics_probability",
        "toolbars": {
            "visible": ["text", "advanced", "symbols", "basic"],
            "hidden": ["calculus", "matrices", "trig"],
            "priority": ["symbols", "advanced", "basic", "text"]
        },
        "button_layout": {
            "size": "medium",
            "grouping": "statistical_operations"
        },
        "quick_inserts": [
            ("Conditional Probability", r"P(A|B) = \frac{P(A \cap B)}{P(B)}"),
            ("Expected Value", r"E[X] = \sum_{i=1}^{n} x_i P(x_i)"),
            ("Mean", r"\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i"),
            ("Variance", r"\text{Var}(X) = E[X^2] - (E[X])^2"),
            ("Standard Deviation", r"\sigma = \sqrt{\text{Var}(X)}"),
            ("Chi-Squared", r"\chi^2"),
            ("Normal Distribution", r"X \sim \mathcal{N}(\mu, \sigma^2)"),
            ("Covariance", r"\text{Cov}(X, Y) = E[XY] - E[X]E[Y]"),
        ]
    }

