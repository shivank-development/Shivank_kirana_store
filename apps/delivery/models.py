"""Delivery app models — DeliveryProfile for delivery boys."""
from django.db import models
from django.conf import settings


class DeliveryProfile(models.Model):
    """Extended profile for delivery personnel."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='delivery_agent_profile'
    )
    vehicle_type = models.CharField(max_length=50, default='bicycle',
                                     choices=[('bicycle','Bicycle'),('bike','Bike'),('ev','EV Scooter')])
    vehicle_number = models.CharField(max_length=20, blank=True)
    is_available    = models.BooleanField(default=True)
    current_lat     = models.FloatField(null=True, blank=True)
    current_lng     = models.FloatField(null=True, blank=True)
    total_deliveries= models.IntegerField(default=0)
    rating          = models.FloatField(default=5.0)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'delivery_agent_profiles'

    def __str__(self):
        return f'{self.user.full_name} — Delivery Boy'


class DeliveryPincode(models.Model):
    """Allowed pincodes for delivery."""
    pincode = models.CharField(max_length=10, unique=True)
    area_name = models.CharField(max_length=100, blank=True, help_text="Optional locality name e.g. Meerut Cantt")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'delivery_pincodes'
        ordering = ['pincode']

    def __str__(self):
        return f"{self.pincode} - {self.area_name or 'Active'}"

