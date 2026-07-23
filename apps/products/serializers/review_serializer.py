from rest_framework import serializers
from apps.products.models.gallery import ProductReview

class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer for product reviews."""
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = ProductReview
        fields = ['id', 'user_name', 'rating', 'comment', 'is_verified', 'created_at']
        read_only_fields = ['id', 'user_name', 'is_verified', 'created_at']
