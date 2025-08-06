import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

# --- Configuration ---
DATA_PATH = r"C:\Users\utkar\Desktop\Project Topics\Real-Time Road Accident Alert System\data\RTA Dataset.csv"
MODEL_PATH = "accident_severity_model.joblib"
ENCODER_PATH = "encoders.joblib"

# --- Step 1: Load Dataset ---
df = pd.read_csv(DATA_PATH)
print("✅ Dataset loaded.")

# --- Step 2: Normalize Column Names ---
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("📋 Columns:", df.columns.tolist())

# --- Step 3: Define Features and Target ---
features = ['day_of_week', 'age_band_of_driver', 'light_conditions',
            'weather_conditions', 'road_surface_type', 'type_of_vehicle']
target = 'accident_severity'

missing = [col for col in features + [target] if col not in df.columns]
if missing:
    raise ValueError(f"❌ Missing columns: {missing}")

X = df[features].copy()
y = df[target].copy()

# Show class distribution
print("\n📊 Class distribution:")
print(y.value_counts(normalize=True))

# --- Step 4: Encode Categorical Features ---
encoders = {}
for col in X.columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    encoders[col] = le
print("✅ Features encoded.")

# --- Step 5: Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Step 6: Train Model with Class Balancing ---
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# --- Step 7: Evaluation ---
y_pred = model.predict(X_test)
print(f"\n✅ Accuracy: {model.score(X_test, y_test):.2%}")
print("📋 Classification Report:")
print(classification_report(y_test, y_pred))

# --- Step 8: Save Model and Encoders ---
joblib.dump(model, MODEL_PATH)
joblib.dump(encoders, ENCODER_PATH)
print(f"✅ Model saved to {MODEL_PATH}")
print(f"✅ Encoders saved to {ENCODER_PATH}")
