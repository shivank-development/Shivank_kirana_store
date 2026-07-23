"""
WebSocket URL routing for Shivank Kirana Store.
"""
from django.urls import path
from apps.orders.websocket import consumers as order_consumers
from apps.delivery.websocket import consumers as delivery_consumers
from apps.notifications.websocket import consumers as notification_consumers

websocket_urlpatterns = [
    # Order status updates (customer)
    path('ws/orders/<str:order_id>/', order_consumers.OrderStatusConsumer.as_asgi()),

    # Live delivery tracking (customer)
    path('ws/delivery/<str:order_id>/', delivery_consumers.DeliveryTrackingConsumer.as_asgi()),

    # Push notifications (customer)
    path('ws/notifications/<int:user_id>/', notification_consumers.NotificationConsumer.as_asgi()),

    # Admin live dashboard
    path('ws/admin/dashboard/', order_consumers.AdminDashboardConsumer.as_asgi()),

    # GPS location upload (delivery boy)
    path('ws/delivery-boy/<int:delivery_boy_id>/', delivery_consumers.DeliveryBoyLocationConsumer.as_asgi()),
]
