"""
Production settings for Shivank Kirana Store
DEBUG=False, Secure headers, Allowed hosts
"""
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']  # Replace with your domain in production

# ── SECURITY ──
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# ── DATABASE (same SQLite in production) ──
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
        }
    }
}

# ── STATIC & MEDIA ──
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'
