import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import joblib
import os

# --- Configuration ---
DATA_PATH = r"C:\Users\utkar\Desktop\Project Topics\Road-Accident-Prediction-System\data\RTA Dataset.csv"
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
print("📋 Columns:", df.columns.tolist())

# --- Step 3: Check target distribution ---
if 'accident_severity' not in df.columns:
    raise ValueError("❌ 'accident_severity' column not found in dataset")

print("📊 Target distribution:\n", df['accident_severity'].value_counts())

# --- Step 4: Define Features and Target ---
features = ['day_of_week', 'age_band_of_driver', 'light_conditions', 
            'weather_conditions', 'road_surface_type', 'type_of_vehicle']

target = 'accident_severity'

# Optional: Add more features if available
optional_features = ['road_type', 'speed_limit', 'number_of_vehicles_involved']
features += [f for f in optional_features if f in df.columns]

# --- Step 5: Check for missing columns ---
missing_cols = [col for col in features + [target] if col not in df.columns]
if missing_cols:
    raise ValueError(f"❌ Missing columns: {missing_cols}")

X = df[features].copy()
y = df[target].copy()

# --- Step 5.1: Handle Missing Values ---
X.fillna("Unknown", inplace=True)

# --- Step 6: Encode categorical features ---
encoders = {}
for col in X.columns:
    encoder = LabelEncoder()
    X[col] = encoder.fit_transform(X[col].astype(str))
    encoders[col] = encoder
print("✅ Features encoded.")

# Encode target
target_encoder = LabelEncoder()
y = target_encoder.fit_transform(y)
encoders['__target__'] = target_encoder  # Save target encoder

# --- Step 7: Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Step 8: Train RandomForest with balanced class weights ---
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# --- Step 9: Evaluation ---
train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)
print(f"✅ Model trained.")
print(f"📈 Train Accuracy: {train_acc:.2%}")
print(f"📉 Test Accuracy: {test_acc:.2%}")

# Detailed report
y_pred = model.predict(X_test)
print("🧾 Classification Report:\n", classification_report(y_test, y_pred, target_names=target_encoder.classes_))

# --- Step 9.1: Confusion Matrix ---
ConfusionMatrixDisplay.from_estimator(
    model, X_test, y_test,
    display_labels=target_encoder.classes_,
    cmap='Blues'
)
plt.title("Confusion Matrix")
plt.show()

# --- Step 10: Save model and encoders ---
joblib.dump(model, MODEL_PATH)
joblib.dump(encoders, ENCODER_PATH)
print(f"💾 Model saved to: {MODEL_PATH}")
print(f"💾 Encoders saved to: {ENCODER_PATH}")
