"""
Order/Invoice Number Generators — Shivank Kirana Store
"""
import uuid
import random
import string
from datetime import datetime


def generate_order_number() -> str:
    """Generate unique order number: ORD-2026-00001"""
    from apps.orders.models import Order
    year = datetime.now().year
    count = Order.objects.filter(created_at__year=year).count() + 1
    return f"ORD-{year}-{count:05d}"


def generate_invoice_number() -> str:
    """Generate invoice number: INV-2026-00001"""
    year = datetime.now().year
    seq = random.randint(10000, 99999)
    return f"INV-{year}-{seq}"


def generate_otp(length: int = 6) -> str:
    """Generate numeric OTP."""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def generate_transaction_id() -> str:
    """Generate UPI transaction ID."""
    return 'TXN' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


def generate_tracking_id() -> str:
    """Generate delivery tracking ID."""
    return 'TRK' + ''.join(random.choices(string.digits, k=8))
