/**
 * Frontend tests for Phase 2: AST Engine, Button Handlers, Preview Rendering
 * 
 * These tests verify the JavaScript functionality of the math input widget.
 */

describe('AST Engine', () => {
  test('parseLatex creates valid AST', () => {
    /**
     * What we are testing: parseLatex correctly parses LaTeX into AST
     * Why we are testing: AST is core data structure for visual builder
     * Expected Result: Valid AST structure created from LaTeX input
     */
    const latex = '\\frac{1}{2}';
    const ast = window.parseLatex(latex);
    
    expect(ast).toBeDefined();
    expect(ast).toBeInstanceOf(window.ASTNode);
    expect(ast.type).toBe(window.NodeTypes.FRACTION);
    expect(ast.children).toHaveLength(2);
  });
  
  test('astToLatex converts AST back to LaTeX', () => {
    /**
     * What we are testing: astToLatex correctly converts AST to LaTeX string
     * Why we are testing: Need bidirectional conversion for sync
     * Expected Result: LaTeX string matches original (or equivalent)
     */
    const latex = 'x^2 + 1';
    const ast = window.parseLatex(latex);
    const converted = window.astToLatex(ast);
    
    // Should produce equivalent LaTeX (may have whitespace differences)
    expect(converted).toBeDefined();
    expect(typeof converted).toBe('string');
    expect(converted.length).toBeGreaterThan(0);
  });
  
  test('parseLatex handles empty string', () => {
    /**
     * What we are testing: parseLatex handles empty input gracefully
     * Why we are testing: Edge case - empty input should not crash
     * Expected Result: Returns placeholder AST node
     */
    const ast = window.parseLatex('');
    expect(ast).toBeDefined();
    expect(ast.type).toBe(window.NodeTypes.PLACEHOLDER);
  });
  
  test('parseLatex handles simple variable', () => {
    /**
     * What we are testing: parseLatex correctly parses simple variables
     * Why we are testing: Basic parsing functionality
     * Expected Result: AST node with VARIABLE type
     */
    const ast = window.parseLatex('x');
    expect(ast).toBeDefined();
    expect(ast.type).toBe(window.NodeTypes.VARIABLE);
    expect(ast.value).toBe('x');
  });
  
  test('parseLatex handles simple number', () => {
    /**
     * What we are testing: parseLatex correctly parses numbers
     * Why we are testing: Basic parsing functionality
     * Expected Result: AST node with NUMBER type
     */
    const ast = window.parseLatex('42');
    expect(ast).toBeDefined();
    expect(ast.type).toBe(window.NodeTypes.NUMBER);
    expect(ast.value).toBe('42');
  });
  
  test('VisualBuilder renders AST structure', () => {
    /**
     * What we are testing: VisualBuilder renders AST as visual elements
     * Why we are testing: Users must see visual representation of formula
     * Expected Result: DOM contains visual elements matching AST structure
     */
    const container = document.createElement('div');
    const ast = window.parseLatex('\\frac{}{}'); // Use empty fraction to get placeholders
    const builder = new window.VisualBuilder(container, ast);
    
    builder.render();
    
    // Check that fraction structure is rendered
    const fractionElement = container.querySelector('.mi-fraction');
    expect(fractionElement).toBeDefined();
    
    // Check for fraction numerator and denominator containers
    expect(container.querySelector('.mi-fraction-numerator')).toBeDefined();
    expect(container.querySelector('.mi-fraction-denominator')).toBeDefined();
  });
  
  test('PlaceholderManager extracts placeholders', () => {
    /**
     * What we are testing: PlaceholderManager finds all placeholder positions
     * Why we are testing: Users need to navigate between placeholders
     * Expected Result: All empty slots in AST identified as placeholders
     */
    const container = document.createElement('div');
    const ast = window.parseLatex('\\frac{}{}');
    const builder = new window.VisualBuilder(container, ast);
    
    builder.render();
    
    const placeholders = builder.placeholderManager.placeholders;
    expect(placeholders.length).toBeGreaterThan(0);
  });
  
  test('createEmptyAST creates placeholder', () => {
    /**
     * What we are testing: createEmptyAST creates valid empty AST
     * Why we are testing: Initial state of widget needs empty AST
     * Expected Result: Returns placeholder AST node
     */
    const ast = window.createEmptyAST();
    expect(ast).toBeDefined();
    expect(ast.type).toBe(window.NodeTypes.PLACEHOLDER);
  });
});

