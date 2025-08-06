import joblib
import pandas as pd
import numpy as np

# Load encoders
encoders = joblib.load("encoders.joblib")

def preprocess_input(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    for col, encoder in encoders.items():
        if col not in df.columns:
            raise ValueError(f"Missing expected column: {col}")

        # Get the mapping from label -> int
        classes = list(encoder.classes_)

        # Replace unseen labels with a default (e.g., most frequent or 'Unknown')
        df[col] = df[col].apply(lambda x: x if x in classes else classes[0])

        # Transform with known classes only
        df[col] = encoder.transform(df[col])
        
    return df
