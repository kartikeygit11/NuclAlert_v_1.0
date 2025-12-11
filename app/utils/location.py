"""Location services for user geolocation."""

import geocoder
import time
from app.config import DEFAULT_LOCATION, LOCATION_RETRY_ATTEMPTS, LOCATION_RETRY_DELAY


def get_user_location():
    """
    Get user's current location using IP geolocation.
    
    Returns:
        tuple: (latitude, longitude) or (None, None) if failed
    """
    max_retries = LOCATION_RETRY_ATTEMPTS
    
    for attempt in range(max_retries):
        try:
            user_location = geocoder.ip('me')
            if user_location.latlng:
                return user_location.latlng[0], user_location.latlng[1]
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(LOCATION_RETRY_DELAY)
    
    # Return default location if all attempts fail
    return DEFAULT_LOCATION["latitude"], DEFAULT_LOCATION["longitude"]


def update_user_location_with_fallback():
    """
    Get user location with fallback to default.
    
    Returns:
        tuple: (latitude, longitude)
    """
    latitude, longitude = get_user_location()
    
    # If location detection failed, use default
    if latitude is None or longitude is None:
        return DEFAULT_LOCATION["latitude"], DEFAULT_LOCATION["longitude"]
    
    return latitude, longitude

