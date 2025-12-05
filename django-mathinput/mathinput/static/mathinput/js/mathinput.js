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

    /**
     * Sync source mode textarea with LaTeX.
     * 
     * @param {HTMLElement} widget - Widget container element
     * @param {string} latex - LaTeX string
     */
    function syncSourceMode(widget, latex) {
        if (!widget) return;

        const sourceTextarea = widget.querySelector('.mi-source-textarea');
        if (sourceTextarea) {
            sourceTextarea.value = latex || '';
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

    /**
     * Setup event listeners for a widget.
     * 
     * @param {HTMLElement} widget - Widget container element
     */
    function setupEventListeners(widget) {
        if (!widget) return;

        // Setup toolbar button click handlers
        const toolbarButtons = widget.querySelectorAll('.mi-button[data-action="insert"]');
        toolbarButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                handleButtonClick(this, widget);
            });
        });

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

        // Setup event listeners
        setupEventListeners(widget);

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

