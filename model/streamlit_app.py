import streamlit as st
import requests

st.set_page_config(page_title="Accident Severity Predictor", layout="centered")

st.title("🚦 Real-Time Road Accident Severity Predictor")
st.write("Enter the conditions below to predict accident severity:")

# Input form
with st.form("accident_form"):
    day_of_week = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    age_band = st.selectbox("Driver's Age Band", ["Under 18", "18-30", "31-50", "Over 51", "Unknown"])
    light_conditions = st.selectbox("Light Conditions", ["Daylight", "Darkness - lights lit", "Darkness - lights unlit", "Darkness - no lighting"])
    weather = st.selectbox("Weather Conditions", ["Clear", "Rain", "Fog or mist", "Other", "Unknown"])
    road_surface = st.selectbox("Road Surface Type", ["Asphalt roads", "Gravel roads", "Earth roads", "Other"])
    vehicle_type = st.selectbox("Type of Vehicle", ["Automobile", "Public (12 seater)", "Lorry", "Motorcycle", "Bicycle", "Other"])

    submitted = st.form_submit_button("Predict Severity")

# Prediction
if submitted:
    with st.spinner("Predicting..."):
        data = {
            "day_of_week": day_of_week,
            "age_band_of_driver": age_band,
            "light_conditions": light_conditions,
            "weather_conditions": weather,
            "road_surface_type": road_surface,
            "type_of_vehicle": vehicle_type
        }

        try:
            response = requests.post("http://localhost:5000/predict", json=data)
            if response.status_code == 200:
                severity = response.json().get("severity", "Unknown")
                st.success(f"🚑 **Predicted Severity:** {severity}")
            else:
                st.error(f"❌ Error: {response.json().get('error')}")
        except Exception as e:
            st.error(f"❌ Could not connect to the API: {e}")
