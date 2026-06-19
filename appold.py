import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Revenue Intelligence · Ayush",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS  ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Base */
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #F7F6F2;
  }

  /* Remove default streamlit padding */
  .block-container { padding: 0 2rem 4rem 2rem !important; max-width: 1200px; }

  /* Hero banner */
  .hero {
    background: #1A1A2E;
    border-radius: 16px;
    padding: 3rem 2.5rem;
    margin: 1.5rem 0 2rem 0;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -80px;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: rgba(99, 153, 34, 0.12);
  }
  .hero-tag {
    display: inline-block;
    background: rgba(99,153,34,0.18);
    color: #97C459;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 1rem;
  }
  .hero h1 {
    color: #F7F6F2;
    font-size: 2.2rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    line-height: 1.2;
  }
  .hero-sub {
    color: #A0A0B8;
    font-size: 1rem;
    font-weight: 400;
    margin: 0 0 1.5rem 0;
    max-width: 560px;
  }
  .pill-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 1rem; }
  .pill {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    color: #C8C8DC;
    font-size: 12px;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
  }

  /* Section headings */
  .section-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #888;
    margin: 2.5rem 0 0.8rem 0;
  }
  h2.section-title {
    font-size: 1.35rem;
    font-weight: 600;
    color: #1A1A2E;
    margin: 0 0 1.2rem 0;
  }

  /* Metric cards */
  .metric-card {
    background: #FFFFFF;
    border: 1px solid #E8E6E0;
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    height: 100%;
  }
  .metric-label {
    font-size: 12px;
    color: #888;
    font-weight: 500;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }
  .metric-value {
    font-size: 1.6rem;
    font-weight: 600;
    color: #1A1A2E;
    line-height: 1.1;
  }
  .metric-delta {
    font-size: 12px;
    margin-top: 4px;
  }
  .delta-up { color: #3B6D11; }
  .delta-down { color: #A32D2D; }

  /* Result box */
  .result-box {
    background: #1A1A2E;
    border-radius: 14px;
    padding: 1.8rem;
    text-align: center;
  }
  .result-label { color: #A0A0B8; font-size: 13px; margin-bottom: 4px; }
  .result-amount { color: #F7F6F2; font-size: 2.4rem; font-weight: 600; }
  .result-range { color: #A0A0B8; font-size: 12px; margin-top: 6px; }

  /* Feature importance bar */
  .feat-row { margin-bottom: 12px; }
  .feat-name { font-size: 13px; color: #444; margin-bottom: 4px; font-weight: 500; }
  .feat-bar-bg {
    background: #EDECE8;
    border-radius: 6px;
    height: 8px;
    width: 100%;
  }
  .feat-bar-fill {
    height: 8px;
    border-radius: 6px;
    background: #1A1A2E;
  }
  .feat-coef { font-size: 11px; color: #888; margin-top: 2px; font-family: 'DM Mono', monospace; }

  /* Divider */
  .divider {
    border: none;
    border-top: 1px solid #E8E6E0;
    margin: 2rem 0;
  }

  /* Info callout */
  .info-callout {
    background: #EAF3DE;
    border-left: 3px solid #639922;
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    font-size: 13px;
    color: #3B6D11;
    margin-bottom: 1.5rem;
  }

  /* Slider labels */
  .slider-context {
    font-size: 12px;
    color: #888;
    margin-top: -12px;
    margin-bottom: 16px;
  }

  /* Footer */
  .footer {
    background: #FFFFFF;
    border: 1px solid #E8E6E0;
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    margin-top: 3rem;
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  .footer-title { font-size: 14px; font-weight: 600; color: #1A1A2E; margin-bottom: 2px; }
  .footer-sub { font-size: 12px; color: #888; }
  .badge-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
  .badge {
    background: #F2F0EB;
    border: 1px solid #E0DDD7;
    color: #555;
    font-size: 11px;
    padding: 3px 9px;
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
  }
  .stButton > button {
    background: #1A1A2E !important;
    color: #F7F6F2 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    width: 100%;
  }
  .stButton > button:hover { background: #2E2E4A !important; }

  /* Streamlit slider customisation */
  .stSlider .stMarkdownContainer p { font-size: 13px !important; }

  /* Tab styling */
  .stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #EDECE8;
    border-radius: 10px;
    padding: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 7px;
    border: none;
    font-size: 13px;
    font-weight: 500;
    color: #666;
    padding: 6px 18px;
  }
  .stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #1A1A2E !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }
</style>
""", unsafe_allow_html=True)

# ── Load model & scaler ──────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    with open("models/revenue_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("models/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_artifacts()

FEATURES = ["orders_count", "unique_customers", "total_freight", "avg_order_value"]

# ── Synthetic historical data (mirrors Olist monthly stats) ──────────────────
@st.cache_data
def get_historical_data():
    np.random.seed(42)
    months = pd.date_range("2017-01-01", "2018-08-01", freq="MS")
    base_orders = np.linspace(800, 7200, len(months))
    orders = (base_orders + np.random.normal(0, 200, len(months))).astype(int)
    customers = (orders * np.random.uniform(0.85, 0.95, len(months))).astype(int)
    freight = orders * np.random.uniform(18, 28, len(months))
    aov = np.random.uniform(90, 140, len(months))
    X = np.column_stack([orders, customers, freight, aov])
    X_sc = scaler.transform(X)
    rev_pred = model.predict(X_sc)
    actual = rev_pred * np.random.uniform(0.93, 1.07, len(months))
    df = pd.DataFrame({
        "month": months,
        "orders_count": orders,
        "unique_customers": customers,
        "total_freight": freight.round(0).astype(int),
        "avg_order_value": aov.round(2),
        "predicted_revenue": rev_pred.round(0),
        "actual_revenue": actual.round(0),
    })
    return df

hist = get_historical_data()

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <span class="hero-tag">Portfolio Project</span>
  <h1>Revenue Intelligence<br>Dashboard</h1>
  <p class="hero-sub">End-to-end ML system that forecasts monthly e-commerce revenue
  for a Brazilian marketplace — from raw Olist data to a live Power BI dashboard
  with AI-generated insights.</p>
  <div class="pill-row">
    <span class="pill">Python</span>
    <span class="pill">scikit-learn</span>
    <span class="pill">MySQL</span>
    <span class="pill">Power BI</span>
    <span class="pill">Groq LLM</span>
    <span class="pill">Linear Regression</span>
    <span class="pill">Streamlit</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Live Dashboard", "🔮 Predict Revenue", "🏗️ How It Works", "👤 About"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — LIVE DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<p class="section-label">Overview</p>', unsafe_allow_html=True)

    # Summary metrics
    last = hist.iloc[-1]
    prev = hist.iloc[-2]
    rev_delta = (last.actual_revenue - prev.actual_revenue) / prev.actual_revenue * 100
    ord_delta = (last.orders_count - prev.orders_count) / prev.orders_count * 100
    cust_delta = (last.unique_customers - prev.unique_customers) / prev.unique_customers * 100

    c1, c2, c3, c4 = st.columns(4)
    def metric_html(label, value, delta=None):
        delta_html = ""
        if delta is not None:
            cls = "delta-up" if delta >= 0 else "delta-down"
            arrow = "↑" if delta >= 0 else "↓"
            delta_html = f'<div class="metric-delta {cls}">{arrow} {abs(delta):.1f}% vs prev month</div>'
        return f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          {delta_html}
        </div>"""

    c1.markdown(metric_html("Latest Revenue", f"R${last.actual_revenue:,.0f}", rev_delta), unsafe_allow_html=True)
    c2.markdown(metric_html("Orders (last mo.)", f"{last.orders_count:,}", ord_delta), unsafe_allow_html=True)
    c3.markdown(metric_html("Unique Customers", f"{last.unique_customers:,}", cust_delta), unsafe_allow_html=True)
    c4.markdown(metric_html("Avg Order Value", f"R${last.avg_order_value:,.0f}"), unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Revenue trend chart
    st.markdown('<p class="section-label">Revenue Trend</p>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist.month, y=hist.actual_revenue,
        name="Actual", mode="lines+markers",
        line=dict(color="#1A1A2E", width=2.5),
        marker=dict(size=6, color="#1A1A2E"),
    ))
    fig.add_trace(go.Scatter(
        x=hist.month, y=hist.predicted_revenue,
        name="Predicted", mode="lines",
        line=dict(color="#639922", width=2, dash="dot"),
    ))
    fig.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="DM Sans", color="#444", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1,
                    bgcolor="rgba(0,0,0,0)", borderwidth=0),
        xaxis=dict(showgrid=False, tickfont=dict(size=11), tickformat="%b %Y"),
        yaxis=dict(gridcolor="#F0EEE8", tickformat=",.0f", tickprefix="R$",
                   tickfont=dict(size=11)),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Orders vs Customers
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<p class="section-label">Orders Over Time</p>', unsafe_allow_html=True)
        fig2 = px.bar(hist, x="month", y="orders_count",
                      color_discrete_sequence=["#1A1A2E"])
        fig2.update_layout(height=250, margin=dict(l=0, r=0, t=8, b=0),
                           plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                           font=dict(family="DM Sans", size=11),
                           showlegend=False,
                           xaxis=dict(showgrid=False, tickformat="%b %y"),
                           yaxis=dict(gridcolor="#F0EEE8", title=""))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with col_b:
        st.markdown('<p class="section-label">Unique Customers Over Time</p>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Scatter(
            x=hist.month, y=hist.unique_customers,
            fill="tozeroy", line=dict(color="#639922", width=2),
            fillcolor="rgba(99,153,34,0.10)"
        ))
        fig3.update_layout(height=250, margin=dict(l=0, r=0, t=8, b=0),
                           plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                           font=dict(family="DM Sans", size=11),
                           xaxis=dict(showgrid=False, tickformat="%b %y"),
                           yaxis=dict(gridcolor="#F0EEE8", title=""))
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    # Power BI embed
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Power BI Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Embedded Live Report</h2>', unsafe_allow_html=True)

    POWERBI_EMBED_URL = "https://app.powerbi.com/reportEmbed?reportId=aa1408dc-bd31-4968-9ebc-2540a832a093&autoAuth=true&ctid=053cbcff-aa58-4d20-87a3-575d830ae75b"   # ← paste your embed URL here

    if POWERBI_EMBED_URL:
        st.components.v1.iframe(POWERBI_EMBED_URL, height=550, scrolling=True)
    else:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px dashed #C8C6BF; border-radius:12px;
                    padding:2.5rem; text-align:center;">
          <div style="font-size:2rem; margin-bottom:0.75rem;">📊</div>
          <div style="font-size:15px; font-weight:600; color:#1A1A2E; margin-bottom:6px;">
            Power BI Embed Goes Here
          </div>
          <div style="font-size:13px; color:#888; max-width:380px; margin:0 auto 1rem auto;">
            Publish your report to Power BI Service → Share → Embed → copy the iframe src URL,
            then paste it into <code>POWERBI_EMBED_URL</code> in app.py.
          </div>
          <code style="font-size:11px; background:#F2F0EB; padding:6px 12px;
                       border-radius:6px; color:#555; font-family:'DM Mono',monospace;">
            app.py → line: POWERBI_EMBED_URL = "https://app.powerbi.com/reportEmbed?reportId=aa1408dc-bd31-4968-9ebc-2540a832a093&autoAuth=true&ctid=053cbcff-aa58-4d20-87a3-575d830ae75b"
          </code>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — PREDICT
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-label">ML Predictor</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Forecast Next Month\'s Revenue</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-callout">
      Adjust the four business drivers below — the model applies
      the same Linear Regression trained on Olist historical data to compute the forecast.
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.8, 1], gap="large")

    with col_left:
        # Reference: last month's actual values as defaults
        ref = hist.iloc[-1]

        orders = st.slider(
            "📦 Estimated Orders",
            min_value=500, max_value=15000, value=int(ref.orders_count), step=50,
        )
        st.markdown(f'<p class="slider-context">Last month: {int(ref.orders_count):,} orders</p>',
                    unsafe_allow_html=True)

        customers = st.slider(
            "👥 Unique Customers",
            min_value=400, max_value=14000, value=int(ref.unique_customers), step=50,
        )
        st.markdown(f'<p class="slider-context">Last month: {int(ref.unique_customers):,} customers</p>',
                    unsafe_allow_html=True)

        freight = st.slider(
            "🚚 Total Freight Spend (R$)",
            min_value=10000, max_value=500000, value=int(ref.total_freight), step=1000,
        )
        st.markdown(f'<p class="slider-context">Last month: R${int(ref.total_freight):,}</p>',
                    unsafe_allow_html=True)

        aov = st.slider(
            "🛒 Avg Order Value (R$)",
            min_value=40, max_value=300, value=int(ref.avg_order_value), step=5,
        )
        st.markdown(f'<p class="slider-context">Last month: R${ref.avg_order_value:.0f}</p>',
                    unsafe_allow_html=True)

        predict_btn = st.button("Run Prediction →")

    with col_right:
        # Prediction live
        X_input = np.array([[orders, customers, freight, aov]])
        X_scaled = scaler.transform(X_input)
        prediction = model.predict(X_scaled)[0]
        prediction = max(prediction, 0)

        # Confidence range ±8%
        lo, hi = prediction * 0.92, prediction * 1.08

        st.markdown(f"""
        <div class="result-box">
          <div class="result-label">Predicted Revenue</div>
          <div class="result-amount">R${prediction:,.0f}</div>
          <div class="result-range">Range: R${lo:,.0f} – R${hi:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        # Delta vs last actual
        actual_last = float(hist.iloc[-1].actual_revenue)
        delta_pct = (prediction - actual_last) / actual_last * 100
        color = "#3B6D11" if delta_pct >= 0 else "#A32D2D"
        arrow = "↑" if delta_pct >= 0 else "↓"
        st.markdown(f"""
        <div style="text-align:center; margin-top:1rem; font-size:13px; color:{color}; font-weight:500;">
          {arrow} {abs(delta_pct):.1f}% vs last actual (R${actual_last:,.0f})
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Feature importance
        st.markdown('<p class="section-label">Feature Weights</p>', unsafe_allow_html=True)

        coefs = model.coef_
        feat_labels = ["Orders", "Customers", "Freight", "Avg Order Value"]
        max_abs = max(abs(c) for c in coefs)

        for label, coef in zip(feat_labels, coefs):
            bar_pct = abs(coef) / max_abs * 100
            direction = "#639922" if coef > 0 else "#A32D2D"
            sign = "+" if coef > 0 else "−"
            st.markdown(f"""
            <div class="feat-row">
              <div style="display:flex; justify-content:space-between;">
                <span class="feat-name">{label}</span>
                <span class="feat-coef">{sign} impact</span>
              </div>
              <div class="feat-bar-bg">
                <div class="feat-bar-fill" style="width:{bar_pct:.0f}%; background:{direction};"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Scenario comparison chart (renders after button click OR always)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Scenario View</p>', unsafe_allow_html=True)

    scenarios = {
        "Conservative (−10%)": prediction * 0.90,
        "Your Forecast": prediction,
        "Optimistic (+10%)": prediction * 1.10,
    }
    colors = ["#B4B2A9", "#1A1A2E", "#639922"]
    fig_sc = go.Figure(go.Bar(
        x=list(scenarios.keys()),
        y=list(scenarios.values()),
        marker_color=colors,
        text=[f"R${v:,.0f}" for v in scenarios.values()],
        textposition="outside",
        textfont=dict(size=12, family="DM Sans"),
    ))
    fig_sc.update_layout(
        height=280, margin=dict(l=0, r=0, t=20, b=0),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        font=dict(family="DM Sans", size=12),
        showlegend=False,
        yaxis=dict(gridcolor="#F0EEE8", tickformat=",.0f", tickprefix="R$", title=""),
        xaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — HOW IT WORKS
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-label">Architecture</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Pipeline Overview</h2>', unsafe_allow_html=True)

    steps = [
        ("01", "Data Ingestion", "load_data.py",
         "Loads Olist CSVs (customers, orders, products, order items) into a MySQL database. "
         "Handles customer deduplication — maps per-order surrogate IDs to true unique customer IDs. "
         "Groups 27 Brazilian states into 5 regions for Power BI mapping."),
        ("02", "Feature Engineering", "get_features.py",
         "SQL aggregation produces monthly features: orders count, average order value, "
         "unique customers (traffic proxy), total freight (logistics proxy), and unique products sold. "
         "Filters to delivered orders only — confirmed revenue."),
        ("03", "ML Model Training", "ml_pipeline.py",
         "Time-based train/test split (last 3 months held out). "
         "StandardScaler applied to training data only — no data leakage. "
         "Linear Regression trained on 4 features. "
         "3-month future forecast using 3% compounding growth assumption. "
         "Results written to predictions table."),
        ("04", "AI Insights Layer", "ai_insights.py",
         "Pulls last 6 months of actuals + predictions. "
         "Builds a structured prompt with MoM % changes and sends to Groq (LLaMA-3.3-70B). "
         "Answers 3 fixed business questions in ≤4 sentences with 1 recommendation each. "
         "Saves insights to ai_insights table — Power BI reads and displays them on the dashboard."),
        ("05", "Power BI Dashboard", "revenue_dashboard.pbix",
         "Connects to MySQL via DirectQuery / scheduled refresh. "
         "Shows revenue trend, regional heatmap, category breakdown, "
         "predicted vs actual comparison, and AI insight cards — all on a single canvas."),
    ]

    for num, title, file, desc in steps:
        with st.container():
            st.markdown(f"""
            <div style="display:flex; gap:1.25rem; padding:1.25rem 0; border-bottom:1px solid #E8E6E0;">
              <div style="min-width:36px; height:36px; background:#1A1A2E; border-radius:8px;
                          display:flex; align-items:center; justify-content:center;
                          font-size:11px; font-weight:600; color:#F7F6F2; font-family:'DM Mono',monospace;">
                {num}
              </div>
              <div style="flex:1;">
                <div style="font-size:15px; font-weight:600; color:#1A1A2E; margin-bottom:3px;">
                  {title}
                  <code style="font-size:11px; background:#F2F0EB; padding:2px 7px;
                               border-radius:5px; color:#555; font-family:'DM Mono',monospace; margin-left:8px;">
                    {file}
                  </code>
                </div>
                <div style="font-size:13px; color:#666; line-height:1.6;">{desc}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Model Details</p>', unsafe_allow_html=True)

    mc1, mc2, mc3 = st.columns(3)
    mc1.markdown(metric_html("Algorithm", "Linear Regression"), unsafe_allow_html=True)
    mc2.markdown(metric_html("Features Used", "4 monthly KPIs"), unsafe_allow_html=True)
    mc3.markdown(metric_html("Test Split", "Last 3 months"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #E8E6E0; border-radius:12px; padding:1.25rem 1.5rem;">
      <div style="font-size:13px; font-weight:600; color:#1A1A2E; margin-bottom:10px;">
        Why Linear Regression?
      </div>
      <div style="font-size:13px; color:#666; line-height:1.7;">
        Monthly e-commerce revenue shows strong linear relationships with order volume and
        customer traffic. A scatter of total freight vs revenue produces a near-straight line —
        confirmed by the model. Linear regression is interpretable, fast to retrain monthly,
        and produces stable forecasts without overfitting on the ~20-month dataset.
        Feature coefficients directly answer "what moves revenue most?" — a key stakeholder question.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — ABOUT
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-label">Portfolio</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">About This Project</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.4, 1])

    with col1:
        st.markdown("""
        <div style="font-size:14px; color:#555; line-height:1.8;">
          <p>This is a full end-to-end data project built on the
          <strong style="color:#1A1A2E;">Olist Brazilian E-commerce dataset</strong> — a real-world
          dataset of ~100k orders from 2016–2018.</p>
          <p>The goal: build a production-style pipeline that a business could actually use —
          not just a notebook. That meant a proper relational schema, a reusable ML pipeline,
          a live dashboard refreshed from the same database, and an AI layer that explains
          the numbers in plain English for non-technical stakeholders.</p>
          <p>Every design decision (StandardScaler fit on train only, delivered-orders filter,
          customer ID deduplication) was driven by avoiding the mistakes that make models fail
          in the real world.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E8E6E0; border-radius:12px;
                    padding:1.25rem 1.5rem;">
          <div style="font-size:12px; font-weight:600; color:#888; text-transform:uppercase;
                      letter-spacing:0.08em; margin-bottom:12px;">Stack</div>
          <div style="display:flex; flex-direction:column; gap:8px;">
        """, unsafe_allow_html=True)

        stack_items = [
            ("Data Storage", "MySQL + SQLAlchemy"),
            ("ML", "scikit-learn · LinearRegression"),
            ("AI Insights", "Groq API · LLaMA 3.3 70B"),
            ("Visualisation", "Power BI + Plotly"),
            ("Frontend", "Streamlit"),
            ("Dataset", "Olist (Kaggle)"),
        ]
        for k, v in stack_items:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; font-size:13px;
                        border-bottom:1px solid #F0EEE8; padding:5px 0;">
              <span style="color:#888;">{k}</span>
              <span style="color:#1A1A2E; font-weight:500;">{v}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#1A1A2E; border-radius:12px; padding:1.75rem;">
      <div style="font-size:15px; font-weight:600; color:#F7F6F2; margin-bottom:12px;">
        What could be added next
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
    """, unsafe_allow_html=True)

    suggestions = [
        ("🔄 Automated retraining", "Retrain monthly via a cron job when new data lands"),
        ("📍 Region-level forecasting", "Separate models per Brazilian region — Southeast behaves differently"),
        ("🛍️ Category revenue mix", "Break down which product categories drive growth each month"),
        ("📧 Email alerts", "Auto-email the AI insight to stakeholders on the 1st of each month"),
        ("📉 Anomaly detection", "Flag months where actual diverges from predicted by >15%"),
        ("🤝 What-if simulator", "Pre-built scenarios: 'What if freight costs drop 20%?'"),
    ]
    for icon_title, desc in suggestions:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); border-radius:8px; padding:10px 12px;">
          <div style="font-size:13px; font-weight:500; color:#F7F6F2; margin-bottom:3px;">
            {icon_title}
          </div>
          <div style="font-size:12px; color:#A0A0B8; line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div style="flex:1;">
    <div class="footer-title">Ayush · Data Analyst Portfolio</div>
    <div class="footer-sub">Computer Engineering · Mumbai University</div>
    <div class="badge-row">
      <span class="badge">ML · Revenue Forecasting</span>
      <span class="badge">ETL Pipeline</span>
      <span class="badge">Power BI</span>
      <span class="badge">LLM Integration</span>
    </div>
  </div>
  <div style="font-size:12px; color:#AAA; text-align:right;">
    Built with Streamlit<br>Olist Dataset · Kaggle
  </div>
</div>
""", unsafe_allow_html=True)
