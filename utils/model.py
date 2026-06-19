# utils/model.py
# Loads the ML model and scaler from disk once and caches them.

import pickle
import streamlit as st

@st.cache_resource
def load_model():
    with open('models/revenue_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler