import math
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula
    
    Args:
        lat1, lon1: First coordinate (latitude, longitude)
        lat2, lon2: Second coordinate (latitude, longitude)
    
    Returns:
        Distance in kilometers
    """
    # Earth radius in kilometers
    R = 6371.0
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

def validate_location(latitude, longitude):
    """
    Validate latitude and longitude values
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
    
    Returns:
        True if valid, False otherwise
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return True
        return False
    except (ValueError, TypeError):
        return False

def format_distance(distance_km):
    """
    Format distance for display
    
    Args:
        distance_km: Distance in kilometers
    
    Returns:
        Formatted string (e.g., "500m" or "1.2km")
    """
    if distance_km < 1:
        return f"{int(distance_km * 1000)}m"
    return f"{distance_km:.1f}km"

def safe_get(data, *keys, default=None):
    """
    Safely get nested dictionary values
    
    Args:
        data: Dictionary to search
        *keys: Keys to traverse
        default: Default value if key not found
    
    Returns:
        Value or default
    """
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError, IndexError):
            return default
    return data
