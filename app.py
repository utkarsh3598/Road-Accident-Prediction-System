from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

# --- Setup ---
app = Flask(__name__)
CORS(app)

# --- Load Model and Encoders ---
try:
    model = joblib.load("accident_severity_model.joblib")
    encoders = joblib.load("encoders.joblib")
    print("✅ Model and encoders loaded.")
except Exception as e:
    raise RuntimeError(f"❌ Failed to load model or encoders: {e}")

# --- Preprocessing Function ---
def preprocess_input(data):
    df = pd.DataFrame([data])
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    for col in df.columns:
        if col in encoders:
            try:
                df[col] = encoders[col].transform(df[col])
            except ValueError:
                raise ValueError(f"Invalid value '{df[col].iloc[0]}' for column '{col}'")
    return df

# --- Prediction Endpoint ---
@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.get_json()
        if not input_data:
            return jsonify({"error": "❌ No input provided"}), 400

        processed_input = preprocess_input(input_data)
        prediction = model.predict(processed_input)[0]

        return jsonify({"severity": prediction})
    
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 422

    except Exception as e:
        return jsonify({"error": f"❌ Unexpected error: {str(e)}"}), 500

# --- Start Server ---
if __name__ == '__main__':
    app.run(debug=True)
