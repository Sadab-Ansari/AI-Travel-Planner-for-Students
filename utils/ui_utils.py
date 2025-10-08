import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app."""
    st.markdown("""
    <style>
    .big-title {
        font-size: 3em;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 1.2em;
        color: #4ECDC4;
        text-align: center;
        margin-bottom: 30px;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
        padding: 10px;
    }
    .stNumberInput > div > div > input {
        font-size: 16px;
        padding: 10px;
    }
    .stSelectbox > div > div > select {
        font-size: 16px;
        padding: 10px;
    }
    .stButton > button {
        font-size: 18px;
        padding: 10px 20px;
        background-color: #45B7D1;
        color: white;
        border: none;
        border-radius: 5px;
    }
    .stButton > button:hover {
        background-color: #3A9DBF;
    }
    .itinerary-container {
        background-color: #F0F8FF;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #45B7D1;
    }
    </style>
    """, unsafe_allow_html=True)

def render_title():
    """Render the app title and subtitle."""
    st.markdown('<h1 class="big-title">🎒 AI Travel Planner for Students</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Plan budget-friendly, personalized trips in seconds!</p>', unsafe_allow_html=True)

def render_travel_form():
    """Render the travel planning form with enhanced UI."""
    with st.form(key="travel_form"):
        st.markdown("### 📍 Trip Details")
        col1, col2 = st.columns(2)
        with col1:
            destination = st.text_input("🏖️ Destination", placeholder="e.g., Goa, Manali, Jaipur", help="Where do you want to go?")
            starting_location = st.text_input("🏠 Starting Location", placeholder="e.g., Mumbai", help="Where are you starting from?")
            duration_days = st.number_input("📅 Duration (days)", min_value=1, max_value=30, value=3, help="How many days?")
            budget = st.number_input("💰 Budget (₹)", min_value=500, value=5000, step=500, help="Your total budget in INR")

        with col2:
            group_type = st.selectbox("👥 Group Type", ["Solo", "Friends", "Couple", "Family"], help="Who are you traveling with?")
            travel_mode = st.selectbox("🚗 Travel Mode", ["Train", "Bus", "Flight", "Car"], help="How will you travel?")
            stay_preference = st.selectbox("🏨 Stay Preference", ["Hostel", "Budget Hotel", "Airbnb"], help="Where will you stay?")
            food_preference = st.selectbox("🍽️ Food Preference", ["Veg", "Non-Veg", "Mix"], help="Your food choices")
            interests = st.text_input("🎉 Interests / Vibe", placeholder="e.g., Beaches, Adventure, Foodie", help="What are you into?")

        # Optional fields in an expander
        with st.expander("🔧 Optional Preferences"):
            travel_goal = st.text_input("🎯 Travel Goal", placeholder="e.g., Refresh, Photography, College Trip", help="Purpose of the trip")
            weather_preference = st.text_input("🌤️ Weather Preference", placeholder="e.g., Cold, Moderate, Warm", help="Preferred weather")
            special_conditions = st.text_input("⚠️ Special Conditions", placeholder="e.g., Female-only group, no night travel", help="Any special requirements")

        submit_button = st.form_submit_button(label="🚀 Generate Itinerary")

    return destination, starting_location, duration_days, budget, group_type, travel_mode, stay_preference, food_preference, interests, travel_goal, weather_preference, special_conditions, submit_button

def display_itinerary(itinerary):
    """Display the generated itinerary in a styled container."""
    st.success("🎉 Your AI Travel Itinerary is ready!")
    st.markdown('<div class="itinerary-container">', unsafe_allow_html=True)
    st.markdown(itinerary)
    st.markdown('</div>', unsafe_allow_html=True)
