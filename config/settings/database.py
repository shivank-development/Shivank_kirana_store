"""
★ SQLite Database Configuration — Shivank Kirana Store
No external database needed — pure SQLite
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,            # Wait 20s before "database is locked" error
            'check_same_thread': False,
        },
        'TEST': {
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }
}

# Enable WAL mode for better concurrent read performance
DATABASE_OPTIONS = {
    'transaction_mode': 'IMMEDIATE',
}
