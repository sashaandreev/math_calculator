# Implementation Plan - Phase 6: Release

## Overview
Phase 6 prepares the package for PyPI release: package preparation, release candidate testing, and production release.

## Tasks

### ✅Task 24: PyPI Package Preparation
**Owner:** Lead Dev  
**Duration:** 2 days  
**Dependencies:** Task 23

**Implementation:**
- Finalize `setup.py`:
  ```python
  from setuptools import setup, find_packages
  
  with open("README.md", "r", encoding="utf-8") as fh:
      long_description = fh.read()
  
  setup(
      name="django-mathinput",
      version="1.0.0",
      author="Your Name",
      author_email="your.email@example.com",
      description="CKEditor-style math formula editor for Django",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/yourusername/django-mathinput",
      packages=find_packages(),
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Framework :: Django",
          "Framework :: Django :: 3.2",
          "Framework :: Django :: 4.0",
          "Framework :: Django :: 4.1",
          "Framework :: Django :: 4.2",
      ],
      python_requires=">=3.8",
      install_requires=[
          "Django>=3.2",
      ],
      include_package_data=True,
      zip_safe=False,
  )
  ```

- Update `MANIFEST.in`:
  ```
  include README.md
  include LICENSE
  include CHANGELOG.md
  recursive-include mathinput/templates *
  recursive-include mathinput/static *
  recursive-include tests *
  global-exclude *.pyc
  global-exclude __pycache__
  ```

- Create `CHANGELOG.md`
- Create `LICENSE` file (MIT)
- Verify package structure
- Test package installation

**Deliverables:**
- Complete `setup.py`
- Updated `MANIFEST.in`
- `CHANGELOG.md`
- `LICENSE` file
- Package installable locally

---

### Task 25: Release Candidate
**Owner:** Lead Dev  
**Duration:** 3 days  
**Dependencies:** Task 24

**Implementation:**
- Build package:
  ```bash
  python setup.py sdist bdist_wheel
  ```

- Test package installation:
  ```bash
  pip install dist/django-mathinput-1.0.0rc1.tar.gz
  ```

- Test in clean environment
- Verify all features work
- Run full test suite
- Performance testing
- Security audit
- Documentation review
- Create release notes

**Deliverables:**
- Release candidate package
- Test results
- Release notes
- Known issues list (if any)

---

### Task 26: Production Release
**Owner:** Lead Dev  
**Duration:** 1 day  
**Dependencies:** Task 25

**Implementation:**
- Final version bump
- Upload to PyPI:
  ```bash
  twine upload dist/*
  ```

- Create GitHub release
- Announce release
- Monitor for issues
- Prepare hotfix process (if needed)

**Deliverables:**
- Package on PyPI
- GitHub release
- Release announcement
- Monitoring setup

---

## Phase 6 Testing Requirements

### Release Testing

#### Test File: `tests/test_release.py`

```python
import pytest
import subprocess
import sys


@pytest.mark.release
def test_package_installable():
    """
    What we are testing: Package can be installed via pip
    Why we are testing: Users must be able to install package
    Expected Result: pip install succeeds without errors
    """
    # Test implementation
    pass


@pytest.mark.release
def test_package_imports_correctly():
    """
    What we are testing: Package imports correctly after installation
    Why we are testing: Package must be importable
    Expected Result: All modules import without errors
    """
    # Test implementation
    pass


@pytest.mark.release
def test_all_static_files_included():
    """
    What we are testing: All static files included in package
    Why we are testing: Widget needs CSS/JS files to function
    Expected Result: All static files present in installed package
    """
    # Test implementation
    pass


@pytest.mark.release
def test_all_templates_included():
    """
    What we are testing: All template files included in package
    Why we are testing: Widget needs templates to render
    Expected Result: All template files present in installed package
    """
    # Test implementation
    pass


@pytest.mark.release
def test_package_works_in_clean_environment():
    """
    What we are testing: Package works in fresh virtual environment
    Why we are testing: Users install in clean environments
    Expected Result: Package installs and works in fresh venv
    """
    # Test implementation
    pass


@pytest.mark.release
def test_backward_compatibility():
    """
    What we are testing: Package maintains backward compatibility
    Why we are testing: Existing users should not break
    Expected Result: No breaking changes from previous versions
    """
    # Test implementation
    pass
```

