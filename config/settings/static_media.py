"""
Static and Media URL/Root Configuration — Shivank Kirana Store
"""
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ── STATIC FILES ──
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# ── MEDIA FILES (user uploads) ──
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
