import pandas as pd
import joblib

# Load encoders
ENCODER_PATH = "encoders.joblib"
encoders = joblib.load(ENCODER_PATH)

def preprocess(input_df):
    """
    Preprocess input data using saved encoders.
    Handles missing values and encodes categorical columns.
    """
    # Normalize column names
    input_df.columns = input_df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Fill missing values
    input_df.fillna("Unknown", inplace=True)

    # Apply label encoding
    for col, encoder in encoders.items():
        if col == '__target__':
            continue  # Skip target encoder

        if col not in input_df.columns:
            raise ValueError(f"Column '{col}' is missing from input.")

        # Encode using saved encoder, handle unseen values
        input_df[col] = input_df[col].apply(
            lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1
        )

    return input_df