### Integration Tests - Production Environment

#### Test File: `tests/test_production_integration.py`

```python
import pytest
from django.test import TestCase


@pytest.mark.production
class TestProductionIntegration(TestCase):
    """
    What we are testing: Package works in production-like environment
    Why we are testing: Production environment may differ from development
    Expected Result: All features work correctly in production setup
    """
    
    def test_production_settings():
        """
        What we are testing: Widget works with DEBUG=False
        Why we are testing: Production uses DEBUG=False
        Expected Result: Widget functions correctly with production settings
        """
        # Test implementation
        pass
    
    def test_static_files_collected():
        """
        What we are testing: Static files work after collectstatic
        Why we are testing: Production uses collected static files
        Expected Result: Widget CSS/JS load correctly after collectstatic
        """
        # Test implementation
        pass
    
    def test_cdn_fallback_works():
        """
        What we are testing: CDN fallback works if CDN unavailable
        Why we are testing: Network issues should not break widget
        Expected Result: Widget falls back to local assets if CDN fails
        """
        # Test implementation
        pass
```

### User Story Tests - Final Verification

All 16 user stories should be tested one final time in production-like environment:

```python
@pytest.mark.release
@pytest.mark.user_story
def test_all_user_stories_in_production():
    """
    What we are testing: All 16 user stories work in production environment
    Why we are testing: Final verification before release
    Expected Result: All user stories pass in production setup
    """
    # Run all user story tests
    pass
```

---

## Phase 6 Completion Criteria

- [ ] Package builds successfully
- [ ] Package installs successfully
- [ ] All tests pass in clean environment
- [ ] All static files included
- [ ] All templates included
- [ ] Documentation complete
- [ ] CHANGELOG.md updated
- [ ] LICENSE file included
- [ ] Release notes prepared
- [ ] Package uploaded to PyPI
- [ ] GitHub release created
- [ ] Release announcement published
- [ ] Monitoring setup
- [ ] Support channels ready

---

## Post-Release Tasks

### Monitoring
- Monitor PyPI download statistics
- Monitor GitHub issues
- Monitor error logs (if applicable)
- Track user feedback

### Support
- Respond to issues
- Answer questions
- Provide support
- Update documentation as needed

### Maintenance
- Plan bug fixes
- Plan feature enhancements
- Plan next version
- Security updates

---

## Phase 6 Manual Testing Checklist

### Package Build Testing

**Test 6.1: Package Build**
- [ ] Run `python setup.py sdist bdist_wheel`
- [ ] Verify build succeeds without errors
- [ ] Verify dist/ directory contains files
- [ ] Verify .tar.gz and .whl files created
- **Expected Result:** Package builds successfully

**Test 6.2: Package Contents**
- [ ] Extract built package
- [ ] Verify all Python files included
- [ ] Verify all templates included
- [ ] Verify all static files included
- [ ] Verify README.md included
- [ ] Verify LICENSE included
- **Expected Result:** All required files in package

**Test 6.3: MANIFEST.in Verification**
- [ ] Check package contents
- [ ] Verify templates in package
- [ ] Verify static files in package
- [ ] Verify no unnecessary files
- **Expected Result:** MANIFEST.in works correctly

### Installation Testing

**Test 6.4: Clean Installation**
- [ ] Create fresh virtual environment
- [ ] Install package: `pip install dist/django-mathinput-1.0.0.tar.gz`
- [ ] Verify installation succeeds
- [ ] Verify no errors or warnings
- **Expected Result:** Package installs in clean environment

**Test 6.5: PyPI Installation Simulation**
- [ ] Test installation from local package (simulating PyPI)
- [ ] Verify dependencies install correctly
- [ ] Verify package imports correctly
- [ ] Verify all modules accessible
- **Expected Result:** Installation works as if from PyPI

**Test 6.6: Upgrade Installation**
- [ ] Install previous version (if exists)
- [ ] Upgrade to new version
- [ ] Verify upgrade succeeds
- [ ] Verify backward compatibility
- **Expected Result:** Upgrade works without breaking changes

### Package Functionality Testing

**Test 6.7: Import Testing**
- [ ] After installation, test: `from mathinput.widgets import MathInputWidget`
- [ ] Test: `from mathinput.templatetags.mathinput_tags import as_mathinput`
- [ ] Verify all imports work
- [ ] Verify no import errors
- **Expected Result:** All imports work correctly

