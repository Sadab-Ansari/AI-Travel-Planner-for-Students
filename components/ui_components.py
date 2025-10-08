"""
UI Components Module for AI Travel Planner
Contains reusable UI components and styling functions
"""

import streamlit as st
from config.constants import APP_NAME, APP_ICON, CURRENCY_SYMBOL

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app."""
    with open("static/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_header():
    """Render the app header with title and subtitle."""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>{APP_ICON} {APP_NAME}</h1>
        <p style="font-size: 1.2em; color: #a0aec0; margin-top: 10px;">
            Plan budget-friendly, personalized trips in seconds! ✈️
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with navigation and info."""
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2>{APP_ICON} Student Travel Planner</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📝 Quick Tips")
        st.info("""
        💡 **Pro Tips:**
        - Use specific city names for better results
        - Include your interests for personalized plans
        - Check weather and safety tabs before packing
        """)
        
        st.markdown("---")
        
        st.markdown("### 🆘 Support")
        st.markdown("Having issues? Check our FAQ or contact support.")
        
        # Add user session info if available
        if 'user_name' in st.session_state:
            st.success(f"Welcome back, {st.session_state.user_name}! 👋")

def render_travel_form():
    """Render the travel planning form."""
    with st.form(key="travel_form"):
        st.subheader("📍 Trip Details")
        
        col1, col2 = st.columns(2)
        with col1:
            destination = st.text_input(
                "Destination*", 
                placeholder="Goa, Manali, Jaipur", 
                help="Enter city or popular destination"
            )
            starting_location = st.text_input(
                "Starting Location*", 
                placeholder="Mumbai, Delhi, Bangalore",
                help="Your starting point"
            )
            duration_days = st.number_input(
                "Duration (days)*", 
                min_value=1, 
                max_value=30, 
                value=3, 
                help="1-30 days"
            )
            budget = st.number_input(
                f"Budget ({CURRENCY_SYMBOL})*", 
                min_value=500, 
                value=5000, 
                step=500, 
                help=f"Total trip budget in {CURRENCY_SYMBOL}"
            )
        
        with col2:
            group_type = st.selectbox(
                "Group Type*", 
                ["Solo", "Friends", "Couple", "Family"],
                help="Who are you traveling with?"
            )
            travel_mode = st.selectbox(
                "Travel Mode*", 
                ["Train", "Bus", "Flight", "Car", "Bike"],
                help="Preferred mode of transportation"
            )
            stay_preference = st.selectbox(
                "Stay Preference*", 
                ["Hostel", "Budget Hotel", "Airbnb", "Luxury Hotel"],
                help="Where would you like to stay?"
            )
            food_preference = st.selectbox(
                "Food Preference*", 
                ["Veg", "Non-Veg", "Mix", "Vegan"],
                help="Your dietary preferences"
            )
        
        st.subheader("🎯 Preferences (Optional)")
        col3, col4 = st.columns(2)
        with col3:
            interests = st.text_input(
                "Interests / Activities", 
                placeholder="Beaches, Adventure, Foodie, Photography",
                help="What activities interest you?"
            )
            travel_goal = st.text_input(
                "Travel Goal", 
                placeholder="Refresh, College Trip, Photography",
                help="What's the purpose of your trip?"
            )
        with col4:
            weather_preference = st.text_input(
                "Weather Preference", 
                placeholder="Cold, Moderate, Warm",
                help="Preferred weather conditions"
            )
            special_conditions = st.text_input(
                "Special Conditions", 
                placeholder="Female-only group, no night travel, wheelchair accessible",
                help="Any special requirements?"
            )
        
        # Form submission
        submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
        with submit_col2:
            submit_button = st.form_submit_button(
                label="🚀 Generate Travel Plan", 
                use_container_width=True,
                type="primary"
            )
            
    return (destination, starting_location, duration_days, budget, group_type, 
            travel_mode, stay_preference, food_preference, interests, travel_goal, 
            weather_preference, special_conditions, submit_button)

def render_welcome_section():
    """Render the welcome section when no submission has been made."""
    st.markdown("---")
    
    # Features overview
    st.subheader("🚀 Why Use AI Travel Planner?")
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown("### 💰 Budget Smart")
        st.write("Get cost-effective plans tailored to student budgets with real-time budget tracking.")
    
    with feature_col2:
        st.markdown("### 🎯 Personalized")
        st.write("AI-powered itineraries based on your interests, group type, and preferences.")
    
    with feature_col3:
        st.markdown("### 🛡️ Safety First")
        st.write("Safety recommendations and emergency info specific to your destination.")
    
    st.markdown("---")
    
    # Quick examples
    st.subheader("🎯 Popular Student Destinations")
    example_col1, example_col2, example_col3 = st.columns(3)
    
    with example_col1:
        st.markdown("**🏖️ Beach Trip**")
        st.caption(f"Goa • 4 days • {CURRENCY_SYMBOL}8000")
        st.markdown("*Friends group • Hostels • Beach parties*")
    
    with example_col2:
        st.markdown("**🏔️ Adventure Trip**")
        st.caption(f"Manali • 5 days • {CURRENCY_SYMBOL}10000") 
        st.markdown("*Couple • Airbnb • Trekking*")
    
    with example_col3:
        st.markdown("**🏛️ Heritage Trip**")
        st.caption(f"Jaipur • 3 days • {CURRENCY_SYMBOL}6000")
        st.markdown("*Solo • Budget hotel • Photography*")
    
    st.markdown("---")
    st.info("💡 **Ready to plan?** Fill out the form above and click 'Generate Travel Plan'!")

def render_itinerary_content(itinerary):
    """Render the itinerary content with improved styling."""
    st.markdown('<div class="itinerary-content">', unsafe_allow_html=True)
    st.markdown(itinerary)
    st.markdown('</div>', unsafe_allow_html=True)

def render_footer():
    """Render the app footer."""
    st.markdown("---")
    footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])
    with footer_col1:
        st.caption(f"{APP_ICON} {APP_NAME} • Built with ❤️ for student travelers")
    with footer_col2:
        st.caption("[Report Issue](https://github.com/your-repo/issues)")
    with footer_col3:
        st.caption("[Privacy Policy](#)")