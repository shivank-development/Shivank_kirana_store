"""Notifications app models."""
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """User notification — order updates, stock alerts, promos."""
    TYPE_CHOICES = [
        ('order', 'Order Update'),
        ('payment', 'Payment'),
        ('delivery', 'Delivery'),
        ('stock', 'Stock Alert'),
        ('promo', 'Promotion'),
        ('system', 'System'),
    ]

    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='user_notifications', null=True, blank=True
    )
    title       = models.CharField(max_length=255)
    message     = models.TextField()
    notif_type  = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')
    is_read     = models.BooleanField(default=False)
    action_url  = models.CharField(max_length=500, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} → {self.user}'

    @classmethod
    def send(cls, user, title, message, notif_type='system', action_url=''):
        """Quick helper to create and return a notification."""
        return cls.objects.create(
            user=user, title=title, message=message,
            notif_type=notif_type, action_url=action_url
        )