**Test 6.8: Static Files Access**
- [ ] After installation, verify static files accessible
- [ ] Check CSS file loads
- [ ] Check JS file loads
- [ ] Verify file paths correct
- **Expected Result:** Static files accessible after installation

**Test 6.9: Template Files Access**
- [ ] After installation, verify templates accessible
- [ ] Render widget in template
- [ ] Verify template loads correctly
- **Expected Result:** Templates accessible after installation

**Test 6.10: Django Integration**
- [ ] Add to INSTALLED_APPS
- [ ] Run `python manage.py check`
- [ ] Verify no errors
- [ ] Create form with widget
- [ ] Verify widget renders
- **Expected Result:** Django integration works

### Release Candidate Testing

**Test 6.11: Full Feature Test**
- [ ] Install release candidate
- [ ] Test all 16 user stories
- [ ] Test all modes
- [ ] Test all presets
- [ ] Test all features
- **Expected Result:** All features work in release candidate

**Test 6.12: Performance Test**
- [ ] Test preview update speed
- [ ] Test initial load speed
- [ ] Test with large formulas
- [ ] Verify performance meets requirements
- **Expected Result:** Performance meets all targets

**Test 6.13: Security Test**
- [ ] Run all security tests
- [ ] Try XSS attacks
- [ ] Try injection attacks
- [ ] Verify all blocked
- **Expected Result:** Security measures working

**Test 6.14: Compatibility Test**
- [ ] Test on all supported Django versions
- [ ] Test on all supported Python versions
- [ ] Test on all supported browsers
- [ ] Verify compatibility
- **Expected Result:** Compatible with all supported versions

### Documentation Verification

**Test 6.15: README Accuracy**
- [ ] Read README from package
- [ ] Follow installation instructions
- [ ] Follow quick start guide
- [ ] Verify all examples work
- **Expected Result:** README is accurate

**Test 6.16: CHANGELOG Verification**
- [ ] Read CHANGELOG.md
- [ ] Verify all changes documented
- [ ] Verify version numbers correct
- [ ] Verify dates correct
- **Expected Result:** CHANGELOG is complete and accurate

**Test 6.17: License Verification**
- [ ] Verify LICENSE file included
- [ ] Verify license is MIT
- [ ] Verify license text is correct
- **Expected Result:** License file correct

### PyPI Upload Testing

**Test 6.18: Package Validation**
- [ ] Run `twine check dist/*`
- [ ] Verify no errors
- [ ] Verify package valid
- **Expected Result:** Package passes twine validation

**Test 6.19: Test PyPI Upload (Optional)**
- [ ] Upload to Test PyPI first
- [ ] Install from Test PyPI
- [ ] Verify installation works
- [ ] Verify package functional
- **Expected Result:** Test PyPI upload successful

**Test 6.20: Production PyPI Upload**
- [ ] Upload to production PyPI
- [ ] Verify upload succeeds
- [ ] Verify package appears on PyPI
- [ ] Verify package page displays correctly
- **Expected Result:** Package on PyPI

### Post-Release Testing

**Test 6.21: PyPI Installation**
- [ ] Create fresh environment
- [ ] Install from PyPI: `pip install django-mathinput`
- [ ] Verify installation succeeds
- [ ] Verify package works
- **Expected Result:** Installation from PyPI works

**Test 6.22: GitHub Release**
- [ ] Verify GitHub release created
- [ ] Verify release notes included
- [ ] Verify assets attached
- [ ] Verify release tag correct
- **Expected Result:** GitHub release complete

**Test 6.23: Documentation Links**
- [ ] Check PyPI package page
- [ ] Verify links work (homepage, docs, etc.)
- [ ] Verify description accurate
- **Expected Result:** Package page is complete

**Test 6.24: Search Discovery**
- [ ] Search PyPI for "django-mathinput"
- [ ] Verify package appears in results
- [ ] Verify package description helpful
- **Expected Result:** Package discoverable on PyPI

---

## Notes

- Release process must be repeatable
- All credentials must be secure
- Version numbers must follow semantic versioning
- Release notes must be clear and comprehensive
- Support channels must be ready before release
- **Manual Testing:** Complete all manual tests in checklist before marking phase complete

