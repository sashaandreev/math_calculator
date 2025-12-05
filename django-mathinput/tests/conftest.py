"""
Pytest configuration for django-mathinput tests.

Sets up Django settings and ensures proper test environment.
"""
import os
import django
from django.conf import settings

# Set Django settings module if not already set
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')

# Configure Django if not already configured
if not settings.configured:
    django.setup()

