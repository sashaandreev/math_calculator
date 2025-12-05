"""
Basic tests for MathInputWidget structure.

These tests verify the widget can be instantiated and has the correct structure.
Full tests will be in Phase 1 testing.
"""
import pytest
import os
import django
from django.conf import settings

# Configure Django settings for testing
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    django.setup()

from mathinput.widgets import MathInputWidget


@pytest.mark.unit
def test_widget_instantiation():
    """
    What we are testing: MathInputWidget initializes with default mode and preset
    Why we are testing: Ensure widget works without explicit configuration
    Expected Result: Widget created with default mode='regular_functions', preset='algebra'
    """
    widget = MathInputWidget()
    assert widget.mode == 'regular_functions'
    assert widget.preset == 'algebra'
    assert widget.template_name == 'mathinput/widget.html'


@pytest.mark.unit
def test_widget_with_custom_mode():
    """
    What we are testing: MathInputWidget accepts custom mode parameter
    Why we are testing: Users need to specify input modes for different math types
    Expected Result: Widget created with specified mode
    """
    widget = MathInputWidget(mode='integrals_differentials')
    assert widget.mode == 'integrals_differentials'
    assert widget.preset == 'algebra'  # Default preset


@pytest.mark.unit
def test_widget_with_custom_preset():
    """
    What we are testing: MathInputWidget accepts custom preset parameter
    Why we are testing: Users need to specify domain presets for different subjects
    Expected Result: Widget created with specified preset
    """
    widget = MathInputWidget(preset='calculus')
    assert widget.mode == 'regular_functions'  # Default mode
    assert widget.preset == 'calculus'


@pytest.mark.unit
def test_widget_media():
    """
    What we are testing: Widget Media class includes CSS and JavaScript files
    Why we are testing: Ensure stylesheets and scripts are loaded for widget rendering
    Expected Result: CSS and JS files listed in widget.Media.css and widget.Media.js
    """
    widget = MathInputWidget()
    assert hasattr(widget, 'Media')
    assert 'all' in widget.Media.css
    assert 'mathinput/css/mathinput.css' in widget.Media.css['all']
    assert 'mathinput/js/mathinput.js' in widget.Media.js


@pytest.mark.unit
def test_widget_renders_basic_html():
    """
    What we are testing: Widget render method produces HTML output
    Why we are testing: Widget must render to be usable in forms
    Expected Result: HTML string returned with widget structure
    """
    widget = MathInputWidget()
    html = widget.render('equation', None, {'id': 'id_equation'})
    
    # Check that HTML is returned
    assert isinstance(html, str)
    assert len(html) > 0
    
    # Check for key widget structure elements
    assert 'mi-widget' in html or 'id_equation' in html
    assert 'equation' in html  # Field name should be in HTML

