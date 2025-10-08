import requests
import streamlit as st
from datetime import datetime, timedelta

def get_weather_forecast(destination, duration_days):
    """Get 5-day weather forecast using free Open-Meteo API"""
    try:
        from utils.map_utils import get_coordinates
        coords = get_coordinates(destination)
        
        if not coords:
            st.warning(f"Could not find coordinates for {destination}")
            return create_detailed_mock_weather(duration_days)  # FIXED: changed from create_mock_weather
            
        lat, lon = coords
        
        # Open-Meteo API - 7-day forecast, completely free
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_mean,weathercode,uv_index_max,wind_speed_10m_max',
            'hourly': 'temperature_2m,relative_humidity_2m,precipitation_probability,weathercode',
            'timezone': 'auto',
            'forecast_days': 7  # Get 7 days forecast
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return process_5day_forecast(data, duration_days)
        else:
            st.info("Using sample weather data")
            return create_detailed_mock_weather(duration_days)
            
    except Exception as e:
        st.info("Using sample weather data")
        return create_detailed_mock_weather(duration_days)

def process_5day_forecast(data, duration_days):
    """Process 5-day detailed forecast"""
    forecasts = []
    
    daily = data['daily']
    
    # Show 5 days or trip duration, whichever is smaller
    days_to_show = min(5, duration_days)
    
    for i in range(days_to_show):
        # Get hourly data for this day to show variation
        day_hourly_data = get_hourly_data_for_day(data, i)
        
        forecast = {
            'date': datetime.strptime(daily['time'][i], '%Y-%m-%d').strftime('%a, %d %b'),
            'day_name': datetime.strptime(daily['time'][i], '%Y-%m-%d').strftime('%A'),
            'temp_max': round(daily['temperature_2m_max'][i]),
            'temp_min': round(daily['temperature_2m_min'][i]),
            'temp_avg': round((daily['temperature_2m_max'][i] + daily['temperature_2m_min'][i]) / 2),
            'description': get_weather_description(daily['weathercode'][i]),
            'icon': get_weather_icon(daily['weathercode'][i]),
            'rain_chance': daily['precipitation_probability_mean'][i],
            'uv_index': daily['uv_index_max'][i],
            'wind_speed': daily['wind_speed_10m_max'][i],
            'hourly_temps': day_hourly_data['temps'],
            'hourly_rain': day_hourly_data['rain_chance'],
            'humidity_avg': day_hourly_data['humidity_avg']
        }
        forecasts.append(forecast)
    
    return forecasts

def get_hourly_data_for_day(data, day_index):
    """Get hourly data for a specific day"""
    target_date = datetime.strptime(data['daily']['time'][day_index], '%Y-%m-%d').date()
    
    temps = []
    rain_chances = []
    humidities = []
    
    hourly = data['hourly']
    
    for i in range(len(hourly['time'])):
        hour_time = datetime.fromisoformat(hourly['time'][i].replace('Z', '+00:00'))
        if hour_time.date() == target_date:
            temps.append(hourly['temperature_2m'][i])
            rain_chances.append(hourly['precipitation_probability'][i])
            humidities.append(hourly['relative_humidity_2m'][i])
    
    return {
        'temps': [round(t) for t in temps[::3]],  # Sample every 3 hours
        'rain_chance': [round(r) for r in rain_chances[::3]],
        'humidity_avg': round(sum(humidities) / len(humidities)) if humidities else 65
    }

def get_weather_description(weather_code):
    """Convert weather code to description"""
    codes = {
        0: 'Clear Sky', 1: 'Mainly Clear', 2: 'Partly Cloudy', 3: 'Overcast',
        45: 'Foggy', 48: 'Foggy', 51: 'Light Drizzle', 53: 'Moderate Drizzle',
        55: 'Dense Drizzle', 61: 'Light Rain', 63: 'Moderate Rain', 65: 'Heavy Rain',
        80: 'Light Showers', 81: 'Moderate Showers', 82: 'Heavy Showers',
        95: 'Thunderstorm', 96: 'Thunderstorm with Hail', 99: 'Severe Thunderstorm'
    }
    return codes.get(weather_code, 'Partly Cloudy')

def get_weather_icon(weather_code):
    """Convert weather code to icon"""
    if weather_code == 0:
        return '01d'
    elif weather_code in [1, 2]:
        return '02d'
    elif weather_code == 3:
        return '03d'
    elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        return '10d'
    elif weather_code in [95, 96, 99]:
        return '11d'
    else:
        return '02d'

def create_detailed_mock_weather(duration_days):
    """Create detailed 5-day sample weather data"""
    forecasts = []
    base_temp = 25
    
    for i in range(min(5, duration_days)):
        day_temps = [base_temp + i*2 + j for j in range(0, 24, 3)]
        
        forecasts.append({
            'date': (datetime.now() + timedelta(days=i)).strftime('%a, %d %b'),
            'day_name': (datetime.now() + timedelta(days=i)).strftime('%A'),
            'temp_max': base_temp + i*2 + 5,
            'temp_min': base_temp + i*2 - 3,
            'temp_avg': base_temp + i*2,
            'description': ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Clear'][i % 5],
            'icon': ['01d', '02d', '03d', '10d', '01d'][i % 5],
            'rain_chance': [10, 20, 40, 70, 30][i % 5],
            'uv_index': [6, 5, 3, 2, 7][i % 5],
            'wind_speed': [12, 15, 20, 25, 10][i % 5],
            'hourly_temps': day_temps[:8],  # 8 samples for the day
            'hourly_rain': [10, 5, 0, 0, 20, 40, 30, 10],
            'humidity_avg': [60, 65, 75, 80, 55][i % 5]
        })
    
    return forecasts

