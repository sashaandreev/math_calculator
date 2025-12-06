"""
Comprehensive end-to-end tests for Phase 5.

Tests complete workflows, all modes, and all presets to ensure
everything works together correctly.
"""
import pytest
import os
import django
from django.conf import settings
from django.test import TestCase, Client
from django import forms
from django.contrib.auth.models import User

# Configure Django settings for testing
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    django.setup()

from mathinput.widgets import MathInputWidget
from mathinput.validators import MathInputValidator
from mathinput.security import sanitize_latex
from mathinput.modes import load_mode, is_valid_mode
from mathinput.presets import load_preset, is_valid_preset
from mathinput.templatetags.mathinput_tags import as_mathinput, render_math


@pytest.mark.comprehensive
class TestEndToEndWorkflow(TestCase):
    """
    What we are testing: Complete end-to-end workflow from widget to storage
    Why we are testing: Ensure all components work together correctly
    Expected Result: User can create formula, validate, save, and display it
    """
    
    def test_complete_workflow(self):
        """
        What we are testing: Complete workflow: create → validate → save → display
        Why we are testing: Real-world usage scenario
        Expected Result: Formula created, validated, saved, and displayed successfully
        """
        # Step 1: Create widget
        widget = MathInputWidget()
        assert widget is not None
        
        # Step 2: Render widget with initial value
        initial_latex = r'\frac{1}{2}'
        html = widget.render('equation', initial_latex)
        assert html is not None
        assert 'mi-widget' in html or 'widget' in html.lower()
        
        # Step 3: Validate formula
        validator = MathInputValidator()
        try:
            validated_latex = validator.validate(initial_latex)
            assert validated_latex is not None
            assert 'frac' in validated_latex
        except Exception as e:
            pytest.fail(f"Validation failed: {e}")
        
        # Step 4: Sanitize formula
        sanitized = sanitize_latex(initial_latex)
        assert sanitized is not None
        assert 'frac' in sanitized
        
        # Step 5: Display formula using template filter
        rendered = render_math(initial_latex)
        assert rendered is not None
        assert len(rendered) > 0
    
    def test_form_submission_workflow(self):
        """
        What we are testing: Complete form submission workflow
        Why we are testing: Real-world form usage
        Expected Result: Form can be submitted, validated, and processed
        """
        class MathForm(forms.Form):
            equation = forms.CharField(
                widget=MathInputWidget(),
                validators=[MathInputValidator()]
            )
        
        # Create form with valid data
        form = MathForm(data={'equation': r'\frac{1}{2}'})
        assert form.is_valid()
        assert 'equation' in form.cleaned_data
        assert form.cleaned_data['equation'] == r'\frac{1}{2}'
        
        # Create form with invalid data
        invalid_form = MathForm(data={'equation': r'\input{/etc/passwd}'})
        assert not invalid_form.is_valid()
        assert 'equation' in invalid_form.errors
    
    def test_widget_to_template_workflow(self):
        """
        What we are testing: Widget → Template → Display workflow
        Why we are testing: Complete rendering pipeline
        Expected Result: Widget renders, template filter works, display is correct
        """
        # Widget renders
        widget = MathInputWidget()
        html = widget.render('equation', r'\sqrt{x}')
        assert html is not None
        
        # Template filter renders widget
        widget_html = as_mathinput(r'\sqrt{x}')
        assert widget_html is not None
        assert 'mi-widget' in widget_html or 'widget' in widget_html.lower()
        
        # Display filter renders formula
        display_html = render_math(r'\sqrt{x}')
        assert display_html is not None
        assert len(display_html) > 0


