# app.py
# Streamlit frontend — Warm & Trustworthy Business Dashboard

import streamlit as st
from engine.elasticity import calculate_elasticity, interpret_elasticity, get_margin
from engine.competitor import analyze_competitors
from engine.recommender import get_recommendation

st.set_page_config(page_title="Pricing Intelligence", page_icon="📈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0f1729;
    color: #e8eaf0;
}

.stApp { background: #0f1729; }
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 2.5rem 3rem;
    max-width: 1300px;
}

.app-header {
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1e2d4a;
}
.app-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: #f0f2f7;
    font-weight: 400;
    letter-spacing: -0.3px;
    margin: 0 0 0.3rem 0;
}
.app-title span { color: #E8A838; }
.app-tagline {
    font-size: 0.8rem;
    color: #5a6a8a;
    font-weight: 400;
    letter-spacing: 0.3px;
}

.section-header {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #E8A838;
    margin: 1.75rem 0 0.85rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e2d4a;
}

.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    color: #7a8aaa !important;
    letter-spacing: 0.3px !important;
    text-transform: uppercase !important;
    margin-bottom: 0.3rem !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #162035 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 8px !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.6rem 0.85rem !important;
    transition: border-color 0.2s !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #E8A838 !important;
    box-shadow: 0 0 0 3px rgba(232, 168, 56, 0.1) !important;
}

.stSelectbox > div > div {
    background: #162035 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 8px !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
}

.metric-card {
    background: #162035;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 1.25rem 1.4rem;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #2a3d5a; }
.metric-card-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #5a6a8a;
    margin-bottom: 0.5rem;
}
.metric-card-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: #E8A838;
    line-height: 1.1;
}
.metric-card-sub {
    font-size: 0.72rem;
    color: #4a5a7a;
    margin-top: 0.3rem;
}

.stButton > button {
    background: #E8A838 !important;
    color: #0f1729 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    margin-top: 0.5rem !important;
}
.stButton > button:hover {
    background: #f0b940 !important;
    box-shadow: 0 4px 16px rgba(232, 168, 56, 0.25) !important;
    transform: translateY(-1px) !important;
}

