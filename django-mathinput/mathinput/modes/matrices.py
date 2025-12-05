"""
Matrices mode configuration.

Target Users: Linear algebra students, ML practitioners, data scientists
Toolbar Focus: Matrices, Advanced, Symbols, Text
"""
from typing import Dict


def get_mode() -> Dict:
    """
    Get Matrices mode configuration.
    
    Returns:
        Mode configuration dictionary with:
        - name: Display name
        - code: Mode identifier
        - toolbars: Toolbar visibility and priority
        - button_layout: Button size and grouping
        - quick_inserts: Common formula templates
    """
    return {
        "name": "Matrices",
        "code": "matrices",
        "toolbars": {
            "visible": ["text", "matrices", "advanced", "symbols"],
            "hidden": ["basic", "trig", "calculus"],
            "priority": ["matrices", "advanced", "symbols", "text"]
        },
        "button_layout": {
            "size": "medium",
            "grouping": "matrix_operations"
        },
        "quick_inserts": [
            ("2×2 Matrix", r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}"),
            ("3×3 Matrix", r"\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}"),
            ("Matrix Inverse", r"A^{-1}"),
            ("Matrix Transpose", r"A^T"),
            ("Determinant", r"\det(A)"),
            ("Vector", r"\mathbf{v} = \begin{pmatrix} x \\ y \\ z \end{pmatrix}"),
            ("Matrix Product", r"AB"),
            ("ML Layer Notation", r"W^{[l]}"),
        ]
    }

