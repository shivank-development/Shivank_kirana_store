"""
Supporting product models: Gallery, BulkPricing, Review, Stock.
"""
from django.db import models
from django.conf import settings
from apps.products.models.product import Product


class ProductImage(models.Model):
    """Multiple images per product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_gallery'
        ordering = ['sort_order']

    def __str__(self):
        return f'{self.product.name} - Image {self.sort_order}'


class BulkPricing(models.Model):
    """Buy More Save More pricing tiers."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bulk_prices')
    min_quantity = models.IntegerField(help_text='Minimum qty for this price (e.g. 1, 2, 3, 4+)')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    discount_label = models.CharField(max_length=50, blank=True,
                                       help_text='e.g. "11% OFF", "14% OFF"')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bulk_pricing'
        ordering = ['min_quantity']

    def __str__(self):
        return f'{self.product.name} - {self.min_quantity}+ units @ ₹{self.price_per_unit}'


class ProductReview(models.Model):
    """Product reviews and ratings."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False, help_text='Verified purchase')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_reviews'
        ordering = ['-created_at']
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.user.full_name} → {self.product.name}: {self.rating}★'


class StockHistory(models.Model):
    """Track stock level changes."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_history')
    change = models.IntegerField(help_text='Positive=restock, negative=sold')
    reason = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True, blank=True)

    class Meta:
        db_table = 'stock_history'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.product.name}: {self.change:+d} ({self.reason})'
