import streamlit as st
import requests
import numpy as np      

# Streamlit App Title
st.title("💳 Credit Card Fraud Detection")

# API Endpoint (Flask should be running)
API_URL = "http://127.0.0.1:5000/predict"
  # Update if running on a different port

# Define feature input fields
st.sidebar.header("Enter Transaction Details")
features = []
feature_names = ["V3", "V4", "V9", "V10", "V11", "V12", "V14", "V16", "V17", "V18"]

for feature in feature_names:
    value = st.sidebar.number_input(f"Enter {feature}", value=0.0, format="%.4f")
    features.append(value)

# Convert inputs to JSON format
if st.sidebar.button("Predict Fraud"):
    try:
        payload = {"features": features}
        response = requests.post(API_URL, json=payload)
        result = response.json()

        if "prediction" in result:
            prediction = result["prediction"]
            if prediction == 1:
                st.error("🚨 Fraudulent Transaction Detected!")
            else:
                st.success("✅ Legitimate Transaction")
        else:
            st.warning("Error: Invalid response from the API")

    except Exception as e:
        st.error(f"API Error: {e}")
