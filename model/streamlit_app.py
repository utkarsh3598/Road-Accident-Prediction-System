import streamlit as st
import joblib
import pandas as pd
from preprocess import preprocess_input  # your custom function

# Load the trained model
model = joblib.load("accident_severity_model.joblib")

# App Title
st.title("🚨 Road Accident Severity Predictor")

st.markdown("""
This app predicts the **severity of a road accident** based on various conditions like weather, road type, and vehicle info.
""")

# Collect user inputs
st.header("Enter Accident Details")

# Example input fields — customize as per your dataset
col1, col2 = st.columns(2)

with col1:
    weather = st.selectbox("Weather Conditions", ['Clear', 'Rain', 'Fog', 'Snow'])
    road_type = st.selectbox("Road Type", ['Single Carriageway', 'Dual Carriageway', 'Roundabout', 'One way street'])
    day_of_week = st.selectbox("Day of Week", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

with col2:
    light_conditions = st.selectbox("Light Conditions", ['Daylight', 'Darkness - lights lit', 'Darkness - no lighting'])
    speed_limit = st.number_input("Speed Limit (km/h)", min_value=10, max_value=150, step=5)
    age_of_driver = st.number_input("Age of Driver", min_value=16, max_value=100)

# Submit button
if st.button("Predict Severity"):
    # Create a single row dataframe for prediction
    input_df = pd.DataFrame({
        'Weather_Conditions': [weather],
        'Road_Type': [road_type],
        'Day_of_Week': [day_of_week],
        'Light_Conditions': [light_conditions],
        'Speed_limit': [speed_limit],
        'Age_of_Driver': [age_of_driver],
        # Add other features as per your model
    })

    try:
        # Preprocess input
        processed_input = preprocess_input(input_df)

        # Predict
        prediction = model.predict(processed_input)

        # Display result
        st.success(f"🔎 Predicted Severity: **{prediction[0]}**")

    except ValueError as e:
        st.error(f"⚠️ Error in prediction: {str(e)}")
