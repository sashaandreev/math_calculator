"""
Pytest configuration for django-mathinput tests.

Sets up Django settings and ensures proper test environment.
"""
import os
import sys
import django
import pytest
from pathlib import Path
from django.conf import settings
from django.core.management import call_command

# Ensure we can import from the mathinput package and tests.settings
# Handle both running from root directory and from django-mathinput directory
current_dir = Path(__file__).parent  # django-mathinput/tests/
parent_dir = current_dir.parent       # django-mathinput/
root_dir = parent_dir.parent          # root directory (if running from root)

# Add django-mathinput to path so we can import mathinput and tests.settings
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# If running from root, also add root to path (though it's usually already there)
# This ensures tests.settings can be found when DJANGO_SETTINGS_MODULE=tests.settings
if root_dir.exists() and str(root_dir) not in sys.path:
    # Check if we're actually in a root directory structure
    if (root_dir / 'django-mathinput').exists():
        # We're in the root, but we don't need to add it since parent_dir is already added
        pass

# Set Django settings module if not already set
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')

# Configure Django if not already configured
if not settings.configured:
    django.setup()


# pytest-django should automatically handle migrations, but when running from root
# directory, it sometimes doesn't. We ensure migrations run before database tests.

_migrations_run_for_session = False

@pytest.hookimpl(trylast=True)
def pytest_runtest_setup(item):
    """
    Ensure migrations are run before the first database test.
    This hook runs after pytest-django's setup but before the test.
    """
    global _migrations_run_for_session
    
    # Only run for tests marked with django_db
    if item.get_closest_marker('django_db') and not _migrations_run_for_session:
        # Run migrations - the migrate command is idempotent, so it's safe to run multiple times
        # We use a flag to avoid running it for every test, but we'll run it for the first one
        try:
            from django.db import connection
            # Ensure connection is ready
            connection.ensure_connection()
            
            # Try to use pytest-django's db_blocker if available
            try:
                from pytest_django.fixtures import django_db_blocker
                with django_db_blocker.unblock():
                    call_command('migrate', verbosity=0, interactive=False, run_syncdb=True)
                    _migrations_run_for_session = True
            except (ImportError, AttributeError, NameError):
                # pytest-django fixtures not available, run migrations directly
                call_command('migrate', verbosity=0, interactive=False, run_syncdb=True)
                _migrations_run_for_session = True
        except Exception:
            # If the first attempt fails, try again without db_blocker
            try:
                from django.db import connection
                connection.ensure_connection()
                call_command('migrate', verbosity=0, interactive=False, run_syncdb=True)
                _migrations_run_for_session = True
            except Exception:
                # If migrations still fail, don't set the flag so we'll try again
                # This allows retry on the next test
                pass