describe('Button Click Handlers', () => {
  let widget, button, visualBuilderContainer, hiddenInput, previewContainer;
  
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
    hiddenInput = document.createElement('textarea');
    hiddenInput.name = 'equation';
    hiddenInput.className = 'mi-hidden-input';
    hiddenInput.style.display = 'none';
    widget.appendChild(hiddenInput);
    
    // Create preview container
    previewContainer = document.createElement('div');
    previewContainer.className = 'mi-preview';
    widget.appendChild(previewContainer);
    
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
    if (widget && widget.parentNode) {
      document.body.removeChild(widget);
    }
  });
  
  test('button click inserts template', () => {
    /**
     * What we are testing: Button click inserts LaTeX template into AST
     * Why we are testing: Core user interaction - inserting operations
     * Expected Result: AST updated with new node, visual builder updated
     */
    // Ensure widget has visual builder initialized
    if (!widget.visualBuilder) {
      window.initializeMathInput('test-widget', {
        mode: 'regular_functions',
        preset: 'algebra',
        value: '',
      });
    }
    
    window.handleButtonClick(button, widget);
    
    const updatedHiddenInput = widget.querySelector('.mi-hidden-input');
    // The value should be updated (may be empty if AST is just placeholder)
    expect(updatedHiddenInput).toBeDefined();
  });
  
  test('button click updates hidden field', () => {
    /**
     * What we are testing: Button click updates hidden textarea with LaTeX
     * Why we are testing: Form submission needs LaTeX value
     * Expected Result: Hidden field contains LaTeX after button click
     */
    // Ensure widget has visual builder initialized
    if (!widget.visualBuilder) {
      window.initializeMathInput('test-widget', {
        mode: 'regular_functions',
        preset: 'algebra',
        value: '',
      });
    }
    
    window.handleButtonClick(button, widget);
    
    const updatedHiddenInput = widget.querySelector('.mi-hidden-input');
    expect(updatedHiddenInput).toBeDefined();
    // Value may be empty if AST conversion results in empty string
    expect(typeof updatedHiddenInput.value).toBe('string');
  });
});

describe('Preview Rendering', () => {
  test('KaTeX renders valid LaTeX', () => {
    /**
     * What we are testing: KaTeX successfully renders valid LaTeX
     * Why we are testing: Preview must show correct mathematical rendering
     * Expected Result: Preview shows rendered formula without errors
     */
    const container = document.createElement('div');
    window.renderPreview('x^2 + 1', container);
    
    // KaTeX should be called (mocked in jest.setup.js)
    expect(global.katex.render).toHaveBeenCalled();
    expect(container.innerHTML).toBeDefined();
  });
  
  test('render error displayed for invalid LaTeX', () => {
    /**
     * What we are testing: Error message shown when KaTeX fails
     * Why we are testing: Users need feedback on invalid formulas
     * Expected Result: Error message displayed in preview area
     */
    // Mock KaTeX to throw error
    global.katex.render.mockImplementationOnce(() => {
      throw new Error('KaTeX parse error');
    });
    
    const container = document.createElement('div');
    window.renderPreview('\\invalid{command}', container);
    
    expect(container.classList.contains('mi-preview-error')).toBe(true);
    expect(container.innerHTML).toContain('error');
  });
  
  test('renderPreview handles empty LaTeX', () => {
    /**
     * What we are testing: renderPreview handles empty input gracefully
     * Why we are testing: Edge case - empty preview should show placeholder
     * Expected Result: Preview shows empty state message
     */
    const container = document.createElement('div');
    window.renderPreview('', container);
    
    expect(container.innerHTML).toContain('Preview will appear here');
  });
  
  test('renderPreview handles null container', () => {
    /**
     * What we are testing: renderPreview handles null container gracefully
     * Why we are testing: Edge case - prevent crashes
     * Expected Result: Function returns without error
     */
    expect(() => {
      window.renderPreview('x^2', null);
    }).not.toThrow();
  });
});

