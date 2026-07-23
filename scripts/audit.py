import os, sys, django
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

def ok(condition): return '[OK]' if condition else '[!!]'

print('=== FEATURE DEEP AUDIT ===')

# Reviews model
try:
    from apps.products.models.review import ProductReview
    fields = [f.name for f in ProductReview._meta.get_fields()]
    print(ok(True) + ' Reviews model fields: ' + str(fields))
except Exception as e:
    print('[!!] Reviews model: ' + str(e))

# Wishlist
try:
    from apps.wishlist.models import WishlistItem
    print('[OK] Wishlist model: OK')
except Exception as e:
    print('[!!] Wishlist: ' + str(e))

# Notifications
try:
    from apps.notifications.models import Notification
    fields = [f.name for f in Notification._meta.get_fields()]
    print('[OK] Notification model fields: ' + str(fields))
except Exception as e:
    print('[!!] Notifications model: ' + str(e))

# Delivery
try:
    from apps.delivery.models import DeliveryProfile
    print('[OK] Delivery model: OK')
except Exception as e:
    print('[!!] Delivery: ' + str(e))

# WebSocket consumers
for path in ['apps/notifications/websocket/__init__.py', 'apps/delivery/websocket/__init__.py']:
    print(ok(os.path.exists(path)) + ' Consumer: ' + path)

# JS files
js_features = {
    'Cart AJAX': 'static/js/cart/cart_manager.js',
    'Wishlist JS': 'static/js/wishlist/wishlist_manager.js',
    'GSAP animations': 'static/js/animations/gsap_init.js',
    'Search handler': 'static/js/search/search_handler.js',
    'UPI payment JS': 'static/js/checkout/upi_payment.js',
    'Delivery tracker': 'static/js/delivery/live_tracker.js',
}
for name, path in js_features.items():
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(ok(size > 100) + ' ' + name + ': ' + str(size) + ' bytes')
    else:
        print('[!!] ' + name + ': MISSING')

# Admin panel views
try:
    from apps.admin_panel import views as apv
    admin_views = [x for x in dir(apv) if not x.startswith('_')]
    print('[OK] Admin panel views: ' + str(admin_views))
except Exception as e:
    print('[!!] Admin panel: ' + str(e))

# Home view context
try:
    from apps.home import views as hv
    import inspect
    src = inspect.getsource(hv.home_view)
    print(ok('new_arrival' in src or 'featured' in src) + ' Home - new arrivals: ' + str('new_arrival' in src))
    print(ok('popular' in src.lower()) + ' Home - popular products: ' + str('popular' in src.lower()))
    print(ok('brand' in src.lower()) + ' Home - brands: ' + str('brand' in src.lower()))
except Exception as e:
    print('[!!] Home view: ' + str(e))

# Delivery charge service
delivery_svc = 'services/delivery/charge_calculator.py'
if os.path.exists(delivery_svc):
    with open(delivery_svc) as f:
        content = f.read()
    has_haversine = 'haversine' in content.lower() or 'distance' in content.lower()
    print(ok(has_haversine) + ' Delivery charge calculator: haversine=' + str(has_haversine))
else:
    print('[!!] Delivery charge calculator: MISSING')

# Check review view
try:
    from apps.products import views as pv
    import inspect
    src = inspect.getsource(pv.product_detail)
    has_reviews = 'review' in src.lower()
    has_bulk_pricing = 'bulk' in src.lower() or 'BulkPricing' in src
    print(ok(has_reviews) + ' Product detail - reviews: ' + str(has_reviews))
    print(ok(has_bulk_pricing) + ' Product detail - bulk pricing: ' + str(has_bulk_pricing))
except Exception as e:
    print('[!!] Product detail: ' + str(e))

print('=== END AUDIT ===')
