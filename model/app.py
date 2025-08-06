from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import traceback

# --- Load model and encoders ---
model = joblib.load("accident_severity_model.joblib")
encoders = joblib.load("encoders.joblib")  # includes target encoder as '__target__'

# --- Flask App ---
app = Flask(__name__)
CORS(app)

# --- Helper: Preprocess Input ---
def preprocess_input(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    
    for col, encoder in encoders.items():
        if col == '__target__':
            continue  # Skip target encoder

        if col not in df.columns:
            raise ValueError(f"Missing expected column: {col}")

        # Handle unseen labels
        valid_classes = list(encoder.classes_)
        df[col] = df[col].apply(lambda x: x if x in valid_classes else valid_classes[0])
        df[col] = encoder.transform(df[col].astype(str))
    
    return df

# --- Route: Predict Accident Severity ---
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Preprocess input
        input_df = preprocess_input(data)

        # Predict
        prediction = model.predict(input_df)[0]

        # Decode label
        severity_label = encoders['__target__'].inverse_transform([prediction])[0]

        return jsonify({"prediction": severity_label})

    except Exception as e:
        error_trace = traceback.format_exc()
        return jsonify({"error": f"❌ Error in prediction: {str(e)}", "trace": error_trace}), 400

# --- Default Route ---
@app.route("/", methods=["GET"])
def home():
    return "✅ Road Accident Severity Prediction API is running."

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)
