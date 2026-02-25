# app.py
# Streamlit frontend — ties everything together

# app.py
# Streamlit frontend — Black/Gold Data Dashboard UI

import streamlit as st
from engine.elasticity import calculate_elasticity, interpret_elasticity, get_margin
from engine.competitor import analyze_competitors
from engine.recommender import get_recommendation

# --- Page Config ---
st.set_page_config(page_title="Pricing Intelligence Engine", page_icon="📊", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0a0a;
    color: #e8e8e8;
}

.stApp {
    background: #0a0a0a;
}

/* Hide streamlit branding */
#MainMenu, footer, header {visibility: hidden;}

/* Main container */
.block-container {
    padding: 2rem 3rem;
    max-width: 1400px;
}

/* Header */
.dashboard-header {
    border-bottom: 1px solid #C9A84C;
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
}

.dashboard-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    color: #C9A84C;
    letter-spacing: -0.5px;
    margin: 0;
}

.dashboard-subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #666;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* Section labels */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #C9A84C;
    border-left: 2px solid #C9A84C;
    padding-left: 0.75rem;
    margin-bottom: 1rem;
    margin-top: 1.5rem;
}

/* Input styling */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: #111111 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 4px !important;
    color: #e8e8e8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #C9A84C !important;
    box-shadow: 0 0 0 1px #C9A84C !important;
}

/* Labels */
.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 1px !important;
    color: #888 !important;
    text-transform: uppercase !important;
}

/* Metric cards */
.metric-card {
    background: #111111;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: #C9A84C;
}

.metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: #666;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #C9A84C;
    line-height: 1;
}

.metric-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #555;
    margin-top: 0.4rem;
}

/* Generate button */
.stButton > button {
    background: #C9A84C !important;
    color: #0a0a0a !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #e0bc6a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(201, 168, 76, 0.3) !important;
}

/* Recommendation box */
.rec-box {
    background: #0f0f0f;
    border: 1px solid #C9A84C;
    border-radius: 6px;
    padding: 2rem;
    margin-top: 1rem;
    position: relative;
}

.rec-box::before {
    content: '◆ AI RECOMMENDATION';
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 3px;
    color: #C9A84C;
    position: absolute;
    top: -0.6rem;
    left: 1.5rem;
    background: #0f0f0f;
    padding: 0 0.5rem;
}

.rec-text {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    line-height: 1.7;
    color: #e8e8e8;
}

/* Divider */
.gold-divider {
    height: 1px;
    background: linear-gradient(to right, #C9A84C, transparent);
    margin: 2rem 0;
}

/* Price bar chart */
.price-bar-container {
    background: #111;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 1.5rem;
    margin-top: 1rem;
}

.price-bar-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: #666;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.bar-row {
    display: flex;
    align-items: center;
    margin-bottom: 0.75rem;
    gap: 0.75rem;
}

.bar-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #888;
    width: 80px;
    flex-shrink: 0;
}

.bar-track {
    flex: 1;
    background: #1a1a1a;
    height: 24px;
    border-radius: 2px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    border-radius: 2px;
    display: flex;
    align-items: center;
    padding-left: 8px;
}

.bar-fill-you {
    background: #C9A84C;
}

.bar-fill-comp {
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
}

.bar-price {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #0a0a0a;
    font-weight: bold;
}

.bar-price-comp {
    color: #888;
}

/* Warning / success */
.stAlert {
    background: #111 !important;
    border-color: #C9A84C !important;
    color: #e8e8e8 !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #C9A84C !important;
}

