"""
Delivery Charge Calculator — Shivank Kirana Store
★ Free above ₹799 | ₹49 below ₹799 | Distance-based beyond 5km
"""

# ── CONSTANTS ──
FREE_DELIVERY_THRESHOLD = 799      # Orders above this → Free delivery
BASE_DELIVERY_CHARGE = 49          # Standard charge below threshold
FREE_DELIVERY_ZONE_KM = 5          # Within 5km → standard charges apply
PER_KM_RATE = 10                   # ₹10 per km beyond 5km

STORE_LAT = 28.9845                # Shivank Store: Meerut, UP
STORE_LNG = 77.7064


def calculate_delivery_charge(order_total: float, distance_km: float = 0) -> dict:
    """
    Calculate delivery charge based on order total and distance.
    
    Returns:
        dict: {
            'charge': int,       # ₹ delivery charge
            'is_free': bool,     # Free delivery?
            'reason': str,       # Human-readable reason
            'breakdown': dict    # Detailed breakdown
        }
    """
    # Free delivery on orders above threshold
    if order_total >= FREE_DELIVERY_THRESHOLD:
        return {
            'charge': 0,
            'is_free': True,
            'reason': f'Free delivery on orders above ₹{FREE_DELIVERY_THRESHOLD}',
            'breakdown': {
                'order_total': order_total,
                'threshold': FREE_DELIVERY_THRESHOLD,
                'distance_km': distance_km,
            }
        }

    # Within free zone
    if distance_km <= FREE_DELIVERY_ZONE_KM:
        return {
            'charge': BASE_DELIVERY_CHARGE,
            'is_free': False,
            'reason': f'Standard delivery charge (within {FREE_DELIVERY_ZONE_KM}km)',
            'breakdown': {
                'base_charge': BASE_DELIVERY_CHARGE,
                'distance_km': distance_km,
            }
        }

    # Beyond free zone — add per-km charge
    extra_km = distance_km - FREE_DELIVERY_ZONE_KM
    extra_charge = round(extra_km * PER_KM_RATE)
    total_charge = BASE_DELIVERY_CHARGE + extra_charge

    return {
        'charge': total_charge,
        'is_free': False,
        'reason': f'₹{BASE_DELIVERY_CHARGE} base + ₹{extra_charge} for {extra_km:.1f}km extra',
        'breakdown': {
            'base_charge': BASE_DELIVERY_CHARGE,
            'extra_km': extra_km,
            'per_km_rate': PER_KM_RATE,
            'extra_charge': extra_charge,
            'total': total_charge,
        }
    }


def get_free_delivery_shortfall(order_total: float) -> float:
    """How much more to add for free delivery."""
    if order_total >= FREE_DELIVERY_THRESHOLD:
        return 0
    return FREE_DELIVERY_THRESHOLD - order_total
