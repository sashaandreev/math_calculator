# Running Tests

## Quick Start

Since you're in a virtual environment, run tests from the `django-mathinput` directory:

```powershell
cd django-mathinput
python -m pytest tests/ -v
```

Or from the project root:

```powershell
python -m pytest django-mathinput/tests/ -v
```

## Running Specific Tests

```powershell
# Run security tests only
python -m pytest django-mathinput/tests/test_security_basic.py -v

# Run widget tests only
python -m pytest django-mathinput/tests/test_widgets_basic.py -v

# Run with markers
python -m pytest django-mathinput/tests/ -m security -v
python -m pytest django-mathinput/tests/ -m unit -v
```

## Installing Dependencies

If pytest is not found, install it in your virtual environment:

```powershell
python -m pip install pytest pytest-django pytest-cov
python -m pip install -e .
```

## Note

The `pytest.ini` file is in the `django-mathinput` directory, so pytest will use that as the root directory when running tests.

