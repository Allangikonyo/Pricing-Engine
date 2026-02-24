# app.py
# Streamlit frontend — ties everything together

import streamlit as st
from engine.elasticity import calculate_elasticity, interpret_elasticity, get_margin
from engine.competitor import analyze_competitors
from engine.recommender import get_recommendation

# --- Page Config ---
st.set_page_config(page_title="Pricing Intelligence Engine", page_icon="💰", layout="centered")

st.title(" Seller Pricing Intelligence Engine")
st.caption("Enter your product details and get an AI-powered pricing recommendation.")

# --- Product Info ---
st.subheader("Product Details")
col1, col2 = st.columns(2)
with col1:
    product_name = st.text_input("Product Name", placeholder="e.g. Handmade Soy Candle")
    your_price = st.number_input("Your Current Price ($)", min_value=0.0, step=0.01)
with col2:
    category = st.selectbox("Category", ["Handmade Goods", "Electronics", "Clothing", "Food & Beverage", "Home & Garden", "Other"])
    cost = st.number_input("Your Cost to Make/Source ($)", min_value=0.0, step=0.01)

units_sold = st.number_input("Units Sold Per Month", min_value=0, step=1)

# --- Price History ---
st.subheader("Price History (Optional)")
st.caption("If you've changed your price before, enter the old data here to calculate demand elasticity.")
col3, col4 = st.columns(2)
with col3:
    old_price = st.number_input("Previous Price ($)", min_value=0.0, step=0.01)
with col4:
    old_units = st.number_input("Units Sold at Previous Price", min_value=0, step=1)

# --- Competitor Pricing ---
st.subheader("Competitor Pricing")
st.caption("Enter up to 3 competitor prices you've looked up.")
col5, col6, col7 = st.columns(3)
with col5:
    comp1 = st.number_input("Competitor 1 ($)", min_value=0.0, step=0.01)
with col6:
    comp2 = st.number_input("Competitor 2 ($)", min_value=0.0, step=0.01)
with col7:
    comp3 = st.number_input("Competitor 3 ($)", min_value=0.0, step=0.01)

# --- Seller Goal ---
st.subheader("Your Goal")
goal = st.selectbox("What are you optimizing for?", [
    "Maximize Profit",
    "Maximize Sales Volume",
    "Beat Competitors",
    "Stay Competitive While Protecting Margin"
])

# --- Generate Button ---
st.divider()
if st.button(" Generate Pricing Recommendation", use_container_width=True):

    if not product_name:
        st.warning("Please enter a product name.")
    elif your_price == 0:
        st.warning("Please enter your current price.")
    elif cost == 0:
        st.warning("Please enter your cost.")
    else:
        with st.spinner("Analyzing your pricing data..."):

            # Run the engine
            elasticity = calculate_elasticity(old_price, your_price, old_units, units_sold) if old_price > 0 and old_units > 0 else None
            elasticity_label = interpret_elasticity(elasticity)
            margin = get_margin(your_price, cost)

            competitor_prices = [p for p in [comp1, comp2, comp3] if p > 0]
            competitor_data = analyze_competitors(your_price, competitor_prices) if competitor_prices else None

            recommendation = get_recommendation(
                product_name, category, your_price, cost, units_sold,
                elasticity_label, margin, competitor_data, goal
            )

        # --- Output ---
        st.success("Analysis Complete!")

        col8, col9, col10 = st.columns(3)
        with col8:
            st.metric("Your Margin", f"{margin}%")
        with col9:
            st.metric("Price Sensitivity", elasticity_label.title())
        with col10:
            if competitor_data:
                st.metric("vs Market", competitor_data["position"].replace("priced ", "").title())
            else:
                st.metric("vs Market", "No Data")

        st.subheader("💡 AI Recommendation")
        st.write(recommendation)
