import joblib
import pandas as pd
from pathlib import Path


# ==================================================
# MODEL PATH
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "model"
    / "salem_xgboost_groundwater.joblib"
)


# ==================================================
# LOAD MODEL
# ==================================================

model_package = joblib.load(MODEL_PATH)

model = model_package["model"]
FEATURES = model_package["features"]
MEDIANS = model_package["medians"]


# ==================================================
# PREDICTION FUNCTION
# ==================================================

def predict_groundwater(input_data: dict) -> dict:

    # Convert input dictionary to DataFrame
    data = pd.DataFrame([input_data])

    # --------------------------------------------------
    # ADD MISSING FEATURES
    # --------------------------------------------------

    medians_used = {}

    for feature in FEATURES:

        if feature not in data.columns:

            data[feature] = MEDIANS[feature]

            medians_used[feature] = True

        else:

            medians_used[feature] = False

    # --------------------------------------------------
    # KEEP EXACT FEATURE ORDER
    # --------------------------------------------------

    data = data[FEATURES]

    # --------------------------------------------------
    # CONVERT TO NUMERIC
    # --------------------------------------------------

    data = data.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # --------------------------------------------------
    # HANDLE NaN VALUES
    # --------------------------------------------------

    for feature in FEATURES:

        if pd.isna(data.loc[0, feature]):

            data.loc[0, feature] = MEDIANS[feature]

            medians_used[feature] = True

    # --------------------------------------------------
    # SAVE EXACT MODEL INPUTS
    # --------------------------------------------------

    model_inputs = {}

    for feature in FEATURES:

        model_inputs[feature] = float(
            data.loc[0, feature]
        )

    # --------------------------------------------------
    # MAKE PREDICTION
    # --------------------------------------------------

    prediction = model.predict(data)[0]

    prediction = float(prediction)

    # --------------------------------------------------
    # RETURN RESULT + DEBUG INFORMATION
    # --------------------------------------------------

    return {
        "prediction": prediction,

        "model_inputs": model_inputs,

        "medians_used": medians_used
    }