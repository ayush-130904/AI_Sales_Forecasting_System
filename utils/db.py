# utils/db.py
import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env for local testing

@st.cache_resource
def get_engine():
    # Try Streamlit secrets first (for deployment)
    # Fall back to environment variable (for local)
    try:
        db_url = st.secrets["DB_URL"]
    except:
        db_url = os.getenv("DB_URL")
    
    return create_engine(db_url)

def run_query(query: str) -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(query, engine)