"""Data processing utilities for nuclear plant data."""

import pandas as pd
from geopy.distance import geodesic
from app.config import (
    SAFETY_THRESHOLDS,
    DISTANCE_THRESHOLDS,
    SAFETY_COLORS
)


def calculate_safety(age):
    """
    Calculate safety classification based on plant age.
    
    Args:
        age: Plant age in years
        
    Returns:
        str: Safety classification ('Safe', 'Moderate', 'Dangerous', or 'Unknown')
    """
    if pd.isna(age):
        return 'Unknown'
    if age < SAFETY_THRESHOLDS["safe_age"]:
        return 'Safe'
    elif age < SAFETY_THRESHOLDS["moderate_age"]:
        return 'Moderate'
    else:
        return 'Dangerous'


def process_plant_data(df):
    """
    Process and enrich plant data with safety classifications.
    
    Args:
        df: DataFrame with plant data (Name, Latitude, Longitude, Age)
        
    Returns:
        DataFrame: Processed dataframe with Safety column
    """
    df = df.copy()
    df.fillna(0, inplace=True)
    df['Safety'] = df['Age'].apply(calculate_safety)
    return df


def calculate_distances(df, user_latitude, user_longitude):
    """
    Calculate distances from user location to all plants.
    
    Args:
        df: DataFrame with plant data
        user_latitude: User's latitude
        user_longitude: User's longitude
        
    Returns:
        list: List of dictionaries with plant distance information
    """
    plant_distances = []
    
    if user_latitude and user_longitude:
        for _, row in df.iterrows():
            plant_latitude = row['Latitude']
            plant_longitude = row['Longitude']
            
            distance = geodesic(
                (user_latitude, user_longitude),
                (plant_latitude, plant_longitude)
            ).km
            
            plant_distances.append({
                'Name': row['Name'],
                'Distance': distance,
                'Safety': row['Safety'],
                'Age': row['Age']
            })
    
    return plant_distances


def classify_zones(df, user_latitude, user_longitude):
    """
    Classify plants into safety zones based on distance and safety level.
    
    Args:
        df: DataFrame with plant data
        user_latitude: User's latitude
        user_longitude: User's longitude
        
    Returns:
        tuple: (safe_zones, moderate_zones, dangerous_zones) lists
    """
    safe_zones = []
    moderate_zones = []
    dangerous_zones = []
    
    if user_latitude and user_longitude:
        for _, row in df.iterrows():
            plant_latitude = row['Latitude']
            plant_longitude = row['Longitude']
            safety = row['Safety']
            
            distance = geodesic(
                (user_latitude, user_longitude),
                (plant_latitude, plant_longitude)
            ).km
            
            if safety == 'Safe' and distance <= DISTANCE_THRESHOLDS["safe_zone"]:
                safe_zones.append(row['Name'])
            elif safety == 'Moderate' and distance <= DISTANCE_THRESHOLDS["moderate_zone"]:
                moderate_zones.append(row['Name'])
            elif safety == 'Dangerous' and distance <= DISTANCE_THRESHOLDS["dangerous_zone"]:
                dangerous_zones.append(row['Name'])
    
    return safe_zones, moderate_zones, dangerous_zones