/* Sidebar-like panel */
.info-panel {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 6px;
    padding: 1rem 1.25rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #555;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">📊 PRICING INTELLIGENCE ENGINE</div>
    <div class="dashboard-subtitle">AI-Powered Demand Elasticity & Competitor Analysis</div>
</div>
""", unsafe_allow_html=True)

# --- Layout: Two columns ---
left_col, right_col = st.columns([3, 2], gap="large")

with left_col:

    # Product Details
    st.markdown('<div class="section-label">01 — Product Details</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Product Name", placeholder="e.g. Handmade Soy Candle")
        your_price = st.number_input("Current Price ($)", min_value=0.0, step=0.01)
    with col2:
        category = st.selectbox("Category", ["Handmade Goods", "Electronics", "Clothing", "Food & Beverage", "Home & Garden", "Other"])
        cost = st.number_input("Cost to Make/Source ($)", min_value=0.0, step=0.01)

    units_sold = st.number_input("Units Sold Per Month", min_value=0, step=1)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Price History
    st.markdown('<div class="section-label">02 — Price History (Optional)</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        old_price = st.number_input("Previous Price ($)", min_value=0.0, step=0.01)
    with col4:
        old_units = st.number_input("Units Sold at Previous Price", min_value=0, step=1)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Competitor Pricing
    st.markdown('<div class="section-label">03 — Competitor Pricing</div>', unsafe_allow_html=True)
    col5, col6, col7 = st.columns(3)
    with col5:
        comp1 = st.number_input("Competitor 1 ($)", min_value=0.0, step=0.01)
    with col6:
        comp2 = st.number_input("Competitor 2 ($)", min_value=0.0, step=0.01)
    with col7:
        comp3 = st.number_input("Competitor 3 ($)", min_value=0.0, step=0.01)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Goal
    st.markdown('<div class="section-label">04 — Seller Goal</div>', unsafe_allow_html=True)
    goal = st.selectbox("Optimization Target", [
        "Maximize Profit",
        "Maximize Sales Volume",
        "Beat Competitors",
        "Stay Competitive While Protecting Margin"
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button("⚡ GENERATE PRICING RECOMMENDATION")

with right_col:
    st.markdown('<div class="section-label">Live Metrics</div>', unsafe_allow_html=True)

    # Calculate live margin
    live_margin = get_margin(your_price, cost) if your_price > 0 and cost > 0 else None
    competitor_prices_live = [p for p in [comp1, comp2, comp3] if p > 0]
    live_comp_data = analyze_competitors(your_price, competitor_prices_live) if competitor_prices_live and your_price > 0 else None

    # Metric cards
    m1, m2 = st.columns(2)
    with m1:
        margin_display = f"{live_margin}%" if live_margin is not None else "—"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Profit Margin</div>
            <div class="metric-value">{margin_display}</div>
            <div class="metric-sub">per unit sold</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        gap_display = f"{live_comp_data['price_gap_percent']}%" if live_comp_data else "—"
        pos_display = live_comp_data['position'].replace('priced ', '') if live_comp_data else "no data"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">vs Market</div>
            <div class="metric-value">{gap_display}</div>
            <div class="metric-sub">{pos_display}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    m3, m4 = st.columns(2)
    with m3:
        avg_comp = f"${live_comp_data['avg_competitor_price']}" if live_comp_data else "—"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Competitor</div>
            <div class="metric-value">{avg_comp}</div>
            <div class="metric-sub">market average</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        revenue = round(your_price * units_sold, 2) if your_price > 0 and units_sold > 0 else None
        rev_display = f"${revenue}" if revenue else "—"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Monthly Revenue</div>
            <div class="metric-value">{rev_display}</div>
            <div class="metric-sub">at current price</div>
        </div>
        """, unsafe_allow_html=True)

    # Price comparison bar chart
    if your_price > 0 and competitor_prices_live:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Price Comparison</div>', unsafe_allow_html=True)

        all_prices = [your_price] + competitor_prices_live
        max_price = max(all_prices)

        bars_html = '<div class="price-bar-container"><div class="price-bar-title">Your Price vs Competitors</div>'

        your_width = round((your_price / max_price) * 100)
        bars_html += f"""
        <div class="bar-row">
            <div class="bar-label">YOU</div>
            <div class="bar-track">
                <div class="bar-fill bar-fill-you" style="width:{your_width}%">
                    <span class="bar-price">${your_price}</span>
                </div>
            </div>
        </div>"""

        for i, cp in enumerate(competitor_prices_live):
            w = round((cp / max_price) * 100)
            bars_html += f"""
            <div class="bar-row">
                <div class="bar-label">COMP {i+1}</div>
                <div class="bar-track">
                    <div class="bar-fill bar-fill-comp" style="width:{w}%">
                        <span class="bar-price bar-price-comp">${cp}</span>
                    </div>
                </div>
            </div>"""

        bars_html += '</div>'
        st.markdown(bars_html, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="info-panel">
            ENTER YOUR PRICE + COMPETITOR<br>
            PRICES TO SEE LIVE COMPARISON<br>
            CHART AND MARKET METRICS.
        </div>
        """, unsafe_allow_html=True)

# --- Generate Logic ---
if generate:
    if not product_name:
        st.warning("⚠ Please enter a product name.")
    elif your_price == 0:
        st.warning("⚠ Please enter your current price.")
    elif cost == 0:
        st.warning("⚠ Please enter your cost.")
    else:
        with st.spinner("Running analysis..."):
            elasticity = calculate_elasticity(old_price, your_price, old_units, units_sold) if old_price > 0 and old_units > 0 else None
            elasticity_label = interpret_elasticity(elasticity)
            margin = get_margin(your_price, cost)
            competitor_prices = [p for p in [comp1, comp2, comp3] if p > 0]
            competitor_data = analyze_competitors(your_price, competitor_prices) if competitor_prices else None

            recommendation = get_recommendation(
                product_name, category, your_price, cost, units_sold,
                elasticity_label, margin, competitor_data, goal
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="rec-box">
            <div class="rec-text">{recommendation}</div>
        </div>
        """, unsafe_allow_html=True)
