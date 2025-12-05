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
    // Cursor Position Management
    // ============================================================================

    /**
     * Cursor Manager
     * 
     * Manages cursor position in the AST for insertion operations.
     */
    class CursorManager {
        constructor(widget) {
            this.widget = widget;
            this.currentPlaceholder = null;
            this.currentNode = null;
        }

        /**
         * Get current cursor position (active placeholder or root).
         */
        getCursorPosition() {
            const visualBuilder = this.widget.visualBuilder;
            if (!visualBuilder) {
                return { node: visualBuilder ? visualBuilder.ast : null, placeholder: null };
            }

            const placeholderManager = visualBuilder.placeholderManager;
            const activePlaceholder = placeholderManager.activePlaceholder;
            
            if (activePlaceholder) {
                return {
                    node: activePlaceholder.node,
                    placeholder: activePlaceholder,
                    isPlaceholder: true
                };
            }

            // If no active placeholder, find first placeholder or use root
            const placeholders = placeholderManager.placeholders;
            if (placeholders.length > 0) {
                return {
                    node: placeholders[0].node,
                    placeholder: placeholders[0],
                    isPlaceholder: true
                };
            }

            // Default to root AST
            return {
                node: visualBuilder.ast,
                placeholder: null,
                isPlaceholder: false
            };
        }

        /**
         * Set cursor to a specific placeholder.
         */
        setCursor(placeholder) {
            if (placeholder && this.widget.visualBuilder) {
                this.widget.visualBuilder.placeholderManager.activatePlaceholder(placeholder);
            }
        }
    }

    // ============================================================================
    // Template Parsing and Node Creation
    // ============================================================================

    /**
     * Create AST node from LaTeX template.
     * 
     * @param {string} template - LaTeX template (e.g., "\\frac{}{}", "x^{2}")
     * @returns {ASTNode} Created AST node
     */
    function createNodeFromTemplate(template) {
        if (!template) {
            return createPlaceholder();
        }

        // Parse template into AST
        const ast = parseLatex(template);
        
        // If parsing resulted in placeholder, return it
        if (ast.type === NodeTypes.PLACEHOLDER && !ast.value) {
            return ast;
        }

        return ast;
    }

    /**
     * Insert node into AST at cursor position.
     * 
     * @param {Object} cursor - Cursor position from CursorManager
     * @param {ASTNode} newNode - Node to insert
     */
    function insertNode(cursor, newNode) {
        if (!cursor || !cursor.node) {
            return;
        }

        const targetNode = cursor.node;

        // If cursor is in a placeholder, replace the placeholder
        if (cursor.isPlaceholder && targetNode.type === NodeTypes.PLACEHOLDER) {
            // Replace placeholder with new node
            if (targetNode.parent) {
                const parent = targetNode.parent;
                const index = parent.children.indexOf(targetNode);
                if (index > -1) {
                    parent.children[index] = newNode;
                    newNode.parent = parent;
                } else {
                    parent.addChild(newNode);
                }
            } else {
                // Root node - replace it
                cursor.node = newNode;
            }
        } else {
            // Insert as child or sibling based on context
            if (targetNode.type === NodeTypes.EXPRESSION) {
                // Add to expression
                targetNode.addChild(newNode);
            } else if (targetNode.parent) {
                // Insert as sibling
                const parent = targetNode.parent;
                const index = parent.children.indexOf(targetNode);
                if (index > -1) {
                    parent.children.splice(index + 1, 0, newNode);
                    newNode.parent = parent;
                } else {
                    parent.addChild(newNode);
                }
            } else {
                // Root - wrap in expression
                const expression = new ASTNode(NodeTypes.EXPRESSION, '+', [targetNode, newNode]);
                cursor.node = expression;
            }
        }
    }

    // ============================================================================
    // Preview Rendering with KaTeX
    // ============================================================================

    /**
     * Render preview with KaTeX.
     * 
     * @param {string} latex - LaTeX string to render
     * @param {HTMLElement} container - Container element for preview
     */
    function renderPreview(latex, container) {
        if (!container) {
            return;
        }

        // Clear previous content
        container.innerHTML = '';

        if (!latex || latex.trim() === '') {
            container.innerHTML = '<span class="mi-preview-empty">Preview will appear here</span>';
            return;
        }

        // Check if KaTeX is available
        if (typeof katex === 'undefined') {
            // Fallback: show LaTeX code
            container.innerHTML = '<code class="mi-preview-fallback">' + escapeHtml(latex) + '</code>';
            container.innerHTML += '<div class="mi-preview-warning">KaTeX not loaded. Install KaTeX for preview rendering.</div>';
            return;
        }

        try {
            // Render with KaTeX
            katex.render(latex, container, {
                throwOnError: true,
                errorColor: '#cc0000',
                displayMode: false,
                strict: false
            });
            
            // Remove any error classes
            container.classList.remove('mi-preview-error');
        } catch (error) {
            // Show error
            container.innerHTML = '<div class="mi-preview-error">' + escapeHtml(error.message) + '</div>';
            container.innerHTML += '<code class="mi-preview-latex">' + escapeHtml(latex) + '</code>';
            container.classList.add('mi-preview-error');
            console.error('KaTeX render error:', error, 'for LaTeX:', latex);
        }
    }

    /**
     * Show render error message.
     */
    function showRenderError(container, message) {
        if (!container) return;
        
        container.innerHTML = '<div class="mi-preview-error">' + escapeHtml(message) + '</div>';
        container.classList.add('mi-preview-error');
    }

    // ============================================================================
    // Hidden Field Synchronization
    // ============================================================================

    /**
     * Update hidden field with LaTeX value.
     * 
     * @param {HTMLElement} widget - Widget container element
     * @param {string} latex - LaTeX string
     */
    function updateHiddenField(widget, latex) {
        if (!widget) return;

        const hiddenInput = widget.querySelector('.mi-hidden-input');
        if (hiddenInput) {
            hiddenInput.value = latex || '';
        }
    }

    // ============================================================================
    // Bidirectional Sync Manager
    // ============================================================================

    /**
     * Sync Manager Class
     * 
     * Manages bidirectional synchronization between visual builder and source mode.
     */
    class SyncManager {
        constructor(widget) {
            this.widget = widget;
            this.visualBuilder = widget.visualBuilder;
            this.sourceEditor = widget.querySelector('.mi-source-textarea');
            this.syncing = false;
            this.lastEdit = {source: 'visual', timestamp: 0};
            this.syncIndicator = null;
        }

        /**
         * Sync from visual builder to source editor.
         */
        syncFromVisual() {
            if (this.syncing || !this.sourceEditor) {
                return;
            }

            this.syncing = true;
            this.showSyncIndicator();

            try {
                const latex = this.visualBuilder ? this.visualBuilder.getLatex() : '';
                this.sourceEditor.value = latex || '';

                this.lastEdit = {source: 'visual', timestamp: Date.now()};

                // Update hidden field
                const hiddenInput = this.widget.querySelector('.mi-hidden-input');
                if (hiddenInput) {
                    hiddenInput.value = latex;
                }
            } catch (error) {
                console.error('Error syncing from visual:', error);
            } finally {
                this.syncing = false;
                this.hideSyncIndicator();
            }
        }

        /**
         * Sync from source editor to visual builder.
         */
        syncFromSource() {
            if (this.syncing || !this.visualBuilder || !this.sourceEditor) {
                return;
            }

            this.syncing = true;
            this.showSyncIndicator();

            try {
                const latex = this.sourceEditor.value || '';

                // Parse LaTeX into AST
                const ast = parseLatex(latex);

                // Update visual builder
                this.visualBuilder.setAST(ast);
                this.visualBuilder.render();

                this.lastEdit = {source: 'source', timestamp: Date.now()};

                // Update hidden field
                const hiddenInput = this.widget.querySelector('.mi-hidden-input');
                if (hiddenInput) {
                    hiddenInput.value = latex;
                }

                // Update preview
                const previewContainer = this.widget.querySelector('.mi-preview');
                if (previewContainer) {
                    renderPreview(latex, previewContainer);
                }

                // Clear any previous errors
                this.hideParseError();
            } catch (error) {
                console.error('Error syncing from source:', error);
                this.showParseError(error);
            } finally {
                this.syncing = false;
                this.hideSyncIndicator();
            }
        }

        /**
         * Show sync indicator.
         */
        showSyncIndicator() {
            // Create or show sync indicator
            if (!this.syncIndicator) {
                this.syncIndicator = document.createElement('div');
                this.syncIndicator.className = 'mi-sync-indicator';
                this.syncIndicator.textContent = 'Syncing...';
                this.syncIndicator.style.cssText = 'position: absolute; top: 8px; right: 8px; padding: 4px 8px; background: #007bff; color: white; border-radius: 4px; font-size: 11px; z-index: 1000;';
                this.widget.style.position = 'relative';
                this.widget.appendChild(this.syncIndicator);
            }
            this.syncIndicator.style.display = 'block';
        }

        /**
         * Hide sync indicator.
         */
        hideSyncIndicator() {
            if (this.syncIndicator) {
                setTimeout(() => {
                    if (this.syncIndicator) {
                        this.syncIndicator.style.display = 'none';
                    }
                }, 200);
            }
        }

        /**
         * Show parse error.
         */
        showParseError(error) {
            const errorContainer = this.widget.querySelector('.mi-preview-error');
            if (errorContainer) {
                errorContainer.textContent = `Parse error: ${error.message || 'Invalid LaTeX'}`;
                errorContainer.style.display = 'block';
            }
        }

        /**
         * Hide parse error.
         */
        hideParseError() {
            const errorContainer = this.widget.querySelector('.mi-preview-error');
            if (errorContainer) {
                errorContainer.style.display = 'none';
            }
        }

        /**
         * Check if sync is in progress.
         */
        isSyncing() {
            return this.syncing;
        }

        /**
         * Get last edit information.
         */
        getLastEdit() {
            return this.lastEdit;
        }
    }

    /**
     * Sync source mode textarea with LaTeX (legacy function for backward compatibility).
     * 
     * @param {HTMLElement} widget - Widget container element
     * @param {string} latex - LaTeX string
     */
    function syncSourceMode(widget, latex) {
        if (!widget) return;

        const syncManager = widget.syncManager;
        if (syncManager) {
            // Use sync manager if available
            syncManager.syncFromVisual();
        } else {
            // Fallback to direct sync
            const sourceTextarea = widget.querySelector('.mi-source-textarea');
            if (sourceTextarea) {
                sourceTextarea.value = latex || '';
            }
        }
    }

    // ============================================================================
    // Debouncing Utility
    // ============================================================================

    /**
     * Debounce function to limit how often a function is called.
     * 
     * @param {Function} func - Function to debounce
     * @param {number} wait - Wait time in milliseconds
     * @returns {Function} Debounced function
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // ============================================================================
    // Button Click Handlers
    // ============================================================================

    /**
     * Handle toolbar button click.
     * 
     * @param {HTMLElement} buttonElement - Clicked button element
     * @param {HTMLElement} widget - Widget container element
     */
    function handleButtonClick(buttonElement, widget) {
        if (!buttonElement || !widget) {
            return;
        }

        const action = buttonElement.dataset.action;
        const template = buttonElement.dataset.template;

        if (!action || action !== 'insert') {
            return;
        }

        if (!template) {
            console.warn('Button has no template:', buttonElement);
            return;
        }

        // Get visual builder
        const visualBuilder = widget.visualBuilder;
        if (!visualBuilder) {
            console.warn('Visual builder not initialized');
            return;
        }

        // Get cursor position
        const cursorManager = widget.cursorManager || new CursorManager(widget);
        widget.cursorManager = cursorManager;
        const cursor = cursorManager.getCursorPosition();

        // Create node from template
        const newNode = createNodeFromTemplate(template);

        // Insert node at cursor
        insertNode(cursor, newNode);

        // Update AST in visual builder
        if (cursor.node && cursor.node !== visualBuilder.ast) {
            // If cursor was in a specific node, update that node's parent's AST
            // For now, we'll update the entire AST
            visualBuilder.setAST(visualBuilder.ast);
        } else {
            visualBuilder.setAST(cursor.node || visualBuilder.ast);
        }

        // Get updated LaTeX
        const latex = visualBuilder.getLatex();

        // Update hidden field
        updateHiddenField(widget, latex);

        // Sync source mode
        syncSourceMode(widget, latex);

        // Render preview (debounced)
        const previewContainer = widget.querySelector('.mi-preview');
        if (previewContainer) {
            debouncedRenderPreview(latex, previewContainer);
        }

        // Move cursor to first placeholder in new node
        const placeholders = newNode.getPlaceholders();
        if (placeholders.length > 0 && visualBuilder.placeholderManager) {
            const firstPlaceholder = visualBuilder.placeholderManager.placeholders.find(
                p => p.node.id === placeholders[0].id
            );
            if (firstPlaceholder) {
                cursorManager.setCursor(firstPlaceholder);
            }
        }
    }

    /**
     * Debounced preview renderer (300ms delay).
     */
    const debouncedRenderPreview = debounce(renderPreview, 300);

    // ============================================================================
    // Event Listeners Setup
    // ============================================================================

    // ============================================================================
    // Text Formatting Handlers
    // ============================================================================

    /**
     * Handle format button click (bold, color, size).
     * 
     * @param {HTMLElement} buttonElement - The format button element
     * @param {HTMLElement} widget - Widget container element
     */
    function handleFormatButton(buttonElement, widget) {
        const formatType = buttonElement.dataset.format;
        if (!formatType) {
            return;
        }

        const visualBuilder = widget.visualBuilder;
        if (!visualBuilder) {
            console.warn('Visual builder not initialized');
            return;
        }

        // For now, we'll apply formatting to the next placeholder
        // In a full implementation, we'd check for text selection first
        const cursorManager = widget.cursorManager || new CursorManager(widget);
        widget.cursorManager = cursorManager;
        const cursor = cursorManager.getCursorPosition();

        // Apply format based on type
        switch (formatType) {
            case 'bold':
                applyBoldFormat(cursor, widget);
                break;
            case 'color':
                const color = buttonElement.dataset.color;
                if (color) {
                    // Quick color button clicked
                    applyColorFormat(cursor, widget, color);
                } else {
                    // Color picker button clicked - show picker
                    showColorPicker(buttonElement, cursor, widget);
                }
                break;
            case 'size':
                // Size button clicked - show size menu
                showSizePicker(buttonElement, cursor, widget);
                break;
        }
    }

    /**
     * Apply bold formatting.
     * 
     * @param {Object} cursor - Cursor position object
     * @param {HTMLElement} widget - Widget container element
     */
    function applyBoldFormat(cursor, widget) {
        const template = '\\textbf{}';
        const newNode = createNodeFromTemplate(template);
        
        if (!newNode) {
            return;
        }

        insertNode(cursor, newNode);
        updateWidgetAfterInsert(widget);
    }

    /**
     * Apply color formatting.
     * 
     * @param {Object} cursor - Cursor position object
     * @param {HTMLElement} widget - Widget container element
     * @param {string} color - Color name or hex code
     */
    function applyColorFormat(cursor, widget, color) {
        const template = `\\textcolor{${color}}{}`;
        const newNode = createNodeFromTemplate(template);
        
        if (!newNode) {
            return;
        }

        insertNode(cursor, newNode);
        updateWidgetAfterInsert(widget);
    }

    /**
     * Apply size formatting.
     * 
     * @param {Object} cursor - Cursor position object
     * @param {HTMLElement} widget - Widget container element
     * @param {string} sizeTemplate - LaTeX size command template
     */
    function applySizeFormat(cursor, widget, sizeTemplate) {
        if (!sizeTemplate) {
            // Normal size - no formatting needed
            return;
        }

        const template = sizeTemplate;
        const newNode = createNodeFromTemplate(template);
        
        if (!newNode) {
            return;
        }

        insertNode(cursor, newNode);
        updateWidgetAfterInsert(widget);
    }

    /**
     * Show color picker dropdown.
     * 
     * @param {HTMLElement} buttonElement - Color button element
     * @param {Object} cursor - Cursor position object
     * @param {HTMLElement} widget - Widget container element
     */
    function showColorPicker(buttonElement, cursor, widget) {
        const colorSelector = buttonElement.closest('.mi-color-selector');
        if (!colorSelector) {
            return;
        }

        const picker = colorSelector.querySelector('.mi-color-picker');
        const isOpen = !picker.hidden;

        // Close all other pickers
        widget.querySelectorAll('.mi-color-picker, .mi-size-menu').forEach(el => {
            el.hidden = true;
        });
        widget.querySelectorAll('[aria-expanded="true"]').forEach(el => {
            el.setAttribute('aria-expanded', 'false');
        });

        if (isOpen) {
            picker.hidden = true;
            buttonElement.setAttribute('aria-expanded', 'false');
        } else {
            picker.hidden = false;
            buttonElement.setAttribute('aria-expanded', 'true');

            // Setup color picker event listeners
            setupColorPickerListeners(picker, cursor, widget, buttonElement);
        }
    }

    /**
     * Setup color picker event listeners.
     * 
     * @param {HTMLElement} picker - Color picker element
     * @param {Object} cursor - Cursor position object
     * @param {HTMLElement} widget - Widget container element
     * @param {HTMLElement} buttonElement - Color button element
     */
    function setupColorPickerListeners(picker, cursor, widget, buttonElement) {
        // Remove existing listeners to avoid duplicates
        const newPicker = picker.cloneNode(true);
        picker.parentNode.replaceChild(newPicker, picker);

        // Color palette items
        newPicker.querySelectorAll('.mi-color-item').forEach(item => {
            item.addEventListener('click', function() {
                const color = this.dataset.color;
                applyColorFormat(cursor, widget, color);
                newPicker.hidden = true;
                buttonElement.setAttribute('aria-expanded', 'false');
            });
        });

        // Custom color input
        const colorInput = newPicker.querySelector('.mi-color-input');
        const applyButton = newPicker.querySelector('.mi-color-apply');
        
        if (applyButton && colorInput) {
            applyButton.addEventListener('click', function() {
                const hexColor = colorInput.value;
                // Convert hex to color name if possible, or use hex
                const colorName = hexToColorName(hexColor) || hexColor;
                applyColorFormat(cursor, widget, colorName);
                newPicker.hidden = true;
                buttonElement.setAttribute('aria-expanded', 'false');
            });
        }

        // Close on outside click
        setTimeout(() => {
            document.addEventListener('click', function closePicker(e) {
                if (!newPicker.contains(e.target) && !buttonElement.contains(e.target)) {
                    newPicker.hidden = true;
                    buttonElement.setAttribute('aria-expanded', 'false');
                    document.removeEventListener('click', closePicker);
                }
            });
        }, 0);
    }

    /**
     * Show size picker dropdown.
     * 
     * @param {HTMLElement} buttonElement - Size button element
     * @param {Object} cursor - Cursor position object
     * @param {HTMLElement} widget - Widget container element
     */
    function showSizePicker(buttonElement, cursor, widget) {
        const sizeSelector = buttonElement.closest('.mi-size-selector');
        if (!sizeSelector) {
            return;
        }

        const menu = sizeSelector.querySelector('.mi-size-menu');
        const isOpen = !menu.hidden;

        // Close all other pickers
        widget.querySelectorAll('.mi-color-picker, .mi-size-menu').forEach(el => {
            el.hidden = true;
        });
        widget.querySelectorAll('[aria-expanded="true"]').forEach(el => {
            el.setAttribute('aria-expanded', 'false');
        });

        if (isOpen) {
            menu.hidden = true;
            buttonElement.setAttribute('aria-expanded', 'false');
        } else {
            menu.hidden = false;
            buttonElement.setAttribute('aria-expanded', 'true');

            // Setup size menu event listeners
            setupSizeMenuListeners(menu, cursor, widget, buttonElement);
        }
    }

    /**
     * Setup size menu event listeners.
     * 
     * @param {HTMLElement} menu - Size menu element
     * @param {Object} cursor - Cursor position object
     * @param {HTMLElement} widget - Widget container element
     * @param {HTMLElement} buttonElement - Size button element
     */
    function setupSizeMenuListeners(menu, cursor, widget, buttonElement) {
        menu.querySelectorAll('.mi-size-item').forEach(item => {
            item.addEventListener('click', function() {
                const template = this.dataset.template;
                applySizeFormat(cursor, widget, template);
                menu.hidden = true;
                buttonElement.setAttribute('aria-expanded', 'false');
            });
        });

        // Close on outside click
        setTimeout(() => {
            document.addEventListener('click', function closeMenu(e) {
                if (!menu.contains(e.target) && !buttonElement.contains(e.target)) {
                    menu.hidden = true;
                    buttonElement.setAttribute('aria-expanded', 'false');
                    document.removeEventListener('click', closeMenu);
                }
            });
        }, 0);
    }

    /**
     * Convert hex color to color name if it's a standard color.
     * 
     * @param {string} hex - Hex color code (e.g., "#ff0000")
     * @returns {string|null} Color name or null
     */
    function hexToColorName(hex) {
        const colorMap = {
            '#000000': 'black',
            '#ffffff': 'white',
            '#ff0000': 'red',
            '#00ff00': 'green',
            '#0000ff': 'blue',
            '#ffff00': 'yellow',
            '#ffa500': 'orange',
            '#800080': 'purple',
            '#ffc0cb': 'pink',
            '#a52a2a': 'brown',
            '#808080': 'gray',
            '#00ffff': 'cyan',
            '#ff00ff': 'magenta',
        };
        return colorMap[hex.toLowerCase()] || null;
    }

    // ============================================================================
    // Mode Switching
    // ============================================================================

    /**
     * Mode configurations (toolbar visibility data).
     * This should ideally be loaded from Django, but for now we provide a mapping.
     */
    const MODE_CONFIGS = {
        'regular_functions': {
            name: 'Regular Functions',
            toolbars: {
                visible: ['text', 'basic', 'trig'],
                hidden: ['advanced', 'calculus', 'matrices', 'symbols'],
                priority: ['basic', 'text', 'trig']
            }
        },
        'advanced_expressions': {
            name: 'Advanced Expressions',
            toolbars: {
                visible: ['text', 'basic', 'advanced', 'symbols'],
                hidden: ['calculus', 'matrices', 'trig'],
                priority: ['advanced', 'basic', 'text', 'symbols']
            }
        },
        'integrals_differentials': {
            name: 'Integrals/Differentials',
            toolbars: {
                visible: ['text', 'calculus', 'advanced', 'basic'],
                hidden: ['trig', 'symbols', 'matrices'],
                priority: ['calculus', 'advanced', 'basic', 'text']
            }
        },
        'matrices': {
            name: 'Matrices',
            toolbars: {
                visible: ['text', 'matrices', 'advanced', 'symbols'],
                hidden: ['calculus', 'trig', 'basic'],
                priority: ['matrices', 'advanced', 'text', 'symbols']
            }
        },
        'statistics_probability': {
            name: 'Statistics & Probability',
            toolbars: {
                visible: ['text', 'advanced', 'symbols', 'basic'],
                hidden: ['calculus', 'matrices', 'trig'],
                priority: ['advanced', 'symbols', 'text', 'basic']
            }
        },
        'physics_engineering': {
            name: 'Physics & Engineering',
            toolbars: {
                visible: ['text', 'calculus', 'symbols', 'advanced'],
                hidden: ['matrices', 'trig', 'basic'],
                priority: ['calculus', 'symbols', 'advanced', 'text']
            }
        }
    };

    /**
     * Get mode configuration by code.
     * 
     * @param {string} modeCode - Mode code (e.g., 'regular_functions', 'matrices')
     * @returns {Object} Mode configuration object
     */
    function getModeConfig(modeCode) {
        return MODE_CONFIGS[modeCode] || MODE_CONFIGS['regular_functions'];
    }

    /**
     * Get current LaTeX from widget.
     * 
     * @param {HTMLElement} widget - Widget container element
     * @returns {string} Current LaTeX string
     */
    function getCurrentLatex(widget) {
        const visualBuilder = widget.visualBuilder;
        if (visualBuilder) {
            return visualBuilder.getLatex();
        }
        const hiddenInput = widget.querySelector('.mi-hidden-input');
        return hiddenInput ? hiddenInput.value : '';
    }

    /**
     * Check if LaTeX uses operations not available in a mode.
     * 
     * @param {string} latex - LaTeX string to check
     * @param {string} modeCode - Mode code to check against
     * @returns {boolean} True if incompatible operations found
     */
    function usesOperationsNotInMode(latex, modeCode) {
        if (!latex) {
            return false;
        }

        const modeConfig = getModeConfig(modeCode);
        const hiddenToolbars = modeConfig.toolbars.hidden;

        // Check for calculus operations
        if (hiddenToolbars.includes('calculus')) {
            if (latex.includes('\\int') || latex.includes('\\sum') || latex.includes('\\prod') || 
                latex.includes('\\lim') || latex.includes('\\frac{d}{') || latex.includes('\\partial')) {
                return true;
            }
        }

        // Check for matrix operations
        if (hiddenToolbars.includes('matrices')) {
            if (latex.includes('\\begin{matrix') || latex.includes('\\begin{pmatrix') || 
                latex.includes('\\begin{bmatrix') || latex.includes('\\det') || 
                latex.includes('\\mathbf{')) {
                return true;
            }
        }

        // Check for trig operations
        if (hiddenToolbars.includes('trig')) {
            if (latex.includes('\\sin') || latex.includes('\\cos') || latex.includes('\\tan') ||
                latex.includes('\\sec') || latex.includes('\\csc') || latex.includes('\\cot')) {
                return true;
            }
        }

        return false;
    }

    /**
     * Show warning for incompatible operations.
     * 
     * @param {HTMLElement} widget - Widget container element
     * @param {string} message - Warning message
     */
    function showModeWarning(widget, message) {
        const errorContainer = widget.querySelector('.mi-error-container');
        if (!errorContainer) {
            return;
        }

        errorContainer.textContent = message;
        errorContainer.style.display = 'block';
        errorContainer.setAttribute('role', 'alert');

        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorContainer.style.display = 'none';
        }, 5000);
    }

    /**
     * Update toolbar visibility based on mode.
     * 
     * @param {HTMLElement} widget - Widget container element
     * @param {Object} modeConfig - Mode configuration object
     */
    function updateToolbarVisibility(widget, modeConfig) {
        const toolbarContainer = widget.querySelector('.mi-toolbar-container');
        if (!toolbarContainer) {
            return;
        }

        const visibleToolbars = modeConfig.toolbars.visible || [];
        const hiddenToolbars = modeConfig.toolbars.hidden || [];

        // Get all toolbar elements
        const allToolbars = toolbarContainer.querySelectorAll('.mi-toolbar');
        
        allToolbars.forEach(toolbar => {
            const toolbarType = toolbar.className.match(/mi-toolbar-(\w+)/);
            if (toolbarType) {
                const type = toolbarType[1];
                if (visibleToolbars.includes(type)) {
                    toolbar.style.display = '';
                } else if (hiddenToolbars.includes(type)) {
                    toolbar.style.display = 'none';
                }
            }
        });

        // Update toolbar tabs visibility
        const toolbarTabs = toolbarContainer.querySelectorAll('.mi-toolbar-tab');
        toolbarTabs.forEach(tab => {
            const tabType = tab.dataset.toolbar;
            if (tabType) {
                if (visibleToolbars.includes(tabType)) {
                    tab.style.display = '';
                } else if (hiddenToolbars.includes(tabType)) {
                    tab.style.display = 'none';
                }
            }
        });
    }

    /**
     * Handle mode change.
     * 
     * @param {HTMLElement} widget - Widget container element
     * @param {string} newModeCode - New mode code
     */
    function handleModeChange(widget, newModeCode) {
        // 1. Preserve current formula
        const currentLatex = getCurrentLatex(widget);

        // 2. Load new mode config
        const modeConfig = getModeConfig(newModeCode);
        if (!modeConfig) {
            console.warn('Invalid mode code:', newModeCode);
            return;
        }

        // 3. Check for incompatible operations
        if (usesOperationsNotInMode(currentLatex, newModeCode)) {
            showModeWarning(
                widget,
                `Warning: Your formula contains operations that may not be available in "${modeConfig.name}" mode. The formula will be preserved, but some buttons may be hidden.`
            );
        }

        // 4. Update widget data attribute
        widget.dataset.mode = newModeCode;

        // 5. Update toolbar visibility
        updateToolbarVisibility(widget, modeConfig);

        // 6. Update quick insert (if preset changes are needed, handle separately)
        // For now, quick insert is preset-based, not mode-based

        // 7. Re-initialize event listeners for new toolbars
        setupEventListeners(widget);

        console.log('Mode changed to:', newModeCode, modeConfig);
    }

    /**
     * Update widget after inserting a node (render, preview, sync).
     * 
     * @param {HTMLElement} widget - Widget container element
     */
    function updateWidgetAfterInsert(widget) {
        const visualBuilder = widget.visualBuilder;
        if (!visualBuilder) {
            return;
        }

        // Render visual builder
        visualBuilder.render();

        // Get updated LaTeX
        const latex = visualBuilder.getLatex();

        // Update hidden field
        updateHiddenField(widget, latex);

        // Sync to source mode (debounced)
        const syncManager = widget.syncManager;
        if (syncManager) {
            const debouncedSyncFromVisual = debounce(() => {
                syncManager.syncFromVisual();
            }, 300);
            debouncedSyncFromVisual();
        } else {
            // Fallback to legacy sync
            syncSourceMode(widget, latex);
        }

        // Render preview (debounced)
        const previewContainer = widget.querySelector('.mi-preview');
        if (previewContainer) {
            debouncedRenderPreview(latex, previewContainer);
        }

        // Move cursor to first placeholder
        const cursorManager = widget.cursorManager;
        if (cursorManager && visualBuilder.placeholderManager) {
            const placeholders = visualBuilder.placeholderManager.placeholders;
            if (placeholders.length > 0) {
                cursorManager.setCursor(placeholders[0]);
            }
        }
    }

    /**
     * Setup event listeners for a widget.
     * 
     * @param {HTMLElement} widget - Widget container element
     */
    function setupEventListeners(widget) {
        if (!widget) return;

        // Setup toolbar button click handlers for insert actions
        const toolbarButtons = widget.querySelectorAll('.mi-button[data-action="insert"]');
        toolbarButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                handleButtonClick(this, widget);
            });
        });

        // Setup format button click handlers
        const formatButtons = widget.querySelectorAll('.mi-button[data-action="format"]');
        formatButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                handleFormatButton(this, widget);
            });
        });

        // Setup mode selector change handler
        const modeSelect = widget.querySelector('.mi-mode-select');
        if (modeSelect) {
            modeSelect.addEventListener('change', function() {
                const newMode = this.value;
                handleModeChange(widget, newMode);
            });
        }

        // Setup keyboard shortcut (Ctrl+M) for mode toggle
        widget.addEventListener('keydown', function(e) {
            // Ctrl+M or Cmd+M (Mac)
            if ((e.ctrlKey || e.metaKey) && e.key === 'm') {
                e.preventDefault();
                toggleVisualSourceMode(widget);
            }
        });

        // Setup comprehensive keyboard navigation
        setupKeyboardNavigation(widget);

        // Setup placeholder keyboard navigation
        const visualBuilder = widget.visualBuilder;
        if (visualBuilder) {
            const placeholderManager = visualBuilder.placeholderManager;
            
            // Tab navigation between placeholders
            widget.addEventListener('keydown', function(e) {
                if (e.key === 'Tab' && !e.shiftKey) {
                    const next = placeholderManager.getNext();
                    if (next) {
                        e.preventDefault();
                        placeholderManager.activatePlaceholder(next);
                    }
                } else if (e.key === 'Tab' && e.shiftKey) {
                    const prev = placeholderManager.getPrevious();
                    if (prev) {
                        e.preventDefault();
                        placeholderManager.activatePlaceholder(prev);
                    }
                }
            });
        }

        // Setup source mode sync (when typing in source mode)
        const sourceTextarea = widget.querySelector('.mi-source-textarea');
        if (sourceTextarea) {
            const debouncedSyncFromSource = debounce(function() {
                const latex = sourceTextarea.value;
                const visualBuilder = widget.visualBuilder;
                
                if (visualBuilder) {
                    try {
                        const ast = parseLatex(latex);
                        visualBuilder.setAST(ast);
                        
                        // Update hidden field
                        updateHiddenField(widget, latex);
                        
                        // Update preview
                        const previewContainer = widget.querySelector('.mi-preview');
                        if (previewContainer) {
                            debouncedRenderPreview(latex, previewContainer);
                        }
                    } catch (error) {
                        console.error('Error parsing LaTeX from source mode:', error);
                    }
                }
            }, 500);

            sourceTextarea.addEventListener('input', debouncedSyncFromSource);
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
    window.CursorManager = CursorManager;
    window.handleButtonClick = handleButtonClick;
    window.renderPreview = renderPreview;

    /**
     * Quick Insert Manager
     * 
     * Manages the quick insert dropdown menu and template insertion.
     */
    class QuickInsertManager {
        constructor(widget, presetConfig) {
            this.widget = widget;
            this.presetConfig = presetConfig;
            this.toggleButton = widget.querySelector('.mi-quick-insert-toggle');
            this.menu = widget.querySelector('.mi-quick-insert-menu');
            this.isOpen = false;
            this.selectedIndex = -1;
            
            this.initialize();
        }

        /**
         * Initialize quick insert dropdown.
         */
        initialize() {
            if (!this.toggleButton || !this.menu) {
                return;
            }

            // Update button label with preset name
            const presetName = this.presetConfig.name || 'Quick';
            const label = this.toggleButton.querySelector('.mi-quick-insert-label');
            if (label) {
                label.textContent = presetName + ' Quick';
            }

            // Populate menu with templates from preset
            this.populateMenu();

            // Setup event listeners
            this.setupEventListeners();
        }

        /**
         * Populate menu with templates from preset configuration.
         */
        populateMenu() {
            if (!this.menu || !this.presetConfig.quick_inserts) {
                return;
            }

            // Clear existing items
            this.menu.innerHTML = '';

            // Add menu items from preset
            this.presetConfig.quick_inserts.forEach((item, index) => {
                const [name, template] = Array.isArray(item) ? item : [item, item];
                const li = document.createElement('li');
                li.setAttribute('role', 'menuitem');
                
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'mi-quick-insert-item';
                button.setAttribute('data-template', template);
                button.setAttribute('data-index', index);
                button.textContent = name;
                
                // Add click handler
                button.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.handleItemClick(template);
                });

                li.appendChild(button);
                this.menu.appendChild(li);
            });
        }

        /**
         * Setup event listeners for dropdown.
         */
        setupEventListeners() {
            if (!this.toggleButton) {
                return;
            }

            // Toggle button click
            this.toggleButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggle();
            });

            // Close on outside click
            document.addEventListener('click', (e) => {
                if (this.isOpen && !this.widget.contains(e.target)) {
                    this.close();
                }
            });

            // Keyboard navigation
            this.menu.addEventListener('keydown', (e) => {
                this.handleKeyboardNavigation(e);
            });

            // Focus management
            this.toggleButton.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggle();
                } else if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    this.open();
                    this.focusFirstItem();
                }
            });
        }

        /**
         * Toggle dropdown open/closed.
         */
        toggle() {
            if (this.isOpen) {
                this.close();
            } else {
                this.open();
            }
        }

        /**
         * Open dropdown menu.
         */
        open() {
            if (!this.menu || !this.toggleButton) {
                return;
            }

            this.menu.hidden = false;
            this.toggleButton.setAttribute('aria-expanded', 'true');
            this.isOpen = true;
            this.selectedIndex = -1;

            // Focus first item if menu has items
            const firstItem = this.menu.querySelector('.mi-quick-insert-item');
            if (firstItem) {
                setTimeout(() => firstItem.focus(), 0);
            }
        }

        /**
         * Close dropdown menu.
         */
        close() {
            if (!this.menu || !this.toggleButton) {
                return;
            }

            this.menu.hidden = true;
            this.toggleButton.setAttribute('aria-expanded', 'false');
            this.isOpen = false;
            this.selectedIndex = -1;

            // Return focus to toggle button
            this.toggleButton.focus();
        }

        /**
         * Handle keyboard navigation in menu.
         */
        handleKeyboardNavigation(e) {
            const items = Array.from(this.menu.querySelectorAll('.mi-quick-insert-item'));
            if (items.length === 0) {
                return;
            }

            switch (e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    this.selectedIndex = (this.selectedIndex + 1) % items.length;
                    items[this.selectedIndex].focus();
                    break;

                case 'ArrowUp':
                    e.preventDefault();
                    this.selectedIndex = this.selectedIndex <= 0 
                        ? items.length - 1 
                        : this.selectedIndex - 1;
                    items[this.selectedIndex].focus();
                    break;

                case 'Home':
                    e.preventDefault();
                    this.selectedIndex = 0;
                    items[0].focus();
                    break;

                case 'End':
                    e.preventDefault();
                    this.selectedIndex = items.length - 1;
                    items[this.selectedIndex].focus();
                    break;

                case 'Enter':
                case ' ':
                    e.preventDefault();
                    if (this.selectedIndex >= 0 && this.selectedIndex < items.length) {
                        const template = items[this.selectedIndex].dataset.template;
                        this.handleItemClick(template);
                    }
                    break;

                case 'Escape':
                    e.preventDefault();
                    this.close();
                    break;

                default:
                    // Allow typing to search (optional enhancement)
                    break;
            }
        }

        /**
         * Focus first menu item.
         */
        focusFirstItem() {
            const firstItem = this.menu.querySelector('.mi-quick-insert-item');
            if (firstItem) {
                firstItem.focus();
                this.selectedIndex = 0;
            }
        }

        /**
         * Handle menu item click.
         */
        handleItemClick(template) {
            if (!template) {
                return;
            }

            // Insert template into visual builder
            this.insertTemplate(template);

            // Close menu
            this.close();
        }

        /**
         * Insert template into visual builder.
         */
        insertTemplate(template) {
            const visualBuilder = this.widget.visualBuilder;
            const cursorManager = this.widget.cursorManager;

            if (!visualBuilder || !cursorManager) {
                console.warn('Visual builder or cursor manager not available');
                return;
            }

            // Get current cursor position
            const cursor = cursorManager.getCursorPosition();

            // Create node from template
            const newNode = createNodeFromTemplate(template);

            if (!newNode) {
                console.warn('Failed to create node from template:', template);
                return;
            }

            // Insert node at cursor
            insertNode(cursor, newNode);

            // Update visual builder
            visualBuilder.render();

            // Update preview
            const latex = astToLatex(visualBuilder.ast);
            const previewContainer = this.widget.querySelector('.mi-preview');
            if (previewContainer) {
                renderPreview(latex, previewContainer);
            }

            // Update hidden field
            const hiddenInput = this.widget.querySelector('.mi-hidden-input');
            if (hiddenInput) {
                hiddenInput.value = latex;
            }

            // Focus visual builder
            const visualBuilderContainer = this.widget.querySelector('.mi-visual-builder');
            if (visualBuilderContainer) {
                visualBuilderContainer.focus();
            }
        }
    }

    /**
     * Preset configurations (quick_inserts data).
     * This should ideally be loaded from Django, but for now we provide a mapping.
     */
    const PRESET_CONFIGS = {
        'algebra': {
            name: 'Algebra',
            quick_inserts: [
                ['Quadratic Equation', 'ax^2 + bx + c = 0'],
                ['Polynomial', 'p(x) = a_n x^n + a_{n-1} x^{n-1} + \\cdots + a_0'],
                ['Square', 'x^2'],
                ['Square Root', '\\sqrt{x}'],
                ['Fraction', '\\frac{a}{b}'],
                ['Absolute Value', '|x|'],
                ['Factorial', 'n!'],
            ]
        },
        'calculus': {
            name: 'Calculus',
            quick_inserts: [
                ['Indefinite Integral', '\\int f(x) \\, dx'],
                ['Definite Integral', '\\int_{a}^{b} f(x) \\, dx'],
                ['Derivative', '\\frac{d}{dx}'],
                ['Partial Derivative', '\\frac{\\partial}{\\partial x}'],
                ['Limit', '\\lim_{x \\to a} f(x)'],
                ['Second Derivative', '\\frac{d^2}{dx^2}'],
                ['Chain Rule', '\\frac{d}{dx}[f(g(x))] = f\'(g(x)) \\cdot g\'(x)'],
                ['Fundamental Theorem', '\\int_{a}^{b} f\'(x) \\, dx = f(b) - f(a)'],
            ]
        },
        'physics': {
            name: 'Physics',
            quick_inserts: [
                ['Newton\'s Second Law', 'F = ma'],
                ['Kinetic Energy', 'E_k = \\frac{1}{2}mv^2'],
                ['Potential Energy', 'E_p = mgh'],
                ['Wave Equation', 'y(x,t) = A\\sin(kx - \\omega t)'],
                ['Schrödinger Equation', 'i\\hbar\\frac{\\partial}{\\partial t}\\psi = \\hat{H}\\psi'],
            ]
        },
        'machine_learning': {
            name: 'Machine Learning',
            quick_inserts: [
                ['Linear Regression', 'y = \\mathbf{w}^T \\mathbf{x} + b'],
                ['Sigmoid', '\\sigma(x) = \\frac{1}{1 + e^{-x}}'],
                ['Cross Entropy', 'H(p,q) = -\\sum_i p(i)\\log q(i)'],
                ['Gradient', '\\nabla f = \\left(\\frac{\\partial f}{\\partial x_1}, \\ldots, \\frac{\\partial f}{\\partial x_n}\\right)'],
            ]
        },
        'statistics': {
            name: 'Statistics',
            quick_inserts: [
                ['Mean', '\\bar{x} = \\frac{1}{n}\\sum_{i=1}^{n} x_i'],
                ['Variance', '\\sigma^2 = \\frac{1}{n}\\sum_{i=1}^{n}(x_i - \\bar{x})^2'],
                ['Standard Deviation', '\\sigma = \\sqrt{\\frac{1}{n}\\sum_{i=1}^{n}(x_i - \\bar{x})^2}'],
                ['Normal Distribution', 'f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}}e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}'],
            ]
        },
        'probability': {
            name: 'Probability',
            quick_inserts: [
                ['Probability', 'P(A)'],
                ['Conditional Probability', 'P(A|B) = \\frac{P(A \\cap B)}{P(B)}'],
                ['Bayes\' Theorem', 'P(A|B) = \\frac{P(B|A)P(A)}{P(B)}'],
                ['Expected Value', 'E[X] = \\sum_{i} x_i P(x_i)'],
            ]
        }
    };

    /**
     * Get preset configuration by code.
     * 
     * @param {string} presetCode - Preset code (e.g., 'algebra', 'calculus')
     * @returns {Object} Preset configuration object
     */
    function getPresetConfig(presetCode) {
        return PRESET_CONFIGS[presetCode] || PRESET_CONFIGS['algebra'];
    }

    /**
     * Initialize quick insert dropdown.
     * 
     * @param {HTMLElement} widget - Widget container element
     * @param {string} presetCode - Preset code
     */
    function initializeQuickInsert(widget, presetCode) {
        const quickInsertContainer = widget.querySelector('.mi-quick-insert');
        if (!quickInsertContainer) {
            return;
        }

        // Get preset configuration
        const presetConfig = getPresetConfig(presetCode);

        // Create and store QuickInsertManager instance
        const quickInsertManager = new QuickInsertManager(widget, presetConfig);
        widget.quickInsertManager = quickInsertManager;
    }

    // Expose QuickInsertManager and initializeQuickInsert globally
    window.QuickInsertManager = QuickInsertManager;
    window.initializeQuickInsert = initializeQuickInsert;
    
    // Expose formatting functions globally
    window.handleFormatButton = handleFormatButton;
    window.applyBoldFormat = applyBoldFormat;
    window.applyColorFormat = applyColorFormat;
    window.applySizeFormat = applySizeFormat;
    
    // Expose mode switching functions globally
    window.handleModeChange = handleModeChange;
    window.getModeConfig = getModeConfig;
    window.updateToolbarVisibility = updateToolbarVisibility;
    
    // Expose sync manager and related functions globally
    window.SyncManager = SyncManager;
    window.toggleVisualSourceMode = toggleVisualSourceMode;
    
    // Expose mobile features globally
    window.initializeMobileFeatures = initializeMobileFeatures;
    window.initializeCollapsiblePreview = initializeCollapsiblePreview;
    window.initializeSwipeGestures = initializeSwipeGestures;

    // ============================================================================
    // Accessibility: Keyboard Navigation
    // ============================================================================

    /**
     * Setup comprehensive keyboard navigation for the widget.
     * 
     * @param {HTMLElement} widget - Widget container element
     */
    function setupKeyboardNavigation(widget) {
        // Tab navigation through toolbar buttons
        const toolbarContainer = widget.querySelector('.mi-toolbar-container');
        if (toolbarContainer) {
            const buttons = toolbarContainer.querySelectorAll('.mi-button, .mi-toolbar-button');
            
            buttons.forEach((button, index) => {
                // Make buttons keyboard accessible
                button.setAttribute('tabindex', '0');
                
                // Enter/Space to activate button
                button.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        button.click();
                    }
                });
            });
        }

        // Arrow key navigation in visual builder
        const visualBuilder = widget.querySelector('.mi-visual-builder');
        if (visualBuilder && widget.visualBuilder) {
            visualBuilder.addEventListener('keydown', function(e) {
                handleVisualBuilderKeyboard(e, widget);
            });
        }

        // Tab navigation between placeholders (already implemented, but ensure it's active)
        ensurePlaceholderKeyboardNavigation(widget);
    }

    /**
     * Handle keyboard navigation in visual builder.
     * 
     * @param {KeyboardEvent} e - Keyboard event
     * @param {HTMLElement} widget - Widget container element
     */
    function handleVisualBuilderKeyboard(e, widget) {
        const visualBuilder = widget.visualBuilder;
        const cursorManager = widget.cursorManager;
        
        if (!visualBuilder || !cursorManager) {
            return;
        }

        const placeholders = visualBuilder.placeholderManager ? visualBuilder.placeholderManager.placeholders : [];

        switch (e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                navigatePlaceholders(widget, -1);
                break;
            case 'ArrowRight':
                e.preventDefault();
                navigatePlaceholders(widget, 1);
                break;
            case 'ArrowUp':
                e.preventDefault();
                // Move to previous placeholder or first placeholder
                if (placeholders.length > 0) {
                    const currentIndex = getCurrentPlaceholderIndex(widget);
                    const targetIndex = currentIndex > 0 ? currentIndex - 1 : 0;
                    if (placeholders[targetIndex]) {
                        cursorManager.setCursor(placeholders[targetIndex]);
                        placeholders[targetIndex].focus();
                    }
                }
                break;
            case 'ArrowDown':
                e.preventDefault();
                // Move to next placeholder or last placeholder
                if (placeholders.length > 0) {
                    const currentIndex = getCurrentPlaceholderIndex(widget);
                    const targetIndex = currentIndex < placeholders.length - 1 ? currentIndex + 1 : placeholders.length - 1;
                    if (placeholders[targetIndex]) {
                        cursorManager.setCursor(placeholders[targetIndex]);
                        placeholders[targetIndex].focus();
                    }
                }
                break;
            case 'Home':
                e.preventDefault();
                // Move to first placeholder
                if (placeholders.length > 0) {
                    cursorManager.setCursor(placeholders[0]);
                    placeholders[0].focus();
                }
                break;
            case 'End':
                e.preventDefault();
                // Move to last placeholder
                if (placeholders.length > 0) {
                    const lastIndex = placeholders.length - 1;
                    cursorManager.setCursor(placeholders[lastIndex]);
                    placeholders[lastIndex].focus();
                }
                break;
        }
    }

    /**
     * Navigate between placeholders using arrow keys.
     * 
     * @param {HTMLElement} widget - Widget container element
     * @param {number} direction - Direction to navigate (-1 for left, 1 for right)
     */
    function navigatePlaceholders(widget, direction) {
        const visualBuilder = widget.visualBuilder;
        const cursorManager = widget.cursorManager;
        
        if (!visualBuilder || !cursorManager) {
            return;
        }

        const placeholders = visualBuilder.placeholderManager ? visualBuilder.placeholderManager.placeholders : [];
        
        if (placeholders.length === 0) {
            return;
        }

        const currentIndex = getCurrentPlaceholderIndex(widget);
        const targetIndex = currentIndex + direction;

        if (targetIndex >= 0 && targetIndex < placeholders.length) {
            cursorManager.setCursor(placeholders[targetIndex]);
            placeholders[targetIndex].focus();
        }
    }

    /**
     * Get current placeholder index.
     * 
     * @param {HTMLElement} widget - Widget container element
     * @returns {number} Current placeholder index, or -1 if none
     */
    function getCurrentPlaceholderIndex(widget) {
        const visualBuilder = widget.visualBuilder;
        if (!visualBuilder || !visualBuilder.placeholderManager) {
            return -1;
        }

        const placeholders = visualBuilder.placeholderManager.placeholders;
        const activeElement = document.activeElement;

        for (let i = 0; i < placeholders.length; i++) {
            if (placeholders[i] === activeElement || placeholders[i].contains(activeElement)) {
                return i;
            }
        }

        return 0; // Default to first placeholder
    }

    /**
     * Ensure placeholder keyboard navigation is set up.
     * 
     * @param {HTMLElement} widget - Widget container element
     */
    function ensurePlaceholderKeyboardNavigation(widget) {
        // This is already implemented in setupEventListeners, but we ensure it's active
        const visualBuilder = widget.querySelector('.mi-visual-builder');
        if (!visualBuilder) {
            return;
        }

        // Make visual builder focusable
        visualBuilder.setAttribute('tabindex', '0');
        
        // Ensure placeholders are keyboard accessible
        visualBuilder.addEventListener('focus', function() {
            const placeholders = visualBuilder.querySelectorAll('.mi-placeholder');
            placeholders.forEach(placeholder => {
                placeholder.setAttribute('tabindex', '0');
            });
        });
    }

    /**
     * Announce to screen readers.
     * 
     * @param {HTMLElement} widget - Widget container element
     * @param {string} message - Message to announce
     * @param {string} priority - 'polite' or 'assertive'
     */
    function announceToScreenReader(widget, message, priority = 'polite') {
        // Use existing preview aria-live region or create one
        let liveRegion = widget.querySelector('.mi-preview[aria-live]');
        
        if (!liveRegion) {
            // Create a hidden live region if preview doesn't exist
            liveRegion = document.createElement('div');
            liveRegion.className = 'mi-screen-reader-announce';
            liveRegion.setAttribute('role', 'status');
            liveRegion.setAttribute('aria-live', priority);
            liveRegion.setAttribute('aria-atomic', 'true');
            liveRegion.style.cssText = 'position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden;';
            widget.appendChild(liveRegion);
        }

        // Update live region to trigger announcement
        liveRegion.setAttribute('aria-live', priority);
        liveRegion.textContent = message;
        
        // Clear after announcement
        setTimeout(() => {
            liveRegion.textContent = '';
        }, 1000);
    }

    // Expose accessibility functions globally
    window.setupKeyboardNavigation = setupKeyboardNavigation;
    window.announceToScreenReader = announceToScreenReader;

    // ============================================================================
    // Mobile Responsive Features
    // ============================================================================

    /**
     * Initialize collapsible preview for mobile.
     * 
     * @param {HTMLElement} widget - Widget container element
     */
    function initializeCollapsiblePreview(widget) {
        const previewContainer = widget.querySelector('.mi-preview-container');
        const previewToggle = widget.querySelector('.mi-preview-toggle');
        
        if (!previewContainer || !previewToggle) {
            return;
        }

        // Check if we're on mobile
        const isMobile = window.matchMedia('(max-width: 768px)').matches;
        
        if (!isMobile) {
            // On desktop, always show preview
            previewContainer.classList.remove('collapsed');
            previewToggle.setAttribute('aria-expanded', 'true');
            return;
        }

        // On mobile, make preview collapsible
        previewToggle.addEventListener('click', function() {
            const isExpanded = previewContainer.classList.contains('collapsed');
            
            if (isExpanded) {
                previewContainer.classList.remove('collapsed');
                previewToggle.setAttribute('aria-expanded', 'true');
            } else {
                previewContainer.classList.add('collapsed');
                previewToggle.setAttribute('aria-expanded', 'false');
            }
        });

        // Listen for media query changes
        const mediaQuery = window.matchMedia('(max-width: 768px)');
        mediaQuery.addEventListener('change', function(e) {
            if (!e.matches) {
                // Desktop - always show
                previewContainer.classList.remove('collapsed');
                previewToggle.setAttribute('aria-expanded', 'true');
            }
        });
    }

    /**
     * Initialize swipe gestures for tab switching.
     * 
     * @param {HTMLElement} widget - Widget container element
     */
    function initializeSwipeGestures(widget) {
        const modeTabs = widget.querySelector('.mi-mode-tabs');
        
        if (!modeTabs) {
            return;
        }

        // Check if we're on a touch device
        const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
        
        if (!isTouchDevice) {
            return;
        }

        let touchStartX = 0;
        let touchStartY = 0;
        let touchEndX = 0;
        let touchEndY = 0;
        const swipeThreshold = 50; // Minimum distance for swipe
        const swipeMaxVertical = 30; // Maximum vertical movement to consider horizontal swipe

        modeTabs.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
            touchStartY = e.changedTouches[0].screenY;
        }, { passive: true });

        modeTabs.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            touchEndY = e.changedTouches[0].screenY;
            
            const deltaX = touchEndX - touchStartX;
            const deltaY = Math.abs(touchEndY - touchStartY);
            
            // Only process horizontal swipes (vertical movement should be minimal)
            if (deltaY > swipeMaxVertical) {
                return;
            }
            
            // Swipe right (next tab)
            if (deltaX > swipeThreshold) {
                const visualTab = widget.querySelector('.mi-tab-visual');
                const sourceTab = widget.querySelector('.mi-tab-source');
                
                if (sourceTab && sourceTab.classList.contains('active')) {
                    visualTab.click();
                }
            }
            
            // Swipe left (previous tab)
            if (deltaX < -swipeThreshold) {
                const visualTab = widget.querySelector('.mi-tab-visual');
                const sourceTab = widget.querySelector('.mi-tab-source');
                
                if (visualTab && visualTab.classList.contains('active')) {
                    sourceTab.click();
                }
            }
        }, { passive: true });
    }

    /**
     * Initialize mobile-specific features.
     * 
     * @param {HTMLElement} widget - Widget container element
     */
    function initializeMobileFeatures(widget) {
        initializeCollapsiblePreview(widget);
        initializeSwipeGestures(widget);
    }

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
            
            // Create and store CursorManager
            const cursorManager = new CursorManager(widget);
            widget.cursorManager = cursorManager;
            
            // Render the AST
            visualBuilder.render();
        }

        // Initialize source mode sync
        initializeSourceMode(widget, config.value || '');

        // Initialize preview with KaTeX
        const previewContainer = widget.querySelector('.mi-preview');
        if (previewContainer && config.value) {
            renderPreview(config.value, previewContainer);
        } else if (previewContainer) {
            previewContainer.innerHTML = '<span class="mi-preview-empty">Preview will appear here</span>';
        }

        // Initialize quick insert dropdown
        initializeQuickInsert(widget, config.preset || 'algebra');

        // Initialize mobile features
        initializeMobileFeatures(widget);

        // Setup event listeners
        setupEventListeners(widget);

        console.log('MathInput widget initialized:', widgetId, config);
    }

    /**
     * Toggle between visual and source modes.
     * 
     * @param {HTMLElement} widget - Widget container element
     */
    function toggleVisualSourceMode(widget) {
        const tabs = widget.querySelectorAll('.mi-tab');
        const visualTab = widget.querySelector('.mi-tab-visual');
        const sourceTab = widget.querySelector('.mi-tab-source');
        
        if (!visualTab || !sourceTab) {
            return;
        }

        // Determine current mode
        const isVisualActive = visualTab.classList.contains('active');
        
        // Toggle to opposite mode
        if (isVisualActive) {
            sourceTab.click();
        } else {
            visualTab.click();
        }
    }

    /**
     * Initialize mode tabs (Visual/Source switching).
     */
    function initializeModeTabs(widget) {
        const tabs = widget.querySelectorAll('.mi-tab');
        const visualContainer = widget.querySelector('.mi-visual-builder-container');
        const sourceContainer = widget.querySelector('.mi-source-container');
        const syncManager = widget.syncManager;

        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const mode = this.dataset.mode;

                // Sync before switching if needed
                if (syncManager && !syncManager.isSyncing()) {
                    if (mode === 'source') {
                        // Switching to source - sync from visual
                        syncManager.syncFromVisual();
                    } else if (mode === 'visual') {
                        // Switching to visual - sync from source
                        syncManager.syncFromSource();
                    }
                }

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
     * Initialize source mode textarea and sync manager.
     */
    function initializeSourceMode(widget, initialValue) {
        const sourceTextarea = widget.querySelector('.mi-source-textarea');
        const hiddenInput = widget.querySelector('.mi-hidden-input');

        if (sourceTextarea) {
            // Set initial value
            if (initialValue) {
                sourceTextarea.value = initialValue;
            }

            // Create sync manager
            const syncManager = new SyncManager(widget);
            widget.syncManager = syncManager;

            // Debounced sync from source to visual
            const debouncedSyncFromSource = debounce(() => {
                syncManager.syncFromSource();
            }, 300);

            // Sync source to visual builder on input
            sourceTextarea.addEventListener('input', function() {
                // Update hidden input immediately
                if (hiddenInput) {
                    hiddenInput.value = this.value;
                }
                // Debounced sync to visual builder
                debouncedSyncFromSource();
            });

            // Sync on blur (immediate sync when user leaves source mode)
            sourceTextarea.addEventListener('blur', function() {
                if (!syncManager.isSyncing()) {
                    syncManager.syncFromSource();
                }
            });
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

