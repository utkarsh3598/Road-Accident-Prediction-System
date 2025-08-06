import joblib
import pandas as pd

# Load encoders
encoders = joblib.load("encoders.joblib")

def preprocess_input(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    for col, encoder in encoders.items():
        if col not in df.columns:
            raise ValueError(f"Missing expected column: {col}")

        # Replace unknown values with the first known class
        classes = list(encoder.classes_)
        df[col] = df[col].apply(lambda x: x if x in classes else classes[0])
        df[col] = encoder.transform(df[col])

    return df
