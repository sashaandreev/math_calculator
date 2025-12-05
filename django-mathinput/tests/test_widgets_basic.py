"""
Basic tests for MathInputWidget structure.

These tests verify the widget can be instantiated and has the correct structure.
Full tests will be in Phase 1 testing.
"""
import os
import django
from django.conf import settings

# Configure Django settings for testing
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    django.setup()

from mathinput.widgets import MathInputWidget


def test_widget_instantiation():
    """Test that widget can be instantiated with defaults."""
    widget = MathInputWidget()
    assert widget.mode == 'regular_functions'
    assert widget.preset == 'algebra'
    assert widget.template_name == 'mathinput/widget.html'


def test_widget_with_custom_mode():
    """Test widget with custom mode."""
    widget = MathInputWidget(mode='integrals_differentials')
    assert widget.mode == 'integrals_differentials'
    assert widget.preset == 'algebra'  # Default preset


def test_widget_with_custom_preset():
    """Test widget with custom preset."""
    widget = MathInputWidget(preset='calculus')
    assert widget.mode == 'regular_functions'  # Default mode
    assert widget.preset == 'calculus'


def test_widget_media():
    """Test that widget has Media class with CSS and JS."""
    widget = MathInputWidget()
    assert hasattr(widget, 'Media')
    assert 'all' in widget.Media.css
    assert 'mathinput/css/mathinput.css' in widget.Media.css['all']
    assert 'mathinput/js/mathinput.js' in widget.Media.js


if __name__ == '__main__':
    # Simple test runner
    test_widget_instantiation()
    print("✓ Widget instantiation test passed")
    
    test_widget_with_custom_mode()
    print("✓ Custom mode test passed")
    
    test_widget_with_custom_preset()
    print("✓ Custom preset test passed")
    
    test_widget_media()
    print("✓ Media class test passed")
    
    print("\nAll basic widget tests passed!")

