from rest_framework import generics
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from apps.products.models.category import Category
from apps.products.models.product import Product
from apps.products.serializers.category_serializer import CategorySerializer
from apps.products.serializers.product_serializer import ProductSerializer

class CategoryListAPIView(generics.ListAPIView):
    """
    API endpoint to list all active categories.
    """
    queryset = Category.objects.filter(is_active=True).prefetch_related('products')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class CategoryProductListAPIView(generics.ListAPIView):
    """
    API endpoint to list products belonging to a specific category.
    """
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['brand__slug', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'discount_price', 'created_at', 'rating_avg']
    ordering = ['-created_at']

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        return Product.objects.filter(is_active=True, category__slug=category_slug).select_related('category', 'brand')