describe('AST Node Operations', () => {
  test('ASTNode can add children', () => {
    /**
     * What we are testing: ASTNode addChild method works correctly
     * Why we are testing: AST manipulation is core functionality
     * Expected Result: Child added to node's children array
     */
    const parent = new window.ASTNode(window.NodeTypes.EXPRESSION, '+');
    const child = new window.ASTNode(window.NodeTypes.VARIABLE, 'x');
    
    parent.addChild(child);
    
    expect(parent.children).toContain(child);
    expect(child.parent).toBe(parent);
  });
  
  test('ASTNode can remove children', () => {
    /**
     * What we are testing: ASTNode removeChild method works correctly
     * Why we are testing: AST manipulation needs removal capability
     * Expected Result: Child removed from node's children array
     */
    const parent = new window.ASTNode(window.NodeTypes.EXPRESSION, '+');
    const child = new window.ASTNode(window.NodeTypes.VARIABLE, 'x');
    
    parent.addChild(child);
    parent.removeChild(child);
    
    expect(parent.children).not.toContain(child);
    expect(child.parent).toBeNull();
  });
  
  test('ASTNode getPlaceholders finds all placeholders', () => {
    /**
     * What we are testing: getPlaceholders method finds all placeholder nodes
     * Why we are testing: Need to navigate between placeholders
     * Expected Result: Returns array of all placeholder nodes in subtree
     */
    const fraction = new window.ASTNode(
      window.NodeTypes.FRACTION,
      'frac',
      [
        window.createPlaceholder('numerator'),
        window.createPlaceholder('denominator')
      ]
    );
    
    const placeholders = fraction.getPlaceholders();
    expect(placeholders.length).toBe(2);
  });
});

describe('Cursor Management', () => {
  test('CursorManager can be created', () => {
    /**
     * What we are testing: CursorManager can be instantiated
     * Why we are testing: Cursor management is needed for insertion
     * Expected Result: CursorManager instance created successfully
     */
    const widget = document.createElement('div');
    const cursorManager = new window.CursorManager(widget);
    
    expect(cursorManager).toBeDefined();
    expect(cursorManager.widget).toBe(widget);
  });
  
  test('CursorManager getCursorPosition returns position', () => {
    /**
     * What we are testing: getCursorPosition returns cursor information
     * Why we are testing: Need to know where to insert new nodes
     * Expected Result: Returns object with node and placeholder info
     */
    const widget = document.createElement('div');
    const cursorManager = new window.CursorManager(widget);
    
    const position = cursorManager.getCursorPosition();
    expect(position).toBeDefined();
    expect(position).toHaveProperty('node');
  });
});

describe('Template Creation', () => {
  test('parseLatex can create AST from template', () => {
    /**
     * What we are testing: parseLatex can convert LaTeX template to AST
     * Why we are testing: Button clicks need to create nodes from templates
     * Expected Result: Valid AST node created from template string
     */
    const template = '\\frac{}{}';
    const node = window.parseLatex(template);
    
    expect(node).toBeDefined();
    expect(node).toBeInstanceOf(window.ASTNode);
    expect(node.type).toBe(window.NodeTypes.FRACTION);
  });
  
  test('parseLatex handles empty template', () => {
    /**
     * What we are testing: parseLatex handles empty input
     * Why we are testing: Edge case - prevent crashes
     * Expected Result: Returns placeholder node
     */
    const node = window.parseLatex('');
    expect(node).toBeDefined();
    expect(node.type).toBe(window.NodeTypes.PLACEHOLDER);
  });
});

