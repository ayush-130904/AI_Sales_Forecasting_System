import streamlit as st
from PIL import Image
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import GLOBAL_CSS

st.set_page_config(page_title="Power BI Dashboard", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── PAGE HEADER ───────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <p class="eyebrow">Business Intelligence</p>
    <h1>Power BI Dashboard</h1>
    <p>Interactive dashboard built on the same MySQL database — KPI cards, forecast chart, and regional map.</p>
</div>
""", unsafe_allow_html=True)

# ── WHAT THE DASHBOARD SHOWS ──────────────────────────────────────
d1, d2, d3, d4 = st.columns(4)
for col, icon, title, desc in zip(
    [d1, d2, d3, d4],
    ["📊", "📈", "🗺️", "🤖"],
    ["KPI Cards", "Forecast Chart", "Regional Map", "AI Insights Table"],
    [
        "Total revenue, orders, avg order value, forecast accuracy",
        "Predicted vs actual revenue — month by month + 3-month outlook",
        "Revenue by Brazilian state, colour-coded by volume",
        "AI-generated answers pulled directly from the database",
    ]
):
    with col:
        st.markdown(f"""
        <div class="card" style="text-align:center">
            <div class="card-icon">{icon}</div>
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
st.markdown("---")

# ── TABS ──────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["Dashboard preview", "Live embed"])

with tab1:
    st.markdown(
        "<p style='color:#888;font-size:0.875rem;margin-bottom:1rem'>"
        "Built in Power BI Desktop · Connected to Aiven MySQL · "
        "Exported as screenshot below.</p>",
        unsafe_allow_html=True
    )

    screenshot_path = "assets/powerbi_screenshot.png"
    if os.path.exists(screenshot_path):
        img = Image.open(screenshot_path)
        st.image(img, use_column_width=True, caption="Power BI — Revenue Intelligence Dashboard")
    else:
        st.markdown("""
        <div class="insight-box" style="background:#FFFBEB;border-color:#FCD34D;border-left-color:#F59E0B">
        <p style="color:#92400E">
        <b>Screenshot not found.</b><br><br>
        To add it:<br>
        1. Open your Power BI Desktop file<br>
        2. Press <code>Windows + Shift + S</code> to screenshot<br>
        3. Save as <code>assets/powerbi_screenshot.png</code><br>
        4. Restart the app — it will appear here automatically.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown("#### Dashboard layout")
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            st.markdown("""
            <div class="card">
                <h4>📊 KPI row (top)</h4>
                <p>Total Revenue · Total Orders · Avg Order Value · Forecast Accuracy %</p>
            </div>""", unsafe_allow_html=True)
        with r1c2:
            st.markdown("""
            <div class="card">
                <h4>📈 Line chart</h4>
                <p>Predicted vs Actual Revenue · Month-by-month · 3-month forward forecast</p>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        r2c1, r2c2 = st.columns(2)
        with r2c1:
            st.markdown("""
            <div class="card">
                <h4>🗺️ Regional map</h4>
                <p>Revenue by Brazilian state · Colour-coded by volume · Hover for order count</p>
            </div>""", unsafe_allow_html=True)
        with r2c2:
            st.markdown("""
            <div class="card">
                <h4>🤖 AI Insights table</h4>
                <p>Month · Question · AI answer · Filterable by month and revenue change</p>
            </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown("#### Embed a live Power BI report")
    st.markdown("""
    <div class="insight-box">
    <p>
    <b>Step 1 — Publish from Power BI Desktop</b><br>
    File → Publish → Publish to Power BI → sign in with a free Microsoft account → My Workspace<br><br>
    <b>Step 2 — Get embed URL</b><br>
    app.powerbi.com → open your report → Share → Embed report → Website or portal → copy the iframe URL<br><br>
    <b>Step 3 — Paste it below</b>
    </p>
    </div>
    """, unsafe_allow_html=True)

    embed_url = st.text_input(
        "Power BI embed URL",
        placeholder="https://app.powerbi.com/reportEmbed?reportId=...",
        label_visibility="visible"
    )

    if embed_url:
        st.components.v1.iframe(embed_url, height=620, scrolling=True)
    else:
        st.info("Paste your embed URL above to display the live interactive dashboard.")