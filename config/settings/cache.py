"""
Cache Configuration — Local memory cache (no Redis needed)
"""
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'shivank-kirana-cache',
        'TIMEOUT': 300,  # 5 minutes default
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Cache timeouts (seconds)
CACHE_TTL_PRODUCTS = 300       # 5 min
CACHE_TTL_CATEGORIES = 3600    # 1 hour
CACHE_TTL_BRANDS = 3600        # 1 hour
CACHE_TTL_HOME_PAGE = 600      # 10 min
