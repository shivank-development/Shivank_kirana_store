"""
★ Haversine Distance Calculator — Shivank Kirana Store
Calculates real-world distance between two GPS coordinates
"""
import math


EARTH_RADIUS_KM = 6371.0


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate the great-circle distance between two GPS points.
    
    Args:
        lat1, lng1: Source coordinates (store)
        lat2, lng2: Destination coordinates (customer)
    
    Returns:
        float: Distance in kilometers
    """
    # Convert to radians
    lat1_r = math.radians(lat1)
    lat2_r = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def get_distance_from_store(customer_lat: float, customer_lng: float) -> float:
    """Distance from Shivank Store (Meerut) to customer location."""
    from .charge_calculator import STORE_LAT, STORE_LNG
    return haversine_distance(STORE_LAT, STORE_LNG, customer_lat, customer_lng)


def is_deliverable(customer_lat: float, customer_lng: float, max_km: float = 20.0) -> bool:
    """Check if customer location is within delivery range."""
    distance = get_distance_from_store(customer_lat, customer_lng)
    return distance <= max_km


def estimate_travel_time(distance_km: float, speed_kmh: float = 25.0) -> int:
    """Estimate delivery time in minutes."""
    return round((distance_km / speed_kmh) * 60) + 10  # +10 min for packing
