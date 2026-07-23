from rest_framework import generics
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from apps.products.models.brand import Brand
from apps.products.models.product import Product
from apps.products.serializers.brand_serializer import BrandSerializer
from apps.products.serializers.product_serializer import ProductSerializer

class BrandListAPIView(generics.ListAPIView):
    """
    API endpoint to list all active brands.
    """
    queryset = Brand.objects.filter(is_active=True).prefetch_related('products')
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class BrandProductListAPIView(generics.ListAPIView):
    """
    API endpoint to list products belonging to a specific brand.
    """
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'discount_price', 'created_at', 'rating_avg']
    ordering = ['-created_at']

    def get_queryset(self):
        brand_slug = self.kwargs.get('slug')
        return Product.objects.filter(is_active=True, brand__slug=brand_slug).select_related('category', 'brand')
