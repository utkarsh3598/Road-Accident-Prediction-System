import streamlit as st
import joblib
import pandas as pd
from preprocess import preprocess_input  # your preprocessing function

# Load trained model
model = joblib.load("accident_severity_model.joblib")

st.set_page_config(page_title="Road Accident Severity Predictor", layout="centered")
st.title("🚧 Road Accident Severity Predictor")
st.markdown("Predict the **severity** of a road accident based on accident conditions and driver info.")

# Convert numerical age to age band
def get_age_band(age):
    if age <= 16:
        return '0-16'
    elif age <= 25:
        return '17-25'
    elif age <= 35:
        return '26-35'
    elif age <= 45:
        return '36-45'
    elif age <= 55:
        return '46-55'
    elif age <= 65:
        return '56-65'
    else:
        return '66+'

# Input form
with st.form("prediction_form"):
    st.header("Enter Accident Details")

    col1, col2 = st.columns(2)

    with col1:
        weather = st.selectbox("Weather Conditions", ['Clear', 'Rain', 'Fog', 'Snow'])
        road_type = st.selectbox("Road Type", ['Single Carriageway', 'Dual Carriageway', 'Roundabout', 'One way street'])
        day_of_week = st.selectbox("Day of Week", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        road_surface_type = st.selectbox(
            "Road Surface Type", 
            ['Dry', 'Wet or damp', 'Snow', 'Frost or ice', 'Flood over 3cm', 'Oil or diesel', 'Mud']
        )

    with col2:
        light_conditions = st.selectbox("Light Conditions", ['Daylight', 'Darkness - lights lit', 'Darkness - no lighting'])
        speed_limit = st.number_input("Speed Limit (km/h)", min_value=10, max_value=150, step=5)
        age = st.number_input("Age of Driver", min_value=10, max_value=100, value=25)

    submitted = st.form_submit_button("Predict Severity")

    if submitted:
        try:
            # Convert age to age band
            age_band_of_driver = get_age_band(age)

            # Create input dataframe
            input_df = pd.DataFrame({
                'Weather_Conditions': [weather],
                'Road_Type': [road_type],
                'Day_of_Week': [day_of_week],
                'Light_Conditions': [light_conditions],
                'Speed_limit': [speed_limit],
                'age_band_of_driver': [age_band_of_driver],
                'road_surface_type': [road_surface_type],
            })

            # Preprocess and predict
            processed_input = preprocess_input(input_df)
            prediction = model.predict(processed_input)

            st.success(f"🎯 Predicted Severity: **{prediction[0]}**")

        except Exception as e:
            st.error(f"❌ Error in prediction: {str(e)}")
