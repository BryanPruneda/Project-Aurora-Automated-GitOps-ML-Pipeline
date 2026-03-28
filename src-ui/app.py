import streamlit as st
import requests
import os

# Get the API URL from an environment variable (standard K8s practice)
API_URL = os.getenv("MODEL_API_URL", "http://aurora-service:80")

st.title("🚀 Project Aurora: ML Inference Portal")
st.write("Interact with your deployed Kubernetes ML model in real-time.")

value = st.slider("Select Input Value", 0.0, 100.0, 50.0)

if st.button("Get Prediction"):
    try:
        response = requests.get(f"{API_URL}/predict", params={"value": value})
        data = response.json()
        st.success(f"Prediction Received: {data['prediction']}")
        st.json(data)
    except Exception as e:
        st.error(f"Error connecting to Model API: {e}")
