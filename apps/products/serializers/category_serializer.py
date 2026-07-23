from rest_framework import serializers
from apps.products.models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon_svg', 'description', 'image', 'product_count']
