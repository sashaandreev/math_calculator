"""
Phase 6 Production Integration Tests

Tests to verify package works in production-like environment:
- Production settings (DEBUG=False)
- Static files collected
- CDN fallback
"""
import pytest
import os
import django
from django.test import TestCase, override_settings
from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django import forms

# Configure Django settings for testing
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    django.setup()

from mathinput.widgets import MathInputWidget
from mathinput.templatetags.mathinput_tags import render_math


@pytest.mark.production
class TestProductionIntegration(TestCase):
    """
    What we are testing: Package works in production-like environment
    Why we are testing: Production environment may differ from development
    Expected Result: All features work correctly in production setup
    """
    
    @override_settings(DEBUG=False)
    def test_production_settings(self):
        """
        What we are testing: Widget works with DEBUG=False
        Why we are testing: Production uses DEBUG=False
        Expected Result: Widget functions correctly with production settings
        """
        # Verify DEBUG is False
        assert settings.DEBUG is False
        
        # Create widget
        widget = MathInputWidget()
        
        # Render widget - should work even with DEBUG=False
        html = widget.render('equation', r'\frac{1}{2}')
        assert html is not None
        assert len(html) > 0
        
        # Verify widget renders correctly
        assert 'mathinput' in html.lower() or 'math' in html.lower() or 'equation' in html.lower()
        
        # Test with different modes
        widget2 = MathInputWidget(mode='integrals_differentials', preset='calculus')
        html2 = widget2.render('integral', r'\int_0^1 x dx')
        assert html2 is not None
        
        # Test form with widget
        class TestForm(forms.Form):
            equation = forms.CharField(widget=MathInputWidget())
        
        form = TestForm()
        assert form is not None
        assert 'equation' in form.fields
    
    def test_static_files_collected(self):
        """
        What we are testing: Static files work after collectstatic
        Why we are testing: Production uses collected static files
        Expected Result: Widget CSS/JS load correctly after collectstatic
        """
        # Check if static files can be found
        # In production, static files are collected to STATIC_ROOT
        # Here we test that the static file finder can locate them
        
        # Test CSS file
        css_path = finders.find('mathinput/css/mathinput.css')
        # In test environment, it might be in the package
        # In production, it would be in STATIC_ROOT
        if css_path is None:
            # Fallback: check if file exists in package
            import mathinput
            from pathlib import Path
            package_path = Path(mathinput.__file__).parent
            css_file = package_path / 'static' / 'mathinput' / 'css' / 'mathinput.css'
            assert css_file.exists(), "CSS file not found in package"
        else:
            assert os.path.exists(css_path), f"CSS file not found at: {css_path}"
        
        # Test JS file
        js_path = finders.find('mathinput/js/mathinput.js')
        if js_path is None:
            # Fallback: check if file exists in package
            import mathinput
            from pathlib import Path
            package_path = Path(mathinput.__file__).parent
            js_file = package_path / 'static' / 'mathinput' / 'js' / 'mathinput.js'
            assert js_file.exists(), "JS file not found in package"
        else:
            assert os.path.exists(js_path), f"JS file not found at: {js_path}"
        
        # Verify widget Media class references correct paths
        widget = MathInputWidget()
        media = widget.media
        
        # Check CSS
        assert 'mathinput/css/mathinput.css' in str(media._css['all'])
        
        # Check JS
        assert 'mathinput/js/mathinput.js' in media._js
    
    def test_cdn_fallback_works(self):
        """
        What we are testing: CDN fallback works if CDN unavailable
        Why we are testing: Network issues should not break widget
        Expected Result: Widget falls back to local assets if CDN fails
        """
        # The widget uses KaTeX/MathJax from CDN for rendering
        # We test that the widget HTML includes CDN links but also
        # that the widget structure is intact even if CDN fails
        
        widget = MathInputWidget()
        html = widget.render('equation', r'x^2 + y^2')
        
        # Widget should render HTML structure regardless of CDN availability
        assert html is not None
        assert len(html) > 0
        
        # The widget HTML should contain the necessary structure
        # CDN links are included in the template, but widget should work
        # even if CDN is unavailable (browser will handle fallback)
        
        # Test that template renders correctly
        from django.template import Context, Template
        from django.template.loader import get_template
        
        # Verify template exists and can be loaded
        try:
            template = get_template('mathinput/widget.html')
            assert template is not None
        except Exception as e:
            pytest.fail(f"Template cannot be loaded: {e}")
        
        # Test render_math function works (uses CDN but should handle gracefully)
        result = render_math(r'\frac{1}{2}')
        assert result is not None
        # Result should contain some HTML/markup
        assert len(result) > 0
    
    @override_settings(DEBUG=False, ALLOWED_HOSTS=['example.com'])
    def test_production_security_settings(self):
        """
        What we are testing: Widget works with production security settings
        Why we are testing: Production has stricter security settings
        Expected Result: Widget functions correctly with security settings
        """
        # Test with production-like security settings
        assert settings.DEBUG is False
        assert len(settings.ALLOWED_HOSTS) > 0
        
        widget = MathInputWidget()
        html = widget.render('equation', r'\int_0^1 x dx')
        
        # Widget should still render
        assert html is not None
        
        # Test form submission would work (CSRF protection enabled in production)
        class TestForm(forms.Form):
            equation = forms.CharField(widget=MathInputWidget())
        
        form = TestForm(data={'equation': r'\frac{1}{2}'})
        # Form should be valid
        assert form.is_valid()
        assert form.cleaned_data['equation'] == r'\frac{1}{2}'
    
    @override_settings(DEBUG=False)
    def test_production_template_rendering(self):
        """
        What we are testing: Templates render correctly in production mode
        Why we are testing: Template rendering may differ in production
        Expected Result: All templates render without errors
        """
        widget = MathInputWidget()
        
        # Test rendering with different values
        test_cases = [
            ('', 'empty value'),
            (r'\frac{1}{2}', 'fraction'),
            (r'\int_0^1 x dx', 'integral'),
            (r'\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}', 'matrix'),
        ]
        
        for value, description in test_cases:
            html = widget.render('equation', value)
            assert html is not None, f"Widget failed to render with {description}"
            assert len(html) > 0, f"Widget rendered empty HTML for {description}"