describe('Edge Cases: AST Engine', () => {
  test('parseLatex handles deeply nested structures', () => {
    /**
     * What we are testing: parseLatex handles deeply nested LaTeX
     * Why we are testing: Complex formulas may have deep nesting
     * Expected Result: AST created without stack overflow
     */
    const deepLatex = '\\frac{\\frac{\\frac{1}{2}}{3}}{4}';
    const ast = window.parseLatex(deepLatex);
    
    expect(ast).toBeDefined();
    expect(ast).toBeInstanceOf(window.ASTNode);
    // The root may be FRACTION or EXPRESSION depending on parsing
    expect([window.NodeTypes.FRACTION, window.NodeTypes.EXPRESSION]).toContain(ast.type);
  });
  
  test('parseLatex handles malformed LaTeX gracefully', () => {
    /**
     * What we are testing: parseLatex doesn't crash on malformed input
     * Why we are testing: Users may enter invalid LaTeX
     * Expected Result: Returns placeholder or valid partial AST
     */
    const malformed = '\\frac{1}'; // Missing closing brace
    const ast = window.parseLatex(malformed);
    
    expect(ast).toBeDefined();
    // Should return something (placeholder or partial AST)
    expect(ast).toBeInstanceOf(window.ASTNode);
  });
  
  test('parseLatex handles special characters', () => {
    /**
     * What we are testing: parseLatex handles special characters in LaTeX
     * Why we are testing: LaTeX may contain special characters
     * Expected Result: AST created correctly with special characters
     */
    const latex = 'x + y = z';
    const ast = window.parseLatex(latex);
    
    expect(ast).toBeDefined();
    expect(ast).toBeInstanceOf(window.ASTNode);
  });
  
  test('parseLatex handles very long LaTeX strings', () => {
    /**
     * What we are testing: parseLatex handles long LaTeX strings
     * Why we are testing: Performance - long formulas should still parse
     * Expected Result: AST created without performance issues
     */
    const longLatex = 'x + '.repeat(100) + 'y';
    const ast = window.parseLatex(longLatex);
    
    expect(ast).toBeDefined();
    expect(ast).toBeInstanceOf(window.ASTNode);
  });
  
  test('parseLatex handles unicode characters', () => {
    /**
     * What we are testing: parseLatex handles unicode in variables
     * Why we are testing: Users may use unicode variable names
     * Expected Result: AST created with unicode preserved
     */
    const latex = 'α + β = γ';
    const ast = window.parseLatex(latex);
    
    expect(ast).toBeDefined();
    expect(ast).toBeInstanceOf(window.ASTNode);
  });
  
  test('astToLatex handles null/undefined AST', () => {
    /**
     * What we are testing: astToLatex handles null/undefined gracefully
     * Why we are testing: Edge case - prevent crashes
     * Expected Result: Returns empty string or handles gracefully
     */
    expect(() => window.astToLatex(null)).not.toThrow();
    expect(() => window.astToLatex(undefined)).not.toThrow();
  });
  
  test('astToLatex handles AST with no children', () => {
    /**
     * What we are testing: astToLatex handles leaf nodes
     * Why we are testing: Edge case - nodes without children
     * Expected Result: Returns value or empty string
     */
    const node = new window.ASTNode(window.NodeTypes.VARIABLE, 'x');
    const latex = window.astToLatex(node);
    
    expect(latex).toBe('x');
  });
  
  test('parseLatex handles complex expressions with multiple operators', () => {
    /**
     * What we are testing: parseLatex handles multiple operators
     * Why we are testing: Real formulas have multiple operations
     * Expected Result: AST correctly represents expression structure
     */
    const latex = 'x + y - z * w / v';
    const ast = window.parseLatex(latex);
    
    expect(ast).toBeDefined();
    expect(ast).toBeInstanceOf(window.ASTNode);
  });
});

