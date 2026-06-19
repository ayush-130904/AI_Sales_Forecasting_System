import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import GLOBAL_CSS
from utils.model import load_model
from utils.db import run_query

st.set_page_config(page_title="Revenue Predictor", page_icon="🔮", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── PAGE HEADER ───────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <p class="eyebrow">Machine learning</p>
    <h1>Revenue Predictor</h1>
    <p>Enter expected business metrics for next month to get a revenue forecast from the trained model.</p>
</div>
""", unsafe_allow_html=True)

model, scaler = load_model()

# ── LOAD LAST MONTH AS DEFAULTS ───────────────────────────────────
try:
    last = run_query("""
        SELECT orders_count, unique_customers, total_freight, actual_revenue
        FROM predictions
        WHERE actual_revenue IS NOT NULL
        ORDER BY month DESC LIMIT 1
    """)
    last_orders    = int(last['orders_count'].iloc[0])
    last_customers = int(last['unique_customers'].iloc[0])
    last_freight   = float(last['total_freight'].iloc[0])
    last_revenue   = float(last['actual_revenue'].iloc[0])
    has_last = True
except:
    last_orders, last_customers, last_freight, last_revenue = 5000, 4000, 30000.0, 0
    has_last = False

if has_last:
    st.markdown(f"""
    <div class="hint-bar">
        📌 <b>Last known month —</b>
        Orders: {last_orders:,} &nbsp;·&nbsp;
        Customers: {last_customers:,} &nbsp;·&nbsp;
        Freight: R${last_freight:,.0f} &nbsp;·&nbsp;
        Revenue: R${last_revenue:,.0f}
    </div>""", unsafe_allow_html=True)

# ── INPUTS + REFERENCE TABLE ──────────────────────────────────────
col_in, col_ref = st.columns([1, 1], gap="large")

with col_in:
    st.markdown("#### Enter next month's metrics")
    orders_count = st.number_input(
        "Expected orders",
        min_value=100, max_value=50000,
        value=last_orders, step=100
    )
    unique_customers = st.number_input(
        "Expected unique customers",
        min_value=100, max_value=50000,
        value=last_customers, step=100
    )
    total_freight = st.number_input(
        "Expected total freight spend (R$)",
        min_value=1000.0, max_value=500000.0,
        value=last_freight, step=500.0
    )
    avg_order_value = st.number_input(
        "Expected avg order value (R$)",
        min_value=10.0, max_value=1000.0,
        value=120.0, step=5.0
    )

with col_ref:
    st.markdown("#### How each input affects revenue")
    st.markdown("""
| Input | Effect on revenue |
|---|---|
| Orders count | Strongest positive driver |
| Unique customers | Reflects demand breadth |
| Freight spend | Proxy for operational activity |
| Avg order value | Higher spend = more revenue |
""")
    st.markdown(
        "<p style='font-size:0.82rem;color:#999;margin-top:0.5rem'>"
        "Model trained on 24 months of real Brazilian e-commerce data.</p>",
        unsafe_allow_html=True
    )

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
run = st.button("Generate forecast →", type="primary", use_container_width=True)

# ── RESULT ────────────────────────────────────────────────────────
if run:
    features        = np.array([[orders_count, unique_customers, total_freight, avg_order_value]])
    features_scaled = scaler.transform(features)
    prediction      = model.predict(features_scaled)[0]
    change          = ((prediction - last_revenue) / last_revenue * 100) if last_revenue else 0
    arrow           = "↑" if change >= 0 else "↓"

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    res_col, chart_col = st.columns([1, 1], gap="large")

    with res_col:
        st.markdown(f"""
        <div class="result-box">
            <p class="result-label">Predicted revenue — next month</p>
            <p class="result-value">R${prediction:,.0f}</p>
            <p class="result-delta">{arrow} {abs(change):.1f}% vs last month</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        if abs(change) < 5:
            st.success("Stable forecast — within 5% of last month.")
        elif abs(change) < 15:
            st.warning("Moderate change predicted — review your inputs.")
        else:
            st.error("Large variance predicted — verify your assumptions.")

    with chart_col:
        try:
            hist = run_query("""
                SELECT month, actual_revenue FROM predictions
                WHERE actual_revenue IS NOT NULL
                ORDER BY month DESC LIMIT 5
            """)
            hist = hist.sort_values('month')
            hist['month'] = pd.to_datetime(hist['month'])
            next_month = hist['month'].max() + pd.DateOffset(months=1)

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=hist['month'].dt.strftime('%b %Y'),
                y=hist['actual_revenue'],
                name='Actual',
                marker_color='#DBEAFE',
                marker_line_color='#2563EB',
                marker_line_width=1.5
            ))
            fig.add_trace(go.Scatter(
                x=[next_month.strftime('%b %Y')],
                y=[prediction],
                mode='markers',
                name='Your forecast',
                marker=dict(color='#2563EB', size=14, symbol='diamond')
            ))
            fig.update_layout(
                title=dict(text='Last 5 months + your forecast', font_size=13),
                xaxis_title=None,
                yaxis_title='Revenue (R$)',
                hovermode='x unified',
                legend=dict(orientation='h', y=1.12),
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=0, r=0, t=40, b=0),
                font=dict(family='Inter', size=11, color='#555')
            )
            fig.update_xaxes(showgrid=False, linecolor='#EBEBEB')
            fig.update_yaxes(gridcolor='#F5F5F5', linecolor='#EBEBEB')
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.info("Chart unavailable — DB connection issue.")