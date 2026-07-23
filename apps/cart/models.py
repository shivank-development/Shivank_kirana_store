"""Cart models."""
from django.db import models
from django.conf import settings
from apps.products.models.product import Product


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=255, blank=True, help_text='For guest users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f'Cart - {self.user or self.session_key}'

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_mrp(self):
        return sum(item.mrp_total for item in self.items.all())

    @property
    def savings(self):
        return self.total_mrp - self.subtotal

    @property
    def delivery_charge(self):
        FREE_DELIVERY_THRESHOLD = 799
        return 0 if self.subtotal >= FREE_DELIVERY_THRESHOLD else 49

    @property
    def total(self):
        return self.subtotal + self.delivery_charge

    @property
    def item_count(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_items'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    @property
    def subtotal(self):
        return self.product.selling_price * self.quantity

    @property
    def mrp_total(self):
        return self.product.price * self.quantity
