# Changelog

All notable changes to django-mathinput will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-XX

### Added
- Initial release of django-mathinput
- CKEditor-style math formula editor widget for Django
- Graphical button-based interface for formula building
- Visual formula builder with live preview
- Multiple input modes:
  - Regular Functions
  - Advanced Expressions
  - Integrals/Differentials
  - Matrices
  - Statistics/Probability
  - Physics/Engineering
- Domain presets:
  - Algebra
  - Calculus
  - Physics
  - Machine Learning
  - Statistics
  - Probability
- Visual and Source mode switching
- 7 tabbed toolbars: Text, Basic, Advanced, Calculus, Matrices, Trigonometry, Symbols
- Quick insert templates for common formulas
- LaTeX storage format
- Template filters: `as_mathinput`, `render_math`, `render_math_inline`
- Comprehensive security features:
  - XSS protection
  - Command injection prevention
  - DoS attack prevention
  - Input sanitization
- Form validation with `MathInputValidator`
- Django Admin integration
- Mobile responsive design
- Keyboard navigation support
- WCAG 2.1 AA accessibility compliance
- Comprehensive test suite (unit, integration, security, performance, compatibility)
- Complete documentation:
  - README.md with installation and quick start
  - User Guide
  - Developer Guide
  - API Documentation
  - Code Examples

### Security
- XSS attack vector protection (script tags, JavaScript protocol, event handlers)
- Command injection prevention (LaTeX commands, file system access, system commands)
- DoS attack prevention (length limits, nesting depth limits, matrix size limits)
- Input sanitization and validation
- Command whitelist/blacklist system

### Performance
- Fast preview updates (< 100ms for moderate formulas)
- Efficient widget rendering
- Optimized validation
- Memory-efficient operations

### Compatibility
- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Django 3.2, 4.0, 4.1, 4.2
- Modern web browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)

### Documentation
- Complete README with examples
- User Guide with mode/preset selection
- Developer Guide with customization examples
- API Documentation
- Code Examples for common use cases
- Security Audit Report

### Testing
- 500+ unit tests
- Integration tests for forms, templates, admin
- Security tests for XSS, injection, DoS
- Performance tests
- Compatibility tests
- User story tests (all 16 stories)
- Frontend JavaScript tests

---

## [Unreleased]

### Planned
- Additional input modes
- More domain presets
- Enhanced visual builder features
- Additional template filters
- Performance optimizations
- Extended browser support

---

[1.0.0]: https://github.com/yourusername/django-mathinput/releases/tag/v1.0.0

