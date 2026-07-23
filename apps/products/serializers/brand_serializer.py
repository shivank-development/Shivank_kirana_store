from rest_framework import serializers
from apps.products.models.brand import Brand

class BrandSerializer(serializers.ModelSerializer):
    """Serializer for the Brand model."""
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo', 'description', 'product_count']
