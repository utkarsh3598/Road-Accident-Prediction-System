import streamlit as st
import pandas as pd
import joblib
from preprocess_input import preprocess_input  # Make sure the filename matches

# Load model and encoders
model = joblib.load("accident_severity_model.joblib")
encoders = joblib.load("encoders.joblib")
target_encoder = encoders.get("accident_severity")  # ✅ corrected key

# Page configuration
st.set_page_config(page_title="Accident Severity Predictor", page_icon="🚨")

st.title("🚗 Road Accident Severity Predictor")

# Form inputs
with st.form("prediction_form"):
    st.subheader("Enter accident details:")

    day_of_week = st.selectbox("Day of Week", encoders['day_of_week'].classes_)
    age_band_of_driver = st.selectbox("Age Band of Driver", encoders['age_band_of_driver'].classes_)
    light_conditions = st.selectbox("Light Conditions", encoders['light_conditions'].classes_)
    weather_conditions = st.selectbox("Weather Conditions", encoders['weather_conditions'].classes_)
    road_surface_type = st.selectbox("Road Surface Type", encoders['road_surface_type'].classes_)
    type_of_vehicle = st.selectbox("Type of Vehicle", encoders['type_of_vehicle'].classes_)

    submit = st.form_submit_button("Predict")

# Predict on submit
if submit:
    input_data = {
        "day_of_week": day_of_week,
        "age_band_of_driver": age_band_of_driver,
        "light_conditions": light_conditions,
        "weather_conditions": weather_conditions,
        "road_surface_type": road_surface_type,
        "type_of_vehicle": type_of_vehicle
    }

    try:
        df_input = pd.DataFrame([input_data])
        processed = preprocess_input(df_input, encoders)
        prediction = model.predict(processed)[0]
        prediction_label = target_encoder.inverse_transform([prediction])[0]

        st.success(f"🟢 Predicted Accident Severity: **{prediction_label}**")
    except Exception as e:
        st.error(f"❌ Prediction failed: {str(e)}")
