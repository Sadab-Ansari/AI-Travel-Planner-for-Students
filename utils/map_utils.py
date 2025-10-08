import folium
from geopy.geocoders import Nominatim
import math
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def get_coordinates(location_name):
    """Get latitude/longitude for a location using free geocoding"""
    try:
        geolocator = Nominatim(user_agent="travel_planner_app")
        location = geolocator.geocode(location_name + ", India")
        if location:
            return (location.latitude, location.longitude)
        return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None

def calculate_distance(coord1, coord2):
    """Calculate straight-line distance between two coordinates in km"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Haversine formula
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def create_folium_map(start_coords, end_coords, start_name, end_name):
    """Create an interactive Folium map with route"""
    # Calculate center point for map
    center_lat = (start_coords[0] + end_coords[0]) / 2
    center_lon = (start_coords[1] + end_coords[1]) / 2
    
    # Create map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Add markers
    folium.Marker(
        start_coords,
        popup=f'🟢 Start: {start_name}',
        tooltip=start_name,
        icon=folium.Icon(color='green', icon='play', prefix='fa')
    ).add_to(m)
    
    folium.Marker(
        end_coords,
        popup=f'🔴 Destination: {end_name}',
        tooltip=end_name,
        icon=folium.Icon(color='red', icon='flag-checkered', prefix='fa')
    ).add_to(m)
    
    # Draw route line
    folium.PolyLine(
        [start_coords, end_coords],
        color='blue',
        weight=3,
        opacity=0.7,
        dash_array='5, 5'
    ).add_to(m)
    
    # Fit map to show both points
    m.fit_bounds([start_coords, end_coords])
    
    return m

def display_map_in_streamlit(folium_map):
    """Display Folium map in Streamlit - FIXED VERSION"""
    # Save map to temporary HTML file and read it back
    folium_map.save('temp_map.html')
    with open('temp_map.html', 'r', encoding='utf-8') as f:
        map_html = f.read()
    
    # Use a simpler approach that actually works
    components.html(map_html, height=500, scrolling=True)

def create_static_map(start_coords, end_coords, start_name, end_name):
    """Create a simple static map visualization that always works"""
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the route line
    ax.plot([start_coords[1], end_coords[1]], 
            [start_coords[0], end_coords[0]], 
            'b-', linewidth=3, alpha=0.7, label='Route')
    
    # Plot start point
    ax.plot(start_coords[1], start_coords[0], 'go', markersize=12, 
            label=f'Start: {start_name}', markeredgecolor='black', markeredgewidth=1)
    
    # Plot end point  
    ax.plot(end_coords[1], end_coords[0], 'ro', markersize=12,
            label=f'Destination: {end_name}', markeredgecolor='black', markeredgewidth=1)
    
    # Calculate and display distance
    distance = calculate_distance(start_coords, end_coords)
    mid_lon = (start_coords[1] + end_coords[1]) / 2
    mid_lat = (start_coords[0] + end_coords[0]) / 2
    
    # Add distance annotation
    ax.annotate(f'Distance: {distance:.1f} km', 
               xy=(mid_lon, mid_lat),
               xytext=(10, 10), textcoords='offset points',
               bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
               fontsize=11, fontweight='bold')
    
    # Add labels and title
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.set_title(f'🚗 Route: {start_name} → {end_name}', fontsize=14, fontweight='bold')
    
    # Add grid and legend
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right')
    
    # Adjust layout
    plt.tight_layout()
    
    return fig