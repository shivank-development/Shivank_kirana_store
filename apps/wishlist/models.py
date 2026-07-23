"""Wishlist model."""
from django.db import models
from django.conf import settings
from apps.products.models.product import Product


class WishlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wishlists'
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.full_name} ❤️ {self.product.name}'
