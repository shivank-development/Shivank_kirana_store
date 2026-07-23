import os
from datetime import timedelta

# ==========================================
# ADVANCED SECURITY & JWT CONFIGURATIONS
# ==========================================

# 1. JWT (JSON Web Token) Security Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),    # Short-lived access tokens (high security)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),       # 7 days to refresh session
    'ROTATE_REFRESH_TOKENS': True,                     # Issue a new refresh token on use
    'BLACKLIST_AFTER_ROTATION': True,                  # Invalidate old refresh tokens
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.getenv('SECRET_KEY', 'django-insecure-shivank-kirana-store-2026'),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': 'shivank_kirana_store',
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    'JTI_CLAIM': 'jti',
}

# 2. General HTTP Security Hardening
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# 3. Cookie Security 
# (HttpOnly prevents JavaScript access to cookies, mitigating XSS risks)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# For Production (Requires HTTPS):
CSRF_COOKIE_SECURE = os.getenv('SECURE_COOKIES', 'False') == 'True'
SESSION_COOKIE_SECURE = os.getenv('SECURE_COOKIES', 'False') == 'True'
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'