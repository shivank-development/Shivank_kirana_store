"""API v1 URL routes."""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.v1.auth_api import RegisterAPIView
from api.v1.products_api import ProductListAPIView, ProductDetailAPIView
from api.v1.categories_api import CategoryListAPIView, CategoryProductListAPIView
from api.v1.brands_api import BrandListAPIView, BrandProductListAPIView
from api.v1 import cart_api, wishlist_api, orders_api, delivery_api, payment_api, notifications_api, admin_api

urlpatterns = [
    # Auth Endpoints
    path('auth/register/', RegisterAPIView.as_view(), name='api-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='api-refresh'),
    
    # Products Endpoint
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
    
    # Categories Endpoint
    path('categories/', CategoryListAPIView.as_view(), name='api-category-list'),
    path('categories/<slug:slug>/products/', CategoryProductListAPIView.as_view(), name='api-category-product-list'),
    
    # Brands Endpoint
    path('brands/', BrandListAPIView.as_view(), name='api-brand-list'),
    path('brands/<slug:slug>/products/', BrandProductListAPIView.as_view(), name='api-brand-product-list'),
    
    # Cart Endpoints (Authenticated)
    path('cart/', cart_api.CartAPIView.as_view(), name='api-cart'),
    path('cart/add/', cart_api.CartAddAPIView.as_view(), name='api-cart-add'),
    path('cart/update/<int:item_id>/', cart_api.CartUpdateAPIView.as_view(), name='api-cart-update'),
    path('cart/remove/<int:item_id>/', cart_api.CartRemoveAPIView.as_view(), name='api-cart-remove'),
    
    # Wishlist Endpoints (Authenticated)
    path('wishlist/', wishlist_api.WishlistAPIView.as_view(), name='api-wishlist'),
    path('wishlist/toggle/', wishlist_api.WishlistToggleAPIView.as_view(), name='api-wishlist-toggle'),

    # Orders Endpoints (Authenticated)
    path('orders/', orders_api.OrderListAPIView.as_view(), name='api-order-list'),
    path('orders/create/', orders_api.OrderCreateAPIView.as_view(), name='api-order-create'),
    path('orders/<int:pk>/', orders_api.OrderDetailAPIView.as_view(), name='api-order-detail'),
    path('orders/<int:pk>/track/', orders_api.OrderTrackAPIView.as_view(), name='api-order-track'),

    # Delivery Endpoints (Authenticated)
    path('delivery/check/', delivery_api.DeliveryCheckAPIView.as_view(), name='api-delivery-check'),
    path('delivery/calculate-charge/', delivery_api.DeliveryChargeAPIView.as_view(), name='api-delivery-charge'),

    # Payment Endpoints (Authenticated)
    path('payment/initiate/', payment_api.PaymentInitiateAPIView.as_view(), name='api-payment-initiate'),
    path('payment/verify-upi/', payment_api.PaymentVerifyAPIView.as_view(), name='api-payment-verify-upi'),
    path('payment/cod-advance/', payment_api.PaymentCODAdvanceAPIView.as_view(), name='api-payment-cod-advance'),

    # Notifications Endpoint (Authenticated)
    path('notifications/', notifications_api.NotificationListAPIView.as_view(), name='api-notifications'),

    # Admin Endpoints (is_admin required)
    path('admin/dashboard/stats/', admin_api.AdminDashboardStatsAPIView.as_view(), name='api-admin-stats'),
    path('admin/orders/', admin_api.AdminOrderListAPIView.as_view(), name='api-admin-orders'),
    path('admin/orders/<int:pk>/status/', admin_api.AdminOrderStatusUpdateAPIView.as_view(), name='api-admin-order-status'),
    path('admin/payments/<int:pk>/action/', admin_api.AdminPaymentActionAPIView.as_view(), name='api-admin-payment-action'),
    path('admin/products/', admin_api.AdminProductListCreateAPIView.as_view(), name='api-admin-products'),
    path('admin/products/<int:pk>/', admin_api.AdminProductRetrieveUpdateDestroyAPIView.as_view(), name='api-admin-product-detail'),
    path('admin/import/products/', admin_api.AdminProductBulkImportAPIView.as_view(), name='api-admin-import-products'),
    path('admin/analytics/revenue/', admin_api.AdminRevenueAnalyticsAPIView.as_view(), name='api-admin-revenue'),
    path('admin/stock/alerts/', admin_api.AdminLowStockAlertsAPIView.as_view(), name='api-admin-stock-alerts'),
]
