import joblib
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "salem_xgboost_groundwater.joblib"

model_package = joblib.load(MODEL_PATH)

model = model_package["model"]
FEATURES = model_package["features"]


def explain_prediction(input_data: dict) -> dict:

    # Get feature importance from trained XGBoost model
    importances = model.feature_importances_

    feature_importance = []

    for feature, importance in zip(FEATURES, importances):
        feature_importance.append({
            "feature": feature,
            "importance": round(float(importance), 4)
        })

    # Sort from highest to lowest
    feature_importance.sort(
        key=lambda x: x["importance"],
        reverse=True
    )

    # Top 5 influential features
    top_features = feature_importance[:5]

    # Human-readable explanation
    explanations = []

    for item in top_features:

        feature = item["feature"]

        if feature == "gw_lag_1":
            text = "The previous month's groundwater level strongly influences the prediction."

        elif feature == "gw_lag_2":
            text = "The groundwater level from two months earlier strongly influences the prediction."

        elif feature == "gw_lag_3":
            text = "The groundwater level from three months earlier contributes significantly to the prediction."

        elif feature == "gw_rolling_3":
            text = "The recent three-month groundwater trend influences the prediction."

        elif feature == "gw_change_1m":
            text = "The recent monthly groundwater change affects the predicted condition."

        elif feature == "rainfall_mm":
            text = "Recent rainfall contributes to the groundwater prediction."

        elif feature == "rain_lag_1":
            text = "Previous month's rainfall contributes to the prediction."

        elif feature == "rain_lag_2":
            text = "Rainfall from two months earlier contributes to the prediction."

        elif feature == "rain_lag_3":
            text = "Rainfall from three months earlier contributes to the prediction."

        elif feature == "rain_rolling_3":
            text = "The recent three-month rainfall pattern contributes to the prediction."

        elif feature == "month_num":
            text = "Seasonal month information contributes to the prediction."

        elif feature == "year":
            text = "The year information contributes to the prediction."

        else:
            text = f"{feature} contributes to the prediction."

        explanations.append({
            "feature": feature,
            "importance": item["importance"],
            "explanation": text
        })

    return {
        "method": "XGBoost feature importance",
        "top_features": explanations
    }