# ==================================================
# GROUNDWATER FORECAST ENGINE
# 1 MONTH / 3 MONTH / 6 MONTH
# ==================================================

from datetime import datetime
from dateutil.relativedelta import relativedelta

from backend.service.prediction import predict_groundwater


# Validation-based error scale from the existing model evaluation.
# This is an uncertainty band for the MVP, NOT a statistical confidence interval.
VALIDATION_MAE = 2.68


def generate_forecast(station_data: dict) -> dict:
    """
    Generate recursive 1M / 3M / 6M groundwater forecasts.

    Future rainfall is unknown, so the forecast uses the
    recent 3-month average rainfall as the baseline assumption.
    """

    # --------------------------------------------------
    # 1. Copy current station features
    # --------------------------------------------------

    features = {
        "gw_lag_1": station_data["gw_lag_1"],
        "gw_lag_2": station_data["gw_lag_2"],
        "gw_lag_3": station_data["gw_lag_3"],
        "gw_rolling_3": station_data["gw_rolling_3"],
        "gw_change_1m": station_data["gw_change_1m"],
        "rainfall_mm": station_data["rainfall_mm"],
        "rain_lag_1": station_data["rain_lag_1"],
        "rain_lag_2": station_data["rain_lag_2"],
        "rain_lag_3": station_data["rain_lag_3"],
        "rain_rolling_3": station_data["rain_rolling_3"],
        "month_num": station_data["month_num"],
        "year": station_data["year"],
    }

    current_groundwater = float(station_data["current_groundwater"])

    # --------------------------------------------------
    # 2. Determine current date
    # --------------------------------------------------

    current_date = datetime.strptime(
        station_data["month"],
        "%Y-%m-%d"
    )

    # --------------------------------------------------
    # 3. Future rainfall assumption
    # --------------------------------------------------

    # rain_rolling_3 represents the recent 3-month rainfall total.
    # Therefore divide by 3 to get an approximate monthly baseline.

    recent_rainfall_average = (
        float(features["rain_rolling_3"]) / 3.0
    )

    # --------------------------------------------------
    # 4. Forecast containers
    # --------------------------------------------------

    forecasts = []

    previous_groundwater = current_groundwater

    # --------------------------------------------------
    # 5. Recursive forecasting
    # --------------------------------------------------

    for horizon in range(1, 7):

        future_date = current_date + relativedelta(
            months=horizon
        )

        # ----------------------------------------------
        # Future rainfall assumption
        # ----------------------------------------------

        future_rainfall = recent_rainfall_average

        # ----------------------------------------------
        # Predict next month
        # ----------------------------------------------

        prediction_result = predict_groundwater(features)

        predicted_groundwater = float(
            prediction_result["prediction"]
        )

        # ----------------------------------------------
        # Uncertainty band
        # ----------------------------------------------

        # Error grows with forecast horizon.
        uncertainty = VALIDATION_MAE * (horizon ** 0.5)

        lower_bound = predicted_groundwater - uncertainty
        upper_bound = predicted_groundwater + uncertainty

        # ----------------------------------------------
        # Store selected horizons
        # ----------------------------------------------

        if horizon in [1, 3, 6]:

            forecasts.append(
                {
                    "horizon_months": horizon,
                    "horizon": f"{horizon} month"
                    if horizon == 1
                    else f"{horizon} months",

                    "forecast_date": future_date.strftime(
                        "%Y-%m-%d"
                    ),

                    "predicted_groundwater":
                        round(predicted_groundwater, 3),

                    "lower_bound":
                        round(lower_bound, 3),

                    "upper_bound":
                        round(upper_bound, 3),

                    "uncertainty":
                        round(uncertainty, 3),

                    "unit": "meters"
                }
            )

        # ----------------------------------------------
        # Update groundwater lag features
        # ----------------------------------------------

        old_lag_1 = float(features["gw_lag_1"])
        old_lag_2 = float(features["gw_lag_2"])

        features["gw_lag_3"] = old_lag_2
        features["gw_lag_2"] = old_lag_1
        features["gw_lag_1"] = predicted_groundwater

        # Rolling 3-month groundwater average
        features["gw_rolling_3"] = (
            features["gw_lag_1"]
            + features["gw_lag_2"]
            + features["gw_lag_3"]
        ) / 3.0

        # Month-to-month groundwater change
        features["gw_change_1m"] = (
            predicted_groundwater
            - previous_groundwater
        )

        # ----------------------------------------------
        # Update rainfall lag features
        # ----------------------------------------------

        old_rain_lag_1 = float(features["rain_lag_1"])
        old_rain_lag_2 = float(features["rain_lag_2"])

        features["rain_lag_3"] = old_rain_lag_2
        features["rain_lag_2"] = old_rain_lag_1
        features["rain_lag_1"] = future_rainfall

        features["rainfall_mm"] = future_rainfall

        features["rain_rolling_3"] = (
            features["rain_lag_1"]
            + features["rain_lag_2"]
            + features["rain_lag_3"]
        )

        # ----------------------------------------------
        # Update month/year
        # ----------------------------------------------

        features["month_num"] = future_date.month
        features["year"] = future_date.year

        previous_groundwater = predicted_groundwater

    # --------------------------------------------------
    # 6. Final response
    # --------------------------------------------------

    return {
        "status": "forecast_available",

        "assumption": {
            "rainfall": "Recent 3-month average rainfall",
            "monthly_baseline_mm":
                round(recent_rainfall_average, 2)
        },

        "forecasts": forecasts,

        "unit": "meters",

        "uncertainty_note": (
            "Uncertainty bands are an MVP validation-based "
            "estimate and should not be interpreted as "
            "formal statistical confidence intervals."
        )
    }