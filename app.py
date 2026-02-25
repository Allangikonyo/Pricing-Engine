# app.py
# Streamlit frontend — Fun, Light, Friendly Business UI

import streamlit as st
from engine.elasticity import calculate_elasticity, interpret_elasticity, get_margin
from engine.competitor import analyze_competitors
from engine.recommender import get_recommendation

st.set_page_config(page_title="Pricing Intelligence", page_icon="🏷️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #faf9f6;
    color: #1a1a1a;
}

.stApp { background: #faf9f6; }
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 2.5rem 3rem;
    max-width: 1300px;
}

/* ── Header ── */
.app-header {
    background: #fff;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    border: 1.5px solid #f0ede6;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.app-title {
    font-size: 1.75rem;
    font-weight: 800;
    color: #1a1a1a;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}
.app-title span { color: #F25C2B; }
.app-tagline {
    font-size: 0.85rem;
    color: #888;
    font-weight: 400;
}
.header-badge {
    background: #FFF4F0;
    border: 1.5px solid #F25C2B;
    color: #F25C2B;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 0.4rem 0.85rem;
    border-radius: 20px;
}

/* ── Cards ── */
.card {
    background: #fff;
    border-radius: 14px;
    border: 1.5px solid #f0ede6;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
}

/* ── Section labels ── */
.section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #aaa;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #F25C2B;
    display: inline-block;
}

/* ── Inputs ── */
.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    color: #555 !important;
    letter-spacing: 0.2px !important;
    margin-bottom: 0.25rem !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #faf9f6 !important;
    border: 1.5px solid #e8e4dc !important;
    border-radius: 10px !important;
    color: #1a1a1a !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #F25C2B !important;
    box-shadow: 0 0 0 3px rgba(242, 92, 43, 0.1) !important;
    background: #fff !important;
}

.stSelectbox > div > div {
    background: #faf9f6 !important;
    border: 1.5px solid #e8e4dc !important;
    border-radius: 10px !important;
    color: #1a1a1a !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
}

