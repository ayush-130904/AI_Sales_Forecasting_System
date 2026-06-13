import pandas as pd
import os
from groq import Groq
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # Load environment variables from .env file

engine = create_engine(os.getenv('DB_URL'))
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def get_monthly_summary():
    #We pull the last 6 months of actual+predicted revenue,
    #then calculate month-over-month change using LAG().
    query = """
    SELECT
        month,
        predicted_revenue,
        actual_revenue,
        orders_count,
        unique_customers,
        total_freight,

        LAG(actual_revenue) OVER (ORDER BY month) AS prev_revenue

    FROM predictions
    WHERE actual_revenue IS NOT NULL
    ORDER BY month DESC
    LIMIT 6;
    """
    return pd.read_sql(query, engine)


# Build AI prompt with real data

def build_prompt(df, user_question):
    latest = df.iloc[0]   # most recent month
    prev   = df.iloc[1] if len(df) > 1 else None

    # calculate percentage change

    if prev is not None and prev['actual_revenue'] != 0:
        rev_change = (latest['actual_revenue'] - prev['actual_revenue']) / prev['actual_revenue'] * 100
        order_change   = ((latest['orders_count'] - prev['orders_count'])/ prev['orders_count'] * 100)
        traffic_change = ((latest['unique_customers'] - prev['unique_customers'])/ prev['unique_customers'] * 100)
    else:
        rev_change = order_change = traffic_change = 0

    # Build a history string the AI can read

    history = ""

    for _, row in df.iterrows():
        history += (
            f"  {str(row['month'])[:7]}: "
            f"Revenue=R${row['actual_revenue']:,.0f}, "
            f"Orders={int(row['orders_count'])}, "
            f"Customers={int(row['unique_customers'])}\n"
        )

    prompt = f"""You are a senior e-commerce revenue analyst reviewing Brazilian market data.

## Recent Monthly Performance (newest first):
{history}

## Key Month-over-Month Changes:
- Revenue:        {rev_change:+.1f}%
- Orders:         {order_change:+.1f}%
- Unique customers (traffic): {traffic_change:+.1f}%
- Model predicted: R${latest['predicted_revenue']:,.0f} | Actual: R${latest['actual_revenue']:,.0f}

## Business Question:
{user_question}

## Your Task:
- Answer in 3-4 sentences maximum
- Reference specific numbers from the data above
- End with exactly 1 actionable recommendation
- Write in plain English for a non-technical business audience
"""
    return prompt, rev_change

# Call Groq, get insight, save to DB
def generate_insight(user_question:str):
    df = get_monthly_summary()

    if df.empty:
        print("No prediction data found. Run ml_pipeline.py first.")
        return

    prompt, rev_change  = build_prompt(df, user_question)
    latest_month        = df.iloc[0]['month']

    print(f"\nQuestion: {user_question}")
    print("Thinking...\n")

    # temperature=0.3
    # Temperature controls randomness. 0 = robotic/repetitive, 1 = creative/hallucinating.
    # 0.3 gives factual, consistent answers with slight natural variation.

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # free on Groq, very capable
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a concise business analyst. "
                    "Always cite specific numbers. Never make up data not provided."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=300    # ~3-4 sentences
    )

    insight_text = response.choices[0].message.content

    print("─" * 55)
    print(insight_text)
    print("─" * 55)

    # Save insight to database
    # Power BI will read the ai_insights table to display these explanations on the dashboard automatically.

    row = pd.DataFrame([{
        'month':          latest_month,
        'question':       user_question,
        'insight_text':   insight_text,
        'revenue_change': round(rev_change, 2),
        'created_at':     datetime.now()
    }])
    row.to_sql('ai_insights', engine, if_exists='append', index=False)
    print("Insight saved to ai_insights table\n")

    return insight_text

# Run with 3 standard business questions
if __name__ == "__main__":
    questions = [
        "Why did revenue change this month compared to last month?",
        "What is the biggest driver of current revenue performance?",
        "What should the business focus on to improve revenue next quarter?"
    ]
    for q in questions:
        generate_insight(q)