import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import GLOBAL_CSS
from utils.db import run_query

st.set_page_config(page_title="Data Explorer", page_icon="🗃️", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── PAGE HEADER ───────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <p class="eyebrow">Live database</p>
    <h1>Data Explorer</h1>
    <p>Browse all six tables from the live MySQL database — pulled directly from Aiven Cloud.</p>
</div>
""", unsafe_allow_html=True)

# ── DATABASE SUMMARY STATS ────────────────────────────────────────
try:
    stats = run_query("""
        SELECT
            (SELECT COUNT(*) FROM customers) AS customers,
            (SELECT COUNT(*) FROM orders)    AS orders,
            (SELECT COUNT(*) FROM products)  AS products,
            (SELECT COUNT(*) FROM sales)     AS sales_rows,
            (SELECT ROUND(SUM(unit_price * quantity),0) FROM sales) AS total_revenue
    """).iloc[0]

    s1, s2, s3, s4, s5 = st.columns(5)
    for col, val, label in zip(
        [s1, s2, s3, s4, s5],
        [f"{int(stats['customers']):,}", f"{int(stats['orders']):,}",
         f"{int(stats['products']):,}", f"{int(stats['sales_rows']):,}",
         f"R${int(stats['total_revenue']):,}"],
        ["Customers", "Orders", "Products", "Sales records", "Total revenue"]
    ):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <span class="stat-value" style="font-size:1.5rem">{val}</span>
                <span class="stat-label">{label}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Stats unavailable: {e}")

st.markdown("---")

# ── TABLE SELECTOR ────────────────────────────────────────────────
table_options = {
    "📦 Orders":       ("orders",      "ORDER BY purchase_date DESC"),
    "👥 Customers":    ("customers",   "ORDER BY customer_id"),
    "🏷️ Products":    ("products",    "ORDER BY price DESC"),
    "💰 Sales":        ("sales",       "ORDER BY sale_id DESC"),
    "🔮 Predictions":  ("predictions", "ORDER BY month DESC"),
    "🤖 AI Insights":  ("ai_insights", "ORDER BY created_at DESC"),
}

sel_col, rows_col, btn_col = st.columns([3, 1, 1])
with sel_col:
    selected_label = st.selectbox("Table", list(table_options.keys()), label_visibility="collapsed")
with rows_col:
    row_limit = st.selectbox("Rows", [50, 100, 250, 500], label_visibility="collapsed")
with btn_col:
    load_btn = st.button("Load table →", type="primary", use_container_width=True)

table_name, order_clause = table_options[selected_label]

# ── LOAD TABLE ────────────────────────────────────────────────────
if load_btn or True:
    with st.spinner(f"Loading {table_name}..."):
        try:
            df = run_query(f"SELECT * FROM {table_name} {order_clause} LIMIT {row_limit}")

            # Summary metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Rows loaded",  f"{len(df):,}")
            m2.metric("Columns",      f"{len(df.columns)}")
            if table_name == 'sales':
                total = (df['unit_price'] * df['quantity']).sum()
                m3.metric("Revenue in view", f"R${total:,.0f}")
            elif table_name == 'predictions':
                filled = df['actual_revenue'].notna().sum()
                m3.metric("Months with actual data", str(filled))
            else:
                m3.metric("Table", table_name)

            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

            # Search
            search = st.text_input(
                "Search", placeholder="Filter rows across all columns...",
                label_visibility="collapsed"
            )
            if search:
                mask = df.astype(str).apply(
                    lambda col: col.str.contains(search, case=False)
                ).any(axis=1)
                df = df[mask]
                st.caption(f"{len(df)} matching rows")

            st.dataframe(df, use_container_width=True, hide_index=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download as CSV",
                data=csv,
                file_name=f"{table_name}.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Could not load table: {e}")