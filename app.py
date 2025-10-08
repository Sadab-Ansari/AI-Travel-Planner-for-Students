# app.py
import streamlit as st
from config.openai_config import client
from utils.prompt_builder import build_travel_prompt
from utils.map_utils import get_coordinates, create_folium_map, calculate_distance, display_map_in_streamlit, create_static_map
from utils.budget_utils import display_budget_breakdown
from utils.packing_utils import generate_packing_list, display_packing_checklist
from utils.weather_utils import get_weather_forecast, display_weather_forecast, get_weather_packing_tips
from utils.safety_utils import display_safety_dashboard
from components.ui_components import apply_custom_styles, render_header, render_travel_form, render_welcome_section, render_footer
from config.constants import APP_NAME, APP_ICON
import matplotlib.pyplot as plt

# ------------------------
# Streamlit App UI
# ------------------------
st.set_page_config(
    page_title=APP_NAME, 
    page_icon=APP_ICON, 
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapse sidebar by default
)

# Apply custom styles
apply_custom_styles()

# Render header
render_header()

# ------------------------
# User Inputs
# ------------------------
form_data = render_travel_form()
(destination, starting_location, duration_days, budget, group_type, 
 travel_mode, stay_preference, food_preference, interests, travel_goal, 
 weather_preference, special_conditions, submit_button) = form_data

# Required fields validation
def validate_inputs():
    required_fields = {
        "Destination": destination,
        "Starting Location": starting_location
    }
    
    missing_fields = [field for field, value in required_fields.items() if not value.strip()]
    if missing_fields:
        st.error(f"❌ Please fill in required fields: {', '.join(missing_fields)}")
        return False
    return True

