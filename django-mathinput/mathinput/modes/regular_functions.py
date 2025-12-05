"""
Regular Functions mode configuration.

Target Users: High school students, basic math courses
Toolbar Focus: Text formatting, Basic operations, Trigonometry
"""
from typing import Dict, List, Tuple


def get_mode() -> Dict:
    """
    Get Regular Functions mode configuration.
    
    Returns:
        Mode configuration dictionary with:
        - name: Display name
        - code: Mode identifier
        - toolbars: Toolbar visibility and priority
        - button_layout: Button size and grouping
        - quick_inserts: Common formula templates
    """
    return {
        "name": "Regular Functions",
        "code": "regular_functions",
        "toolbars": {
            "visible": ["text", "basic", "trig"],
            "hidden": ["advanced", "calculus", "matrices", "symbols"],
            "priority": ["basic", "text", "trig"]
        },
        "button_layout": {
            "size": "large",  # 44×44px minimum for touch-friendly educational use
            "grouping": "basic_operations"
        },
        "quick_inserts": [
            ("Simple Function", r"f(x) = x^2 + 1"),
            ("Trigonometric Function", r"g(x) = \sin(x) + \cos(x)"),
            ("Logarithmic Function", r"h(x) = \log(x)"),
            ("Exponential Function", r"k(x) = e^x"),
            ("Polynomial", r"p(x) = x^2 + 3x - 5"),
        ]
    }