@pytest.mark.comprehensive
class TestAllModesFunctional:
    """
    What we are testing: All 6 input modes are functional
    Why we are testing: All modes must work correctly
    Expected Result: Each mode renders and functions correctly
    """
    
    def test_regular_functions_mode(self):
        """Test regular_functions mode."""
        widget = MathInputWidget(mode='regular_functions')
        assert widget.mode == 'regular_functions'
        
        html = widget.render('equation', r'\frac{1}{2}')
        assert html is not None
        
        # Verify mode config exists
        mode_config = load_mode('regular_functions')
        assert mode_config is not None
        assert 'name' in mode_config  # Config has name field
    
    def test_advanced_expressions_mode(self):
        """Test advanced_expressions mode."""
        widget = MathInputWidget(mode='advanced_expressions')
        assert widget.mode == 'advanced_expressions'
        
        html = widget.render('equation', r'\frac{\sqrt{x}}{2}')
        assert html is not None
        
        mode_config = load_mode('advanced_expressions')
        assert mode_config is not None
    
    def test_integrals_differentials_mode(self):
        """Test integrals_differentials mode."""
        widget = MathInputWidget(mode='integrals_differentials')
        assert widget.mode == 'integrals_differentials'
        
        html = widget.render('equation', r'\int_{0}^{1} f(x) dx')
        assert html is not None
        
        mode_config = load_mode('integrals_differentials')
        assert mode_config is not None
    
    def test_matrices_mode(self):
        """Test matrices mode."""
        widget = MathInputWidget(mode='matrices')
        assert widget.mode == 'matrices'
        
        html = widget.render('equation', r'\begin{pmatrix} a & b \\ c & d \end{pmatrix}')
        assert html is not None
        
        mode_config = load_mode('matrices')
        assert mode_config is not None
    
    def test_statistics_probability_mode(self):
        """Test statistics_probability mode."""
        widget = MathInputWidget(mode='statistics_probability')
        assert widget.mode == 'statistics_probability'
        
        html = widget.render('equation', r'\sum_{i=1}^{n} x_i')
        assert html is not None
        
        mode_config = load_mode('statistics_probability')
        assert mode_config is not None
    
    def test_physics_engineering_mode(self):
        """Test physics_engineering mode."""
        widget = MathInputWidget(mode='physics_engineering')
        assert widget.mode == 'physics_engineering'
        
        html = widget.render('equation', r'F = ma')
        assert html is not None
        
        mode_config = load_mode('physics_engineering')
        assert mode_config is not None
    
    def test_all_modes_valid(self):
        """Test that all modes are valid."""
        all_modes = [
            'regular_functions',
            'advanced_expressions',
            'integrals_differentials',
            'matrices',
            'statistics_probability',
            'physics_engineering',
        ]
        
        for mode in all_modes:
            assert is_valid_mode(mode), f"Mode {mode} should be valid"
            widget = MathInputWidget(mode=mode)
            assert widget.mode == mode


@pytest.mark.comprehensive
class TestAllPresetsFunctional:
    """
    What we are testing: All 6 presets are functional
    Why we are testing: All presets must work correctly
    Expected Result: Each preset loads and applies correctly
    """
    
    def test_algebra_preset(self):
        """Test algebra preset."""
        widget = MathInputWidget(preset='algebra')
        assert widget.preset == 'algebra'
        
        html = widget.render('equation', r'x^2 + y^2')
        assert html is not None
        
        preset_config = load_preset('algebra')
        assert preset_config is not None
        assert 'name' in preset_config  # Config has name field
    
    def test_calculus_preset(self):
        """Test calculus preset."""
        widget = MathInputWidget(preset='calculus')
        assert widget.preset == 'calculus'
        
        html = widget.render('equation', r'\int f(x) dx')
        assert html is not None
        
        preset_config = load_preset('calculus')
        assert preset_config is not None
    
    def test_physics_preset(self):
        """Test physics preset."""
        widget = MathInputWidget(preset='physics')
        assert widget.preset == 'physics'
        
        html = widget.render('equation', r'E = mc^2')
        assert html is not None
        
        preset_config = load_preset('physics')
        assert preset_config is not None
    
    def test_machine_learning_preset(self):
        """Test machine_learning preset."""
        widget = MathInputWidget(preset='machine_learning')
        assert widget.preset == 'machine_learning'
        
        html = widget.render('equation', r'\mathbf{X} = \begin{pmatrix} x_1 \\ x_2 \end{pmatrix}')
        assert html is not None
        
        preset_config = load_preset('machine_learning')
        assert preset_config is not None
    
    def test_statistics_preset(self):
        """Test statistics preset."""
        widget = MathInputWidget(preset='statistics')
        assert widget.preset == 'statistics'
        
        html = widget.render('equation', r'\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i')
        assert html is not None
        
        preset_config = load_preset('statistics')
        assert preset_config is not None
    
    def test_probability_preset(self):
        """Test probability preset."""
        widget = MathInputWidget(preset='probability')
        assert widget.preset == 'probability'
        
        html = widget.render('equation', r'P(A \cap B) = P(A) \cdot P(B)')
        assert html is not None
        
        preset_config = load_preset('probability')
        assert preset_config is not None
    
    def test_all_presets_valid(self):
        """Test that all presets are valid."""
        all_presets = [
            'algebra',
            'calculus',
            'physics',
            'machine_learning',
            'statistics',
            'probability',
        ]
        
        for preset in all_presets:
            assert is_valid_preset(preset), f"Preset {preset} should be valid"
            widget = MathInputWidget(preset=preset)
            assert widget.preset == preset
    
    def test_mode_preset_combinations(self):
        """Test that mode and preset combinations work."""
        combinations = [
            ('regular_functions', 'algebra'),
            ('integrals_differentials', 'calculus'),
            ('matrices', 'machine_learning'),
            ('statistics_probability', 'statistics'),
            ('statistics_probability', 'probability'),
            ('physics_engineering', 'physics'),
        ]
        
        for mode, preset in combinations:
            widget = MathInputWidget(mode=mode, preset=preset)
            assert widget.mode == mode
            assert widget.preset == preset
            
            html = widget.render('equation', r'\frac{1}{2}')
            assert html is not None

