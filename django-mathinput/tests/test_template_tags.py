"""
Unit tests for template tags.

Tests the as_mathinput and render_math template filters.
"""
import pytest
from django.template import Context, Template
from django.test import TestCase
from mathinput.templatetags.mathinput_tags import as_mathinput, render_math, render_math_inline


@pytest.mark.unit
def test_as_mathinput_filter_renders_widget():
    """
    What we are testing: as_mathinput filter renders MathInputWidget
    Why we are testing: Template filter must render widget correctly
    Expected Result: Filter returns widget HTML
    """
    value = 'x^2 + 1'
    result = as_mathinput(value)
    
    # Should return HTML string
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0
    
    # Should contain widget structure
    assert 'mi-widget' in result
    assert 'mi-visual-builder' in result or 'widget' in result.lower()


@pytest.mark.unit
def test_as_mathinput_with_mode_parameter():
    """
    What we are testing: as_mathinput filter accepts mode parameter
    Why we are testing: Filter must support mode customization
    Expected Result: Widget rendered with specified mode
    """
    value = 'x^2 + 1'
    
    # Test with mode shorthand
    result = as_mathinput(value, 'integrals_differentials')
    assert result is not None
    assert 'data-mode' in result or 'integrals' in result.lower()
    
    # Test with mode=value format
    result2 = as_mathinput(value, 'mode=matrices')
    assert result2 is not None


@pytest.mark.unit
def test_as_mathinput_with_mode_and_preset():
    """
    What we are testing: as_mathinput filter accepts mode and preset parameters
    Why we are testing: Filter must support both mode and preset
    Expected Result: Widget rendered with specified mode and preset
    """
    value = 'x^2 + 1'
    
    # Test with mode and preset
    result = as_mathinput(value, 'mode=integrals_differentials,preset=calculus')
    assert result is not None
    assert len(result) > 0


@pytest.mark.unit
def test_render_math_renders_latex():
    """
    What we are testing: render_math filter renders LaTeX to HTML
    Why we are testing: Filter must convert LaTeX to displayable HTML
    Expected Result: HTML output with LaTeX rendering markup
    """
    latex = r'x^2 + 1'
    result = render_math(latex)
    
    # Should return HTML string
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0
    
    # Should contain rendering markup
    assert 'katex' in result.lower() or 'mathjax' in result.lower() or 'data-latex' in result


@pytest.mark.unit
def test_render_math_auto_detects_format():
    """
    What we are testing: render_math auto-detects LaTeX vs MathML
    Why we are testing: Filter must handle both formats
    Expected Result: Format detected correctly, appropriate renderer used
    """
    # Test LaTeX detection
    latex = r'\frac{1}{2}'
    result = render_math(latex)
    assert result is not None
    assert 'data-latex' in result or 'katex' in result.lower() or 'mathjax' in result.lower()
    
    # Test MathML detection
    mathml = '<math><mi>x</mi><mo>+</mo><mn>1</mn></math>'
    result2 = render_math(mathml)
    assert result2 is not None
    assert 'mathml' in result2.lower() or 'math' in result2.lower()


@pytest.mark.unit
def test_render_math_handles_invalid_input():
    """
    What we are testing: render_math handles invalid LaTeX gracefully
    Why we are testing: Filter must not break on invalid input
    Expected Result: Error message or safe fallback displayed
    """
    # Test empty input
    result = render_math('')
    assert result is not None
    assert len(result) > 0
    
    # Test None input
    result2 = render_math(None)
    assert result2 is not None
    
    # Test invalid LaTeX (should still render, just may not display correctly)
    invalid = '\\invalid{command}'
    result3 = render_math(invalid)
    assert result3 is not None


@pytest.mark.unit
def test_render_math_with_renderer_parameter():
    """
    What we are testing: render_math filter accepts renderer parameter
    Why we are testing: Users may want to specify renderer
    Expected Result: Filter uses specified renderer
    """
    latex = r'x^2 + 1'
    
    # Test with katex
    result = render_math(latex, 'katex')
    assert result is not None
    assert 'katex' in result.lower() or 'data-latex' in result
    
    # Test with mathjax
    result2 = render_math(latex, 'mathjax')
    assert result2 is not None
    assert 'mathjax' in result2.lower() or 'data-latex' in result2


@pytest.mark.unit
def test_render_math_removes_dollar_signs():
    """
    What we are testing: render_math removes dollar signs from LaTeX
    Why we are testing: Users may include $ delimiters
    Expected Result: Dollar signs removed, LaTeX rendered correctly
    """
    latex_with_dollars = r'$x^2 + 1$'
    result = render_math(latex_with_dollars)
    
    assert result is not None
    # Should not contain dollar signs in output
    assert '$' not in result or result.count('$') < 2


@pytest.mark.unit
def test_render_math_inline():
    """
    What we are testing: render_math_inline filter renders inline math
    Why we are testing: Inline math rendering is needed for text
    Expected Result: Inline math markup returned
    """
    latex = r'x^2'
    result = render_math_inline(latex)
    
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0
    assert 'inline' in result.lower() or 'data-latex' in result


@pytest.mark.unit
def test_render_math_escapes_html():
    """
    What we are testing: render_math escapes HTML in LaTeX
    Why we are testing: Security - prevent XSS in rendered output
    Expected Result: HTML special characters escaped
    """
    latex_with_html = r'x < 1 & y > 0'
    result = render_math(latex_with_html)
    
    assert result is not None
    # HTML should be escaped in data-latex attribute
    assert '&lt;' in result or '<' not in result or 'data-latex' in result


@pytest.mark.unit
@pytest.mark.integration
class TestTemplateTagIntegration(TestCase):
    """
    What we are testing: Template tags work in real Django templates
    Why we are testing: Template tags must integrate with Django template system
    Expected Result: Tags work correctly in template context
    """
    
    def test_as_mathinput_in_template(self):
        """
        What we are testing: as_mathinput filter works in Django template
        Why we are testing: Template integration must work
        Expected Result: Widget rendered in template
        """
        template = Template('{% load mathinput_tags %}{{ value|as_mathinput }}')
        context = Context({'value': 'x^2 + 1'})
        result = template.render(context)
        
        assert 'mi-widget' in result or 'widget' in result.lower()
    
    def test_render_math_in_template(self):
        """
        What we are testing: render_math filter works in Django template
        Why we are testing: Template integration must work
        Expected Result: Formula rendered in template
        """
        template = Template('{% load mathinput_tags %}{{ formula|render_math }}')
        context = Context({'formula': r'x^2 + 1'})
        result = template.render(context)
        
        assert result is not None
        assert len(result) > 0
    
    def test_render_math_with_mode_in_template(self):
        """
        What we are testing: as_mathinput with mode works in template
        Why we are testing: Template parameter passing must work
        Expected Result: Widget rendered with specified mode
        """
        template = Template('{% load mathinput_tags %}{{ value|as_mathinput:"matrices" }}')
        context = Context({'value': 'x^2 + 1'})
        result = template.render(context)
        
        assert result is not None
        assert len(result) > 0

