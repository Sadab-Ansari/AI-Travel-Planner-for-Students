import streamlit as st
import requests

def get_safety_info(destination):
    """Get emergency contacts and safety information for destination"""
    
    # Indian emergency contacts database
    emergency_contacts = {
        'general': {
            'National Emergency': '112',
            'Police': '100',
            'Fire': '101',
            'Ambulance': '102',
            'Women Helpline': '1091',
            'Tourist Helpline': '1363'
        },
        'cities': {
            'mumbai': {
                'Local Police': '022-22621855',
                'Tourist Police': '022-22027706',
                'Major Hospital': 'KEM Hospital - 022-24107500',
                'Railway Police': '022-23752125'
            },
            'delhi': {
                'Local Police': '011-23233333',
                'Tourist Police': '011-23490234',
                'Major Hospital': 'AIIMS - 011-26588500',
                'Railway Police': '011-23230110'
            },
            'goa': {
                'Local Police': '0832-2428400',
                'Tourist Police': '0832-2428114',
                'Major Hospital': 'GMC - 0832-2458700',
                'Beach Safety': '1077'
            },
            'bangalore': {
                'Local Police': '080-22942222',
                'Tourist Police': '080-22212121',
                'Major Hospital': 'Victoria Hospital - 080-26701111',
                'Cyber Crime': '080-22942550'
            },
            'chennai': {
                'Local Police': '044-23452345',
                'Tourist Police': '044-28593992',
                'Major Hospital': 'GH Chennai - 044-25305000',
                'Coastal Security': '044-23455800'
            },
            'kolkata': {
                'Local Police': '033-22145486',
                'Tourist Police': '033-22488250',
                'Major Hospital': 'SSKM Hospital - 033-22041101',
                'Tourist Security': '033-22255436'
            },
            'hyderabad': {
                'Local Police': '040-27852008',
                'Tourist Police': '040-23244444',
                'Major Hospital': 'Osmania Hospital - 040-24600121',
                'Tourist Assistance': '040-23450444'
            },
            'pune': {
                'Local Police': '020-26126296',
                'Tourist Police': '020-26122880',
                'Major Hospital': 'Sassoon Hospital - 020-26127300',
                'Highway Patrol': '020-26101100'
            },
            'jaipur': {
                'Local Police': '0141-2744450',
                'Tourist Police': '0141-2379460',
                'Major Hospital': 'SMS Hospital - 0141-2560291',
                'Heritage Site Security': '0141-2618864'
            },
            'manali': {
                'Local Police': '01902-252112',
                'Tourist Police': '01902-252339',
                'Major Hospital': 'Regional Hospital - 01902-252237',
                'Mountain Rescue': '01902-252100'
            }
        }
    }
    
    # Find city-specific contacts
    destination_lower = destination.lower()
    city_contacts = {}
    
    for city in emergency_contacts['cities']:
        if city in destination_lower:
            city_contacts = emergency_contacts['cities'][city]
            break
    
    # If no specific city found, use general contacts
    if not city_contacts:
        city_contacts = {
            'Local Police': 'Check with hotel/hostel',
            'Nearest Hospital': 'Ask locals for directions',
            'Tourist Assistance': 'Contact hotel manager'
        }
    
    return {
        'national': emergency_contacts['general'],
        'local': city_contacts,
        'destination': destination.title()
    }

def get_safety_tips(destination, group_type, special_conditions):
    """Generate safety tips based on destination and traveler profile"""
    
    tips = []
    
    # General safety tips for India
    general_tips = [
        "🔒 **Keep documents safe** - Carry photocopies, keep originals locked",
        "📱 **Save emergency numbers** - Save in phone and write down",
        "💧 **Drink bottled water** - Avoid tap water to prevent illness",
        "🌡️ **Carry basic medicines** - For headache, stomach issues, motion sickness",
        "📞 **Inform someone** - Share itinerary with family/friends",
        "💰 **Carry cash wisely** - Don't show large amounts in public"
    ]
    
    tips.extend(general_tips)
    
    # Destination-specific tips
    dest_lower = destination.lower()
    
    if any(city in dest_lower for city in ['goa', 'beach', 'coastal']):
        tips.extend([
            "🏖️ **Beach safety** - Don't swim alone, watch for currents",
            "☀️ **Sun protection** - Use high SPF, avoid midday sun",
            "🌊 **Water activities** - Use licensed operators only"
        ])
    
    if any(city in dest_lower for city in ['manali', 'shimla', 'darjeeling', 'hill']):
        tips.extend([
            "⛰️ **Mountain safety** - Acclimatize to altitude, stay hydrated",
            "🚗 **Road safety** - Mountain roads can be dangerous at night",
            "🧥 **Weather prep** - Mountain weather changes rapidly"
        ])
    
    if any(city in dest_lower for city in ['delhi', 'mumbai', 'kolkata', 'metro']):
        tips.extend([
            "🚇 **Public transport** - Keep bags closed in crowded areas",
            "🚖 **Taxi safety** - Use app-based taxis, share ride details",
            "🌃 **Night safety** - Avoid isolated areas after dark"
        ])
    
    # Group-specific tips
    if group_type == "Solo":
        tips.extend([
            "👤 **Solo travel** - Stay in well-lit areas, avoid remote places at night",
            "🏨 **Accommodation** - Choose reputable hostels/hotels with good reviews",
            "📱 **Check-ins** - Regular check-ins with family/friends"
        ])
    
    if "female" in str(special_conditions).lower():
        tips.extend([
            "👩 **Women safety** - Avoid traveling alone at night",
            "🚗 **Transport** - Prefer women-only compartments in trains/buses",
            "🏨 **Accommodation** - Choose female-only dorms or reputed hotels",
            "👗 **Dress modestly** - Respect local customs to avoid attention"
        ])
    
    if "night" in str(special_conditions).lower():
        tips.extend([
            "🌙 **Night travel** - Plan routes in advance, use well-lit roads",
            "🚗 **Transport** - Avoid empty public transport late at night",
            "📞 **Emergency ready** - Keep phone charged and accessible"
        ])
    
    return tips