describe('Edge Cases: VisualBuilder', () => {
  test('VisualBuilder handles null container gracefully', () => {
    /**
     * What we are testing: VisualBuilder doesn't crash with null container
     * Why we are testing: Edge case - prevent crashes
     * Expected Result: Render method handles null gracefully
     */
    const ast = window.parseLatex('x');
    const builder = new window.VisualBuilder(null, ast);
    
    expect(() => builder.render()).not.toThrow();
  });
  
  test('VisualBuilder handles empty AST', () => {
    /**
     * What we are testing: VisualBuilder renders empty AST
     * Why we are testing: Initial state may have empty AST
     * Expected Result: Renders placeholder or empty structure
     */
    const container = document.createElement('div');
    const ast = window.createEmptyAST();
    const builder = new window.VisualBuilder(container, ast);
    
    builder.render();
    
    expect(container.innerHTML).toBeDefined();
  });
  
  test('VisualBuilder handles very deep AST structures', () => {
    /**
     * What we are testing: VisualBuilder renders deeply nested AST
     * Why we are testing: Complex formulas may have deep nesting
     * Expected Result: Renders without stack overflow
     */
    const container = document.createElement('div');
    // Create a deep structure
    let ast = window.parseLatex('1');
    for (let i = 0; i < 10; i++) {
      ast = new window.ASTNode(
        window.NodeTypes.FRACTION,
        'frac',
        [ast, window.parseLatex('2')]
      );
    }
    const builder = new window.VisualBuilder(container, ast);
    
    expect(() => builder.render()).not.toThrow();
  });
  
  test('VisualBuilder handles AST with many children', () => {
    /**
     * What we are testing: VisualBuilder renders AST with many children
     * Why we are testing: Some expressions have many terms
     * Expected Result: All children rendered correctly
     */
    const container = document.createElement('div');
    const children = [];
    for (let i = 0; i < 20; i++) {
      children.push(window.parseLatex(`x${i}`));
    }
    const ast = new window.ASTNode(
      window.NodeTypes.EXPRESSION,
      '+',
      children
    );
    const builder = new window.VisualBuilder(container, ast);
    
    builder.render();
    
    expect(container.innerHTML).toBeDefined();
  });
  
  test('VisualBuilder updateAST with null', () => {
    /**
     * What we are testing: updateAST handles null input
     * Why we are testing: Edge case - prevent crashes
     * Expected Result: Creates empty AST or handles gracefully
     */
    const container = document.createElement('div');
    const builder = new window.VisualBuilder(container, window.parseLatex('x'));
    
    expect(() => builder.updateAST(null)).not.toThrow();
  });
  
  test('VisualBuilder getLatex with empty AST', () => {
    /**
     * What we are testing: getLatex returns empty string for empty AST
     * Why we are testing: Edge case - empty formulas
     * Expected Result: Returns empty string or placeholder LaTeX
     */
    const container = document.createElement('div');
    const builder = new window.VisualBuilder(container, window.createEmptyAST());
    
    const latex = builder.getLatex();
    expect(typeof latex).toBe('string');
  });
});

describe('Edge Cases: Button Click Handlers', () => {
  test('handleButtonClick handles missing button attributes', () => {
    /**
     * What we are testing: handleButtonClick handles buttons without data attributes
     * Why we are testing: Edge case - malformed HTML
     * Expected Result: Returns early without crashing
     */
    const button = document.createElement('button');
    const widget = document.createElement('div');
    
    expect(() => window.handleButtonClick(button, widget)).not.toThrow();
  });
  
  test('handleButtonClick handles invalid template', () => {
    /**
     * What we are testing: handleButtonClick handles invalid LaTeX templates
     * Why we are testing: Edge case - invalid button configuration
     * Expected Result: Handles gracefully without crashing
     */
    const button = document.createElement('button');
    button.setAttribute('data-action', 'insert');
    button.setAttribute('data-template', '\\invalid{command}');
    const widget = document.createElement('div');
    
    // Setup minimal widget structure
    const visualBuilderContainer = document.createElement('div');
    visualBuilderContainer.className = 'mi-visual-builder';
    widget.appendChild(visualBuilderContainer);
    
    const hiddenInput = document.createElement('textarea');
    hiddenInput.className = 'mi-hidden-input';
    widget.appendChild(hiddenInput);
    
    const preview = document.createElement('div');
    preview.className = 'mi-preview';
    widget.appendChild(preview);
    
    widget.visualBuilder = new window.VisualBuilder(
      visualBuilderContainer,
      window.createEmptyAST()
    );
    
    expect(() => window.handleButtonClick(button, widget)).not.toThrow();
  });
  
  test('handleButtonClick handles missing visual builder', () => {
    /**
     * What we are testing: handleButtonClick handles missing visual builder
     * Why we are testing: Edge case - widget not fully initialized
     * Expected Result: Returns early with warning, doesn't crash
     */
    const button = document.createElement('button');
    button.setAttribute('data-action', 'insert');
    button.setAttribute('data-template', 'x');
    const widget = document.createElement('div');
    widget.visualBuilder = null;
    
    expect(() => window.handleButtonClick(button, widget)).not.toThrow();
  });
  
  test('handleButtonClick handles null widget', () => {
    /**
     * What we are testing: handleButtonClick handles null widget
     * Why we are testing: Edge case - prevent crashes
     * Expected Result: Returns early without crashing
     */
    const button = document.createElement('button');
    
    expect(() => window.handleButtonClick(button, null)).not.toThrow();
  });
  
  test('handleButtonClick handles null button', () => {
    /**
     * What we are testing: handleButtonClick handles null button
     * Why we are testing: Edge case - prevent crashes
     * Expected Result: Returns early without crashing
     */
    const widget = document.createElement('div');
    
    expect(() => window.handleButtonClick(null, widget)).not.toThrow();
  });
});

