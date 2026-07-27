import os
from django.core.asgi import get_asgi_application

# Default to production settings for cloud deployments
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.production'))

# Expose ASGI application for Daphne, Shipit, Uvicorn, and Channels
from config.asgi import application
