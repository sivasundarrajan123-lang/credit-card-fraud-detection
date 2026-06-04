import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv('cdd.csv')

# Split features and target
X = data.drop('Class', axis=1)
y = data['Class']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Streamlit UI
st.title("🚀 Credit Card Fraud Detection")
st.write("Enter transaction details to check for fraud.")

# Store user input as a session state dictionary
if "user_input" not in st.session_state:
    st.session_state.user_input = {feature: 0.0 for feature in X.columns}

with st.expander("🔢 Enter Transaction Details"):
    for feature in X.columns:
        st.session_state.user_input[feature] = st.number_input(f"{feature}", step=0.01, value=st.session_state.user_input[feature])

# Fill Sample Data
if st.button("🎲 Fill Sample Data"):
    sample_data = X.sample(1).values.flatten().tolist()
    st.session_state.user_input = {feature: sample_data[i] for i, feature in enumerate(X.columns)}
    st.rerun()  # Corrected function to refresh the UI

# Predict Button
if st.button("🚀 Predict"):
    user_input_values = np.array(list(st.session_state.user_input.values())).reshape(1, -1)
    user_input_scaled = scaler.transform(user_input_values)
    prediction = model.predict(user_input_scaled)

    # Display Result
    st.subheader("🔍 Prediction Result")
    st.markdown(
        "🚨 **Fraud Detected!**" if prediction[0] == 1 else "✅ **Transaction is Legitimate.**",
        unsafe_allow_html=True
    )
