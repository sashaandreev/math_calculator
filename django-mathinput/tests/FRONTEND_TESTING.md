# Frontend Testing Guide

This guide explains how to set up and run frontend tests for the `django-mathinput` package.

## Overview

Frontend tests are JavaScript tests that verify the client-side functionality of the math input widget, including:
- AST (Abstract Syntax Tree) engine
- LaTeX parsing and conversion
- Visual builder rendering
- Button click handlers
- Preview rendering
- Placeholder management

## Prerequisites

- Node.js (v14 or higher) and npm
- Access to the `django-mathinput` package directory

## Setup Instructions

### Step 1: Initialize npm in the package directory

```bash
cd django-mathinput
npm init -y
```

### Step 2: Install Jest and testing dependencies

```bash
npm install --save-dev jest @jest/globals jsdom jest-environment-jsdom
```

### Step 3: Create Jest configuration

Create `django-mathinput/jest.config.js`:

```javascript
module.exports = {
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/test_frontend_*.js'],
  setupFilesAfterEnv: ['<rootDir>/tests/jest.setup.js'],
  moduleNameMapper: {
    '^mathinput/(.*)$': '<rootDir>/mathinput/static/mathinput/$1',
  },
  collectCoverageFrom: [
    'mathinput/static/mathinput/js/**/*.js',
    '!mathinput/static/mathinput/js/**/*.min.js',
  ],
  coverageDirectory: 'tests/coverage',
  verbose: true,
};
```

### Step 4: Create Jest setup file

Create `django-mathinput/tests/jest.setup.js`:

```javascript
// Mock KaTeX if not available
if (typeof katex === 'undefined') {
  global.katex = {
    render: jest.fn((latex, container, options) => {
      if (options && options.throwOnError && latex.includes('error')) {
        throw new Error('KaTeX parse error');
      }
      container.innerHTML = `<span class="katex-rendered">${latex}</span>`;
    }),
  };
}

// Setup DOM environment
global.document = require('jsdom').jsdom().defaultView.document;
global.window = document.defaultView;
```

### Step 5: Update package.json scripts

Add to `django-mathinput/package.json`:

```json
{
  "scripts": {
    "test:frontend": "jest",
    "test:frontend:watch": "jest --watch",
    "test:frontend:coverage": "jest --coverage"
  }
}
```

## Running Tests

### Run all frontend tests

```bash
cd django-mathinput
npm run test:frontend
```

### Run tests in watch mode (for development)

```bash
npm run test:frontend:watch
```

### Run tests with coverage

```bash
npm run test:frontend:coverage
```

### Run specific test file

```bash
npm run test:frontend -- test_frontend_phase2.js
```

### Run tests matching a pattern

```bash
npm run test:frontend -- -t "AST Engine"
```

## Test File Structure

Frontend tests should be placed in `django-mathinput/tests/` with the naming pattern `test_frontend_*.js`.

Example structure:

```javascript
// tests/test_frontend_phase2.js
const fs = require('fs');
const path = require('path');

// Load the mathinput.js file
const mathinputPath = path.join(__dirname, '../mathinput/static/mathinput/js/mathinput.js');
const mathinputCode = fs.readFileSync(mathinputPath, 'utf8');

// Evaluate the code in the test environment
eval(mathinputCode);

describe('AST Engine', () => {
  test('parseLatex creates valid AST', () => {
    // Test implementation
  });
  
  // More tests...
});
```

## Testing the AST Engine

### Loading the JavaScript code

Since `mathinput.js` is wrapped in an IIFE (Immediately Invoked Function Expression), you need to load it properly:

```javascript
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// Create a DOM environment
const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>', {
  url: 'http://localhost',
  pretendToBeVisual: true,
  resources: 'usable',
});

global.window = dom.window;
global.document = dom.window.document;
global.Node = dom.window.Node;

// Load and execute mathinput.js
const mathinputPath = path.join(__dirname, '../mathinput/static/mathinput/js/mathinput.js');
const mathinputCode = fs.readFileSync(mathinputPath, 'utf8');
eval(mathinputCode);
```

### Example Test: AST Parsing

```javascript
describe('AST Engine', () => {
  test('parseLatex creates valid AST', () => {
    const latex = '\\frac{1}{2}';
    const ast = window.parseLatex(latex);
    
    expect(ast).toBeDefined();
    expect(ast.type).toBe(window.NodeTypes.FRACTION);
    expect(ast.children).toHaveLength(2);
  });
  
  test('astToLatex converts AST back to LaTeX', () => {
    const latex = 'x^2 + 1';
    const ast = window.parseLatex(latex);
    const converted = window.astToLatex(ast);
    
    // Should produce equivalent LaTeX
    expect(converted).toContain('x');
    expect(converted).toContain('^');
  });
});
```

## Testing Button Click Handlers

### Mock DOM elements

