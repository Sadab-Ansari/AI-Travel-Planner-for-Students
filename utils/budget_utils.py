import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def display_budget_breakdown():
    st.header("💰 Travel Budget Planner")
    
    # Sample complete budget data - you can replace this with dynamic data
    budget_items = [
        {"category": "Accommodation", "amount": 4000, "color": "#FF6B6B"},
        {"category": "Transportation", "amount": 3000, "color": "#4ECDC4"},
        {"category": "Food", "amount": 1500, "color": "#45B7D1"},
        {"category": "Activities", "amount": 1000, "color": "#96CEB4"},
        {"category": "Shopping", "amount": 800, "color": "#FFEAA7"},
        {"category": "Emergency", "amount": 700, "color": "#DDA0DD"}
    ]
    
    df = pd.DataFrame(budget_items)
    total_budget = df['amount'].sum()
    estimated_cost = 580  # This should come from your actual calculations
    remaining = total_budget - estimated_cost
    
    # Display key metrics
    st.subheader("Budget Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Budget", 
            f"¥{total_budget:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Estimated Cost", 
            f"¥{estimated_cost:,}",
            delta=f"-¥{total_budget - estimated_cost:,}"
        )
    
    with col3:
        st.metric(
            "Remaining", 
            f"¥{remaining:,}",
            delta_color="inverse" if remaining < 0 else "normal"
        )
    
    # Progress bar for budget usage
    if total_budget > 0:
        usage_percentage = (estimated_cost / total_budget) * 100
        st.progress(min(usage_percentage / 100, 1.0))
        st.caption(f"Budget used: {usage_percentage:.1f}%")
    
    # Create two columns for chart and table
    chart_col, table_col = st.columns([2, 1])
    
    with chart_col:
        # Pie Chart
        st.subheader("Budget Distribution")
        fig_pie = px.pie(
            df, 
            values='amount', 
            names='category',
            color='category',
            color_discrete_map={
                'Accommodation': '#FF6B6B',
                'Transportation': '#4ECDC4', 
                'Food': '#45B7D1',
                'Activities': '#96CEB4',
                'Shopping': '#FFEAA7',
                'Emergency': '#DDA0DD'
            },
            hole=0.4,
            template='plotly_white'
        )
        
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Amount: ¥%{value:,}<br>Percentage: %{percent}",
            marker=dict(line=dict(color='#ffffff', width=2))
        )
        
        fig_pie.update_layout(
            height=500,
            showlegend=False,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with table_col:
        # Detailed Budget Table
        st.subheader("Breakdown Details")
        
        # Calculate percentages
        df_display = df.copy()
        df_display['percentage'] = (df_display['amount'] / total_budget * 100).round(1)
        df_display['amount_display'] = df_display['amount'].apply(lambda x: f"¥{x:,}")
        df_display['percentage_display'] = df_display['percentage'].apply(lambda x: f"{x}%")
        
        # Display as a nice table
        for _, row in df_display.iterrows():
            with st.container():
                cols = st.columns([3, 2, 1])
                with cols[0]:
                    st.write(f"**{row['category']}**")
                with cols[1]:
                    st.write(row['amount_display'])
                with cols[2]:
                    st.write(row['percentage_display'])
                st.progress(row['percentage'] / 100)
    
    # Budget Planning Tips
    st.subheader("💡 Budget Tips for Students")
    
    tip_col1, tip_col2, tip_col3 = st.columns(3)
    
    with tip_col1:
        st.info("""
        **Accommodation**  
        • Hostels & dorms  
        • Student discounts  
        • Early bookings
        """)
    
    with tip_col2:
        st.info("""
        **Food Savings**  
        • Local markets  
        • Street food  
        • Cook yourself
        """)
    
    with tip_col3:
        st.info("""
        **Transport**  
        • Student passes  
        • Off-peak travel  
        • Walk/bike routes
        """)
    
    # Budget Input Section for Customization
    st.subheader("Customize Your Budget")
    
    with st.expander("Adjust Budget Categories"):
        new_budget = {}
        
        for item in budget_items:
            new_value = st.number_input(
                f"{item['category']} (¥)",
                min_value=0,
                value=item['amount'],
                key=f"budget_{item['category']}"
            )
            new_budget[item['category']] = new_value
        
        if st.button("Update Budget"):
            # Update the budget data here
            st.success("Budget updated successfully!")
            st.rerun()

def calculate_budget_metrics(transport_cost, accommodation_cost, food_cost, activities_cost, duration_days):
    """
    Calculate comprehensive budget metrics
    """
    total_cost = transport_cost + accommodation_cost + food_cost + activities_cost
    daily_cost = total_cost / duration_days if duration_days > 0 else 0
    
    return {
        'total_cost': total_cost,
        'daily_cost': daily_cost,
        'transport_percentage': (transport_cost / total_cost * 100) if total_cost > 0 else 0,
        'accommodation_percentage': (accommodation_cost / total_cost * 100) if total_cost > 0 else 0,
        'food_percentage': (food_cost / total_cost * 100) if total_cost > 0 else 0,
        'activities_percentage': (activities_cost / total_cost * 100) if total_cost > 0 else 0
    }

# For testing the module directly
if __name__ == "__main__":
    display_budget_breakdown()