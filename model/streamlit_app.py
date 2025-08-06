import streamlit as st
import pandas as pd
import joblib
from preprocess import preprocess_input  # Make sure this is the correct import

# Load model and encoders
model = joblib.load("accident_severity_model.joblib")

# Streamlit UI
st.set_page_config(page_title="Road Accident Severity Predictor", layout="centered")
st.title("🚧 Road Accident Severity Prediction")

st.markdown("Provide the following details:")

# Input fields
day_of_week = st.selectbox("Day of Week", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
age_band_of_driver = st.selectbox("Age Band of Driver", ['Under 18', '18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
light_conditions = st.selectbox("Light Conditions", ['Daylight', 'Darkness - lights lit', 'Darkness - lights unlit', 'Darkness - no lighting'])
weather_conditions = st.selectbox("Weather Conditions", ['Clear', 'Rain', 'Fog or mist', 'Other'])
road_surface_type = st.selectbox("Road Surface Type", ['Dry', 'Wet or damp', 'Snow', 'Flood over 3cm'])
type_of_vehicle = st.selectbox("Type of Vehicle", ['Car', 'Motorcycle', 'Bus', 'Truck', 'Bicycle', 'Other'])

# Predict button
if st.button("Predict Severity"):
    try:
        input_df = pd.DataFrame([{
            'day_of_week': day_of_week,
            'age_band_of_driver': age_band_of_driver,
            'light_conditions': light_conditions,
            'weather_conditions': weather_conditions,
            'road_surface_type': road_surface_type,
            'type_of_vehicle': type_of_vehicle,
        }])

        # Preprocess input
        processed_input = preprocess_input(input_df)

        # Predict
        prediction = model.predict(processed_input)[0]

        st.success(f"🛑 Predicted Accident Severity: **{prediction}**")

    except ValueError as ve:
        st.error(f"❌ Error in prediction: {ve}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
