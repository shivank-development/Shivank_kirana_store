from rest_framework import serializers
from apps.wishlist.models import WishlistItem
from apps.products.serializers.product_serializer import ProductSerializer

class WishlistItemSerializer(serializers.ModelSerializer):
    """Serializer for wishlist items."""
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'product', 'product_id', 'created_at']
        read_only_fields = ['id', 'created_at']
