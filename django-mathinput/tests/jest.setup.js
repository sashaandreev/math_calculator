/**
 * Jest setup file for frontend tests.
 * 
 * This file runs before each test file and sets up the testing environment.
 */

// Polyfill TextEncoder/TextDecoder for Node.js
const { TextEncoder, TextDecoder } = require('util');
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

// Mock KaTeX if not available
if (typeof katex === 'undefined') {
  global.katex = {
    render: jest.fn((latex, container, options) => {
      if (options && options.throwOnError) {
        // Simulate parse errors for invalid LaTeX
        if (latex.includes('\\invalid') || latex.includes('error')) {
          throw new Error('KaTeX parse error: Invalid LaTeX');
        }
      }
      // Mock successful rendering
      container.innerHTML = `<span class="katex-rendered">${latex}</span>`;
    }),
  };
}

// Setup DOM environment
// Note: jsdom is already set up by Jest's jsdom environment
// We just need to ensure window and document are available
if (typeof window === 'undefined') {
  const { JSDOM } = require('jsdom');
  const dom = new JSDOM('<!DOCTYPE html><html><head></head><body></body></html>', {
    url: 'http://localhost',
    pretendToBeVisual: true,
    resources: 'usable',
  });

  global.window = dom.window;
  global.document = dom.window.document;
  global.Node = dom.window.Node;
  global.HTMLElement = dom.window.HTMLElement;
  global.Element = dom.window.Element;
} else {
  // jsdom environment already provides these
  global.window = window;
  global.document = document;
}

// Load mathinput.js
const fs = require('fs');
const path = require('path');

const mathinputPath = path.join(__dirname, '../mathinput/static/mathinput/js/mathinput.js');
if (fs.existsSync(mathinputPath)) {
  const mathinputCode = fs.readFileSync(mathinputPath, 'utf8');
  // Execute the IIFE to expose functions to window
  eval(mathinputCode);
}

