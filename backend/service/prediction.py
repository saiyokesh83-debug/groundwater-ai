import joblib
import pandas as pd
from pathlib import Path


# Find the trained model file
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "salem_xgboost_groundwater.joblib"


# Load the trained model package
model_package = joblib.load(MODEL_PATH)

model = model_package["model"]
FEATURES = model_package["features"]
MEDIANS = model_package["medians"]


def predict_groundwater(input_data: dict) -> float:
    """
    Predict groundwater level using the trained XGBoost model.
    """

    # Create input dataframe
    data = pd.DataFrame([input_data])

    # Make sure all required features exist
    for feature in FEATURES:
        if feature not in data.columns:
            data[feature] = MEDIANS[feature]

    # Keep features in the exact order used during training
    data = data[FEATURES]

    # Convert values to numeric
    data = data.apply(pd.to_numeric, errors="coerce")

    # Fill missing values using training medians
    for feature in FEATURES:
        data[feature] = data[feature].fillna(MEDIANS[feature])

    # Generate prediction
    prediction = model.predict(data)[0]

    return float(prediction)