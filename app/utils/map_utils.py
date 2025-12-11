"""Map visualization utilities using Folium."""

import folium
from app.config import (
    MAP_SETTINGS,
    SAFETY_COLORS,
    DISTANCE_THRESHOLDS
)


def create_map(user_latitude, user_longitude):
    """
    Create a base Folium map with multiple tile layers.
    
    Args:
        user_latitude: User's latitude
        user_longitude: User's longitude
        
    Returns:
        folium.Map: Configured map object
    """
    # Create map with OpenStreetMap as default (no attribution issues)
    map_obj = folium.Map(
        location=[user_latitude or 0, user_longitude or 0],
        zoom_start=MAP_SETTINGS["default_zoom"],
        tiles='OpenStreetMap'
    )
    
    # Add CartoDB Dark Matter with proper attribution
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        name='CartoDB Dark Matter',
        overlay=False,
        control=True
    ).add_to(map_obj)
    
    # Add CartoDB Positron with proper attribution
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        name='CartoDB Positron',
        overlay=False,
        control=True
    ).add_to(map_obj)
    
    # Add Stamen Terrain with proper attribution
    folium.TileLayer(
        tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}{r}.png',
        attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        name='Stamen Terrain',
        overlay=False,
        control=True
    ).add_to(map_obj)
    
    folium.LayerControl().add_to(map_obj)
    
    return map_obj


def add_plant_markers(map_obj, df):
    """
    Add plant markers and circles to the map.
    
    Args:
        map_obj: Folium map object
        df: DataFrame with plant data
    """
    for _, row in df.iterrows():
        reactor_safety = row['Safety']
        plant_latitude = row['Latitude']
        plant_longitude = row['Longitude']
        
        # Get color and icon for safety level
        color_info = SAFETY_COLORS.get(reactor_safety, {})
        color = color_info.get('color', 'blue')
        icon = color_info.get('icon', 'info-circle')
        
        # Add circle for radiation zone
        folium.Circle(
            location=[plant_latitude, plant_longitude],
            radius=MAP_SETTINGS["circle_radius"],
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.2,
            tooltip=f"{row['Name']} - {reactor_safety} ({row['Age']} years)"
        ).add_to(map_obj)
        
        # Add marker for plant location
        folium.Marker(
            location=[plant_latitude, plant_longitude],
            icon=folium.Icon(
                color='white',
                icon_color=color,
                icon=icon,
                prefix='fa'
            ),
            popup=f"<b>{row['Name']}</b><br>Age: {row['Age']} years<br>Status: {reactor_safety}"
        ).add_to(map_obj)


def add_user_marker(map_obj, user_latitude, user_longitude, on_site_plants=None):
    """
    Add user location marker and radius circle to the map.
    
    Args:
        map_obj: Folium map object
        user_latitude: User's latitude
        user_longitude: User's longitude
        on_site_plants: Optional list of plant names user is on-site at
    """
    if user_latitude and user_longitude:
        popup_msg = "Your Location"
        if on_site_plants:
            popup_msg = f"On site at: {', '.join(on_site_plants)}"
        
        # Add user location marker
        folium.Marker(
            location=[user_latitude, user_longitude],
            icon=folium.CustomIcon(
                icon_image="https://cdn-icons-png.flaticon.com/512/447/447031.png",
                icon_size=MAP_SETTINGS["user_icon_size"]
            ),
            tooltip="Your Location",
            popup=popup_msg
        ).add_to(map_obj)
        
        # Add radius circle around user location
        folium.Circle(
            location=[user_latitude, user_longitude],
            radius=MAP_SETTINGS["user_radius"],
            color='#007bff',
            fill=True,
            fill_color='#007bff',
            fill_opacity=0.1,
            tooltip=f"{DISTANCE_THRESHOLDS['dangerous_zone']}km radius from your location"
        ).add_to(map_obj)