.rec-container {
    background: #162035;
    border: 1px solid #E8A838;
    border-radius: 10px;
    padding: 1.75rem 2rem;
    margin-top: 1.5rem;
}
.rec-header {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #E8A838;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.rec-header::before { content: '●'; font-size: 0.5rem; }
.rec-body {
    font-size: 0.97rem;
    line-height: 1.75;
    color: #c8ccd8;
    font-weight: 400;
}

.chart-container {
    background: #162035;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 1.25rem 1.4rem;
    margin-top: 1rem;
}
.chart-title {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #5a6a8a;
    margin-bottom: 1.1rem;
}
.bar-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.65rem;
}
.bar-name {
    font-size: 0.68rem;
    font-weight: 600;
    color: #7a8aaa;
    width: 72px;
    flex-shrink: 0;
    letter-spacing: 0.5px;
}
.bar-track {
    flex: 1;
    background: #0f1729;
    border-radius: 4px;
    height: 28px;
    overflow: hidden;
}
.bar-you {
    background: linear-gradient(90deg, #E8A838, #f0b940);
    height: 100%;
    border-radius: 4px;
    display: flex;
    align-items: center;
    padding-left: 10px;
    min-width: 40px;
}
.bar-comp {
    background: #1e2d4a;
    height: 100%;
    border-radius: 4px;
    display: flex;
    align-items: center;
    padding-left: 10px;
    min-width: 40px;
}
.bar-you-label { font-size: 0.72rem; font-weight: 700; color: #0f1729; }
.bar-comp-label { font-size: 0.72rem; font-weight: 600; color: #7a8aaa; }

.empty-state {
    background: #162035;
    border: 1px dashed #1e2d4a;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    color: #3a4a6a;
    font-size: 0.8rem;
    line-height: 1.8;
}

.soft-divider { height: 1px; background: #1e2d4a; margin: 1.5rem 0; }
.stSpinner > div { border-top-color: #E8A838 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="app-header">
    <div class="app-title">📈 Pricing <span>Intelligence</span> Engine</div>
    <div class="app-tagline">Enter your product details and get an AI-powered pricing recommendation in seconds</div>
</div>
""", unsafe_allow_html=True)

# ── Initialize inputs with defaults ──
comp1 = comp2 = comp3 = old_price = old_units = 0.0

# ── Two column layout ──
left, right = st.columns([3, 2], gap="large")

with left:
    st.markdown('<div class="section-header">Product Details</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        product_name = st.text_input("Product Name", placeholder="e.g. Handmade Soy Candle")
        your_price = st.number_input("Your Current Price ($)", min_value=0.0, step=0.01)
    with c2:
        category = st.selectbox("Category", [
            "Handmade Goods", "Electronics", "Clothing",
            "Food & Beverage", "Home & Garden", "Other"
        ])
        cost = st.number_input("Cost to Make / Source ($)", min_value=0.0, step=0.01)

    units_sold = st.number_input("Units Sold Per Month", min_value=0, step=1)

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Price History — Optional</div>', unsafe_allow_html=True)
    st.caption("Unlocks demand elasticity analysis. Enter your previous price and sales to see how sensitive your buyers are to price changes.")

    c3, c4 = st.columns(2)
    with c3:
        old_price = st.number_input("Previous Price ($)", min_value=0.0, step=0.01)
    with c4:
        old_units = st.number_input("Units Sold at That Price", min_value=0, step=1)

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Competitor Prices</div>', unsafe_allow_html=True)
    st.caption("Look up what similar products sell for and enter them below.")

    c5, c6, c7 = st.columns(3)
    with c5:
        comp1 = st.number_input("Competitor 1 ($)", min_value=0.0, step=0.01)
    with c6:
        comp2 = st.number_input("Competitor 2 ($)", min_value=0.0, step=0.01)
    with c7:
        comp3 = st.number_input("Competitor 3 ($)", min_value=0.0, step=0.01)

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Your Goal</div>', unsafe_allow_html=True)

    goal = st.selectbox("What are you trying to achieve?", [
        "Maximize Profit",
        "Maximize Sales Volume",
        "Beat Competitors",
        "Stay Competitive While Protecting Margin"
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button("✦ Generate My Pricing Recommendation")

with right:
    competitor_prices_live = [p for p in [comp1, comp2, comp3] if p > 0]
    live_comp = analyze_competitors(your_price, competitor_prices_live) if competitor_prices_live and your_price > 0 else None
    live_margin = get_margin(your_price, cost) if your_price > 0 and cost > 0 else None
    live_revenue = round(your_price * units_sold, 2) if your_price > 0 and units_sold > 0 else None

    st.markdown('<div class="section-header">Live Metrics</div>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">Profit Margin</div>
            <div class="metric-card-value">{f"{live_margin}%" if live_margin is not None else "—"}</div>
            <div class="metric-card-sub">per unit</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">Monthly Revenue</div>
            <div class="metric-card-value">{f"${live_revenue:,}" if live_revenue else "—"}</div>
            <div class="metric-card-sub">at current price</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    m3, m4 = st.columns(2)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">Avg Competitor</div>
            <div class="metric-card-value">{f"${live_comp['avg_competitor_price']}" if live_comp else "—"}</div>
            <div class="metric-card-sub">market average</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        pos = live_comp['position'].replace('priced ', '').title() if live_comp else "—"
        gap = f"{live_comp['price_gap_percent']}%" if live_comp else "—"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">Market Position</div>
            <div class="metric-card-value">{gap}</div>
            <div class="metric-card-sub">{pos}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Price Comparison</div>', unsafe_allow_html=True)

    if your_price > 0 and competitor_prices_live:
        all_prices = [your_price] + competitor_prices_live
        max_p = max(all_prices)

        chart = '<div class="chart-container"><div class="chart-title">Your Price vs Competitors</div>'
        yw = max(12, round((your_price / max_p) * 100))
        chart += f"""
        <div class="bar-row">
            <div class="bar-name">YOU</div>
            <div class="bar-track">
                <div class="bar-you" style="width:{yw}%">
                    <span class="bar-you-label">${your_price}</span>
                </div>
            </div>
        </div>"""
        for i, cp in enumerate(competitor_prices_live):
            cw = max(12, round((cp / max_p) * 100))
            chart += f"""
            <div class="bar-row">
                <div class="bar-name">COMP {i+1}</div>
                <div class="bar-track">
                    <div class="bar-comp" style="width:{cw}%">
                        <span class="bar-comp-label">${cp}</span>
                    </div>
                </div>
            </div>"""
        chart += '</div>'
        st.markdown(chart, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            Enter your price and at least<br>
            one competitor price to see<br>
            the comparison chart
        </div>""", unsafe_allow_html=True)

# ── Generate ──
if generate:
    if not product_name:
        st.warning("Please enter a product name to continue.")
    elif your_price == 0:
        st.warning("Please enter your current price.")
    elif cost == 0:
        st.warning("Please enter your production or sourcing cost.")
    else:
        with st.spinner("Analyzing your pricing data..."):
            elasticity = calculate_elasticity(old_price, your_price, old_units, units_sold) if old_price > 0 and old_units > 0 else None
            elasticity_label = interpret_elasticity(elasticity)
            margin = get_margin(your_price, cost)
            competitor_prices = [p for p in [comp1, comp2, comp3] if p > 0]
            competitor_data = analyze_competitors(your_price, competitor_prices) if competitor_prices else None

            recommendation = get_recommendation(
                product_name, category, your_price, cost, units_sold,
                elasticity_label, margin, competitor_data, goal
            )

        st.markdown(f"""
        <div class="rec-container">
            <div class="rec-header">AI Pricing Recommendation</div>
            <div class="rec-body">{recommendation}</div>
        </div>
        """, unsafe_allow_html=True)