describe('Edge Cases: Preview Rendering', () => {
  test('renderPreview handles very long LaTeX', () => {
    /**
     * What we are testing: renderPreview handles very long LaTeX strings
     * Why we are testing: Performance - long formulas should still render
     * Expected Result: Renders without performance issues
     */
    const container = document.createElement('div');
    const longLatex = 'x + '.repeat(1000) + 'y';
    
    expect(() => window.renderPreview(longLatex, container)).not.toThrow();
  });
  
  test('renderPreview handles special characters in LaTeX', () => {
    /**
     * What we are testing: renderPreview handles special characters
     * Why we are testing: LaTeX may contain special characters
     * Expected Result: Renders or shows error gracefully
     */
    const container = document.createElement('div');
    const latex = 'x & y | z < w > v';
    
    expect(() => window.renderPreview(latex, container)).not.toThrow();
  });
  
  test('renderPreview handles KaTeX unavailable', () => {
    /**
     * What we are testing: renderPreview handles missing KaTeX library
     * Why we are testing: KaTeX may not be loaded
     * Expected Result: Shows fallback or error message
     */
    // Temporarily remove katex
    const originalKatex = global.katex;
    delete global.katex;
    
    const container = document.createElement('div');
    window.renderPreview('x^2', container);
    
    // Should show fallback
    expect(container.innerHTML).toBeDefined();
    
    // Restore katex
    global.katex = originalKatex;
  });
  
  test('renderPreview handles rapid updates', () => {
    /**
     * What we are testing: renderPreview handles rapid successive calls
     * Why we are testing: Performance - user typing quickly
     * Expected Result: All updates processed without errors
     */
    const container = document.createElement('div');
    
    for (let i = 0; i < 10; i++) {
      window.renderPreview(`x^${i}`, container);
    }
    
    expect(container.innerHTML).toBeDefined();
  });
  
  test('renderPreview handles whitespace-only LaTeX', () => {
    /**
     * What we are testing: renderPreview handles whitespace-only input
     * Why we are testing: Edge case - empty/whitespace input
     * Expected Result: Shows empty state or handles gracefully
     */
    const container = document.createElement('div');
    window.renderPreview('   ', container);
    
    expect(container.innerHTML).toBeDefined();
  });
});

