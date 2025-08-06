import joblib
import pandas as pd

def preprocess(df):
    # Load encoders from file
    encoders = joblib.load("encoders.joblib")
    
    # Fill missing values just like training
    df.fillna("Unknown", inplace=True)

    # Apply label encoding
    for col, encoder in encoders.items():
        if col == "__target__":
            continue  # skip the target label encoder

        if col not in df.columns:
            raise ValueError(f"Missing expected column: {col}")

        # Replace unseen values with "Unknown" if it exists, else first class
        known_classes = list(encoder.classes_)
        if "Unknown" in known_classes:
            df[col] = df[col].apply(lambda x: x if x in known_classes else "Unknown")
        else:
            df[col] = df[col].apply(lambda x: x if x in known_classes else known_classes[0])

        df[col] = encoder.transform(df[col])
    
    return df
