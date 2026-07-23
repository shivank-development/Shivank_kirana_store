"""
Order models — core business logic.
"""
from django.db import models
from django.conf import settings
from apps.accounts.models import UserAddress
from apps.products.models.product import Product


class Order(models.Model):
    """Main order model with UPI/COD payment support."""
    
    STATUS_CHOICES = [
        ('placed', 'Order Placed'),
        ('confirmed', 'Confirmed'),
        ('packed', 'Packed'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('UPI', 'UPI Payment'),
        ('COD', 'Cash on Delivery'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('rejected', 'Rejected'),
    ]

    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='orders')
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    distance_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    coupon_discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES,
                                       default='pending')
    upi_transaction_id = models.CharField(max_length=100, blank=True)
    cod_advance_paid = models.BooleanField(default=False)
    cod_call_confirmed = models.BooleanField(default=False)
    
    # Status
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='placed')
    
    # Distance
    distance_km = models.FloatField(null=True, blank=True)
    delivery_boy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                      null=True, blank=True, related_name='deliveries')
    
    notes = models.TextField(blank=True)
    cancel_reason = models.TextField(blank=True)
    
    # Timestamps
    placed_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    packed_at = models.DateTimeField(null=True, blank=True)
    out_for_delivery_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-placed_at']

    def __str__(self):
        return f'{self.order_number} - {self.user.full_name}'

    def save(self, *args, **kwargs):
        if not self.order_number:
            import datetime
            count = Order.objects.count() + 1
            year = datetime.datetime.now().year
            self.order_number = f'ORD-{year}-{count:05d}'
        super().save(*args, **kwargs)

    @property
    def status_display_class(self):
        classes = {
            'placed': 'info',
            'confirmed': 'primary',
            'packed': 'warning',
            'out_for_delivery': 'warning',
            'delivered': 'success',
            'cancelled': 'danger',
        }
        return classes.get(self.status, 'secondary')


class OrderItem(models.Model):
    """Individual items within an order (snapshot at time of purchase)."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255, help_text='Snapshot of product name')
    product_image = models.CharField(max_length=500, blank=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return f'{self.order.order_number} - {self.product_name} x {self.quantity}'


class Payment(models.Model):
    """Payment record for each order."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('rejected', 'Rejected'),
        ('refunded', 'Refunded'),
    ]
    
    ADMIN_ACTION_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    upi_txn_id = models.CharField(max_length=100, blank=True)
    payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)
    
    # Admin actions
    admin_action = models.CharField(max_length=20, choices=ADMIN_ACTION_CHOICES, blank=True)
    admin_action_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='payment_actions')
    admin_action_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']

    def __str__(self):
        return f'Payment #{self.id} - {self.order.order_number} ({self.status})'


class DeliveryTracking(models.Model):
    """Real-time delivery tracking data."""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='tracking')
    delivery_boy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                      null=True, blank=True, related_name='tracking_sessions')
    
    # Live GPS
    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)
    
    # Store location (fixed — Meerut)
    store_lat = models.FloatField(default=28.9845)
    store_lng = models.FloatField(default=77.7064)
    
    # Customer location
    customer_lat = models.FloatField(null=True, blank=True)
    customer_lng = models.FloatField(null=True, blank=True)
    
    distance_km = models.FloatField(null=True, blank=True)
    eta_minutes = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=30, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'delivery_tracking'

    def __str__(self):
        return f'Tracking: {self.order.order_number}'


class DeliveryBoy(models.Model):
    """Delivery boy profile."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='delivery_profile')
    vehicle_type = models.CharField(max_length=50, blank=True)
    vehicle_number = models.CharField(max_length=20, blank=True)
    is_available = models.BooleanField(default=True)
    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)
    total_deliveries = models.IntegerField(default=0)
    rating_avg = models.FloatField(default=5.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'delivery_boys'

    def __str__(self):
        return f'Delivery: {self.user.full_name}'


class Notification(models.Model):
    """User notifications."""
    
    TYPE_CHOICES = [
        ('order', 'Order'),
        ('payment', 'Payment'),
        ('stock', 'Stock'),
        ('promo', 'Promotion'),
        ('delivery', 'Delivery'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='notifications', null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='order')
    is_read = models.BooleanField(default=False)
    data_json = models.TextField(blank=True, help_text='JSON payload')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} → {self.user}'


class Coupon(models.Model):
    """Discount coupons."""
    DISCOUNT_TYPE_CHOICES = [
        ('percent', 'Percentage'),
        ('flat', 'Flat Amount'),
    ]

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=8, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    usage_limit = models.IntegerField(null=True, blank=True)
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_discount(self, subtotal):
        from decimal import Decimal
        if not self.is_active:
            return Decimal('0')
        subtotal_dec = Decimal(str(subtotal))
        if self.min_order_amount and subtotal_dec < self.min_order_amount:
            return Decimal('0')
        if self.discount_type == 'percent':
            disc = (subtotal_dec * self.discount_value) / Decimal('100')
        else:
            disc = self.discount_value
        if self.max_discount:
            disc = min(disc, self.max_discount)
        return min(disc, subtotal_dec)

    class Meta:
        db_table = 'coupons'

    def __str__(self):
        return f'{self.code} ({self.discount_value}{"%" if self.discount_type == "percent" else "₹"})'


class StoreSettings(models.Model):
    """Key-value store settings."""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'store_settings'

    def __str__(self):
        return f'{self.key} = {self.value[:50]}'