/* ── Metric cards ── */
.metric-card {
    background: #fff;
    border: 1.5px solid #f0ede6;
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    transition: all 0.2s;
}
.metric-card:hover {
    border-color: #F25C2B;
    box-shadow: 0 4px 16px rgba(242, 92, 43, 0.08);
}
.metric-card-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #aaa;
    margin-bottom: 0.4rem;
}
.metric-card-value {
    font-size: 1.75rem;
    font-weight: 800;
    color: #1a1a1a;
    line-height: 1.1;
    letter-spacing: -0.5px;
}
.metric-card-value.highlight { color: #F25C2B; }
.metric-card-sub {
    font-size: 0.72rem;
    color: #bbb;
    margin-top: 0.25rem;
    font-weight: 500;
}

/* ── Button ── */
.stButton > button {
    background: #F25C2B !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.3px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #d94e20 !important;
    box-shadow: 0 6px 20px rgba(242, 92, 43, 0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── Recommendation ── */
.rec-container {
    background: #FFF4F0;
    border: 1.5px solid #F25C2B;
    border-radius: 14px;
    padding: 1.75rem 2rem;
    margin-top: 1.5rem;
}
.rec-header {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #F25C2B;
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.rec-body {
    font-size: 0.97rem;
    line-height: 1.75;
    color: #333;
    font-weight: 400;
}

/* ── Price chart ── */
.chart-container {
    background: #fff;
    border: 1.5px solid #f0ede6;
    border-radius: 12px;
    padding: 1.25rem 1.4rem;
}
.chart-title {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #bbb;
    margin-bottom: 1rem;
}
.bar-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.6rem;
}
.bar-name {
    font-size: 0.7rem;
    font-weight: 700;
    color: #888;
    width: 64px;
    flex-shrink: 0;
}
.bar-track {
    flex: 1;
    background: #faf9f6;
    border-radius: 6px;
    height: 30px;
    overflow: hidden;
}
.bar-you {
    background: linear-gradient(90deg, #F25C2B, #f57c52);
    height: 100%;
    border-radius: 6px;
    display: flex;
    align-items: center;
    padding-left: 10px;
    min-width: 48px;
}
.bar-comp {
    background: #e8e4dc;
    height: 100%;
    border-radius: 6px;
    display: flex;
    align-items: center;
    padding-left: 10px;
    min-width: 48px;
}
.bar-you-label { font-size: 0.72rem; font-weight: 700; color: #fff; }
.bar-comp-label { font-size: 0.72rem; font-weight: 600; color: #888; }

/* ── Empty state ── */
.empty-state {
    background: #faf9f6;
    border: 1.5px dashed #e8e4dc;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    color: #ccc;
    font-size: 0.82rem;
    line-height: 1.9;
    font-weight: 500;
}

.soft-divider { height: 1px; background: #f0ede6; margin: 1.25rem 0; }
.stSpinner > div { border-top-color: #F25C2B !important; }

/* Caption text */
.stCaption { color: #aaa !important; font-size: 0.78rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="app-header">
    <div>
        <div class="app-title">🏷️ Pricing <span>Intelligence</span> Engine</div>
        <div class="app-tagline">Get an AI-powered pricing recommendation for your product in seconds</div>
    </div>
    <div class="header-badge">✦ AI Powered</div>
</div>
""", unsafe_allow_html=True)

# ── Initialize ──
comp1 = comp2 = comp3 = old_price = old_units = 0.0

left, right = st.columns([3, 2], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label"><span class="dot"></span> Product Details</div>', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label"><span class="dot"></span> Price History — Optional</div>', unsafe_allow_html=True)
    st.caption("Unlocks demand elasticity — helps the AI understand how price-sensitive your buyers are.")
    c3, c4 = st.columns(2)
    with c3:
        old_price = st.number_input("Previous Price ($)", min_value=0.0, step=0.01)
    with c4:
        old_units = st.number_input("Units Sold at That Price", min_value=0, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label"><span class="dot"></span> Competitor Prices</div>', unsafe_allow_html=True)
    st.caption("Look up what similar products sell for on Etsy, Amazon, or wherever you compete.")
    c5, c6, c7 = st.columns(3)
    with c5:
        comp1 = st.number_input("Competitor 1 ($)", min_value=0.0, step=0.01)
    with c6:
        comp2 = st.number_input("Competitor 2 ($)", min_value=0.0, step=0.01)
    with c7:
        comp3 = st.number_input("Competitor 3 ($)", min_value=0.0, step=0.01)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label"><span class="dot"></span> Your Goal</div>', unsafe_allow_html=True)
    goal = st.selectbox("What are you optimizing for?", [
        "Maximize Profit",
        "Maximize Sales Volume",
        "Beat Competitors",
        "Stay Competitive While Protecting Margin"
    ])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button("✦ Generate My Pricing Recommendation")

with right:
    competitor_prices_live = [p for p in [comp1, comp2, comp3] if p > 0]
    live_comp = analyze_competitors(your_price, competitor_prices_live) if competitor_prices_live and your_price > 0 else None
    live_margin = get_margin(your_price, cost) if your_price > 0 and cost > 0 else None
    live_revenue = round(your_price * units_sold, 2) if your_price > 0 and units_sold > 0 else None

    st.markdown('<div class="section-label"><span class="dot"></span> Live Metrics</div>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">Profit Margin</div>
            <div class="metric-card-value highlight">{f"{live_margin}%" if live_margin is not None else "—"}</div>
            <div class="metric-card-sub">per unit sold</div>
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
    st.markdown('<div class="section-label"><span class="dot"></span> Price Comparison</div>', unsafe_allow_html=True)

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
            Enter your price + at least<br>
            one competitor to see the<br>
            comparison chart 📊
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
            <div class="rec-header">✦ AI Pricing Recommendation</div>
            <div class="rec-body">{recommendation}</div>
        </div>
        """, unsafe_allow_html=True)
