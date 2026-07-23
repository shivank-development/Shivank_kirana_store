"""
Core context processors — inject store-wide variables into all templates.
"""
from django.conf import settings


def store_context(request):
    """Inject store configuration into every template."""
    return {
        'STORE_NAME': settings.STORE_NAME,
        'STORE_PHONE': settings.STORE_PHONE,
        'STORE_EMAIL': settings.STORE_EMAIL,
        'STORE_ADDRESS': settings.STORE_ADDRESS,
        'WHATSAPP_NUMBER': settings.WHATSAPP_NUMBER,
        'UPI_ID': settings.UPI_ID,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
    }
