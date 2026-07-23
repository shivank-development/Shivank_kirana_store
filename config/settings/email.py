"""
Email Settings — Shivank Kirana Store
Uses Gmail SMTP for transactional emails
"""
import os

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = f"Shivank Kirana Store <{EMAIL_HOST_USER}>"

# In development: use console backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