```javascript
describe('Button Click Handlers', () => {
  let widget, button, visualBuilderContainer;
  
  beforeEach(() => {
    // Create widget container
    widget = document.createElement('div');
    widget.id = 'test-widget';
    widget.className = 'mi-widget';
    document.body.appendChild(widget);
    
    // Create visual builder container
    visualBuilderContainer = document.createElement('div');
    visualBuilderContainer.className = 'mi-visual-builder';
    widget.appendChild(visualBuilderContainer);
    
    // Create hidden input
    const hiddenInput = document.createElement('textarea');
    hiddenInput.name = 'equation';
    hiddenInput.className = 'mi-hidden-input';
    hiddenInput.style.display = 'none';
    widget.appendChild(hiddenInput);
    
    // Create preview container
    const preview = document.createElement('div');
    preview.className = 'mi-preview';
    widget.appendChild(preview);
    
    // Create button
    button = document.createElement('button');
    button.className = 'mi-button';
    button.setAttribute('data-action', 'insert');
    button.setAttribute('data-template', '\\frac{}{}');
    widget.appendChild(button);
    
    // Initialize widget
    window.initializeMathInput('test-widget', {
      mode: 'regular_functions',
      preset: 'algebra',
      value: '',
    });
  });
  
  afterEach(() => {
    document.body.removeChild(widget);
  });
  
  test('button click inserts template', () => {
    window.handleButtonClick(button, widget);
    
    const hiddenInput = widget.querySelector('.mi-hidden-input');
    expect(hiddenInput.value).toContain('\\frac');
  });
});
```

## Testing Preview Rendering

### Mock KaTeX

```javascript
// In jest.setup.js or test file
global.katex = {
  render: jest.fn((latex, container, options) => {
    if (options && options.throwOnError) {
      if (latex.includes('error') || latex.includes('\\invalid')) {
        throw new Error('KaTeX parse error');
      }
    }
    container.innerHTML = `<span class="katex">${latex}</span>`;
  }),
};

describe('Preview Rendering', () => {
  test('KaTeX renders valid LaTeX', () => {
    const container = document.createElement('div');
    window.renderPreview('x^2 + 1', container);
    
    expect(global.katex.render).toHaveBeenCalled();
    expect(container.innerHTML).toContain('katex');
  });
  
  test('render error displayed for invalid LaTeX', () => {
    const container = document.createElement('div');
    window.renderPreview('\\invalid{command}', container);
    
    expect(container.classList.contains('mi-preview-error')).toBe(true);
  });
});
```

## Testing Visual Builder

```javascript
describe('VisualBuilder', () => {
  test('VisualBuilder renders AST structure', () => {
    const container = document.createElement('div');
    const ast = window.parseLatex('\\frac{1}{2}');
    const builder = new window.VisualBuilder(container, ast);
    
    builder.render();
    
    expect(container.querySelector('.mi-fraction')).toBeDefined();
    expect(container.querySelectorAll('.mi-placeholder').length).toBeGreaterThan(0);
  });
});
```

## Testing Placeholder Management

```javascript
describe('PlaceholderManager', () => {
  test('PlaceholderManager extracts placeholders', () => {
    const container = document.createElement('div');
    const ast = window.parseLatex('\\frac{}{}');
    const builder = new window.VisualBuilder(container, ast);
    
    builder.render();
    
    const placeholders = builder.placeholderManager.placeholders;
    expect(placeholders.length).toBe(2); // numerator and denominator
  });
});
```

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/frontend-tests.yml`:

```yaml
name: Frontend Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: |
        cd django-mathinput
        npm install
    
    - name: Run frontend tests
      run: |
        cd django-mathinput
        npm run test:frontend
```

## Troubleshooting

### Issue: `window is not defined`

**Solution:** Ensure you're using `jsdom` test environment and setting up the DOM properly in your test setup file.

### Issue: `katex is not defined`

**Solution:** Mock KaTeX in your `jest.setup.js` file as shown above.

### Issue: Tests can't find `mathinput.js`

**Solution:** Use absolute paths with `path.join(__dirname, ...)` to locate the file.

### Issue: IIFE code not executing

**Solution:** Use `eval()` to execute the JavaScript code, or refactor `mathinput.js` to export functions for testing.

## Best Practices

1. **Isolate tests**: Each test should be independent and not rely on other tests
2. **Mock external dependencies**: Mock KaTeX, DOM APIs, etc.
3. **Use descriptive test names**: Test names should clearly describe what is being tested
4. **Test edge cases**: Include tests for empty inputs, invalid LaTeX, etc.
5. **Maintain test coverage**: Aim for >80% coverage of JavaScript code

## Next Steps

1. Create `test_frontend_phase2.js` with the tests from the implementation plan
2. Run tests and fix any issues
3. Add tests for Phase 3 features as they are implemented
4. Set up CI/CD to run frontend tests automatically

## Additional Resources

- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [jsdom Documentation](https://github.com/jsdom/jsdom)
- [Testing JavaScript with Jest](https://jestjs.io/docs/tutorial-jquery)

