from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
from preprocess_input import preprocess_input

app = Flask(__name__)
CORS(app)

# Load model and encoders
model = joblib.load("accident_severity_model.joblib")
encoders = joblib.load("encoders.joblib")
target_encoder = encoders.get("__target__")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_json = request.get_json()
        df = pd.DataFrame([input_json])
        processed = preprocess_input(df)
        prediction = model.predict(processed)

        if target_encoder is not None:
            predicted_label = target_encoder.inverse_transform(prediction)[0]
        else:
            predicted_label = str(prediction[0])

        return jsonify({"prediction": predicted_label})

    except Exception as e:
        return jsonify({"error": f"❌ Prediction failed: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
