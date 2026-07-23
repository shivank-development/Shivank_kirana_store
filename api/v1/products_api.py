from rest_framework import generics
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from apps.products.models.product import Product
from apps.products.serializers.product_serializer import ProductSerializer

class ProductListAPIView(generics.ListAPIView):
    """
    API endpoint to list all products.
    Supports filtering by category, brand, and searching by name.
    """
    queryset = Product.objects.filter(is_active=True).select_related('category', 'brand')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'brand__slug', 'is_featured', 'is_new_launch']
    search_fields = ['name', 'description', 'category__name', 'brand__name']
    ordering_fields = ['price', 'discount_price', 'created_at', 'rating_avg']
    ordering = ['-created_at']

class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve detailed information for a single product.
    Lookup field is 'slug'.
    """
    queryset = Product.objects.filter(is_active=True).select_related('category', 'brand')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
