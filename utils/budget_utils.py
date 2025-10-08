import re
import streamlit as st
import pandas as pd
import plotly.express as px

def extract_budget_data(itinerary_text):
    """Extract budget information from AI itinerary output"""
    budget_data = {
        'transport': 0,
        'accommodation': 0, 
        'food': 0,
        'activities': 0,
        'misc': 0
    }
    
    # Patterns to find costs in the itinerary
    patterns = {
        'transport': r'[Tt]rain.*?₹(\d+)',
        'accommodation': r'[Hh]ostel.*?₹(\d+)', 
        'food': r'[Ff]ood.*?₹(\d+)',
        'activities': r'[Ee]ntry.*?₹(\d+)'
    }
    
    for category, pattern in patterns.items():
        matches = re.findall(pattern, itinerary_text)
        if matches:
            budget_data[category] = sum(int(match) for match in matches)
    
    return budget_data

def create_budget_charts(budget_data, total_budget):
    """Create pie chart and budget breakdown"""
    # Prepare data for visualization
    categories = ['Transport', 'Accommodation', 'Food', 'Activities', 'Misc']
    values = [
        budget_data['transport'],
        budget_data['accommodation'], 
        budget_data['food'],
        budget_data['activities'],
        budget_data['misc']
    ]
    
    # Remove zero values for cleaner chart
    filtered_categories = []
    filtered_values = []
    
    for cat, val in zip(categories, values):
        if val > 0:
            filtered_categories.append(cat)
            filtered_values.append(val)
    
    # Create pie chart
    if filtered_values:
        fig = px.pie(
            names=filtered_categories,
            values=filtered_values,
            title="💰 Budget Distribution",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
    else:
        fig = None
    
    return fig, filtered_categories, filtered_values

def display_budget_breakdown(itinerary_text, total_budget):
    """Main function to display budget breakdown"""
    # Extract budget data
    budget_data = extract_budget_data(itinerary_text)
    
    # Create charts
    fig, categories, values = create_budget_charts(budget_data, total_budget)
    
    # Display in Streamlit
    if fig:
        st.plotly_chart(fig, use_container_width=True)
        
        # Show budget table
        st.subheader("📊 Detailed Budget Breakdown")
        
        budget_df = pd.DataFrame({
            'Category': categories,
            'Amount (₹)': values,
            'Percentage': [f"{(val/total_budget)*100:.1f}%" for val in values]
        })
        
        st.dataframe(budget_df, hide_index=True)
        
        # Show remaining budget
        total_spent = sum(values)
        remaining = total_budget - total_spent
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Budget", f"₹{total_budget}")
        with col2:
            st.metric("Estimated Cost", f"₹{total_spent}")
        with col3:
            st.metric("Remaining", f"₹{remaining}", delta=f"{(remaining/total_budget)*100:.1f}%")
    else:
        st.warning("Could not extract budget details from itinerary")