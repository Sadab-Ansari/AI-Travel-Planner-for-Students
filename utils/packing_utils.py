import streamlit as st
import re

def generate_packing_list(itinerary_text, destination, duration_days, interests, weather_preference):
    """Generate smart packing list based on trip details"""
    
    # Base essentials (always included)
    base_items = [
        "✅ Government ID (Aadhar, Driver's License)",
        "✅ Phone + Charger + Power Bank", 
        "✅ Cash + ATM Cards",
        "✅ Basic Medicines (headache, stomach, motion sickness)",
        "✅ Sanitizer & Masks",
        "✅ Reusable Water Bottle"
    ]
    
    # Weather-based items
    weather_items = []
    if weather_preference:
        weather_lower = weather_preference.lower()
        if 'cold' in weather_lower:
            weather_items.extend([
                "🧥 Warm Jacket/Sweater",
                "🧣 Scarf/Shawl", 
                "🧤 Gloves (if very cold)",
                "🔥 Thermal wear (for hill stations)"
            ])
        elif 'warm' in weather_lower or 'hot' in weather_lower:
            weather_items.extend([
                "👕 Light Cotton Clothes",
                "🕶️ Sunglasses",
                "🧴 Sunscreen Lotion",
                "🎩 Cap/Hat"
            ])
        elif 'moderate' in weather_lower:
            weather_items.extend([
                "👚 Layered Clothing",
                "🧥 Light Jacket",
                "🌂 Umbrella (just in case)"
            ])
    
    # Duration-based items
    duration_items = []
    if duration_days <= 3:
        duration_items.extend([
            f"👕 {duration_days} sets of clothes",
            "🎒 Small Backpack"
        ])
    else:
        duration_items.extend([
            f"👕 {duration_days} sets of clothes + 1 extra",
            "🧳 Travel Luggage",
            "🧼 Quick-dry towel",
            "🧴 Travel-sized toiletries"
        ])
    
    # Interest-based items
    interest_items = []
    if interests:
        interests_lower = interests.lower()
        if 'beach' in interests_lower:
            interest_items.extend([
                "🩳 Swimwear",
                "🩴 Flip Flops", 
                "🏖️ Beach Towel",
                "📱 Waterproof Phone Case"
            ])
        if 'adventure' in interests_lower or 'trek' in interests_lower:
            interest_items.extend([
                "🥾 Sports Shoes/Hiking Boots",
                "🎒 Daypack",
                "💧 Hydration Pack/Water Bottle", 
                "🧭 Power Bank (extra)"
            ])
        if 'photography' in interests_lower:
            interest_items.extend([
                "📷 Camera + Extra Memory Cards",
                "🔋 Camera Batteries + Charger",
                "🎒 Camera Bag"
            ])
        if 'food' in interests_lower:
            interest_items.extend([
                "🍴 Hand Sanitizer (extra)",
                "📱 Food Review Apps installed"
            ])
    
    # Destination-specific items (India focus)
    destination_items = []
    if destination:
        dest_lower = destination.lower()
        if any(city in dest_lower for city in ['goa', 'beach', 'coastal']):
            destination_items.extend(["🌊 Beach Bag", "🏊‍♂️ Goggles"])
        elif any(city in dest_lower for city in ['manali', 'shimla', 'darjeeling', 'hill']):
            destination_items.extend(["🧥 Warm Layers", "🥾 Sturdy Shoes"])
        elif any(city in dest_lower for city in ['delhi', 'mumbai', 'metro']):
            destination_items.extend(["👞 Comfortable Walking Shoes", "📱 Local Transport Apps"])
    
    # Combine all items
    all_items = base_items + weather_items + duration_items + interest_items + destination_items
    
    return all_items

def display_packing_checklist(packing_items, duration_days):
    """Display packing list in an organized way"""
    
    st.subheader("🎒 Smart Packing Checklist")
    
    # Show summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Items", len(packing_items))
    with col2:
        st.metric("Trip Duration", f"{duration_days} days")
    with col3:
        st.metric("Categories", "5")
    
    # Display items in expandable sections
    with st.expander("🧳 **Essential Documents & Electronics**", expanded=True):
        essential_items = [item for item in packing_items if '✅' in item]
        for item in essential_items:
            st.write(item)
    
    with st.expander("👕 **Clothing & Personal Items**"):
        clothing_items = [item for item in packing_items if '👕' in item or '🧥' in item or '👚' in item]
        for item in clothing_items:
            st.write(item)
    
    with st.expander("🎯 **Activity-Specific Gear**"):
        activity_items = [item for item in packing_items if any(icon in item for icon in ['🩳', '🥾', '📷', '🍴'])]
        for item in activity_items:
            st.write(item)
    
    with st.expander("🌦️ **Weather & Miscellaneous**"):
        misc_items = [item for item in packing_items if item not in essential_items + clothing_items + activity_items]
        for item in misc_items:
            st.write(item)
    
    # Download option
    packing_text = "\n".join([item.replace('✅ ', '').replace('🧥 ', '').replace('🥾 ', '') for item in packing_items])
    st.download_button(
        label="📥 Download Packing List",
        data=packing_text,
        file_name="packing_checklist.txt",
        mime="text/plain"
    )