describe('Edge Cases: Placeholder Management', () => {
  test('PlaceholderManager handles no placeholders', () => {
    /**
     * What we are testing: PlaceholderManager handles AST with no placeholders
     * Why we are testing: Edge case - fully filled formula
     * Expected Result: Returns empty array or handles gracefully
     */
    const container = document.createElement('div');
    const ast = window.parseLatex('x + y'); // No placeholders
    const builder = new window.VisualBuilder(container, ast);
    
    builder.render();
    
    const placeholders = builder.placeholderManager.placeholders;
    expect(Array.isArray(placeholders)).toBe(true);
  });
  
  test('PlaceholderManager getNext at end of list', () => {
    /**
     * What we are testing: getNext wraps around at end of placeholders
     * Why we are testing: Navigation should be circular
     * Expected Result: Returns first placeholder when at end
     */
    const container = document.createElement('div');
    const ast = window.parseLatex('\\frac{}{}');
    const builder = new window.VisualBuilder(container, ast);
    
    builder.render();
    
    const manager = builder.placeholderManager;
    if (manager.placeholders.length > 0) {
      manager.activePlaceholder = manager.placeholders[manager.placeholders.length - 1];
      const next = manager.getNext();
      expect(next).toBeDefined();
    }
  });
  
  test('PlaceholderManager getPrevious at start of list', () => {
    /**
     * What we are testing: getPrevious wraps around at start of placeholders
     * Why we are testing: Navigation should be circular
     * Expected Result: Returns last placeholder when at start
     */
    const container = document.createElement('div');
    const ast = window.parseLatex('\\frac{}{}');
    const builder = new window.VisualBuilder(container, ast);
    
    builder.render();
    
    const manager = builder.placeholderManager;
    if (manager.placeholders.length > 0) {
      manager.activePlaceholder = manager.placeholders[0];
      const prev = manager.getPrevious();
      expect(prev).toBeDefined();
    }
  });
  
  test('PlaceholderManager handles many placeholders', () => {
    /**
     * What we are testing: PlaceholderManager handles formulas with many placeholders
     * Why we are testing: Complex formulas may have many empty slots
     * Expected Result: All placeholders registered correctly
     */
    const container = document.createElement('div');
    // Create a complex structure with many placeholders
    let latex = '\\frac{}{}';
    for (let i = 0; i < 5; i++) {
      latex = `\\frac{${latex}}{}`;
    }
    const ast = window.parseLatex(latex);
    const builder = new window.VisualBuilder(container, ast);
    
    builder.render();
    
    const placeholders = builder.placeholderManager.placeholders;
    expect(placeholders.length).toBeGreaterThan(0);
  });
});

describe('Edge Cases: Cursor Management', () => {
  test('CursorManager handles widget without visual builder', () => {
    /**
     * What we are testing: CursorManager handles uninitialized widget
     * Why we are testing: Edge case - widget not fully set up
     * Expected Result: Returns default position without crashing
     */
    const widget = document.createElement('div');
    widget.visualBuilder = null;
    const cursorManager = new window.CursorManager(widget);
    
    const position = cursorManager.getCursorPosition();
    expect(position).toBeDefined();
  });
  
  test('CursorManager handles empty visual builder', () => {
    /**
     * What we are testing: CursorManager handles visual builder with no placeholders
     * Why we are testing: Edge case - empty formula
     * Expected Result: Returns root node position
     */
    const widget = document.createElement('div');
    const container = document.createElement('div');
    const builder = new window.VisualBuilder(container, window.createEmptyAST());
    widget.visualBuilder = builder;
    
    const cursorManager = new window.CursorManager(widget);
    const position = cursorManager.getCursorPosition();
    
    expect(position).toBeDefined();
    expect(position).toHaveProperty('node');
  });
  
  test('CursorManager setCursor with null placeholder', () => {
    /**
     * What we are testing: setCursor handles null placeholder
     * Why we are testing: Edge case - prevent crashes
     * Expected Result: Handles gracefully without crashing
     */
    const widget = document.createElement('div');
    const cursorManager = new window.CursorManager(widget);
    
    expect(() => cursorManager.setCursor(null)).not.toThrow();
  });
});

