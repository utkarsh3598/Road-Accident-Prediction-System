import pandas as pd
import joblib

# Load encoders once
ENCODER_PATH = "encoders.joblib"
encoders = joblib.load(ENCODER_PATH)

def preprocess(input_df):
    """
    Preprocess input data using saved encoders.
    """
    input_df.columns = input_df.columns.str.strip().str.lower().str.replace(" ", "_")
    input_df.fillna("Unknown", inplace=True)

    for col, encoder in encoders.items():
        if col == '__target__':
            continue

        if col not in input_df.columns:
            raise ValueError(f"Column '{col}' is missing from input.")

        input_df[col] = input_df[col].apply(
            lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1
        )

    return input_df
