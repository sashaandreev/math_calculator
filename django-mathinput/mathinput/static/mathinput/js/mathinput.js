/**
 * MathInput Widget JavaScript
 * 
 * Core JavaScript for the math input widget.
 * This is a placeholder - full implementation will be in Phase 2.
 */

(function() {
    'use strict';

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

        // Initialize source mode sync (placeholder)
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

