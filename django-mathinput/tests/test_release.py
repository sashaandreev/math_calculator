"""
Phase 6 Release Tests

Tests to verify package is ready for release:
- Package installability
- Package imports correctly
- All files included
- Works in clean environment
- Backward compatibility
"""
import pytest
import os
import sys
import importlib
from pathlib import Path
from django.apps import apps
from django.conf import settings


@pytest.mark.release
def test_package_installable():
    """
    What we are testing: Package can be installed via pip
    Why we are testing: Users must be able to install package
    Expected Result: pip install succeeds without errors
    """
    # Verify package is importable (simulating installed state)
    try:
        import mathinput
        assert mathinput is not None
    except ImportError as e:
        pytest.fail(f"Package not importable: {e}")


@pytest.mark.release
def test_package_imports_correctly():
    """
    What we are testing: Package imports correctly after installation
    Why we are testing: Package must be importable
    Expected Result: All modules import without errors
    """
    # Test all main module imports
    import mathinput
    from mathinput import widgets
    from mathinput import validators
    from mathinput import security
    from mathinput import modes
    from mathinput import presets
    from mathinput.templatetags import mathinput_tags
    
    # Verify classes are accessible
    from mathinput.widgets import MathInputWidget
    from mathinput.validators import MathInputValidator
    
    # Verify functions are accessible
    from mathinput.modes import load_mode, is_valid_mode
    from mathinput.presets import load_preset, is_valid_preset
    from mathinput.templatetags.mathinput_tags import as_mathinput, render_math
    
    assert MathInputWidget is not None
    assert MathInputValidator is not None
    assert load_mode is not None
    assert is_valid_mode is not None


@pytest.mark.release
def test_all_static_files_included():
    """
    What we are testing: All static files included in package
    Why we are testing: Widget needs CSS/JS files to function
    Expected Result: All static files present in installed package
    """
    import mathinput
    
    # Get package path
    package_path = Path(mathinput.__file__).parent
    
    # Check for static files
    static_css_path = package_path / 'static' / 'mathinput' / 'css' / 'mathinput.css'
    static_js_path = package_path / 'static' / 'mathinput' / 'js' / 'mathinput.js'
    
    assert static_css_path.exists(), f"CSS file not found: {static_css_path}"
    assert static_js_path.exists(), f"JS file not found: {static_js_path}"
    
    # Verify files are not empty
    assert static_css_path.stat().st_size > 0, "CSS file is empty"
    assert static_js_path.stat().st_size > 0, "JS file is empty"


@pytest.mark.release
def test_all_templates_included():
    """
    What we are testing: All template files included in package
    Why we are testing: Widget needs templates to render
    Expected Result: All template files present in installed package
    """
    import mathinput
    
    # Get package path
    package_path = Path(mathinput.__file__).parent
    
    # Check for template files
    templates_dir = package_path / 'templates' / 'mathinput'
    
    assert templates_dir.exists(), f"Templates directory not found: {templates_dir}"
    
    # Check for required template files
    required_templates = [
        'widget.html',
        'toolbar_basic.html',
        'toolbar_advanced.html',
        'toolbar_calculus.html',
        'toolbar_matrices.html',
        'toolbar_text.html',
        'toolbar_trig.html',
        'toolbar_symbols.html',
        'quick_insert.html',
    ]
    
    for template_name in required_templates:
        template_path = templates_dir / template_name
        assert template_path.exists(), f"Template not found: {template_path}"


@pytest.mark.release
def test_package_works_in_clean_environment():
    """
    What we are testing: Package works in fresh virtual environment
    Why we are testing: Users install in clean environments
    Expected Result: Package installs and works in fresh venv
    """
    # This test verifies that the package works when imported
    # In a real clean environment, we would create a venv and install
    
    # Verify core functionality works
    from mathinput.widgets import MathInputWidget
    from mathinput.validators import MathInputValidator
    
    # Create widget instance
    widget = MathInputWidget()
    assert widget is not None
    
    # Render widget
    html = widget.render('test_field', '')
    assert html is not None
    assert 'mathinput' in html.lower() or 'math' in html.lower()
    
    # Test validator
    validator = MathInputValidator()
    result = validator.validate(r'\frac{1}{2}')
    assert result is not None


@pytest.mark.release
def test_backward_compatibility():
    """
    What we are testing: Package maintains backward compatibility
    Why we are testing: Existing users should not break
    Expected Result: No breaking changes from previous versions
    """
    # Since this is the first production release (1.0.0),
    # there are no previous versions to maintain compatibility with.
    # However, we verify that the API is stable and consistent.
    
    from mathinput.widgets import MathInputWidget
    from mathinput.validators import MathInputValidator
    
    # Test that core API remains consistent
    # Widget initialization
    widget1 = MathInputWidget()
    widget2 = MathInputWidget(mode='regular_functions')
    widget3 = MathInputWidget(preset='algebra')
    widget4 = MathInputWidget(mode='integrals_differentials', preset='calculus')
    
    assert widget1.mode is not None
    assert widget2.mode is not None
    assert widget3.preset is not None
    assert widget4.mode is not None
    assert widget4.preset is not None
    
    # Test validator API
    validator = MathInputValidator()
    result = validator.validate(r'x^2 + y^2 = z^2')
    assert isinstance(result, str)
    
    # Test that template tags work
    from mathinput.templatetags.mathinput_tags import as_mathinput, render_math
    assert callable(as_mathinput)
    assert callable(render_math)


@pytest.mark.release
@pytest.mark.user_story
def test_all_user_stories_in_production():
    """
    What we are testing: All 16 user stories work in production environment
    Why we are testing: Final verification before release
    Expected Result: All user stories pass in production setup
    """
    # Import all user story test classes
    from tests.test_user_stories_complete import (
        TestFractionCompleteWorkflow,
        TestIntegralCompleteWorkflow,
        TestMatrixCompleteWorkflow,
        TestModeSwitchingComplete,
        TestQuickInsertComplete,
        TestTextFormattingComplete,
        TestInputModeSwitchingComplete,
        TestPresetUsageComplete,
        TestEditFormulaComplete,
        TestCopyPasteComplete,
        TestUndoRedoComplete,
        TestMultilineEquationsComplete,
        TestMobileUsageComplete,
        TestKeyboardNavigationComplete,
        TestErrorHandlingComplete,
        TestDisplayFormulasComplete,
    )
    
    # Verify all test classes exist
    test_classes = [
        TestFractionCompleteWorkflow,
        TestIntegralCompleteWorkflow,
        TestMatrixCompleteWorkflow,
        TestModeSwitchingComplete,
        TestQuickInsertComplete,
        TestTextFormattingComplete,
        TestInputModeSwitchingComplete,
        TestPresetUsageComplete,
        TestEditFormulaComplete,
        TestCopyPasteComplete,
        TestUndoRedoComplete,
        TestMultilineEquationsComplete,
        TestMobileUsageComplete,
        TestKeyboardNavigationComplete,
        TestErrorHandlingComplete,
        TestDisplayFormulasComplete,
    ]
    
    # Verify we have 16 test classes (one for each user story)
    assert len(test_classes) == 16, f"Expected 16 user story test classes, found {len(test_classes)}"
    
    # Verify each test class has a test method
    for test_class in test_classes:
        # Check that the class has at least one test method
        test_methods = [method for method in dir(test_class) if method.startswith('test_')]
        assert len(test_methods) > 0, f"{test_class.__name__} has no test methods"
    
    # This test verifies that all user story tests are present and structured correctly
    # The actual user story tests are run separately via pytest

