# E-Commerce Revenue Intelligence System

A full-stack revenue intelligence platform that combines a trained machine learning model, an LLM-powered insights engine, a live cloud database, and an embedded Power BI dashboard — wrapped in a multi-page Streamlit application.

This README focuses primarily on the **ML engineering pipeline** and **AI integration layer**, since those are the core technical contributions of the project.

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Dataset](#dataset)
- [ML Engineering Pipeline](#ml-engineering-pipeline)
  - [Feature Engineering](#feature-engineering)
  - [Model Selection & Training](#model-selection--training)
  - [Model Evaluation](#model-evaluation)
  - [Model Serialization & Serving](#model-serialization--serving)
- [AI Integration Layer](#ai-integration-layer)
  - [Why an LLM Layer on Top of ML](#why-an-llm-layer-on-top-of-ml)
  - [Prompt Engineering](#prompt-engineering)
  - [Insight Generation Flow](#insight-generation-flow)
  - [Persisting AI Outputs](#persisting-ai-outputs)
- [Database Layer](#database-layer)
- [Application Layer (Streamlit)](#application-layer-streamlit)
- [Business Intelligence Layer (Power BI)](#business-intelligence-layer-power-bi)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Future Improvements](#future-improvements)

---

## Overview

E-commerce businesses generate large volumes of transactional data but often lack tooling to convert that data into **forward-looking, explainable** revenue decisions. This system addresses that gap with an end-to-end pipeline that:

1. **Forecasts** next month's revenue using a trained regression model
2. **Explains** revenue movements in plain English using an LLM grounded in real database values
3. **Visualizes** KPIs, trends, and regional performance through an embedded Power BI report
4. **Answers** open-ended business questions interactively (e.g. *"Why did revenue drop this month?"*)

The project is intentionally built as a **transparent, interpretable system** rather than a black-box model — every prediction and every AI-generated explanation is traceable back to real rows in the database.

---

## System Architecture

```
Raw Data (Kaggle CSVs, 100K+ orders)
        │
        ▼
MySQL Database (Aiven Cloud, 6 normalized tables)
        │
        ├──────────────┬──────────────────┐
        ▼              ▼                  ▼
  Python ML Layer   AI Insights Layer   Power BI
  (scikit-learn     (Llama 3.3 via      (DirectQuery /
  Linear Regression) Groq API)          Import mode)
        │              │                  │
        └──────┬───────┴──────────────────┘
               ▼
     Streamlit Multi-Page App
   (Predictor · Insights · Explorer · Dashboard)
```

Each layer reads from — and in the case of AI Insights, writes back to — the same MySQL instance, so the ML predictions, the AI's natural-language reasoning, and the BI dashboard are always grounded in a single source of truth rather than separate, drifting copies of the data.

---

## Dataset

**Source:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle)

| Metric | Value |
|---|---|
| Real orders | 99,441 |
| Unique customers | 96,096 |
| Unique products | 32,951 |
| Product categories | 73 |
| Time span | 2016 – 2018 |

The raw CSVs were cleaned, joined, and normalized into a 6-table relational schema (see [Database Layer](#database-layer)) before any feature engineering or model training took place.

---

## ML Engineering Pipeline

### Feature Engineering

The model is trained on a **monthly-aggregated** view of the transactional data rather than raw order-level rows, since the business question is "what will next month's revenue look like" — a time-series-adjacent regression problem framed as tabular supervised learning.

Aggregation pipeline (SQL → pandas):

1. Group `sales` joined with `orders` by calendar month
2. Compute, per month:
   - `orders_count` — total order volume
   - `unique_customers` — distinct customers that month (demand breadth / traffic proxy)
   - `total_freight` — summed freight cost (logistics & operational activity proxy)
   - `avg_order_value` — `total_revenue / orders_count` (demand quality)
3. Target variable: `actual_revenue` — summed `unit_price × quantity` for the month

These four features were selected deliberately for **interpretability and business relevance** over exhaustive feature search — each one maps to a metric a non-technical stakeholder already tracks.

### Model Selection & Training

**Algorithm:** Linear Regression (`scikit-learn`)

**Why Linear Regression over a more complex model:**

| Consideration | Linear Regression | Tree-based / Black-box alternatives |
|---|---|---|
| Interpretability | Coefficients map directly to "R$ per additional order/customer/freight unit" | Feature importances are less directly explainable to business users |
| Stakeholder trust | Easy to justify predictions in a meeting | Harder to defend without SHAP/LIME tooling |
| Data volume | 24 months of aggregated data — small sample, high risk of overfitting complex models | More prone to overfitting on a 24-row training set |
| Relationship shape | Revenue vs. order volume is empirically near-linear at this aggregation level | Added complexity not justified by the data |

Given the small number of monthly observations (24 months), a simpler, well-regularized linear model was the more defensible engineering choice than a high-variance model that could overfit noise.

**Training pipeline:**

```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Features are standardized before fitting since freight (R$ thousands)
# and customer counts (low hundreds-thousands) are on very different scales
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # [orders_count, unique_customers, total_freight, avg_order_value]

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
```

### Model Evaluation

| Metric | Value |
|---|---|
| R² | 0.94 |
| Evaluation split | 80/20 train-test on monthly aggregates |

An R² of 0.94 indicates the four engineered features explain the large majority of month-to-month revenue variance — consistent with the expectation that order volume and customer count are the dominant revenue drivers in this dataset.

### Model Serialization & Serving

The trained model and its fitted `StandardScaler` are serialized (`pickle`/`joblib`) and loaded once per Streamlit session via a cached loader:

```python
# utils/model.py
@st.cache_resource
def load_model():
    model  = joblib.load("models/linear_regression.pkl")
    scaler = joblib.load("models/scaler.pkl")
    return model, scaler
```

At inference time (`2_Revenue_Predictor.py`), user-entered values for next month are scaled with the **same fitted scaler** used in training, then passed to `model.predict()` — ensuring train/serve consistency, a common source of silent bugs in ML systems when scaling is re-fit or skipped at inference time.

```python
features        = np.array([[orders_count, unique_customers, total_freight, avg_order_value]])
features_scaled = scaler.transform(features)   # transform, NOT fit_transform
prediction      = model.predict(features_scaled)[0]
```

The app also computes percentage change vs. last known actual revenue and applies a simple threshold-based confidence banding (stable / moderate / large variance) to give users an immediate qualitative read on the forecast, not just a raw number.

---

## AI Integration Layer

### Why an LLM Layer on Top of ML

A regression model can tell you **what** revenue will likely be — it cannot tell you **why** revenue moved, or what to do about it, in language a non-technical stakeholder can act on. The AI Insights layer closes that gap by pairing the structured ML/database output with an LLM that reasons over it in natural language.

This is a **retrieval-grounded generation** pattern, not a free-form chatbot: the model is never allowed to invent numbers — it's fed real, queried data and instructed to cite it.

### Prompt Engineering

**Model:** `llama-3.3-70b-versatile` served via the **Groq API** (chosen for low-latency inference, important for an interactive UI where users expect a near-instant response after clicking "Get AI insight").

The prompt is constructed dynamically per request from live SQL query results — not hardcoded:

```python
prompt = f"""You are a senior e-commerce revenue analyst.

## Recent Monthly Data (newest first):
{history_text}

## Latest Month Summary:
- Revenue change vs prior month: {rev_change:+.1f}%
- Predicted: R${latest['predicted_revenue']:,.0f} | Actual: R${latest['actual_revenue']:,.0f}

## Question: {user_question}

Answer in 3-4 sentences. Use specific numbers. End with 1 actionable recommendation.
Write for a non-technical business audience."""
```

Key prompt engineering decisions:

| Technique | Purpose |
|---|---|
| System message: *"Always cite specific numbers from the data provided"* | Forces grounding in retrieved data, reduces hallucinated figures |
| Explicit data block (last 6 months) injected before the question | Gives the model a fixed, bounded context window instead of relying on its own training knowledge of "e-commerce trends" |
| `temperature=0.3` | Lower temperature for more deterministic, analytical tone vs. creative variance |
| `max_tokens=300` | Keeps responses concise and dashboard-appropriate, prevents rambling |
| "Answer in 3-4 sentences... end with 1 actionable recommendation" | Structures output for consistent UI rendering and ensures every response is actionable, not just descriptive |
| "Write for a non-technical business audience" | Tone-calibrates output away from statistical jargon |

### Insight Generation Flow

```
User selects a preset question OR types a custom one
        │
        ▼
SQL query → last 6 months from `predictions` table
        │
        ▼
Compute derived context (month-over-month % change)
        │
        ▼
Construct grounded prompt (data + question)
        │
        ▼
Groq API call → llama-3.3-70b-versatile
        │
        ▼
Render insight in UI (insight-box component)
        │
        ▼
Persist to `ai_insights` table (see below)
```

Five preset questions are offered as one-click shortcuts (e.g. *"Why did revenue change this month?"*, *"Is the ML model predicting accurately?"*) alongside a free-text input — balancing guided UX for first-time users with flexibility for power users.

### Persisting AI Outputs

Every generated insight is written back to a dedicated `ai_insights` table via SQLAlchemy, turning each query into a durable, auditable record rather than an ephemeral chat response:

```python
conn.execute(text("""
    INSERT INTO ai_insights
        (month, question, insight_text, revenue_change, created_at)
    VALUES (:month, :question, :insight, :change, :now)
"""), {...})
```

This creates a growing, queryable history of "what the business asked, and what the AI said" — itself surfaced back in the UI (`Previous insights` section) and feeding into the Power BI dashboard's AI Insights table panel. This closes the loop: AI output becomes structured data again, not a dead-end chat log.

---

## Database Layer

**Provider:** Aiven Cloud (managed MySQL)

6-table normalized schema:

| Table | Key Columns | Role |
|---|---|---|
| `customers` | `customer_id`, `city`, `state`, `zip_code`, `region` | Customer dimension |
| `orders` | `order_id`, `customer_id`, `status`, `purchase_date`, `delivered_date` | Order fact table |
| `products` | `product_id`, `category`, `weight_g`, `price`, `photos_qty` | Product dimension |
| `sales` | `sale_id`, `order_id`, `product_id`, `unit_price`, `freight_value`, `quantity` | Line-item fact table — primary revenue source |
| `predictions` | `month`, `orders_count`, `predicted_revenue`, `actual_revenue` | ML model input/output log |
| `ai_insights` | `month`, `question`, `insight_text`, `revenue_change`, `created_at` | AI-generated insight log |

All Streamlit pages connect via a shared `utils/db.py` module using SQLAlchemy + PyMySQL, with query results returned as pandas DataFrames for direct use in both the ML pipeline and the Streamlit UI.

---

## Application Layer (Streamlit)

A 5-page Streamlit app, each page independently styled via a shared `style.py` global CSS module:

| Page | Purpose |
|---|---|
| `1_About.py` | Project overview, architecture, schema, and methodology documentation |
| `2_Revenue_Predictor.py` | Interactive ML inference — user inputs next month's expected metrics, gets a live forecast + historical chart |
| `3_AI_Insights.py` | LLM-powered Q&A interface grounded in live database state |
| `4_Data_Explorer.py` | Live browsing/search/export of all 6 underlying database tables |
| `5_PowerBI.py` | Embedded live Power BI report (KPI cards, forecast chart, regional map) |

---

## Business Intelligence Layer (Power BI)

A Power BI report connected to the same Aiven MySQL instance, embedded directly into the Streamlit app via iframe, providing:

- KPI cards (Total Revenue, Total Orders, Avg Order Value, Forecast Accuracy %)
- Predicted vs. Actual revenue line chart with 3-month forward outlook
- Revenue-by-state choropleth map (Brazilian regions)
- A filterable AI Insights table, sourced from the same `ai_insights` table the Streamlit AI layer writes to

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML | scikit-learn (Linear Regression, StandardScaler) |
| AI / LLM | Llama 3.3 70B via Groq API |
| Database | MySQL (Aiven Cloud), SQLAlchemy, PyMySQL |
| App framework | Streamlit (multi-page) |
| Visualization | Plotly, Power BI |
| Language | Python 3.12 |

---

## Project Structure

```
project/
├── pages/
│   ├── 1_About.py
│   ├── 2_Revenue_Predictor.py
│   ├── 3_AI_Insights.py
│   ├── 4_Data_Explorer.py
│   └── 5_PowerBI.py
├── utils/
│   ├── db.py              # SQLAlchemy engine, run_query()
│   └── model.py            # Cached model/scaler loader
├── models/
│   ├── linear_regression.pkl
│   └── scaler.pkl
├── assets/
│   └── powerbi_screenshot.png
├── style.py                 # Shared GLOBAL_CSS
├── requirements.txt
└── README.md
```

---

## Setup & Installation

```bash
# Clone the repository
git clone <repo-url>
cd project

# Install dependencies
pip install -r requirements.txt

# Configure secrets (see below)
# Create .streamlit/secrets.toml with DB credentials and GROQ_API_KEY

# Run the app
streamlit run pages/1_About.py
```

## Environment Variables

Store the following in `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_api_key"

[mysql]
host = "your-aiven-host.aivencloud.com"
port = 20336
user = "avnadmin"
password = "your_password"
database = "your_database"
```

---

## Future Improvements

- Replace single-model Linear Regression with a model comparison harness (Ridge/Lasso/Gradient Boosting) and automated metric logging, while retaining Linear Regression as the interpretable production default
- Add confidence intervals to forecasts rather than a single point estimate
- Introduce retrieval-augmented context windows for the AI layer that scale beyond the last 6 months as more data accumulates
- Add automated model retraining trigger when new `actual_revenue` rows land in `predictions`
- Add evaluation harness for AI Insight quality (e.g. periodic human review flag on `ai_insights` rows)
