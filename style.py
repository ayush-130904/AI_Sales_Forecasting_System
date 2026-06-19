GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

/* ── Reset & Base ─────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 2rem;
    max-width: 1100px;
}

/* Hide streamlit branding — never touch <header> */
#MainMenu { display: none !important; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Sidebar — ALWAYS VISIBLE, no collapse ────────────── */
[data-testid="stSidebar"] {
    background: #FAFAFA;
    border-right: 1px solid #EBEBEB;
    min-width: 290px !important;
    max-width: 290px !important;
    width: 290px !important;
    transform: none !important;
    visibility: visible !important;
    position: relative !important;
}
/* Remove the collapse/expand arrow completely */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
button[kind="header"] {
    display: none !important;
}
/* Push main content over to make room since sidebar can't collapse */
section[data-testid="stMain"],
.main {
    margin-left: 0 !important;
}
[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }
[data-testid="stSidebarNav"] a {
    font-size: 0.875rem;
    font-weight: 500;
    color: #555 !important;
    border-radius: 6px;
    padding: 0.4rem 0.75rem;
}
[data-testid="stSidebarNav"] a:hover { background: #F0F0F0; color: #111 !important; }
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: #EEF4FF;
    color: #2563EB !important;
}

/* ── Sidebar section label ────────────────────────────── */
.sidebar-section {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #AAA;
    margin: 1.25rem 0 0.5rem 0;
    padding: 0 0.25rem;
}

/* ── Typography ───────────────────────────────────────── */
h1 { font-family: 'DM Serif Display', serif !important; font-weight: 400 !important; color: #111 !important; letter-spacing: -0.02em; }
h2, h3 { font-weight: 600 !important; color: #111 !important; letter-spacing: -0.01em; }
h4 { font-weight: 600 !important; color: #333 !important; }
p, li { color: #444; line-height: 1.7; }

/* ── Divider ──────────────────────────────────────────── */
hr { border: none; border-top: 1px solid #EBEBEB; margin: 2rem 0; }

/* ── Page header strip ────────────────────────────────── */
.page-header {
    padding-bottom: 1.25rem;
    margin-bottom: 1.75rem;
    border-bottom: 1px solid #EBEBEB;
}
.page-header h1 { font-size: 2rem; margin: 0 0 0.3rem 0; }
.page-header p  { margin: 0; color: #777; font-size: 0.95rem; }

/* ── Cards ────────────────────────────────────────────── */
.card {
    background: #FFFFFF;
    border: 1px solid #E8E8E8;
    border-radius: 10px;
    padding: 1.25rem 1.4rem;
    height: 100%;
}
.card-icon { font-size: 1.4rem; margin-bottom: 0.5rem; }
.card h4 { margin: 0 0 0.4rem 0; font-size: 0.95rem; color: #111; }
.card p  { margin: 0; font-size: 0.85rem; color: #666; line-height: 1.55; }

/* ── Stat boxes ───────────────────────────────────────── */
.stat-box {
    background: #FAFAFA;
    border: 1px solid #E8E8E8;
    border-radius: 10px;
    padding: 1.1rem 1rem;
    text-align: center;
}
.stat-box .stat-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.85rem;
    color: #2563EB;
    line-height: 1.1;
    display: block;
}
.stat-box .stat-label {
    font-size: 0.8rem;
    color: #888;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-top: 0.25rem;
    display: block;
}

/* ── Badge / pill ─────────────────────────────────────── */
.badge {
    display: inline-block;
    background: #F0F4FF;
    color: #2563EB;
    border: 1px solid #DBEAFE;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 3px 2px;
}

/* ── Section label (eyebrow) ──────────────────────────── */
.eyebrow {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #2563EB;
    margin-bottom: 0.5rem;
}

/* ── Result box (predictor) ───────────────────────────── */
.result-box {
    background: #2563EB;
    color: white;
    border-radius: 12px;
    padding: 2rem 1.5rem;
    text-align: center;
}
.result-box .result-label { font-size: 0.8rem; opacity: 0.75; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.5rem; }
.result-box .result-value { font-family: 'DM Serif Display', serif; font-size: 2.8rem; line-height: 1; margin: 0; }
.result-box .result-delta { font-size: 0.95rem; opacity: 0.85; margin-top: 0.5rem; }

/* ── Insight box ──────────────────────────────────────── */
.insight-box {
    background: #F8FAFF;
    border: 1px solid #DBEAFE;
    border-left: 4px solid #2563EB;
    border-radius: 0 10px 10px 0;
    padding: 1.25rem 1.5rem;
    margin: 1rem 0;
}
.insight-box p { margin: 0; color: #1e293b; line-height: 1.75; font-size: 0.95rem; }

/* ── History rows (AI page) ───────────────────────────── */
.history-row {
    background: #FFFFFF;
    border: 1px solid #EBEBEB;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}
.history-row .meta { font-size: 0.78rem; color: #AAA; margin-bottom: 0.4rem; }
.history-row .question { font-weight: 600; color: #111; font-size: 0.9rem; margin-bottom: 0.35rem; }
.history-row .answer { color: #555; font-size: 0.875rem; line-height: 1.6; }

/* ── Input hint bar ───────────────────────────────────── */
.hint-bar {
    background: #F0F4FF;
    border: 1px solid #DBEAFE;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-size: 0.875rem;
    color: #2563EB;
    margin-bottom: 1.25rem;
}

/* ── Pipeline step ────────────────────────────────────── */
.pipe-step {
    background: #FFFFFF;
    border: 1px solid #E8E8E8;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.pipe-step .pipe-icon { font-size: 1.5rem; display: block; margin-bottom: 0.3rem; }
.pipe-step h5 { margin: 0 0 0.2rem 0; font-size: 0.9rem; color: #111; }
.pipe-step p  { margin: 0; font-size: 0.78rem; color: #888; }

/* ── Schema section block ─────────────────────────────── */
.schema-block {
    background: #FAFAFA;
    border: 1px solid #EBEBEB;
    border-left: 3px solid #2563EB;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.75rem;
}
.schema-block h5 { margin: 0 0 0.25rem 0; font-size: 0.875rem; color: #111; }
.schema-block p  { margin: 0; font-size: 0.82rem; color: #666; }

/* ── Streamlit widget tweaks ──────────────────────────── */
[data-testid="stMetric"] {
    background: #FAFAFA;
    border: 1px solid #E8E8E8;
    border-radius: 8px;
    padding: 0.75rem 1rem;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: #2563EB;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.55rem 1.5rem;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #1D4ED8;
}
div[data-testid="stButton"] > button:not([kind="primary"]) {
    background: #FFFFFF;
    border: 1px solid #DBEAFE;
    color: #2563EB;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 500;
}
div[data-testid="stButton"] > button:not([kind="primary"]):hover {
    background: #F0F4FF;
    border-color: #2563EB;
}
</style>
"""