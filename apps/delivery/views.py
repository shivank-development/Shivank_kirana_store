from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order, DeliveryTracking
import random

@login_required
def delivery_home(request):
    """List of active deliveries for the delivery boy."""
    # Simplified for testing: just show all "out for delivery" orders
    deliveries = Order.objects.filter(status='out_for_delivery')
    return render(request, 'delivery/home.html', {'deliveries': deliveries})

@login_required
def active_delivery(request, order_number):
    """Delivery boy's live tracking view to broadcast coordinates."""
    order = get_object_or_404(Order, order_number=order_number)
    
    # Ensure tracking object exists
    tracking, created = DeliveryTracking.objects.get_or_create(
        order=order,
        defaults={
            'store_lat': 28.9845,
            'store_lng': 77.7064,
            # Randomize customer location slightly around Meerut for demo purposes
            'customer_lat': 28.9845 + random.uniform(-0.02, 0.02),
            'customer_lng': 77.7064 + random.uniform(-0.02, 0.02),
        }
    )
    
    return render(request, 'delivery/active_delivery.html', {
        'order': order,
        'tracking': tracking,
    })
