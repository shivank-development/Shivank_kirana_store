"""
Base settings for Shivank Kirana Store.
Common settings shared across all environments.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-shivank-kirana-store-2026')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'channels',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'django_extensions',
    'drf_spectacular',
]

LOCAL_APPS = [
    'apps.core',
    'apps.accounts',
    'apps.products',
    'apps.categories',
    'apps.brands',
    'apps.cart',
    'apps.wishlist',
    'apps.orders',
    'apps.delivery',
    'apps.payments',
    'apps.notifications',
    'apps.analytics',
    'apps.import_export',
    'apps.chatbot',
    'apps.support',
    'apps.home',
    'apps.checkout',
    'apps.search',
    'apps.admin_panel',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middleware.request_logger.RequestLoggerMiddleware',
    'config.middleware.nocache.NoCacheMiddleware',
]

ROOT_URLCONF = 'config.urls'
ASGI_APPLICATION = 'config.asgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.cart.context_processors.cart_context',
                'apps.core.context_processors.store_context',
            ],
        },
    },
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'utilities.paginator.StandardPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# DRF Spectacular (API docs)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Shivank Kirana Store API',
    'DESCRIPTION': 'Premium Kirana Store E-Commerce REST API',
    'VERSION': '1.0.0',
}

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Store Configuration
STORE_NAME = os.getenv('STORE_NAME', 'Shivank Kirana Store')
STORE_PHONE = os.getenv('STORE_PHONE', '+917599342112')
STORE_EMAIL = os.getenv('STORE_EMAIL', 'support@shivankkirana.com')
STORE_ADDRESS = os.getenv('STORE_ADDRESS', '288, Main Market, Meerut - 250404')
STORE_LAT = float(os.getenv('STORE_LAT', '28.9845'))
STORE_LNG = float(os.getenv('STORE_LNG', '77.7064'))

# UPI Payment
UPI_ID = os.getenv('UPI_ID', '7060169850@ptyes')
UPI_NAME = os.getenv('UPI_NAME', 'Shivank So Om Pal')

# Delivery Charges
FREE_DELIVERY_THRESHOLD = int(os.getenv('FREE_DELIVERY_THRESHOLD', '799'))
BASE_DELIVERY_CHARGE = int(os.getenv('BASE_DELIVERY_CHARGE', '49'))
DISTANCE_BASE_KM = int(os.getenv('DISTANCE_BASE_KM', '10'))
DISTANCE_BASE_CHARGE = int(os.getenv('DISTANCE_BASE_CHARGE', '99'))
DISTANCE_INCREMENT_KM = int(os.getenv('DISTANCE_INCREMENT_KM', '20'))
DISTANCE_INCREMENT_CHARGE = int(os.getenv('DISTANCE_INCREMENT_CHARGE', '50'))

# COD
COD_ADVANCE_AMOUNT = int(os.getenv('COD_ADVANCE_AMOUNT', '49'))

# Google Maps
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

# WhatsApp
WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER', '917599342112')

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = f'{STORE_NAME} <{STORE_EMAIL}>'

# Import Security and JWT settings
from .jwt import *