def get_weather_emoji(icon_code):
    """Convert weather icon code to emoji"""
    emoji_map = {
        '01d': '☀️', '01n': '🌙', '02d': '⛅', '02n': '☁️',
        '03d': '☁️', '03n': '☁️', '04d': '☁️', '04n': '☁️',
        '09d': '🌧️', '09n': '🌧️', '10d': '🌦️', '10n': '🌧️',
        '11d': '⛈️', '11n': '⛈️', '13d': '❄️', '13n': '❄️',
        '50d': '🌫️', '50n': '🌫️'
    }
    return emoji_map.get(icon_code, '🌈')

def display_weather_forecast(forecasts, destination):
    """Display 5-day detailed weather forecast"""
    st.subheader(f"🌤️ 5-Day Weather Forecast for {destination}")
    
    if not forecasts:
        st.info("Weather data unavailable. Check destination spelling.")
        return
    
    # Display daily forecast cards
    cols = st.columns(len(forecasts))
    
    for i, forecast in enumerate(forecasts):
        with cols[i]:
            emoji = get_weather_emoji(forecast['icon'])
            
            st.subheader(f"{forecast['date']}")
            st.write(f"**{forecast['day_name']}** {emoji}")
            
            st.metric(
                label="High / Low",
                value=f"{forecast['temp_max']}°C",
                delta=f"{forecast['temp_min']}°C"
            )
            
            st.caption(f"**{forecast['description']}**")
            st.caption(f"💧 Humidity: {forecast['humidity_avg']}%")
            st.caption(f"🌧️ Rain: {forecast['rain_chance']}%")
            st.caption(f"🌬️ Wind: {forecast['wind_speed']} km/h")
            st.caption(f"☀️ UV: {forecast['uv_index']}")
    
    # Detailed analysis
    st.subheader("📊 Weather Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_temp = sum(f['temp_avg'] for f in forecasts) / len(forecasts)
        st.metric("Average Temperature", f"{avg_temp:.1f}°C")
    
    with col2:
        max_rain = max(f['rain_chance'] for f in forecasts)
        st.metric("Max Rain Chance", f"{max_rain}%")
    
    with col3:
        temp_range = max(f['temp_max'] for f in forecasts) - min(f['temp_min'] for f in forecasts)
        st.metric("Temperature Range", f"{temp_range}°C")
    
    # Hourly forecast for first day (as example)
    if forecasts and len(forecasts) > 0:
        st.subheader(f"⏰ {forecasts[0]['day_name']} - Hourly Overview")
        hours = ['6AM', '9AM', '12PM', '3PM', '6PM', '9PM', '12AM', '3AM']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Temperature**")
            for hour, temp in zip(hours, forecasts[0]['hourly_temps']):
                st.write(f"{hour}: {temp}°C")
        
        with col2:
            st.write("**Rain Chance**")
            for hour, rain in zip(hours, forecasts[0]['hourly_rain']):
                st.write(f"{hour}: {rain}%")

def get_weather_packing_tips(forecasts):
    """Generate detailed packing tips based on 5-day forecast"""
    tips = []
    
    if not forecasts:
        return tips
    
    max_temp = max(f['temp_max'] for f in forecasts)
    min_temp = min(f['temp_min'] for f in forecasts)
    max_rain = max(f['rain_chance'] for f in forecasts)
    avg_uv = sum(f['uv_index'] for f in forecasts) / len(forecasts)
    max_wind = max(f['wind_speed'] for f in forecasts)
    
    # Temperature-based tips
    if max_temp > 35:
        tips.append("🔥 **Extreme heat expected** - Light breathable clothes, extra water")
    elif max_temp > 30:
        tips.append("☀️ **Hot days** - Sunscreen, hat, light cotton clothes")
    elif min_temp < 10:
        tips.append("❄️ **Cold nights** - Warm jacket, thermals, beanie")
    elif min_temp < 15:
        tips.append("🧥 **Cool weather** - Layered clothing, light jacket")
    
    # Rain-based tips
    if max_rain > 70:
        tips.append("🌧️ **Heavy rain likely** - Waterproof jacket, umbrella, quick-dry clothes")
    elif max_rain > 40:
        tips.append("🌦️ **Rain expected** - Light raincoat, waterproof bag cover")
    elif max_rain > 20:
        tips.append("⛅ **Possible showers** - Compact umbrella, water-resistant shoes")
    
    # UV and wind tips
    if avg_uv > 6:
        tips.append("🕶️ **High UV index** - Sunglasses, SPF 50+ sunscreen")
    elif avg_uv > 3:
        tips.append("😎 **Moderate UV** - Sunscreen, cap for protection")
    
    if max_wind > 25:
        tips.append("💨 **Windy conditions** - Windbreaker, secure hat")
    
    # General tips based on variation
    temp_variation = max_temp - min_temp
    if temp_variation > 15:
        tips.append("🔄 **Large temp swings** - Layered clothing for day/night")
    elif temp_variation > 10:
        tips.append("👕 **Moderate variation** - Versatile clothing options")
    
    return tips