import joblib
import pandas as pd

def preprocess(df):
    # Load encoders from file
    encoders = joblib.load("encoders.joblib")
    for col, encoder in encoders.items():
        if col == "__target__":
            continue  # skip the target label encoder

        if col not in df.columns:
            raise ValueError(f"Missing expected column: {col}")

        classes = list(encoder.classes_)
        df[col] = df[col].apply(lambda x: x if x in classes else classes[0])
        df[col] = encoder.transform(df[col])

    return df
