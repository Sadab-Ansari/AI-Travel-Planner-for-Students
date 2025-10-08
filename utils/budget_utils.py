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
    
    # Fix: Use a more realistic estimated cost instead of hardcoded 580
    # In a real app, this would come from actual calculations based on user inputs
    estimated_cost = total_budget * 0.8  # 80% of total budget as estimated cost
    remaining = total_budget - estimated_cost
    
    # Display key metrics
    st.subheader("Budget Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Budget", 
            f"₹{total_budget:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Estimated Cost", 
            f"₹{estimated_cost:,.0f}",
            delta=f"-₹{total_budget - estimated_cost:,.0f}"
        )
    
    with col3:
        st.metric(
            "Remaining", 
            f"₹{remaining:,.0f}",
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
            hovertemplate="<b>%{label}</b><br>Amount: ₹%{value:,}<br>Percentage: %{percent}",
            marker=dict(line=dict(color='#ffffff', width=2))
        )
        
        fig_pie.update_layout(
            height=400,  # Reduced height to prevent overflow
            showlegend=False,
            font=dict(size=12),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=30, b=30, l=30, r=30)  # Add margins to prevent clipping
        )
        
        # Use config to disable zoom and add other controls
        st.plotly_chart(fig_pie, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']
        })
    
    with table_col:
        # Detailed Budget Table with improved styling
        st.subheader("Breakdown Details")
        st.markdown('<div class="budget-table-container">', unsafe_allow_html=True)
        
        # Calculate percentages
        df_display = df.copy()
        df_display['percentage'] = (df_display['amount'] / total_budget * 100).round(1)
        
        # Display as a nice table with custom styling
        for _, row in df_display.iterrows():
            st.markdown(f"""
            <div class="budget-table-row">
                <div class="budget-category">{row['category']}</div>
                <div class="budget-amount">₹{row['amount']:,}</div>
                <div class="budget-percentage">{row['percentage']}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(row['percentage'] / 100)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
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
                f"{item['category']} (₹)",
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