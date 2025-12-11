"""Configuration constants and settings for the application."""

# Page Configuration
PAGE_CONFIG = {
    "page_title": "Nuclear Radiation Detection",
    "page_icon": "☢️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Safety Classification Thresholds
SAFETY_THRESHOLDS = {
    "safe_age": 15,
    "moderate_age": 25,
    "dangerous_age": 40
}

# Distance Thresholds (in kilometers)
DISTANCE_THRESHOLDS = {
    "safe_zone": 100,
    "moderate_zone": 75,
    "dangerous_zone": 50
}

# Default Location (NYC)
DEFAULT_LOCATION = {
    "latitude": 40.7128,
    "longitude": -74.0060
}

# Location Detection Settings
LOCATION_RETRY_ATTEMPTS = 3
LOCATION_RETRY_DELAY = 1  # seconds

# Map Settings
MAP_SETTINGS = {
    "default_zoom": 6,
    "default_tile": "CartoDB dark_matter",
    "circle_radius": 30000,  # meters
    "user_radius": 50000,  # meters for user location circle
    "user_icon_size": (30, 30)
}

# Notification Settings
NOTIFICATION_TIMEOUTS = {
    "dangerous": 15,
    "moderate": 10,
    "safe": 5
}

# Safety Colors and Icons
SAFETY_COLORS = {
    'Safe': {'color': '#28a745', 'icon': 'check-circle'},
    'Dangerous': {'color': '#dc3545', 'icon': 'exclamation-triangle'},
    'Moderate': {'color': '#ffc107', 'icon': 'exclamation-circle'}
}

