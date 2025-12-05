"""
Statistics preset configuration.

Domain: Statistical analysis, data science
Recommended Modes: statistics_probability
"""
from typing import Dict


def get_preset() -> Dict:
    """
    Get Statistics preset configuration.
    
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
        "name": "Statistics",
        "code": "statistics",
        "tab_order": ["text", "advanced", "symbols", "basic", "calculus", "trig", "matrices"],
        "quick_inserts": [
            ("Mean", r"\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i"),
            ("Variance", r"\text{Var}(X) = E[X^2] - (E[X])^2"),
            ("Standard Deviation", r"\sigma = \sqrt{\text{Var}(X)}"),
            ("Chi-Squared", r"\chi^2"),
            ("Normal Distribution", r"X \sim \mathcal{N}(\mu, \sigma^2)"),
            ("Hypothesis Test", r"H_0: \mu = \mu_0"),
            ("Confidence Interval", r"\bar{x} \pm z_{\alpha/2} \frac{\sigma}{\sqrt{n}}"),
            ("Correlation", r"r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}"),
        ],
        "highlight_buttons": ["μ", "σ", "χ²", "∑", "𝔼", "~", "±"],
        "recommended_modes": ["statistics_probability"]
    }

