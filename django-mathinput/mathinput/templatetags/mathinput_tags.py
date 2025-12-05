"""
Template tags for MathInput widget.

Provides template filters for rendering math input widgets and displaying formulas.
"""
import re
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from mathinput.widgets import MathInputWidget

register = template.Library()


@register.filter(name='as_mathinput')
def as_mathinput(value, arg=None):
    """
    Template filter to render field as math input widget.
    
    Usage:
        {{ form.equation|as_mathinput }}
        {{ form.equation|as_mathinput:"regular_functions" }}
        {{ form.equation|as_mathinput:"mode=integrals_differentials,preset=calculus" }}
    
    Args:
        value: Field value (LaTeX string)
        arg: Optional argument string in format "mode=value" or "mode=value,preset=value"
             Or just mode name as shorthand
    
    Returns:
        Safe HTML string containing the widget
    """
    mode = None
    preset = None
    
    # Parse argument if provided
    if arg:
        # Check if it's a simple mode name (shorthand)
        if ',' not in arg and '=' not in arg:
            mode = arg
        else:
            # Parse key=value pairs
            parts = arg.split(',')
            for part in parts:
                part = part.strip()
                if '=' in part:
                    key, val = part.split('=', 1)
                    key = key.strip()
                    val = val.strip()
                    if key == 'mode':
                        mode = val
                    elif key == 'preset':
                        preset = val
                else:
                    # If no =, treat as mode
                    mode = part
    
    # Create widget with specified mode and preset
    widget = MathInputWidget(mode=mode, preset=preset)
    
    # Render widget
    html = widget.render('field', value or '')
    
    return mark_safe(html)


@register.filter(name='render_math')
def render_math(value, renderer=None):
    """
    Template filter to render stored LaTeX/MathML formula.
    
    Usage:
        {{ formula|render_math }}
        {{ formula|render_math:"katex" }}
        {{ formula|render_math:"mathjax" }}
    
    Args:
        value: LaTeX or MathML string to render
        renderer: Optional renderer name ('katex' or 'mathjax')
                  Defaults to MATHINPUT_RENDERER setting
    
    Returns:
        Safe HTML string containing rendered formula
    """
    if not value:
        return mark_safe('<span class="mi-empty-formula">No formula</span>')
    
    # Get renderer from argument or settings
    if renderer:
        renderer_name = renderer.lower()
    else:
        renderer_name = getattr(settings, 'MATHINPUT_RENDERER', 'katex').lower()
    
    # Detect format (LaTeX vs MathML)
    is_mathml = value.strip().startswith('<math') or '<math' in value.lower()
    is_latex = not is_mathml and ('\\' in value or value.strip().startswith('$'))
    
    # If neither detected, assume LaTeX
    if not is_mathml and not is_latex:
        is_latex = True
    
    # Render based on format and renderer
    if is_mathml:
        # MathML - render directly or convert
        if renderer_name == 'mathjax':
            # MathJax can render MathML directly
            return mark_safe(f'<span class="mathjax-mathml">{value}</span>')
        else:
            # KaTeX doesn't support MathML, convert or use MathJax fallback
            return mark_safe(f'<span class="mathjax-mathml">{value}</span>')
    else:
        # LaTeX - render with KaTeX or MathJax
        latex = value.strip()
        
        # Remove dollar signs if present (inline math)
        if latex.startswith('$') and latex.endswith('$'):
            latex = latex[1:-1]
        elif latex.startswith('$$') and latex.endswith('$$'):
            latex = latex[2:-2]
        
        if renderer_name == 'katex':
            # KaTeX rendering - create markup that KaTeX can process
            escaped_latex = escape_latex_for_html(latex)
            # KaTeX will process elements with class "katex" and data-latex attribute
            return mark_safe(
                f'<span class="katex-render" data-latex="{escaped_latex}">'
                f'<span class="katex" data-latex="{escaped_latex}"></span>'
                f'</span>'
            )
        elif renderer_name == 'mathjax':
            # MathJax rendering - use MathJax delimiters
            escaped_latex = escape_latex_for_html(latex)
            # MathJax processes \[...\] for display math
            return mark_safe(
                f'<span class="mathjax-render" data-latex="{escaped_latex}">'
                f'\\[{latex}\\]'
                f'</span>'
            )
        else:
            # Unknown renderer, return as-is with error message
            return mark_safe(
                f'<span class="mi-render-error" title="Unknown renderer: {renderer_name}">'
                f'{value}'
                f'</span>'
            )


def escape_latex_for_html(latex):
    """
    Escape LaTeX string for use in HTML attributes.
    
    Args:
        latex: LaTeX string
    
    Returns:
        Escaped string safe for HTML attributes
    """
    # Replace HTML special characters
    latex = latex.replace('&', '&amp;')
    latex = latex.replace('<', '&lt;')
    latex = latex.replace('>', '&gt;')
    latex = latex.replace('"', '&quot;')
    latex = latex.replace("'", '&#x27;')
    
    return latex


@register.filter(name='render_math_inline')
def render_math_inline(value, renderer=None):
    """
    Template filter to render LaTeX as inline math.
    
    Usage:
        {{ formula|render_math_inline }}
    
    Args:
        value: LaTeX string to render inline
        renderer: Optional renderer name
    
    Returns:
        Safe HTML string containing inline rendered formula
    """
    if not value:
        return mark_safe('')
    
    # Get renderer from argument or settings
    if renderer:
        renderer_name = renderer.lower()
    else:
        renderer_name = getattr(settings, 'MATHINPUT_RENDERER', 'katex').lower()
    
    latex = value.strip()
    
    # Remove dollar signs if present
    if latex.startswith('$') and latex.endswith('$'):
        latex = latex[1:-1]
    elif latex.startswith('$$') and latex.endswith('$$'):
        latex = latex[2:-2]
    
    escaped_latex = escape_latex_for_html(latex)
    
    if renderer_name == 'katex':
        return mark_safe(
            f'<span class="katex-render katex-inline" data-latex="{escaped_latex}">'
            f'<span class="katex" data-latex="{escaped_latex}"></span>'
            f'</span>'
        )
    elif renderer_name == 'mathjax':
        return mark_safe(
            f'<span class="mathjax-render mathjax-inline" data-latex="{escaped_latex}">'
            f'\\({latex}\\)'
            f'</span>'
        )
    else:
        return mark_safe(f'<span class="mi-render-error">{value}</span>')

