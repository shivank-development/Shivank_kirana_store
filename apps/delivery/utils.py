import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers.
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers
    return c * r

def calculate_eta(distance_km, speed_kmh=20):
    """
    Calculate ETA in minutes based on distance and average city speed.
    """
    if distance_km is None or distance_km < 0:
        return 0
    # Add a base time (e.g. 2 mins for parking/handover)
    base_time = 2
    travel_time = (distance_km / speed_kmh) * 60
    return int(travel_time + base_time)
