import streamlit as st
from style import GLOBAL_CSS

st.set_page_config(
    page_title="E-Commerce Revenue Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 3rem 0 2rem 0; border-bottom: 1px solid #EBEBEB; margin-bottom: 2.5rem;">
    <p class="eyebrow">Portfolio Project · Data Science & ML</p>
    <h1 style="font-size:2.8rem; margin: 0.25rem 0 0.75rem 0;">
        E-Commerce Revenue Intelligence
    </h1>
    <p style="font-size:1.05rem; color:#555; max-width:600px; margin:0;">
        An end-to-end ML system that forecasts monthly revenue, explains
        business changes with AI, and visualises performance in Power BI —
        built on 100,000+ real Brazilian e-commerce orders.
    </p>
</div>
""", unsafe_allow_html=True)

# ── STATS ROW ─────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
stats = [
    ("100K+", "Real orders"),
    ("6",     "Database tables"),
    ("91%+",  "Model accuracy"),
    ("Llama 3.3", "AI engine"),
]
for col, (val, label) in zip([c1, c2, c3, c4], stats):
    with col:
        st.markdown(f"""
        <div class="stat-box">
            <span class="stat-value">{val}</span>
            <span class="stat-label">{label}</span>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)

# ── FEATURE CARDS ─────────────────────────────────────────────────
st.markdown('<p class="eyebrow">What\'s inside</p>', unsafe_allow_html=True)
st.markdown("### Explore the project")
st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

cards = [
    ("📋", "About",          "Project architecture, database schema, ML model details, and dataset overview."),
    ("🔮", "Revenue Predictor", "Input next month's business metrics. Get a live forecast from the trained model."),
    ("🤖", "AI Insights",    "Ask questions in plain English. Llama 3.3 analyses your real revenue data."),
    ("🗃️", "Data Explorer",  "Browse all six live database tables — orders, customers, products, and more."),
    ("📊", "Power BI",       "Full dashboard with KPI cards, forecast chart, and regional sales map."),
]
cols = st.columns(5)
for col, (icon, title, desc) in zip(cols, cards):
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="card-icon">{icon}</div>
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)

# ── TECH STACK ────────────────────────────────────────────────────
st.markdown('<p class="eyebrow">Tech stack</p>', unsafe_allow_html=True)
badges = ["Python", "MySQL", "scikit-learn", "Pandas", "Groq Llama 3.3",
          "Streamlit", "Power BI", "Aiven Cloud", "Plotly", "SQLAlchemy"]
st.markdown(
    "".join(f'<span class="badge">{b}</span>' for b in badges),
    unsafe_allow_html=True
)

# ── PIPELINE SUMMARY ──────────────────────────────────────────────
st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)
st.markdown('<p class="eyebrow">Pipeline</p>', unsafe_allow_html=True)
st.markdown("### How data flows through the system")
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

steps = [
    ("📁", "CSV Data",    "Kaggle Olist\n100K+ orders"),
    ("🗄️", "MySQL",       "6 tables\nAiven Cloud"),
    ("🐍", "Python ML",   "Linear Regression\nscikit-learn"),
    ("🤖", "AI Insights", "Llama 3.3\nGroq API"),
    ("📊", "Power BI",    "KPIs + forecast\nregional map"),
]
p_cols = st.columns([3,1,3,1,3,1,3,1,3])
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

# ── FOOTER ────────────────────────────────────────────────────────
st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)
st.markdown(
    "<hr><p style='color:#BBB;font-size:0.8rem;text-align:center;margin:0'>"
    "Built by Ayush Salunkhe &nbsp;·&nbsp; "
    "Dataset: Brazilian E-Commerce (Olist) · Kaggle &nbsp;·&nbsp; "
    "Mumbai University, Computer Engineering"
    "</p>",
    unsafe_allow_html=True
)
