"""
Root URL configuration for Shivank Kirana Store.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import error_404

urlpatterns = [
    # Django Admin
    path('django-admin/', admin.site.urls),

    # Main application URLs
    path('', include('apps.home.urls')),
    path('shop/', include('apps.products.urls')),
    path('category/', include('apps.categories.urls')),
    path('brand/', include('apps.brands.urls')),
    path('cart/', include('apps.cart.urls')),
    path('wishlist/', include('apps.wishlist.urls')),
    path('checkout/', include('apps.checkout.urls')),
    path('orders/', include('apps.orders.urls')),
    path('delivery/', include('apps.delivery.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('search/', include('apps.search.urls')),
    path('auth/', include('apps.accounts.urls')),
    path('hard-5456-work-343-but-12-ha-5/', include('apps.admin_panel.urls')),

    # REST API
    path('api/', include('api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Catch-all pattern for invalid routes -> render custom 404 page
urlpatterns += [
    re_path(r'^.*$', error_404),
]

# Custom error handlers
handler404 = 'apps.core.views.error_404'
handler500 = 'apps.core.views.error_500'
