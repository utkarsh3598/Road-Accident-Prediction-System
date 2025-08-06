from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from preprocess import preprocess

# Load model and encoders
model = joblib.load("accident_severity_model.joblib")
encoders = joblib.load("encoders.joblib")

# Load label encoder for target to decode predictions
target_encoder = encoders.get("__target__", None)

app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_json = request.get_json()
        df = pd.DataFrame([input_json])

        # ✅ Fix: Only pass DataFrame to preprocess
        processed = preprocess(df)

        prediction = model.predict(processed)[0]

        if target_encoder is not None:
            prediction_label = target_encoder.inverse_transform([prediction])[0]
        else:
            prediction_label = prediction  # fallback if encoder missing

        return jsonify({
            "status": "success",
            "predicted_severity": prediction_label
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"❌ Prediction failed: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