# ------------------------
# Generate AI Itinerary
# ------------------------
if submit_button:
    if not validate_inputs():
        st.stop()
    
    with st.spinner("🤖 Generating your personalized travel plan..."):
        # Generate itinerary first (without showing map initially)
        prompt = build_travel_prompt(
            destination=destination,
            duration_days=duration_days,
            budget=budget,
            group_type=group_type,
            travel_mode=travel_mode,
            stay_preference=stay_preference,
            food_preference=food_preference,
            interests=interests,
            starting_location=starting_location,
            travel_goal=travel_goal,
            weather_preference=weather_preference,
            special_conditions=special_conditions
        )

        try:
            response = client.responses.create(
                model="gpt-4o-mini",
                input=prompt
            )
            itinerary = response.output_text
            
            # Store itinerary in session state for tabs
            st.session_state.itinerary = itinerary
            st.session_state.destination = destination
            st.session_state.duration_days = duration_days
            st.session_state.budget = budget
            st.session_state.interests = interests
            st.session_state.weather_preference = weather_preference
            
            st.success("🎉 Your AI Travel Itinerary is ready!")
            
            # Get weather forecast
            weather_forecast = None
            with st.spinner("🌤️ Fetching weather forecast..."):
                weather_forecast = get_weather_forecast(destination, duration_days)
                st.session_state.weather_forecast = weather_forecast
            
            # Create tabs for different sections
            itinerary_tab, budget_tab, packing_tab, weather_tab, safety_tab, map_tab = st.tabs([
                "📅 Itinerary", "💰 Budget", "🎒 Packing", "🌤️ Weather", "🛡️ Safety", "🗺️ Route"
            ])
            
            with itinerary_tab:
                render_itinerary_content(itinerary)
                
                # Add download options
                if starting_location and destination and 'distance_km' in st.session_state:
                    download_col1, download_col2 = st.columns(2)
                    with download_col1:
                        st.download_button(
                            label="📱 Save Route Info",
                            data=f"Route: {starting_location} to {destination}\nDistance: {st.session_state.distance_km:.1f} km\nTravel Time: {st.session_state.approx_time:.1f} hours\nTravel Mode: {travel_mode}",
                            file_name="travel_route.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with download_col2:
                        st.download_button(
                            label="📄 Save Full Itinerary",
                            data=itinerary,
                            file_name=f"{destination}_itinerary.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
            
            with budget_tab:
                # Budget Breakdown Section
                display_budget_breakdown()
                
            with packing_tab:
                # Packing Checklist Section
                packing_items = generate_packing_list(
                    itinerary_text=itinerary,
                    destination=destination,
                    duration_days=duration_days,
                    interests=interests,
                    weather_preference=weather_preference
                )
                
                # Add weather-based packing tips
                if weather_forecast:
                    weather_tips = get_weather_packing_tips(weather_forecast)
                    if weather_tips:
                        with st.expander("🌦️ Weather-based Packing Suggestions", expanded=True):
                            for tip in weather_tips:
                                st.write(f"• {tip}")
                
                display_packing_checklist(packing_items, duration_days)
                
            with weather_tab:
                # Weather Forecast Section
                if weather_forecast:
                    display_weather_forecast(weather_forecast, destination)
                else:
                    st.info("🌤️ Weather data unavailable. This could be due to:")
                    st.write("• Destination name not recognized")
                    st.write("• Weather API limit reached")
                    st.write("• Network connectivity issue")
                    st.write("💡 **Try using major city names for better weather data.**")
            
            with safety_tab:
                # Safety Dashboard Section
                display_safety_dashboard(destination, group_type, special_conditions)
                
            with map_tab:
                # Show route map in its own tab
                st.subheader("📍 Route Overview")
                
                if starting_location and destination:
                    with st.spinner("🗺️ Calculating route and generating map..."):
                        try:
                            # Get coordinates for both locations
                            start_coords = get_coordinates(starting_location)
                            dest_coords = get_coordinates(destination)
                            
                            if start_coords and dest_coords:
                                # Calculate approximate distance
                                distance_km = calculate_distance(start_coords, dest_coords)
                                
                                # Display route info in columns
                                info_col1, info_col2, info_col3 = st.columns(3)
                                with info_col1:
                                    st.metric("📍 Distance", f"{distance_km:.1f} km")
                                with info_col2:
                                    # Show travel time estimate
                                    if travel_mode == "Train":
                                        approx_time = distance_km / 50  # avg train speed
                                    elif travel_mode == "Bus":
                                        approx_time = distance_km / 40  # avg bus speed  
                                    elif travel_mode == "Flight":
                                        approx_time = distance_km / 500  # avg flight speed
                                    elif travel_mode == "Car":
                                        approx_time = distance_km / 60
                                    else:  # Bike
                                        approx_time = distance_km / 30
                                    
                                    st.metric("⏱️ Travel Time", f"{approx_time:.1f} hours")
                                with info_col3:
                                    st.metric("🚗 Travel Mode", travel_mode)
                                
                                # Try interactive map first, fallback to static map
                                try:
                                    # Create and display interactive Folium map
                                    folium_map = create_folium_map(start_coords, dest_coords, starting_location, destination)
                                    display_map_in_streamlit(folium_map)
                                    st.caption("🗺️ Interactive Map - You can zoom and pan for detailed view")
                                except Exception as map_error:
                                    st.warning("🔄 Using static map - interactive features unavailable")
                                    # Fallback to static map
                                    static_fig = create_static_map(start_coords, dest_coords, starting_location, destination)
                                    st.pyplot(static_fig)
                                    st.caption("📍 Static Route Map")
                                
                                # Store distance and time for download button
                                st.session_state.distance_km = distance_km
                                st.session_state.approx_time = approx_time
                                
                                # Additional map controls
                                with st.expander("🗺️ Map Controls"):
                                    st.info("""
                                    **Map Features:**
                                    - Zoom in/out for detailed view
                                    - Click on markers for location info
                                    - Pan around to explore the route
                                    - Blue line shows approximate route
                                    """)
                            else:
                                st.warning("⚠️ Could not find coordinates for the locations. Check spelling and try using major city names.")
                                
                        except Exception as e:
                            st.warning(f"⚠️ Could not generate route map: {str(e)[:100]}... but itinerary will still be created.")
                else:
                    st.info("📍 Enter starting location and destination to see the route map")
                
        except Exception as e:
            st.error(f"❌ Failed to generate itinerary: {str(e)}")
            st.info("💡 **Troubleshooting tips:**")
            st.write("• Check your internet connection")
            st.write("• Verify API keys are properly configured")
            st.write("• Try using different destination names")
            st.write("• Reduce the complexity of your request")

# ------------------------
# Welcome Section (when no submission)
# ------------------------
else:
    render_welcome_section()

# ------------------------
# Footer
# ------------------------
render_footer()