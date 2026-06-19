import streamlit as st
import pandas as pd
from groq import Groq
from datetime import datetime
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style import GLOBAL_CSS
from utils.db import run_query

st.set_page_config(page_title="AI Insights", page_icon="🤖", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── PAGE HEADER ───────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <p class="eyebrow">AI · Llama 3.3 via Groq</p>
    <h1>AI Insights</h1>
    <p>Ask any business question about the revenue data and get a plain-English analysis.</p>
</div>
""", unsafe_allow_html=True)

# ── LOAD CONTEXT DATA ─────────────────────────────────────────────
try:
    context_df = run_query("""
        SELECT month, predicted_revenue, actual_revenue,
               orders_count, unique_customers, total_freight
        FROM predictions
        WHERE actual_revenue IS NOT NULL
        ORDER BY month DESC LIMIT 6
    """)
    has_data = not context_df.empty
except:
    has_data = False

if has_data:
    with st.expander("Data the AI can see — last 6 months", expanded=False):
        display = context_df.copy()
        display['month']             = pd.to_datetime(display['month']).dt.strftime('%b %Y')
        display['actual_revenue']    = display['actual_revenue'].apply(lambda x: f"R${x:,.0f}")
        display['predicted_revenue'] = display['predicted_revenue'].apply(lambda x: f"R${x:,.0f}")
        st.dataframe(display, use_container_width=True, hide_index=True)

# ── PRESET QUESTIONS ──────────────────────────────────────────────
st.markdown('<p class="eyebrow" style="margin-top:1.5rem">Quick questions</p>', unsafe_allow_html=True)

preset_questions = [
    "Why did revenue change this month?",
    "What is the biggest driver of current performance?",
    "What should the business focus on next quarter?",
    "Is the ML model predicting accurately?",
    "Which month had the best performance and why?",
]

cols = st.columns(len(preset_questions))
selected_preset = None
for i, (col, q) in enumerate(zip(cols, preset_questions)):
    with col:
        if st.button(q, key=f"preset_{i}", use_container_width=True):
            selected_preset = q

st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

# ── CUSTOM INPUT ──────────────────────────────────────────────────
st.markdown("#### Ask your own question")
user_question = st.text_input(
    "Business question",
    placeholder="e.g. What caused the revenue drop in the last 2 months?",
    value=selected_preset if selected_preset else "",
    label_visibility="collapsed"
)
ask_btn = st.button("Get AI insight →", type="primary", use_container_width=True)

# ── GENERATE ──────────────────────────────────────────────────────
if ask_btn and user_question.strip():
    if not has_data:
        st.error("No prediction data in DB. Run ml_pipeline.py first.")
    else:
        history_text = ""
        for _, row in context_df.iterrows():
            history_text += (
                f"  {str(row['month'])[:7]}: "
                f"Revenue=R${row['actual_revenue']:,.0f}, "
                f"Orders={int(row['orders_count'])}, "
                f"Customers={int(row['unique_customers'])}\n"
            )

        latest     = context_df.iloc[0]
        prev       = context_df.iloc[1] if len(context_df) > 1 else None
        rev_change = 0
        if prev is not None and prev['actual_revenue']:
            rev_change = ((latest['actual_revenue'] - prev['actual_revenue'])
                          / prev['actual_revenue'] * 100)

        prompt = f"""You are a senior e-commerce revenue analyst.

## Recent Monthly Data (newest first):
{history_text}

## Latest Month Summary:
- Revenue change vs prior month: {rev_change:+.1f}%
- Predicted: R${latest['predicted_revenue']:,.0f} | Actual: R${latest['actual_revenue']:,.0f}

## Question: {user_question}

Answer in 3-4 sentences. Use specific numbers. End with 1 actionable recommendation.
Write for a non-technical business audience."""

        with st.spinner("Analysing your data..."):
            try:
                client   = Groq(api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system",
                         "content": "You are a concise business analyst. Always cite specific numbers from the data provided."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=300
                )
                insight = response.choices[0].message.content

                st.markdown("#### Analysis")
                st.markdown(f"""
                <div class="insight-box">
                    <p>{insight}</p>
                </div>""", unsafe_allow_html=True)

                # Save to DB
                try:
                    from sqlalchemy import text
                    from utils.db import get_engine
                    engine = get_engine()
                    with engine.connect() as conn:
                        conn.execute(text("""
                            INSERT INTO ai_insights
                                (month, question, insight_text, revenue_change, created_at)
                            VALUES (:month, :question, :insight, :change, :now)
                        """), {
                            'month':    str(latest['month'])[:10],
                            'question': user_question,
                            'insight':  insight,
                            'change':   round(rev_change, 2),
                            'now':      datetime.now()
                        })
                        conn.commit()
                    st.caption("Saved to database ✓")
                except Exception as e:
                    st.caption(f"Could not save to DB — {e}")

            except Exception as e:
                st.error(f"Groq API error: {e}")

elif ask_btn:
    st.warning("Enter a question first.")

# ── PAST INSIGHTS ─────────────────────────────────────────────────
st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown('<p class="eyebrow">History</p>', unsafe_allow_html=True)
st.markdown("#### Previous insights")

try:
    past = run_query("""
        SELECT month, question, insight_text, revenue_change, created_at
        FROM ai_insights
        ORDER BY created_at DESC LIMIT 10
    """)
    if past.empty:
        st.info("No saved insights yet — ask your first question above.")
    else:
        for _, row in past.iterrows():
            chg = f"{row['revenue_change']:+.1f}%" if row['revenue_change'] else "—"
            st.markdown(f"""
            <div class="history-row">
                <div class="meta">
                    📅 {str(row['month'])[:7]} &nbsp;·&nbsp;
                    Revenue change: {chg} &nbsp;·&nbsp;
                    {str(row['created_at'])[:16]}
                </div>
                <div class="question">{row['question']}</div>
                <div class="answer">{row['insight_text']}</div>
            </div>""", unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Could not load past insights: {e}")