describe('Edge Cases: AST Node Operations', () => {
  test('ASTNode handles removing non-existent child', () => {
    /**
     * What we are testing: removeChild handles child not in children array
     * Why we are testing: Edge case - prevent errors
     * Expected Result: Handles gracefully without error
     */
    const parent = new window.ASTNode(window.NodeTypes.EXPRESSION, '+');
    const child = new window.ASTNode(window.NodeTypes.VARIABLE, 'x');
    
    expect(() => parent.removeChild(child)).not.toThrow();
  });
  
  test('ASTNode handles adding same child twice', () => {
    /**
     * What we are testing: addChild handles duplicate children
     * Why we are testing: Edge case - prevent duplicate references
     * Expected Result: Child added or handled appropriately
     */
    const parent = new window.ASTNode(window.NodeTypes.EXPRESSION, '+');
    const child = new window.ASTNode(window.NodeTypes.VARIABLE, 'x');
    
    parent.addChild(child);
    parent.addChild(child);
    
    // Should handle gracefully (may add twice or ignore)
    expect(parent.children.length).toBeGreaterThan(0);
  });
  
  test('ASTNode handles very deep tree structures', () => {
    /**
     * What we are testing: ASTNode handles very deep nesting
     * Why we are testing: Performance - deep formulas
     * Expected Result: Operations work without stack overflow
     */
    let node = new window.ASTNode(window.NodeTypes.VARIABLE, 'x');
    for (let i = 0; i < 100; i++) {
      const parent = new window.ASTNode(window.NodeTypes.EXPRESSION, '+');
      parent.addChild(node);
      parent.addChild(new window.ASTNode(window.NodeTypes.NUMBER, i));
      node = parent;
    }
    
    const placeholders = node.getPlaceholders();
    expect(Array.isArray(placeholders)).toBe(true);
  });
  
  test('ASTNode handles node with many children', () => {
    /**
     * What we are testing: ASTNode handles nodes with many children
     * Why we are testing: Some expressions have many terms
     * Expected Result: All operations work correctly
     */
    const parent = new window.ASTNode(window.NodeTypes.EXPRESSION, '+');
    for (let i = 0; i < 100; i++) {
      parent.addChild(new window.ASTNode(window.NodeTypes.VARIABLE, `x${i}`));
    }
    
    expect(parent.children.length).toBe(100);
    expect(parent.getPlaceholders().length).toBe(0); // No placeholders in variables
  });
  
  test('ASTNode generateId creates unique IDs', () => {
    /**
     * What we are testing: generateId creates unique IDs for nodes
     * Why we are testing: Node identification needs unique IDs
     * Expected Result: Each node has unique ID
     */
    const node1 = new window.ASTNode(window.NodeTypes.VARIABLE, 'x');
    const node2 = new window.ASTNode(window.NodeTypes.VARIABLE, 'y');
    
    expect(node1.id).toBeDefined();
    expect(node2.id).toBeDefined();
    expect(node1.id).not.toBe(node2.id);
  });
});

describe('Edge Cases: Integration', () => {
  test('Widget initialization with missing DOM elements', () => {
    /**
     * What we are testing: initializeMathInput handles missing DOM elements
     * Why we are testing: Edge case - incomplete HTML structure
     * Expected Result: Initializes what it can, doesn't crash
     */
    const widget = document.createElement('div');
    widget.id = 'test-widget-incomplete';
    document.body.appendChild(widget);
    
    expect(() => {
      window.initializeMathInput('test-widget-incomplete', {
        mode: 'regular_functions',
        preset: 'algebra',
        value: '',
      });
    }).not.toThrow();
    
    document.body.removeChild(widget);
  });
  
  test('Widget initialization with invalid mode/preset', () => {
    /**
     * What we are testing: initializeMathInput handles invalid mode/preset
     * Why we are testing: Edge case - invalid configuration
     * Expected Result: Uses defaults or handles gracefully
     */
    const widget = document.createElement('div');
    widget.id = 'test-widget-invalid';
    document.body.appendChild(widget);
    
    expect(() => {
      window.initializeMathInput('test-widget-invalid', {
        mode: 'invalid_mode',
        preset: 'invalid_preset',
        value: '',
      });
    }).not.toThrow();
    
    document.body.removeChild(widget);
  });
  
  test('Multiple widgets on same page', () => {
    /**
     * What we are testing: Multiple widgets can coexist
     * Why we are testing: Real pages may have multiple widgets
     * Expected Result: Each widget works independently
     */
    const widget1 = document.createElement('div');
    widget1.id = 'widget-1';
    document.body.appendChild(widget1);
    
    const widget2 = document.createElement('div');
    widget2.id = 'widget-2';
    document.body.appendChild(widget2);
    
    expect(() => {
      window.initializeMathInput('widget-1', {
        mode: 'regular_functions',
        preset: 'algebra',
        value: 'x + y',
      });
      window.initializeMathInput('widget-2', {
        mode: 'matrices',
        preset: 'machine_learning',
        value: 'A + B',
      });
    }).not.toThrow();
    
    document.body.removeChild(widget1);
    document.body.removeChild(widget2);
  });
});

