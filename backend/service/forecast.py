def generate_forecast(predicted_groundwater: float) -> dict:
    """
    Generate a simple 1-month forecast summary
    from the XGBoost prediction.
    """

    return {
        "horizon": "1 month",
        "predicted_groundwater": predicted_groundwater,
        "unit": "meters",
        "status": "forecast_available"
    }