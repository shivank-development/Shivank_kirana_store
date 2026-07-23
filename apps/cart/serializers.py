from rest_framework import serializers
from apps.cart.models import Cart, CartItem
from apps.products.serializers.product_serializer import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for individual items inside the cart."""
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    mrp_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'subtotal', 'mrp_total', 'created_at']


class CartSerializer(serializers.ModelSerializer):
    """Serializer for the user's cart including calculated totals."""
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_mrp = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    savings = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    delivery_charge = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'session_key', 'items', 'item_count',
            'subtotal', 'total_mrp', 'savings', 'delivery_charge', 'total',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'session_key']
