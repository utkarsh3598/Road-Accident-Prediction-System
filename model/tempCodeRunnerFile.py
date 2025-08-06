from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
from preprocess import preprocess_input

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load("accident_severity_model.joblib")

@app.route('/', methods=['GET'])
def home():
    return "Real-Time Road Accident Alert System API is running."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        df = pd.DataFrame([data])
        processed = preprocess_input(df)
        prediction = model.predict(processed)
        return jsonify({"severity": prediction[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)