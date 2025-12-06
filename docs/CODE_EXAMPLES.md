# MathInput Widget - Code Examples

Practical code examples for common use cases.

## Table of Contents

1. [Common Use Cases](#common-use-cases)
2. [Integration Examples](#integration-examples)
3. [Customization Examples](#customization-examples)

---

## Common Use Cases

### Example 1: Basic Math Form

**Use Case:** Simple equation input form

```python
# forms.py
from mathinput.widgets import MathInputWidget
from django import forms

class EquationForm(forms.Form):
    equation = forms.CharField(
        label="Enter Equation",
        widget=MathInputWidget(),
        help_text="Use the toolbar to build your formula"
    )
```

```django
<!-- template.html -->
{% load mathinput_tags %}

<form method="post">
    {% csrf_token %}
    <div class="form-group">
        {{ form.equation.label_tag }}
        {{ form.equation|as_mathinput }}
        {% if form.equation.help_text %}
            <small class="form-text text-muted">{{ form.equation.help_text }}</small>
        {% endif %}
        {% if form.equation.errors %}
            <div class="alert alert-danger">{{ form.equation.errors }}</div>
        {% endif %}
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### Example 2: Calculus Problem Form

**Use Case:** Calculus course with integrals and derivatives

```python
# forms.py
from mathinput.widgets import MathInputWidget
from django import forms

class CalculusForm(forms.Form):
    integral = forms.CharField(
        label="Integral",
        widget=MathInputWidget(
            mode='integrals_differentials',
            preset='calculus'
        )
    )
    derivative = forms.CharField(
        label="Derivative",
        widget=MathInputWidget(
            mode='integrals_differentials',
            preset='calculus'
        )
    )
```

```django
<!-- template.html -->
{% load mathinput_tags %}

<form method="post">
    {% csrf_token %}
    {{ form.integral.label_tag }}
    {{ form.integral|as_mathinput }}
    
    {{ form.derivative.label_tag }}
    {{ form.derivative|as_mathinput }}
    
    <button type="submit">Submit</button>
</form>
```

### Example 3: Matrix Operations Form

**Use Case:** Linear algebra or machine learning

```python
# forms.py
from mathinput.widgets import MathInputWidget
from django import forms

class MatrixForm(forms.Form):
    matrix_a = forms.CharField(
        label="Matrix A",
        widget=MathInputWidget(
            mode='matrices',
            preset='machine_learning'
        )
    )
    matrix_b = forms.CharField(
        label="Matrix B",
        widget=MathInputWidget(
            mode='matrices',
            preset='machine_learning'
        )
    )
```

### Example 4: Statistics Form

**Use Case:** Statistics or probability course

```python
# forms.py
from mathinput.widgets import MathInputWidget
from django import forms

class StatisticsForm(forms.Form):
    probability = forms.CharField(
        label="Probability Expression",
        widget=MathInputWidget(
            mode='statistics_probability',
            preset='probability'
        )
    )
    mean = forms.CharField(
        label="Mean Formula",
        widget=MathInputWidget(
            mode='statistics_probability',
            preset='statistics'
        )
    )
```

### Example 5: Physics Formula Form

**Use Case:** Physics or engineering course

```python
# forms.py
from mathinput.widgets import MathInputWidget
from django import forms

class PhysicsForm(forms.Form):
    formula = forms.CharField(
        label="Physics Formula",
        widget=MathInputWidget(
            mode='physics_engineering',
            preset='physics'
        )
    )
```

### Example 6: Display Stored Formulas

**Use Case:** Display previously saved formulas

```django
<!-- template.html -->
{% load mathinput_tags %}

<div class="problem">
    <h3>Problem 1</h3>
    <p>Solve the following equation:</p>
    <div class="formula-display">
        {{ problem.equation|render_math }}
    </div>
</div>

<div class="solution">
    <h3>Solution</h3>
    <p>The answer is:</p>
    <span class="inline-formula">{{ solution.answer|render_math_inline }}</span>
</div>
```

### Example 7: Form with Validation

**Use Case:** Form with server-side validation

```python
# forms.py
from mathinput.widgets import MathInputWidget
from mathinput.validators import MathInputValidator
from django import forms

class ValidatedMathForm(forms.Form):
    equation = forms.CharField(
        label="Equation",
        widget=MathInputWidget(),
        validators=[MathInputValidator()]
    )
    
    def clean_equation(self):
        equation = self.cleaned_data['equation']
        # Additional custom validation
        if len(equation) < 3:
            raise forms.ValidationError("Equation is too short")
        return equation
```

```python
# views.py
from django.shortcuts import render
from .forms import ValidatedMathForm

def math_form_view(request):
    if request.method == 'POST':
        form = ValidatedMathForm(request.POST)
        if form.is_valid():
            equation = form.cleaned_data['equation']
            # Process equation
            return render(request, 'success.html', {'equation': equation})
    else:
        form = ValidatedMathForm()
    
    return render(request, 'form.html', {'form': form})
```

---

## Integration Examples

### Example 1: Django Admin Integration

**Use Case:** Use widget in Django admin

```python
# admin.py
from django.contrib import admin
from mathinput.widgets import MathInputWidget
from .models import Problem

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': MathInputWidget()},
    }
    
    # Or specify field-specific widget
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['equation'].widget = MathInputWidget(
            mode='regular_functions'
        )
        return form
```

### Example 2: ModelForm Integration

**Use Case:** Use widget in ModelForm

```python
# models.py
from django.db import models

class MathProblem(models.Model):
    title = models.CharField(max_length=200)
    equation = models.TextField()
    solution = models.TextField()

# forms.py
from django.forms import ModelForm
from mathinput.widgets import MathInputWidget
from .models import MathProblem

class MathProblemForm(ModelForm):
    class Meta:
        model = MathProblem
        fields = ['title', 'equation', 'solution']
        widgets = {
            'equation': MathInputWidget(mode='regular_functions'),
            'solution': MathInputWidget(mode='regular_functions'),
        }
```

### Example 3: AJAX Form Submission

**Use Case:** Submit form via AJAX

```django
<!-- template.html -->
{% load mathinput_tags %}

<form id="math-form" method="post">
    {% csrf_token %}
    {{ form.equation|as_mathinput }}
    <button type="submit">Submit</button>
</form>

<script>
document.getElementById('math-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        // Handle response
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
</script>
```

### Example 4: Multiple Widgets on Same Page

**Use Case:** Multiple math inputs on one page

```python
# forms.py
from mathinput.widgets import MathInputWidget
from django import forms

class MultiMathForm(forms.Form):
    equation1 = forms.CharField(
        widget=MathInputWidget(mode='regular_functions')
    )
    equation2 = forms.CharField(
        widget=MathInputWidget(mode='integrals_differentials')
    )
    equation3 = forms.CharField(
        widget=MathInputWidget(mode='matrices')
    )
```

```django
<!-- template.html -->
{% load mathinput_tags %}

<form method="post">
    {% csrf_token %}
    {{ form.equation1|as_mathinput }}
    {{ form.equation2|as_mathinput }}
    {{ form.equation3|as_mathinput }}
    <button type="submit">Submit</button>
</form>
```

### Example 5: Template Filter with Parameters

**Use Case:** Use template filters with different modes

```django
<!-- template.html -->
{% load mathinput_tags %}

<!-- Basic mode -->
{{ form.equation|as_mathinput:"regular_functions" }}

<!-- Calculus mode with preset -->
{{ form.equation|as_mathinput:"mode=integrals_differentials,preset=calculus" }}

<!-- Matrix mode -->
{{ form.matrix|as_mathinput:"matrices" }}
```

---

## Customization Examples

### Example 1: Custom Validator

**Use Case:** Custom validation rules

```python
# validators.py
from django.core.exceptions import ValidationError
from mathinput.validators import MathInputValidator

class CustomMathValidator(MathInputValidator):
    def validate(self, latex_string: str) -> str:
        # Custom check: must contain at least one operator
        operators = ['+', '-', '*', '/', '=', '<', '>']
        if not any(op in latex_string for op in operators):
            raise ValidationError("Equation must contain at least one operator")
        
        # Call parent validation
        return super().validate(latex_string)
```

```python
# forms.py
from .validators import CustomMathValidator

class MyForm(forms.Form):
    equation = forms.CharField(
        widget=MathInputWidget(),
        validators=[CustomMathValidator()]
    )
```

### Example 2: Custom Widget Subclass

**Use Case:** Extended widget functionality

```python
# widgets.py
from mathinput.widgets import MathInputWidget

class CustomMathInputWidget(MathInputWidget):
    def __init__(self, *args, **kwargs):
        self.show_preview = kwargs.pop('show_preview', True)
        self.theme = kwargs.pop('theme', 'light')
        super().__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        
        # Add custom attributes
        if attrs is None:
            attrs = {}
        attrs['data-show-preview'] = str(self.show_preview).lower()
        attrs['data-theme'] = self.theme
        
        return html
```

### Example 3: Custom Template Filter

**Use Case:** Custom rendering with styling

```python
# templatetags/my_math_tags.py
from django import template
from mathinput.templatetags.mathinput_tags import render_math

register = template.Library()

@register.filter
def render_math_display(value, size='normal'):
    """Render math with custom display size."""
    result = render_math(value)
    size_class = f'math-size-{size}'
    return f'<div class="math-display {size_class}">{result}</div>'
```

```django
<!-- template.html -->
{% load my_math_tags %}

{{ formula|render_math_display:"large" }}
```

### Example 4: JavaScript Event Handling

**Use Case:** React to formula changes

```javascript
// static/js/custom_math.js
document.addEventListener('DOMContentLoaded', function() {
    const widgets = document.querySelectorAll('.mi-widget');
    
    widgets.forEach(function(widget) {
        const widgetId = widget.dataset.widgetId;
        const mathInput = window.MathInput.getInstance(widgetId);
        
        // Listen for formula changes
        mathInput.on('formulaChange', function(latex) {
            console.log('Formula changed:', latex);
            
            // Update preview or perform other actions
            updatePreview(latex);
        });
        
        // Listen for mode changes
        mathInput.on('modeChange', function(mode) {
            console.log('Mode changed:', mode);
        });
    });
    
    function updatePreview(latex) {
        // Custom preview update logic
        const preview = document.getElementById('custom-preview');
        if (preview) {
            preview.textContent = latex;
        }
    }
});
```

### Example 5: Custom CSS Styling

**Use Case:** Custom widget appearance

```css
/* static/css/mathinput_custom.css */

/* Custom widget container */
.mi-widget {
    border: 2px solid #007bff;
    border-radius: 8px;
    padding: 15px;
    background: #f8f9fa;
}

/* Custom toolbar */
.mi-toolbar {
    background: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 10px;
}

/* Custom buttons */
.mi-button {
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 12px;
    margin: 2px;
}

.mi-button:hover {
    background: #0056b3;
}

/* Custom visual builder */
.mi-visual-builder {
    min-height: 100px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 10px;
    background: white;
}
```

```django
<!-- template.html -->
{% load static %}
<link rel="stylesheet" href="{% static 'css/mathinput_custom.css' %}">
```

---

## Additional Resources

- **User Guide**: See `docs/USER_GUIDE.md`
- **Developer Guide**: See `docs/DEVELOPER_GUIDE.md`
- **API Documentation**: See `docs/API_DOCUMENTATION.md`

