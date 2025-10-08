# app.py
import streamlit as st
from config.openai_config import client
from utils.prompt_builder import build_travel_prompt
from utils.map_utils import get_coordinates, create_folium_map, calculate_distance, display_map_in_streamlit, create_static_map
from utils.budget_utils import display_budget_breakdown
from utils.packing_utils import generate_packing_list, display_packing_checklist
from utils.weather_utils import get_weather_forecast, display_weather_forecast, get_weather_packing_tips
from utils.safety_utils import display_safety_dashboard  # NEW IMPORT
import matplotlib.pyplot as plt

# ------------------------
# Streamlit App UI
# ------------------------
st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="centered")
st.title("🎒 AI Travel Planner for Students")
st.markdown("Plan budget-friendly, personalized trips in seconds!")

# ------------------------
# User Inputs
# ------------------------
with st.form(key="travel_form"):
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Destination", placeholder="Goa, Manali, Jaipur")
        starting_location = st.text_input("Starting Location", placeholder="Mumbai")
        duration_days = st.number_input("Duration (days)", min_value=1, max_value=30, value=3)
        budget = st.number_input("Budget (₹)", min_value=500, value=5000)
    with col2:
        group_type = st.selectbox("Group Type", ["Solo", "Friends", "Couple", "Family"])
        travel_mode = st.selectbox("Travel Mode", ["Train", "Bus", "Flight", "Car"])
        stay_preference = st.selectbox("Stay Preference", ["Hostel", "Budget Hotel", "Airbnb"])
        food_preference = st.selectbox("Food Preference", ["Veg", "Non-Veg", "Mix"])
        interests = st.text_input("Interests / Vibe", placeholder="Beaches, Adventure, Foodie")
    
    travel_goal = st.text_input("Travel Goal (optional)", placeholder="Refresh / Photography / College Trip")
    weather_preference = st.text_input("Weather Preference (optional)", placeholder="Cold / Moderate / Warm")
    special_conditions = st.text_input("Special Conditions (optional)", placeholder="Female-only group, no night travel")
    
    submit_button = st.form_submit_button(label="Generate Itinerary")

# ------------------------
# Generate AI Itinerary
# ------------------------
if submit_button:
    with st.spinner("Generating your personalized travel plan..."):
        # Show route map first
        if starting_location and destination:
            with st.spinner("Calculating route and generating map..."):
                try:
                    # Get coordinates for both locations
                    start_coords = get_coordinates(starting_location)
                    dest_coords = get_coordinates(destination)
                    
                    if start_coords and dest_coords:
                        st.subheader("🗺️ Route Overview")
                        
                        # Calculate approximate distance
                        distance_km = calculate_distance(start_coords, dest_coords)
                        st.info(f"📍 **Distance**: {distance_km:.1f} km from {starting_location} to {destination}")
                        
                        # Try interactive map first, fallback to static map
                        try:
                            # Create and display interactive Folium map
                            folium_map = create_folium_map(start_coords, dest_coords, starting_location, destination)
                            display_map_in_streamlit(folium_map)
                            st.caption("🗺️ Interactive Map - You can zoom and pan")
                        except Exception as map_error:
                            st.warning("🔄 Using static map - interactive features unavailable")
                            # Fallback to static map
                            static_fig = create_static_map(start_coords, dest_coords, starting_location, destination)
                            st.pyplot(static_fig)
                            st.caption("📍 Static Route Map")
                        
                        # Show travel time estimate
                        if travel_mode == "Train":
                            approx_time = distance_km / 50  # avg train speed
                        elif travel_mode == "Bus":
                            approx_time = distance_km / 40  # avg bus speed  
                        elif travel_mode == "Flight":
                            approx_time = distance_km / 500  # avg flight speed
                        else:  # Car
                            approx_time = distance_km / 60
                            
                        st.write(f"⏱️ **Estimated travel time**: {approx_time:.1f} hours by {travel_mode}")
                        
                        # Store distance and time for download button
                        st.session_state.distance_km = distance_km
                        st.session_state.approx_time = approx_time
                    else:
                        st.warning("⚠️ Could not find coordinates for the locations. Check spelling and try again.")
                        
                except Exception as e:
                    st.warning(f"⚠️ Could not generate route map: {str(e)[:100]}... but itinerary will still be created.")

        # Generate itinerary
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
                model="gpt-4.1-mini",
                input=prompt
            )
            itinerary = response.output_text
            st.success("🎉 Your AI Travel Itinerary is ready!")
            
            # Get weather forecast
            weather_forecast = None
            with st.spinner("🌤️ Fetching weather forecast..."):
                weather_forecast = get_weather_forecast(destination, duration_days)
            
            # NEW: Updated tabs with Safety Dashboard
            itinerary_tab, budget_tab, packing_tab, weather_tab, safety_tab, map_tab = st.tabs(["📅 Itinerary", "💰 Budget", "🎒 Packing", "🌤️ Weather", "🛡️ Safety", "🗺️ Route"])
            
            with itinerary_tab:
                st.markdown(itinerary)
                
                # Add map download option
                if starting_location and destination and 'distance_km' in st.session_state:
                    st.download_button(
                        label="📱 Save Route Info",
                        data=f"Route: {starting_location} to {destination}\nDistance: {st.session_state.distance_km:.1f} km\nTravel Time: {st.session_state.approx_time:.1f} hours\nTravel Mode: {travel_mode}",
                        file_name="travel_route.txt",
                        mime="text/plain"
                    )
            
            with budget_tab:
                # Budget Breakdown Section
                st.subheader("💰 Budget Analysis")
                display_budget_breakdown(itinerary, budget)
                
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
                        st.info("**Weather-based packing suggestions:**")
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
                    st.write("Try using major city names for better weather data.")
            
            with safety_tab:
                # NEW: Safety Dashboard Section
                display_safety_dashboard(destination, group_type, special_conditions)
                
            with map_tab:
                # Show map again in its own tab
                if starting_location and destination:
                    try:
                        start_coords = get_coordinates(starting_location)
                        dest_coords = get_coordinates(destination)
                        if start_coords and dest_coords:
                            folium_map = create_folium_map(start_coords, dest_coords, starting_location, destination)
                            display_map_in_streamlit(folium_map)
                    except:
                        st.info("Map unavailable in this view. Check the main itinerary for route details.")
                
        except Exception as e:
            st.error(f"❌ Failed to generate itinerary: {e}")