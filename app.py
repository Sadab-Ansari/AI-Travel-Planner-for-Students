# app.py
import streamlit as st
from config.openai_config import client
from utils.prompt_builder import build_travel_prompt

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
            st.markdown(itinerary)
        except Exception as e:
            st.error(f"❌ Failed to generate itinerary: {e}")
