import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import GLOBAL_CSS

st.set_page_config(page_title="About", page_icon="📋", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── PAGE HEADER ───────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <p class="eyebrow">Project overview</p>
    <h1>About this project</h1>
    <p>E-Commerce Revenue Intelligence System — architecture, data, and methodology.</p>
</div>
""", unsafe_allow_html=True)

# ── PROBLEM STATEMENT ─────────────────────────────────────────────
st.markdown('<p class="eyebrow">The problem</p>', unsafe_allow_html=True)
st.markdown("### Why this project exists")
st.markdown("""
E-commerce businesses generate massive amounts of transactional data but struggle to
translate it into forward-looking revenue decisions. This system solves that by building
a complete intelligence pipeline that:
""")

p1, p2, p3, p4 = st.columns(4)
for col, icon, text in zip(
    [p1, p2, p3, p4],
    ["📈", "💬", "🗺️", "❓"],
    [
        "**Forecasts** next month's revenue using real historical patterns",
        "**Explains** revenue changes in plain English using AI",
        "**Visualises** KPIs, trends, and regional performance in Power BI",
        "**Answers** business questions like *'Why did revenue drop this month?'*",
    ]
):
    with col:
        st.markdown(f"""
        <div class="card" style="text-align:center">
            <div class="card-icon">{icon}</div>
            <p style="font-size:0.875rem">{text}</p>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

# ── ARCHITECTURE ──────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="eyebrow">System architecture</p>', unsafe_allow_html=True)
st.markdown("### Each stage feeds directly into the next")
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

steps = [
    ("📁", "Raw Data",    "Kaggle CSVs\n100K+ orders"),
    ("🗄️", "MySQL",       "6 tables\nAiven Cloud"),
    ("🐍", "Python ML",   "Linear Regression\nscikit-learn"),
    ("🤖", "AI Insights", "Llama 3.3\nGroq API"),
    ("📊", "Power BI",    "KPIs + Forecast\nRegional Map"),
]
p_cols     = st.columns([3,1,3,1,3,1,3,1,3])
step_cols  = [p_cols[i] for i in [0,2,4,6,8]]
arrow_cols = [p_cols[i] for i in [1,3,5,7]]

for col, (icon, title, desc) in zip(step_cols, steps):
    with col:
        st.markdown(f"""
        <div class="pipe-step">
            <span class="pipe-icon">{icon}</span>
            <h5>{title}</h5>
            <p>{desc.replace(chr(10),'<br>')}</p>
        </div>""", unsafe_allow_html=True)

for col in arrow_cols:
    with col:
        st.markdown(
            "<div style='text-align:center;padding-top:1.1rem;"
            "font-size:1.4rem;color:#CBD5E1'>→</div>",
            unsafe_allow_html=True
        )

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

# ── DATABASE SCHEMA ───────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="eyebrow">Data model</p>', unsafe_allow_html=True)
st.markdown("### Database schema — 6 tables")
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
left_tables = [
    ("👥", "customers",   "customer_id · city · state · zip_code · region"),
    ("📦", "orders",      "order_id · customer_id · status · purchase_date · delivered_date"),
    ("🏷️", "products",   "product_id · category · weight_g · price · photos_qty"),
]
right_tables = [
    ("💰", "sales",       "sale_id · order_id · product_id · unit_price · freight_value · quantity"),
    ("🔮", "predictions", "month · orders_count · predicted_revenue · actual_revenue"),
    ("🤖", "ai_insights", "month · question · insight_text · revenue_change · created_at"),
]

for col, tables in [(col1, left_tables), (col2, right_tables)]:
    with col:
        for icon, name, fields in tables:
            st.markdown(f"""
            <div class="schema-block">
                <h5>{icon} {name}</h5>
                <p>{fields}</p>
            </div>""", unsafe_allow_html=True)

# ── ML MODEL ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="eyebrow">Machine learning</p>', unsafe_allow_html=True)
st.markdown("### Linear Regression model")
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

ml1, ml2 = st.columns(2)
with ml1:
    st.markdown("**Input features**")
    st.markdown("""
| Feature | What it represents |
|---|---|
| `orders_count` | Total order volume |
| `unique_customers` | Website traffic proxy |
| `total_freight` | Logistics & operational spend |
| `avg_order_value` | Quality of demand |
""")

with ml2:
    st.markdown("**Why Linear Regression?**")
    st.markdown("""
    <div class="insight-box">
    <p>Revenue vs. order volume follows a largely linear relationship in practice.
    Linear Regression is fully interpretable — stakeholders can see exactly
    how much each feature contributes to revenue. That transparency is more
    valuable in a business context than a black-box model with marginally
    higher accuracy.</p>
    </div>
    """, unsafe_allow_html=True)

# ── DATASET ───────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="eyebrow">Dataset</p>', unsafe_allow_html=True)
st.markdown("### Brazilian E-Commerce Public Dataset — Olist")
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

d1, d2, d3, d4 = st.columns(4)
for col, val, label in zip(
    [d1, d2, d3, d4],
    ["99,441", "96,096", "32,951", "73"],
    ["real orders", "unique customers", "unique products", "product categories"]
):
    with col:
        st.markdown(f"""
        <div class="stat-box">
            <span class="stat-value">{val}</span>
            <span class="stat-label">{label}</span>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
st.markdown(
    "Covers payments, reviews, geolocation, and seller data · 2016–2018 · "
    "[View on Kaggle →](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)",
    unsafe_allow_html=False
)