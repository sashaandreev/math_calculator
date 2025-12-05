/**
 * MathInput Widget JavaScript
 * 
 * Core JavaScript for the math input widget.
 * Includes AST engine for visual formula building.
 */

(function() {
    'use strict';

    // ============================================================================
    // AST (Abstract Syntax Tree) Engine
    // ============================================================================

    /**
     * AST Node Types
     */
    const NodeTypes = {
        VARIABLE: 'variable',
        NUMBER: 'number',
        OPERATOR: 'operator',
        FRACTION: 'fraction',
        ROOT: 'root',
        POWER: 'power',
        FUNCTION: 'function',
        INTEGRAL: 'integral',
        SUM: 'sum',
        PRODUCT: 'product',
        LIMIT: 'limit',
        MATRIX: 'matrix',
        EXPRESSION: 'expression',
        PLACEHOLDER: 'placeholder',
        TEXT: 'text'
    };

    /**
     * AST Node Class
     * 
     * Represents a node in the Abstract Syntax Tree for mathematical expressions.
     */
    class ASTNode {
        /**
         * Create an AST node.
         * 
         * @param {string} type - Node type (from NodeTypes)
         * @param {string|number} value - Node value
         * @param {Array<ASTNode>} children - Child nodes
         */
        constructor(type, value = null, children = []) {
            this.type = type;
            this.value = value;
            this.children = children;
            this.parent = null;
            this.id = this.generateId();
            
            // Set parent reference for children
            this.children.forEach(child => {
                if (child instanceof ASTNode) {
                    child.parent = this;
                }
            });
        }

        /**
         * Generate unique ID for this node.
         */
        generateId() {
            return 'node_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        }

        /**
         * Add a child node.
         */
        addChild(child) {
            if (child instanceof ASTNode) {
                child.parent = this;
                this.children.push(child);
            }
        }

        /**
         * Remove a child node.
         */
        removeChild(child) {
            const index = this.children.indexOf(child);
            if (index > -1) {
                this.children.splice(index, 1);
                child.parent = null;
            }
        }

        /**
         * Get all placeholder nodes in this subtree.
         */
        getPlaceholders() {
            const placeholders = [];
            if (this.type === NodeTypes.PLACEHOLDER) {
                placeholders.push(this);
            }
            this.children.forEach(child => {
                if (child instanceof ASTNode) {
                    placeholders.push(...child.getPlaceholders());
                }
            });
            return placeholders;
        }
    }

    /**
     * Create an empty AST (placeholder).
     */
    function createEmptyAST() {
        return new ASTNode(NodeTypes.PLACEHOLDER, '');
    }

    /**
     * Create a placeholder node.
     */
    function createPlaceholder(label = '') {
        return new ASTNode(NodeTypes.PLACEHOLDER, label);
    }

    /**
     * LaTeX Parser
     * 
     * Parses LaTeX string into AST.
     * This is a basic parser - can be extended for more complex cases.
     * 
     * @param {string} latex - LaTeX string to parse
     * @returns {ASTNode} Root AST node
     */
    function parseLatex(latex) {
        if (!latex || latex.trim() === '') {
            return createEmptyAST();
        }

        // Remove leading/trailing whitespace
        latex = latex.trim();

        // Try to parse as expression
        try {
            return parseExpression(latex);
        } catch (error) {
            console.warn('LaTeX parse error:', error, 'for:', latex);
            // Return placeholder on parse error
            return createPlaceholder(latex);
        }
    }

    /**
     * Parse a LaTeX expression.
     * 
     * @param {string} latex - LaTeX string
     * @returns {ASTNode} Parsed AST node
     */
    function parseExpression(latex) {
        // Handle fractions: \frac{}{}
        const fracMatch = latex.match(/^\\frac\{([^}]*)\}\{([^}]*)\}(.*)$/);
        if (fracMatch) {
            const numerator = parseExpression(fracMatch[1] || '');
            const denominator = parseExpression(fracMatch[2] || '');
            const remainder = fracMatch[3] || '';
            
            const fractionNode = new ASTNode(NodeTypes.FRACTION, 'frac', [numerator, denominator]);
            
            if (remainder) {
                // Create expression node for remainder
                const remainderNode = parseExpression(remainder);
                return new ASTNode(NodeTypes.EXPRESSION, '+', [fractionNode, remainderNode]);
            }
            return fractionNode;
        }

        // Handle square root: \sqrt{}
        const sqrtMatch = latex.match(/^\\sqrt\{([^}]*)\}(.*)$/);
        if (sqrtMatch) {
            const radicand = parseExpression(sqrtMatch[1] || '');
            const remainder = sqrtMatch[2] || '';
            
            const rootNode = new ASTNode(NodeTypes.ROOT, 'sqrt', [radicand]);
            
            if (remainder) {
                const remainderNode = parseExpression(remainder);
                return new ASTNode(NodeTypes.EXPRESSION, '+', [rootNode, remainderNode]);
            }
            return rootNode;
        }

        // Handle powers: ^{}
        const powerMatch = latex.match(/^(.+?)\^\{([^}]*)\}(.*)$/);
        if (powerMatch) {
            const base = parseExpression(powerMatch[1]);
            const exponent = parseExpression(powerMatch[2] || '');
            const remainder = powerMatch[3] || '';
            
            const powerNode = new ASTNode(NodeTypes.POWER, '^', [base, exponent]);
            
            if (remainder) {
                const remainderNode = parseExpression(remainder);
                return new ASTNode(NodeTypes.EXPRESSION, '+', [powerNode, remainderNode]);
            }
            return powerNode;
        }

        // Handle subscripts: _{}
        const subMatch = latex.match(/^(.+?)_\{([^}]*)\}(.*)$/);
        if (subMatch) {
            const base = parseExpression(subMatch[1]);
            const subscript = parseExpression(subMatch[2] || '');
            const remainder = subMatch[3] || '';
            
            // Create expression with subscript
            const subNode = new ASTNode(NodeTypes.EXPRESSION, '_', [base, subscript]);
            
            if (remainder) {
                const remainderNode = parseExpression(remainder);
                return new ASTNode(NodeTypes.EXPRESSION, '+', [subNode, remainderNode]);
            }
            return subNode;
        }

        // Handle functions: \sin{}, \cos{}, etc.
        const funcMatch = latex.match(/^\\(sin|cos|tan|log|ln|exp|sinh|cosh|tanh|arcsin|arccos|arctan)\{([^}]*)\}(.*)$/);
        if (funcMatch) {
            const funcName = funcMatch[1];
            const argument = parseExpression(funcMatch[2] || '');
            const remainder = funcMatch[3] || '';
            
            const funcNode = new ASTNode(NodeTypes.FUNCTION, funcName, [argument]);
            
            if (remainder) {
                const remainderNode = parseExpression(remainder);
                return new ASTNode(NodeTypes.EXPRESSION, '+', [funcNode, remainderNode]);
            }
            return funcNode;
        }

        // Handle integrals: \int{}, \int_{}^{}{}
        const intMatch = latex.match(/^\\int(?:_\{([^}]*)\})?(?:\^\{([^}]*)\})?\{([^}]*)\}(.*)$/);
        if (intMatch) {
            const lower = intMatch[1] ? parseExpression(intMatch[1]) : null;
            const upper = intMatch[2] ? parseExpression(intMatch[2]) : null;
            const integrand = parseExpression(intMatch[3] || '');
            const remainder = intMatch[4] || '';
            
            const children = [integrand];
            if (lower) children.unshift(lower);
            if (upper) children.push(upper);
            
            const intNode = new ASTNode(NodeTypes.INTEGRAL, 'int', children);
            
            if (remainder) {
                const remainderNode = parseExpression(remainder);
                return new ASTNode(NodeTypes.EXPRESSION, '+', [intNode, remainderNode]);
            }
            return intNode;
        }

        // Handle sums: \sum_{}^{}
        const sumMatch = latex.match(/^\\sum(?:_\{([^}]*)\})?(?:\^\{([^}]*)\})?(.*)$/);
        if (sumMatch) {
            const lower = sumMatch[1] ? parseExpression(sumMatch[1]) : null;
            const upper = sumMatch[2] ? parseExpression(sumMatch[2]) : null;
            const term = parseExpression(sumMatch[3] || '');
            
            const children = [term];
            if (lower) children.unshift(lower);
            if (upper) children.push(upper);
            
            return new ASTNode(NodeTypes.SUM, 'sum', children);
        }

        // Handle simple operators: +, -, *, /
        const operatorMatch = latex.match(/^(.+?)\s*([+\-*/=<>≤≥≈≠])\s*(.+)$/);
        if (operatorMatch) {
            const left = parseExpression(operatorMatch[1]);
            const operator = operatorMatch[2];
            const right = parseExpression(operatorMatch[3]);
            
            return new ASTNode(NodeTypes.EXPRESSION, operator, [left, right]);
        }

        // Handle simple variables and numbers
        const simpleMatch = latex.match(/^([a-zA-Zα-ωΑ-Ω]+|\d+\.?\d*)(.*)$/);
        if (simpleMatch) {
            const value = simpleMatch[1];
            const remainder = simpleMatch[2] || '';
            
            // Determine if number or variable
            const nodeType = /^\d+\.?\d*$/.test(value) ? NodeTypes.NUMBER : NodeTypes.VARIABLE;
            const node = new ASTNode(nodeType, value);
            
            if (remainder) {
                const remainderNode = parseExpression(remainder);
                return new ASTNode(NodeTypes.EXPRESSION, '+', [node, remainderNode]);
            }
            return node;
        }

        // Default: create placeholder
        return createPlaceholder(latex);
    }

    /**
     * AST to LaTeX Converter
     * 
     * Converts AST back to LaTeX string.
     * 
     * @param {ASTNode} ast - AST node to convert
     * @returns {string} LaTeX string
     */
    function astToLatex(ast) {
        if (!ast || !(ast instanceof ASTNode)) {
            return '';
        }

        switch (ast.type) {
            case NodeTypes.VARIABLE:
            case NodeTypes.NUMBER:
                return String(ast.value || '');

            case NodeTypes.PLACEHOLDER:
                return ast.value || '';

            case NodeTypes.FRACTION:
                if (ast.children.length >= 2) {
                    const num = astToLatex(ast.children[0]);
                    const den = astToLatex(ast.children[1]);
                    return `\\frac{${num}}{${den}}`;
                }
                return `\\frac{}{}`;

            case NodeTypes.ROOT:
                if (ast.children.length >= 1) {
                    const radicand = astToLatex(ast.children[0]);
                    return `\\sqrt{${radicand}}`;
                }
                return `\\sqrt{}`;

            case NodeTypes.POWER:
                if (ast.children.length >= 2) {
                    const base = astToLatex(ast.children[0]);
                    const exponent = astToLatex(ast.children[1]);
                    return `${base}^{${exponent}}`;
                }
                return `${astToLatex(ast.children[0] || createPlaceholder())}^{}`;

            case NodeTypes.FUNCTION:
                if (ast.children.length >= 1) {
                    const arg = astToLatex(ast.children[0]);
                    return `\\${ast.value}{${arg}}`;
                }
                return `\\${ast.value}{}`;

            case NodeTypes.INTEGRAL:
                if (ast.children.length >= 1) {
                    const integrand = astToLatex(ast.children[0]);
                    if (ast.children.length >= 3) {
                        // Definite integral
                        const lower = astToLatex(ast.children[1]);
                        const upper = astToLatex(ast.children[2]);
                        return `\\int_{${lower}}^{${upper}} ${integrand}`;
                    }
                    return `\\int ${integrand}`;
                }
                return `\\int{}`;

            case NodeTypes.SUM:
                if (ast.children.length >= 1) {
                    const term = astToLatex(ast.children[0]);
                    if (ast.children.length >= 3) {
                        const lower = astToLatex(ast.children[1]);
                        const upper = astToLatex(ast.children[2]);
                        return `\\sum_{${lower}}^{${upper}} ${term}`;
                    }
                    return `\\sum ${term}`;
                }
                return `\\sum`;

            case NodeTypes.EXPRESSION:
                if (ast.children.length >= 2) {
                    const left = astToLatex(ast.children[0]);
                    const right = astToLatex(ast.children[1]);
                    const op = ast.value || '+';
                    return `${left} ${op} ${right}`;
                } else if (ast.children.length === 1) {
                    return astToLatex(ast.children[0]);
                }
                return '';

            default:
                // For unknown types, try to convert children
                if (ast.children.length > 0) {
                    return ast.children.map(child => astToLatex(child)).join(' ');
                }
                return String(ast.value || '');
        }
    }

    /**
     * Placeholder Manager
     * 
     * Manages placeholders in the visual builder.
     */
    class PlaceholderManager {
        constructor() {
            this.placeholders = [];
            this.activePlaceholder = null;
        }

        /**
         * Register a placeholder element.
         */
        register(placeholderElement, astNode) {
            if (!placeholderElement || !astNode) return;
            
            const placeholder = {
                element: placeholderElement,
                node: astNode,
                id: astNode.id
            };
            
            this.placeholders.push(placeholder);
            
            // Add click handler
            placeholderElement.addEventListener('click', () => {
                this.activatePlaceholder(placeholder);
            });
        }

        /**
         * Activate a placeholder (for editing).
         */
        activatePlaceholder(placeholder) {
            // Deactivate current
            if (this.activePlaceholder) {
                this.activePlaceholder.element.classList.remove('active');
            }
            
            // Activate new
            this.activePlaceholder = placeholder;
            placeholder.element.classList.add('active');
            placeholder.element.focus();
        }

        /**
         * Get next placeholder.
         */
        getNext() {
            if (!this.activePlaceholder) {
                return this.placeholders[0] || null;
            }
            
            const currentIndex = this.placeholders.indexOf(this.activePlaceholder);
            const nextIndex = (currentIndex + 1) % this.placeholders.length;
            return this.placeholders[nextIndex] || null;
        }

        /**
         * Get previous placeholder.
         */
        getPrevious() {
            if (!this.activePlaceholder) {
                return this.placeholders[this.placeholders.length - 1] || null;
            }
            
            const currentIndex = this.placeholders.indexOf(this.activePlaceholder);
            const prevIndex = (currentIndex - 1 + this.placeholders.length) % this.placeholders.length;
            return this.placeholders[prevIndex] || null;
        }

        /**
         * Clear all placeholders.
         */
        clear() {
            this.placeholders = [];
            this.activePlaceholder = null;
        }
    }

    /**
     * Visual Builder Renderer
     * 
     * Renders AST as visual structure with placeholders.
     */
    class VisualBuilder {
        /**
         * Create a VisualBuilder instance.
         * 
         * @param {HTMLElement} container - Container element for visual builder
         * @param {ASTNode} ast - Initial AST
         */
        constructor(container, ast = null) {
            this.container = container;
            this.ast = ast || createEmptyAST();
            this.placeholderManager = new PlaceholderManager();
        }

        /**
         * Set the AST and re-render.
         */
        setAST(ast) {
            this.ast = ast || createEmptyAST();
            this.render();
        }

        /**
         * Get the current AST.
         */
        getAST() {
            return this.ast;
        }

        /**
         * Render the AST as visual structure.
         */
        render() {
            if (!this.container) return;
            
            // Clear existing content
            this.container.innerHTML = '';
            this.placeholderManager.clear();
            
            // Render AST
            const fragment = this.renderNode(this.ast);
            this.container.appendChild(fragment);
        }

        /**
         * Render a single AST node.
         * 
         * @param {ASTNode} node - AST node to render
         * @returns {DocumentFragment} Rendered fragment
         */
        renderNode(node) {
            const fragment = document.createDocumentFragment();
            
            if (!node || !(node instanceof ASTNode)) {
                return fragment;
            }

            switch (node.type) {
                case NodeTypes.VARIABLE:
                case NodeTypes.NUMBER:
                    const textSpan = document.createElement('span');
                    textSpan.className = `mi-element mi-${node.type}`;
                    textSpan.textContent = node.value || '';
                    textSpan.dataset.nodeId = node.id;
                    fragment.appendChild(textSpan);
                    break;

                case NodeTypes.PLACEHOLDER:
                    const placeholder = document.createElement('span');
                    placeholder.className = 'mi-placeholder';
                    placeholder.textContent = node.value || '□';
                    placeholder.dataset.nodeId = node.id;
                    placeholder.setAttribute('contenteditable', 'true');
                    placeholder.setAttribute('role', 'textbox');
                    placeholder.setAttribute('aria-label', `Placeholder: ${node.value || 'empty'}`);
                    this.placeholderManager.register(placeholder, node);
                    fragment.appendChild(placeholder);
                    break;

                case NodeTypes.FRACTION:
                    const fracDiv = document.createElement('div');
                    fracDiv.className = 'mi-fraction';
                    fracDiv.dataset.nodeId = node.id;
                    
                    const numDiv = document.createElement('div');
                    numDiv.className = 'mi-fraction-numerator';
                    numDiv.appendChild(this.renderNode(node.children[0] || createPlaceholder('numerator')));
                    
                    const denDiv = document.createElement('div');
                    denDiv.className = 'mi-fraction-denominator';
                    denDiv.appendChild(this.renderNode(node.children[1] || createPlaceholder('denominator')));
                    
                    fracDiv.appendChild(numDiv);
                    fracDiv.appendChild(denDiv);
                    fragment.appendChild(fracDiv);
                    break;

                case NodeTypes.ROOT:
                    const rootSpan = document.createElement('span');
                    rootSpan.className = 'mi-root';
                    rootSpan.dataset.nodeId = node.id;
                    rootSpan.innerHTML = '√';
                    rootSpan.appendChild(this.renderNode(node.children[0] || createPlaceholder()));
                    fragment.appendChild(rootSpan);
                    break;

                case NodeTypes.POWER:
                    const powerSpan = document.createElement('span');
                    powerSpan.className = 'mi-power';
                    powerSpan.dataset.nodeId = node.id;
                    powerSpan.appendChild(this.renderNode(node.children[0] || createPlaceholder()));
                    
                    const supSpan = document.createElement('sup');
                    supSpan.className = 'mi-exponent';
                    supSpan.appendChild(this.renderNode(node.children[1] || createPlaceholder()));
                    powerSpan.appendChild(supSpan);
                    
                    fragment.appendChild(powerSpan);
                    break;

                case NodeTypes.FUNCTION:
                    const funcSpan = document.createElement('span');
                    funcSpan.className = 'mi-function';
                    funcSpan.dataset.nodeId = node.id;
                    funcSpan.textContent = node.value || '';
                    funcSpan.appendChild(document.createTextNode('('));
                    funcSpan.appendChild(this.renderNode(node.children[0] || createPlaceholder()));
                    funcSpan.appendChild(document.createTextNode(')'));
                    fragment.appendChild(funcSpan);
                    break;

                case NodeTypes.INTEGRAL:
                    const intSpan = document.createElement('span');
                    intSpan.className = 'mi-integral';
                    intSpan.dataset.nodeId = node.id;
                    intSpan.innerHTML = '∫';
                    
                    if (node.children.length >= 3) {
                        // Definite integral
                        const subSpan = document.createElement('sub');
                        subSpan.appendChild(this.renderNode(node.children[1]));
                        intSpan.appendChild(subSpan);
                        
                        const supSpan = document.createElement('sup');
                        supSpan.appendChild(this.renderNode(node.children[2]));
                        intSpan.appendChild(supSpan);
                    }
                    
                    intSpan.appendChild(this.renderNode(node.children[0] || createPlaceholder()));
                    fragment.appendChild(intSpan);
                    break;

                case NodeTypes.EXPRESSION:
                    // Render children with operator
                    node.children.forEach((child, index) => {
                        if (index > 0) {
                            const opSpan = document.createElement('span');
                            opSpan.className = 'mi-operator';
                            opSpan.textContent = ` ${node.value || '+'} `;
                            fragment.appendChild(opSpan);
                        }
                        fragment.appendChild(this.renderNode(child));
                    });
                    break;

                default:
                    // Default: render children
                    node.children.forEach(child => {
                        fragment.appendChild(this.renderNode(child));
                    });
            }

            return fragment;
        }

        /**
         * Update AST and re-render.
         */
        updateAST(newAST) {
            this.ast = newAST || createEmptyAST();
            this.render();
        }

        /**
         * Get LaTeX representation of current AST.
         */
        getLatex() {
            return astToLatex(this.ast);
        }
    }

    // ============================================================================
    // Expose AST functions globally
    // ============================================================================
    window.NodeTypes = NodeTypes;
    window.ASTNode = ASTNode;
    window.parseLatex = parseLatex;
    window.astToLatex = astToLatex;
    window.VisualBuilder = VisualBuilder;
    window.PlaceholderManager = PlaceholderManager;
    window.createEmptyAST = createEmptyAST;
    window.createPlaceholder = createPlaceholder;

    /**
     * Initialize a math input widget instance.
     * 
     * @param {string} widgetId - The ID of the widget container
     * @param {Object} config - Configuration object
     * @param {string} config.mode - Input mode
     * @param {string} config.preset - Domain preset
     * @param {string} config.value - Initial LaTeX value
     */
    function initializeMathInput(widgetId, config) {
        const widget = document.getElementById(widgetId);
        if (!widget) {
            console.warn('MathInput widget not found:', widgetId);
            return;
        }

        // Store config on widget element
        widget.dataset.initialized = 'true';
        widget.dataset.mode = config.mode || 'regular_functions';
        widget.dataset.preset = config.preset || 'algebra';

        // Initialize mode tabs
        initializeModeTabs(widget);

        // Initialize Visual Builder with AST
        const visualBuilderContainer = widget.querySelector('.mi-visual-builder');
        if (visualBuilderContainer) {
            const initialValue = config.value || '';
            let initialAST;
            
            if (initialValue) {
                // Parse existing LaTeX into AST
                initialAST = parseLatex(initialValue);
            } else {
                // Create empty AST with placeholder
                initialAST = createEmptyAST();
            }
            
            // Create and store VisualBuilder instance
            const visualBuilder = new VisualBuilder(visualBuilderContainer, initialAST);
            widget.visualBuilder = visualBuilder;
            
            // Render the AST
            visualBuilder.render();
        }

        // Initialize source mode sync
        initializeSourceMode(widget, config.value || '');

        // Initialize preview (placeholder - will use KaTeX in Phase 2)
        initializePreview(widget, config.value || '');

        console.log('MathInput widget initialized:', widgetId, config);
    }

    /**
     * Initialize mode tabs (Visual/Source switching).
     */
    function initializeModeTabs(widget) {
        const tabs = widget.querySelectorAll('.mi-tab');
        const visualContainer = widget.querySelector('.mi-visual-builder-container');
        const sourceContainer = widget.querySelector('.mi-source-container');

        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const mode = this.dataset.mode;

                // Update tab states
                tabs.forEach(t => {
                    t.classList.remove('active');
                    t.setAttribute('aria-selected', 'false');
                });
                this.classList.add('active');
                this.setAttribute('aria-selected', 'true');

                // Show/hide containers
                if (mode === 'visual') {
                    visualContainer.style.display = 'block';
                    sourceContainer.style.display = 'none';
                } else {
                    visualContainer.style.display = 'none';
                    sourceContainer.style.display = 'block';
                }
            });
        });
    }

    /**
     * Initialize source mode textarea.
     */
    function initializeSourceMode(widget, initialValue) {
        const sourceTextarea = widget.querySelector('.mi-source-textarea');
        const hiddenInput = widget.querySelector('.mi-hidden-input');

        if (sourceTextarea && hiddenInput) {
            // Set initial value
            if (initialValue) {
                sourceTextarea.value = initialValue;
            }

            // Sync source to hidden input (basic - will be enhanced in Phase 3)
            sourceTextarea.addEventListener('input', function() {
                hiddenInput.value = this.value;
            });
        }
    }

    /**
     * Initialize preview area.
     * Placeholder - will use KaTeX in Phase 2.
     */
    function initializePreview(widget, initialValue) {
        const preview = widget.querySelector('.mi-preview');
        if (preview && initialValue) {
            // Placeholder: just show the LaTeX code
            // In Phase 2, this will render with KaTeX
            preview.innerHTML = '<code>' + escapeHtml(initialValue) + '</code>';
        }
    }

    /**
     * Escape HTML to prevent XSS.
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Expose initialization function globally
    window.initializeMathInput = initializeMathInput;

    // Auto-initialize widgets on page load
    document.addEventListener('DOMContentLoaded', function() {
        const widgets = document.querySelectorAll('.mi-widget[data-mode]');
        widgets.forEach(widget => {
            if (!widget.dataset.initialized) {
                const mode = widget.dataset.mode || 'regular_functions';
                const preset = widget.dataset.preset || 'algebra';
                const hiddenInput = widget.querySelector('.mi-hidden-input');
                const value = hiddenInput ? hiddenInput.value : '';

                initializeMathInput(widget.id, {
                    mode: mode,
                    preset: preset,
                    value: value
                });
            }
        });
    });
})();

