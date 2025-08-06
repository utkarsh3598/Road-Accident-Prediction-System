from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from preprocess import preprocess_input

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Load model and encoders
model = joblib.load("accident_severity_model.joblib")

@app.route("/")
def home():
    return "✅ Road Accident Severity Prediction API is running."

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Parse JSON
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Create DataFrame
        input_df = pd.DataFrame([data])

        # Preprocess
        processed_input = preprocess_input(input_df)

        # Predict
        prediction = model.predict(processed_input)[0]

        return jsonify({
            "prediction": prediction
        })

    except ValueError as ve:
        return jsonify({"error": f"❌ Error in prediction: {str(ve)}"}), 400

    except Exception as e:
        return jsonify({"error": f"❌ Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
