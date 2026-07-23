from rest_framework import serializers
from apps.products.models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model, exposing all details and calculated properties.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    savings = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'weight',
            'price', 'discount_price', 'discount_percent', 'selling_price', 'savings',
            'stock', 'in_stock', 'is_featured', 'is_new_launch', 'is_combo_deal',
            'delivery_eta', 'rating_avg', 'rating_count', 'bought_count',
            'image_main', 'category', 'category_name', 'brand', 'brand_name',
            'created_at', 'updated_at'
        ]
