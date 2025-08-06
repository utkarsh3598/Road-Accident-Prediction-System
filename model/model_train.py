import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# --- Configuration ---
DATA_PATH = r"C:\Users\utkar\Desktop\Project Topics\Real-Time Road Accident Alert System\data\RTA Dataset.csv"
MODEL_PATH = "accident_severity_model.joblib"
ENCODER_PATH = "encoders.joblib"

# --- Step 1: Load Dataset ---
try:
    df = pd.read_csv(DATA_PATH)
    print("✅ Dataset loaded successfully.")
except FileNotFoundError:
    raise Exception(f"❌ Dataset not found at {DATA_PATH}")

# --- Step 2: Normalize Column Names ---
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("📋 Columns found:", df.columns.tolist())

# --- Step 3: Define Features and Target ---
features = ['day_of_week', 'age_band_of_driver', 'light_conditions', 
            'weather_conditions', 'road_surface_type', 'type_of_vehicle']
target = 'accident_severity'

# Ensure all expected columns exist
missing = [col for col in features + [target] if col not in df.columns]
if missing:
    raise ValueError(f"❌ Missing columns in dataset: {missing}")

X = df[features].copy()
y = df[target].copy()

# --- Step 4: Encode Categorical Features ---
encoders = {}
for col in X.columns:
    encoder = LabelEncoder()
    X[col] = encoder.fit_transform(X[col])
    encoders[col] = encoder
print("✅ Features encoded.")

# --- Step 5: Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Step 6: Train Model ---
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(f"✅ Model trained. Accuracy: {accuracy:.2%}")

# --- Step 7: Save Model and Encoders ---
joblib.dump(model, MODEL_PATH)
joblib.dump(encoders, ENCODER_PATH)
print(f"✅ Model saved to {MODEL_PATH}")
print(f"✅ Encoders saved to {ENCODER_PATH}")
