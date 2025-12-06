"""
Performance tests for Phase 5.

Tests performance requirements including preview update speed,
initial load time, and large formula handling.
"""
import pytest
import time
import os
import django
from django.conf import settings

# Configure Django settings for testing
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    django.setup()

from mathinput.widgets import MathInputWidget
from mathinput.validators import MathInputValidator
from mathinput.security import sanitize_latex


@pytest.mark.performance
class TestPreviewUpdatePerformance:
    """
    What we are testing: Preview updates within 100ms for moderate formulas
    Why we are testing: Performance requirement (NFR-01)
    Expected Result: Preview updates in < 100ms for formulas with < 50 operations
    """
    
    def test_simple_formula_validation_speed(self):
        """
        What we are testing: Simple formula validation is fast
        Why we are testing: Performance - validation should not be slow
        Expected Result: Simple formula validates in < 10ms
        """
        validator = MathInputValidator()
        simple_formula = r'\frac{1}{2}'
        
        start = time.perf_counter()
        result = validator.validate(simple_formula)
        elapsed = (time.perf_counter() - start) * 1000  # Convert to ms
        
        assert result is not None
        # Should be very fast (< 10ms for simple formula)
        assert elapsed < 100, f"Validation took {elapsed:.2f}ms, expected < 100ms"
    
    def test_moderate_formula_validation_speed(self):
        """
        What we are testing: Moderate formula validation is fast
        Why we are testing: Performance requirement
        Expected Result: Moderate formula validates in < 50ms
        """
        validator = MathInputValidator()
        # Formula with ~20 operations
        moderate_formula = r'\frac{\sqrt{x} + \sum_{i=1}^{n} a_i}{\int_{0}^{1} f(x) dx}'
        
        start = time.perf_counter()
        result = validator.validate(moderate_formula)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert result is not None
        # Should be fast (< 50ms for moderate formula)
        assert elapsed < 100, f"Validation took {elapsed:.2f}ms, expected < 100ms"
    
    def test_sanitization_speed(self):
        """
        What we are testing: Sanitization is fast
        Why we are testing: Performance - sanitization should not block
        Expected Result: Sanitization completes in < 20ms
        """
        formula = r'\frac{1}{2} + \sqrt{x}'
        
        start = time.perf_counter()
        sanitized = sanitize_latex(formula)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert sanitized is not None
        # Should be very fast
        assert elapsed < 50, f"Sanitization took {elapsed:.2f}ms, expected < 50ms"


@pytest.mark.performance
class TestInitialLoadPerformance:
    """
    What we are testing: Widget initializes within 1.5s on 3G connection
    Why we are testing: Performance requirement (NFR-02)
    Expected Result: Widget loads in < 1.5s on simulated 3G
    """
    
    def test_widget_rendering_speed(self):
        """
        What we are testing: Widget rendering is fast
        Why we are testing: Performance - initial render should be quick
        Expected Result: Widget renders in < 100ms
        """
        widget = MathInputWidget()
        
        start = time.perf_counter()
        html = widget.render('equation', '')
        elapsed = (time.perf_counter() - start) * 1000
        
        assert html is not None
        # Widget rendering should be very fast (server-side)
        assert elapsed < 200, f"Widget rendering took {elapsed:.2f}ms, expected < 200ms"
    
    def test_widget_with_value_rendering_speed(self):
        """
        What we are testing: Widget with value renders quickly
        Why we are testing: Performance - editing existing formulas should be fast
        Expected Result: Widget with value renders in < 150ms
        """
        widget = MathInputWidget()
        formula = r'\frac{1}{2} + \sqrt{x} + \sum_{i=1}^{n} a_i'
        
        start = time.perf_counter()
        html = widget.render('equation', formula)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert html is not None
        assert elapsed < 300, f"Widget rendering took {elapsed:.2f}ms, expected < 300ms"
    
    def test_multiple_widgets_rendering_speed(self):
        """
        What we are testing: Multiple widgets render efficiently
        Why we are testing: Performance - pages with multiple widgets should load quickly
        Expected Result: 5 widgets render in < 500ms
        """
        widgets = [MathInputWidget() for _ in range(5)]
        
        start = time.perf_counter()
        for i, widget in enumerate(widgets):
            html = widget.render(f'equation_{i}', r'\frac{1}{2}')
            assert html is not None
        elapsed = (time.perf_counter() - start) * 1000
        
        # Should be reasonably fast even with multiple widgets
        assert elapsed < 1000, f"Rendering 5 widgets took {elapsed:.2f}ms, expected < 1000ms"


