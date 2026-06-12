import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('mysql+pymysql://root:rsayush13@localhost:3306/ecommerce_intelligence')

query = """
SELECT
    -- Why DATE_FORMAT? MySQL doesn't have DATE_TRUNC like PostgreSQL.
    -- DATE_FORMAT with '%Y-%m-01' groups all days in a month together
    -- e.g. 2017-10-07 and 2017-10-25 both become 2017-10-01
    DATE_FORMAT(o.purchase_date, '%Y-%m-01') AS month,

    -- TARGET VARIABLE: what we want the ML model to predict
    ROUND(SUM(s.unit_price * s.quantity), 2) AS actual_revenue,

    -- FEATURE 1: Number of orders (high orders = high revenue signal)
    COUNT(DISTINCT o.order_id) AS orders_count,

    -- FEATURE 2: Average order value (higher spend per order = more revenue)
    ROUND(AVG(s.unit_price * s.quantity), 2) AS avg_order_value,

    -- FEATURE 3: Unique customers (proxy for website traffic/demand)
    -- More unique buyers = more demand that month
    COUNT(DISTINCT o.customer_id) AS unique_customers,

    -- FEATURE 4: Total freight (proxy for marketing/logistics spend)
    -- Higher freight spend = more deliveries = more business activity
    ROUND(SUM(s.freight_value), 2) AS total_freight,

    -- FEATURE 5: Product variety sold (breadth of catalog demand)
    COUNT(DISTINCT s.product_id) AS unique_products_sold

FROM orders o

-- Why JOIN sales? Orders table has dates and customer info.
-- Sales table has prices and product info. We need both.
JOIN sales s ON o.order_id = s.order_id

-- Why filter status = 'delivered'?
-- Cancelled, processing, or shipped orders haven't generated
-- final revenue yet. Only delivered = confirmed revenue.
WHERE o.status = 'delivered'
  AND o.purchase_date IS NOT NULL

GROUP BY DATE_FORMAT(o.purchase_date, '%Y-%m-01')
ORDER BY month;
"""

df = pd.read_sql(text(query), engine)

# Why print describe()? Always inspect your data before ML.
# Check for nulls, weird ranges, or months with very few orders.
print("Monthly Features Preview:")
print(df.head(10))
print("\nStatistics:")
print(df.describe())
print(f"\nTotal months of data: {len(df)}")

df.to_csv('data/monthly_features.csv', index=False)
print("\nSaved to data/monthly_features.csv")