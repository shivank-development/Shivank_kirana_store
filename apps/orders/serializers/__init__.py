from rest_framework import serializers
from apps.orders.models import Order

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the Order model."""
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'address', 'subtotal', 'delivery_charge',
            'distance_charge', 'coupon_discount', 'total_amount', 'payment_method',
            'payment_status', 'status', 'placed_at', 'delivered_at'
        ]
        read_only_fields = [
            'id', 'order_number', 'user', 'subtotal', 'delivery_charge',
            'distance_charge', 'coupon_discount', 'total_amount', 'payment_status',
            'status', 'placed_at', 'delivered_at'
        ]