def get_travel_advisories(destination):
    """Get basic travel advisories for destination"""
    
    advisories = []
    dest_lower = destination.lower()
    
    # Seasonal advisories
    import datetime
    current_month = datetime.datetime.now().month
    
    if current_month in [6, 7, 8, 9]:  # Monsoon season
        advisories.append("🌧️ **Monsoon Alert** - Possible heavy rains, check weather updates")
    
    if current_month in [12, 1, 2]:  # Winter
        if any(city in dest_lower for city in ['manali', 'shimla', 'ladakh']):
            advisories.append("❄️ **Winter Travel** - Roads may be closed due to snow")
    
    # Festival advisories
    if any(city in dest_lower for city in ['delhi', 'mumbai', 'kolkata']):
        advisories.append("🎉 **Festival Season** - Book transport early, expect crowds")
    
    # General advisories
    advisories.extend([
        "📱 **Mobile Connectivity** - Network may be weak in remote areas",
        "💳 **Digital Payments** - UPI widely accepted, carry some cash as backup",
        "🛂 **ID Requirements** - Always carry government ID for hotel check-ins"
    ])
    
    return advisories

def display_safety_dashboard(destination, group_type, special_conditions):
    """Display complete safety dashboard in Streamlit"""
    
    st.subheader("🛡️ Safety & Emergency Dashboard")
    
    # Get all safety information
    safety_info = get_safety_info(destination)
    safety_tips = get_safety_tips(destination, group_type, special_conditions)
    advisories = get_travel_advisories(destination)
    
    # Create tabs for organized display
    contacts_tab, tips_tab, advisories_tab = st.tabs(["📞 Emergency Contacts", "💡 Safety Tips", "⚠️ Travel Advisories"])
    
    with contacts_tab:
        st.subheader(f"🚨 Emergency Contacts - {safety_info['destination']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**National Emergency Numbers**")
            for service, number in safety_info['national'].items():
                st.write(f"• **{service}**: `{number}`")
        
        with col2:
            st.write("**Local Contacts**")
            for service, contact in safety_info['local'].items():
                st.write(f"• **{service}**: `{contact}`")
        
        # Quick action buttons
        st.write("**Quick Actions**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📞 Save Police Number", key="police_btn"):
                st.success("Police number saved to clipboard: 100")
        with col2:
            if st.button("🏥 Save Ambulance", key="ambulance_btn"):
                st.success("Ambulance number saved: 102")
        with col3:
            if st.button("👮 Save Tourist Helpline", key="tourist_btn"):
                st.success("Tourist helpline saved: 1363")
    
    with tips_tab:
        st.subheader("💡 Personalized Safety Tips")
        
        for i, tip in enumerate(safety_tips, 1):
            st.write(f"{i}. {tip}")
        
        # Download safety tips
        tips_text = "\n".join([tip.replace('**', '') for tip in safety_tips])
        st.download_button(
            label="📥 Download Safety Tips",
            data=tips_text,
            file_name="safety_tips.txt",
            mime="text/plain"
        )
    
    with advisories_tab:
        st.subheader("⚠️ Travel Advisories")
        
        for advisory in advisories:
            st.info(advisory)
        
        # Additional resources
        st.write("**Additional Resources**")
        st.write("• [Ministry of Tourism](https://tourism.gov.in) - Official travel guidelines")
        st.write("• [State Tourism Websites](https://tourism.gov.in/states) - Local information")
        st.write("• [Indian Railways Security](https://indianrailways.gov.in) - Train travel safety")