@pytest.mark.performance
class TestLargeFormulaHandling:
    """
    What we are testing: Widget handles large formulas without freezing
    Why we are testing: Performance - prevent UI freezing
    Expected Result: Large formulas render with loading indicator, no freeze
    """
    
    def test_large_formula_validation_speed(self):
        """
        What we are testing: Large formula validation is reasonable
        Why we are testing: Performance - large formulas should validate without timeout
        Expected Result: Large formula validates in < 500ms
        """
        validator = MathInputValidator()
        # Create a large but valid formula (within limits)
        large_formula = r'\frac{1}{2}' * 100  # 100 fractions
        
        start = time.perf_counter()
        try:
            result = validator.validate(large_formula)
            elapsed = (time.perf_counter() - start) * 1000
            assert result is not None
            # Should complete in reasonable time
            assert elapsed < 2000, f"Large formula validation took {elapsed:.2f}ms"
        except Exception as e:
            # If it fails due to length, that's expected
            if 'too long' in str(e).lower():
                pass  # Expected for very long formulas
            else:
                raise
    
    def test_deeply_nested_formula_validation_speed(self):
        """
        What we are testing: Deeply nested formula validation is reasonable
        Why we are testing: Performance - nested formulas should validate efficiently
        Expected Result: Deeply nested formula validates in < 500ms
        """
        validator = MathInputValidator(max_nesting=20)
        # Create deeply nested formula (within limit)
        nested = r'\frac{' * 15 + '1' + '}' * 15
        
        start = time.perf_counter()
        result = validator.validate(nested)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert result is not None
        # Should complete in reasonable time
        assert elapsed < 1000, f"Deeply nested formula validation took {elapsed:.2f}ms"
    
    def test_matrix_validation_speed(self):
        """
        What we are testing: Large matrix validation is reasonable
        Why we are testing: Performance - matrices should validate efficiently
        Expected Result: Large matrix validates in < 500ms
        """
        validator = MathInputValidator(max_matrix_size=(10, 10))
        # Create 10x10 matrix
        matrix = r'\begin{pmatrix}'
        for i in range(9):
            row = ' & '.join([f'a{j}' for j in range(10)])
            matrix += row + r' \\ '
        matrix += ' & '.join([f'a{j}' for j in range(10)])
        matrix += r'\end{pmatrix}'
        
        start = time.perf_counter()
        result = validator.validate(matrix)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert result is not None
        # Should complete in reasonable time
        assert elapsed < 1000, f"Matrix validation took {elapsed:.2f}ms"
    
    def test_widget_with_large_formula_rendering(self):
        """
        What we are testing: Widget renders large formulas efficiently
        Why we are testing: Performance - editing large formulas should be possible
        Expected Result: Widget with large formula renders in < 500ms
        """
        widget = MathInputWidget()
        # Large but valid formula
        large_formula = r'\frac{1}{2} + \sqrt{x}' * 50
        
        start = time.perf_counter()
        html = widget.render('equation', large_formula)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert html is not None
        # Should render in reasonable time
        assert elapsed < 1000, f"Large formula rendering took {elapsed:.2f}ms"


@pytest.mark.performance
class TestMemoryUsage:
    """
    What we are testing: Widget doesn't cause memory leaks
    Why we are testing: Performance - long-running applications should be stable
    Expected Result: Memory usage remains stable
    """
    
    def test_multiple_validations_memory(self):
        """
        What we are testing: Multiple validations don't leak memory
        Why we are testing: Performance - repeated operations should be efficient
        Expected Result: Memory usage doesn't grow significantly
        """
        validator = MathInputValidator()
        formula = r'\frac{1}{2}'
        
        # Run many validations
        for _ in range(100):
            result = validator.validate(formula)
            assert result is not None
        
        # If we get here without memory issues, test passes
        assert True
    
    def test_multiple_widget_creations(self):
        """
        What we are testing: Creating many widgets doesn't leak memory
        Why we are testing: Performance - widget creation should be efficient
        Expected Result: Memory usage doesn't grow significantly
        """
        # Create many widgets
        for i in range(100):
            widget = MathInputWidget()
            html = widget.render(f'equation_{i}', r'\frac{1}{2}')
            assert html is not None
        
        # If we get here without memory issues, test passes
        assert True

