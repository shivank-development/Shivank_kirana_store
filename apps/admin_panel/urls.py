from django.urls import path
from apps.admin_panel import views

app_name = 'admin_panel'

urlpatterns = [
    # ── DASHBOARD ──
    path('', views.admin_dashboard, name='dashboard'),

    # ── ORDERS ──
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/update/', views.order_update, name='order_update'),
    path('orders/<int:pk>/toggle-cod/', views.order_toggle_cod, name='order_toggle_cod'),

    # ── PAYMENTS ──
    path('payments/', views.payments_manage, name='payments_manage'),
    path('payments/<int:pk>/action/', views.payment_action, name='payment_action'),

    # ── PRODUCTS ──
    path('products/', views.product_list, name='product_list'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # ── CATEGORIES ──
    path('categories/', views.categories_manage, name='categories_manage'),

    # ── BRANDS ──
    path('brands/', views.brand_list, name='brand_list'),
    path('brands/new/', views.brand_create, name='brand_create'),
    path('brands/<int:pk>/edit/', views.brand_edit, name='brand_edit'),
    path('brands/<int:pk>/delete/', views.brand_delete, name='brand_delete'),

    # ── CUSTOMERS ──
    path('customers/', views.customers_manage, name='customers_manage'),

    # ── DELIVERY ──
    path('delivery/', views.delivery_manage, name='delivery_manage'),
    path('delivery/add/', views.delivery_boy_add, name='delivery_boy_add'),
    path('delivery/<int:pk>/toggle/', views.delivery_boy_toggle, name='delivery_boy_toggle'),
    path('delivery/<int:pk>/delete/', views.delivery_boy_delete, name='delivery_boy_delete'),

    # ── PINCODES ──
    path('pincodes/', views.pincodes_manage, name='pincodes_manage'),
    path('pincodes/toggle/<int:pk>/', views.pincode_toggle, name='pincode_toggle'),
    path('pincodes/delete/<int:pk>/', views.pincode_delete, name='pincode_delete'),

    # ── ANALYTICS ──
    path('analytics/', views.analytics_page, name='analytics_page'),

    # ── REPORTS ──
    path('reports/', views.reports_page, name='reports_page'),

    # ── STOCK ALERTS ──
    path('stock/', views.stock_alerts, name='stock_alerts'),

    # ── IMPORT ──
    path('import/', views.import_page, name='import_page'),

    # ── REVIEWS ──
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<int:pk>/verify/', views.review_toggle_verify, name='review_toggle_verify'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),

    # ── NOTIFICATIONS ──
    path('notifications/', views.notifications_manage, name='notifications_manage'),
    path('notifications/<int:pk>/delete/', views.notification_delete, name='notification_delete'),

    # ── SETTINGS & COUPONS ──
    path('settings/', views.store_settings_view, name='store_settings'),
    path('coupons/', views.coupon_list, name='coupon_list'),
    path('coupons/<int:pk>/delete/', views.coupon_delete, name='coupon_delete'),
]
