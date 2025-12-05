"""
Advanced Expressions mode configuration.

Target Users: College students, advanced algebra
Toolbar Focus: Text, Basic, Advanced, Symbols
"""
from typing import Dict


def get_mode() -> Dict:
    """
    Get Advanced Expressions mode configuration.
    
    Returns:
        Mode configuration dictionary with:
        - name: Display name
        - code: Mode identifier
        - toolbars: Toolbar visibility and priority
        - button_layout: Button size and grouping
        - quick_inserts: Common formula templates
    """
    return {
        "name": "Advanced Expressions",
        "code": "advanced_expressions",
        "toolbars": {
            "visible": ["text", "basic", "advanced", "symbols"],
            "hidden": ["calculus", "matrices", "trig"],
            "priority": ["advanced", "basic", "symbols", "text"]
        },
        "button_layout": {
            "size": "medium",
            "grouping": "all_operations"
        },
        "quick_inserts": [
            ("Complex Fraction", r"\frac{x^2 + 3x - 5}{x - 1}"),
            ("Nested Expression", r"\sqrt{\frac{a}{b} + \frac{c}{d}}"),
            ("Summation", r"\sum_{i=1}^{n} x_i"),
            ("Product", r"\prod_{i=1}^{n} a_i"),
            ("Limit", r"\lim_{x \to \infty} f(x)"),
        ]
    }

