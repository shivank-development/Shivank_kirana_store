import os
from django.core.wsgi import get_wsgi_application

# Default to production settings for cloud deployments
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.production'))

# Expose WSGI application
from config.wsgi import application
