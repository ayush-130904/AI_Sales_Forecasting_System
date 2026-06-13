import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import numpy as np
import os

engine = create_engine(os.getenv('DB_URL'))

def insert_ignore(table, conn, keys, data_iter):
    columns = ", ".join(keys)
    placeholders = ", ".join([f":{k}" for k in keys])
    stmt = text(f"INSERT IGNORE INTO {table.name} ({columns}) VALUES ({placeholders})")
    conn.execute(stmt, [dict(zip(keys, row)) for row in data_iter])


# ─── LOAD CUSTOMERS ───────────────────────────────────────────────────────────

print('Loading customers...')

customers = pd.read_csv('data/olist_customers_dataset.csv')

customers = customers.drop(columns=['customer_id'])

# We use customer_unique_id as the PK (not customer_id).
# customer_id in the raw CSV is a per-order surrogate key — the same real customer
# gets a different customer_id for every order. customer_unique_id is the true
# unique identifier for a person. Using it as PK lets us correctly foreign-key
# orders → customers after we map orders.customer_id → customer_unique_id below.

customers = customers.rename(columns={
    'customer_unique_id': 'customer_id',    # unique_id becomes our PK
    'customer_city': 'city',
    'customer_state': 'state',
    'customer_zip_code_prefix': 'zip_code'
})

# The dataset has 27 Brazilian states. For the Power BI regional map
# we group them into 5 regions — much easier to visualize.

region_map = {
    'SP': 'Southeast', 'RJ': 'Southeast', 'MG': 'Southeast', 'ES': 'Southeast',
    'RS': 'South',     'SC': 'South',     'PR': 'South',
    'BA': 'Northeast', 'PE': 'Northeast', 'CE': 'Northeast',
    'MA': 'Northeast', 'PB': 'Northeast', 'RN': 'Northeast',
    'PA': 'North',     'AM': 'North',     'RO': 'North',
    'GO': 'Central-West', 'MT': 'Central-West', 'MS': 'Central-West', 'DF': 'Central-West'
}

customers['region'] = customers['state'].map(region_map).fillna('Other')

customers = customers[['customer_id', 'city', 'state', 'zip_code', 'region']].drop_duplicates('customer_id')

customers.to_sql('customers', con=engine, if_exists='append', index=False, method=insert_ignore)
print(f"{len(customers)} Customers loaded successfully!")


# ─── LOAD PRODUCTS ────────────────────────────────────────────────────────────

print("Loading products...")

products = pd.read_csv('data/olist_products_dataset.csv')

products = products.rename(columns={
    'product_category_name': 'category',
    'product_name_lenght': 'name_length',
    'product_description_lenght': 'description_length',
    'product_photos_qty': 'photos_qty',
    'product_weight_g': 'weight_g'
})

# Prices live in order_items, not here — we'll back-fill after loading items.
products['price'] = None

products = products[['product_id', 'category', 'description_length', 'photos_qty', 'weight_g', 'price']]

products.to_sql('products', con=engine, if_exists='append', index=False, method=insert_ignore)
print(f"{len(products)} Products loaded successfully!")


# ─── LOAD ORDERS ──────────────────────────────────────────────────────────────

# Read the mapping table ONCE — customer_id (per-order) → customer_unique_id (true PK)
customers_map = pd.read_csv('data/olist_customers_dataset.csv')[
    ['customer_id', 'customer_unique_id']
].drop_duplicates('customer_id')

# Read orders ONCE (no second read further down)
orders = pd.read_csv('data/olist_orders_dataset.csv')

# Replace per-order customer_id with the true customer_unique_id so the
# foreign key references the customers table we just loaded.
orders = orders.merge(customers_map, on='customer_id', how='left')
orders['customer_id'] = orders['customer_unique_id']

# Keep only orders whose customer exists in the DB (should be ~99k / all of them)
valid_ids = set(pd.read_sql('SELECT customer_id FROM customers', con=engine)['customer_id'])
orders = orders[orders['customer_id'].isin(valid_ids)]


orders = orders[[
    'order_id',
    'customer_id',
    'order_status',
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]].rename(columns={
    'order_status': 'status',
    'order_purchase_timestamp': 'purchase_date',
    'order_approved_at': 'approved_date',
    'order_delivered_customer_date': 'delivered_date',
    'order_estimated_delivery_date': 'estimated_delivery'   # ← was 'estimated_date'
})

orders.to_sql('orders', con=engine, if_exists='append', index=False, method=insert_ignore)
print(f"{len(orders)} Orders loaded successfully!")


# ─── LOAD SALES (Order Items) ─────────────────────────────────────────────────

items = pd.read_csv('data/olist_order_items_dataset.csv')
items = items.rename(columns={'price': 'unit_price'})
items['quantity'] = 1

# Back-fill product prices with the per-product average from order items
product_prices = items.groupby('product_id')['unit_price'].mean().reset_index()
product_prices.columns = ['product_id', 'avg_price']

with engine.begin() as conn:
    for _, row in product_prices.iterrows():
        conn.execute(
            text("UPDATE products SET price = :price WHERE product_id = :pid"),
            {"price": row['avg_price'], "pid": row['product_id']}
        )
print("Product prices updated.")

# Only insert sales for orders we successfully loaded
valid_orders = set(orders['order_id'])
items = items[items['order_id'].isin(valid_orders)]
items = items[['order_id', 'product_id', 'quantity', 'unit_price', 'freight_value']]

items.to_sql('sales', engine, if_exists='append', index=False, method=insert_ignore)
print(f"{len(items)} Sales records loaded successfully!")

print("\nAll tables loaded successfully!")