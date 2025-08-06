from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from preprocess import preprocess_input

app = Flask(__name__)
CORS(app)

# Load model and encoders
model = joblib.load("accident_severity_model.joblib")
encoders = joblib.load("encoders.joblib")
target_encoder = encoders.get("__target__")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        df = pd.DataFrame([data])
        processed = preprocess_input(df, encoders)

        prediction = model.predict(processed)[0]
        prediction_label = target_encoder.inverse_transform([prediction])[0]
        return jsonify({"prediction": prediction_label})
    except Exception as e:
        return jsonify({"error": f"Error in prediction: {str(e)}"}), 400

@app.route("/")
def home():
    return "✅ Real-Time Road Accident Alert System API is running."

if __name__ == "__main__":
    app.run(debug=True)
