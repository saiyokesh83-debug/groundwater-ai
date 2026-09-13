def calculate_risk(
    predicted_groundwater: float,
    current_groundwater: float,
    gw_change_1m: float,
    rainfall_mm: float
) -> dict:
    """
    Calculate groundwater risk based on:
    1. Predicted groundwater level
    2. Recent groundwater change
    3. Rainfall condition
    """

    risk_score = 0

    # -------------------------------------------------
    # 1. Groundwater depletion
    # -------------------------------------------------
    if gw_change_1m < -2:
        risk_score += 40
    elif gw_change_1m < -1:
        risk_score += 30
    elif gw_change_1m < 0:
        risk_score += 15

    # -------------------------------------------------
    # 2. Predicted groundwater level
    # -------------------------------------------------
    if predicted_groundwater > current_groundwater + 2:
        risk_score += 0
    elif predicted_groundwater >= current_groundwater - 1:
        risk_score += 10
    elif predicted_groundwater >= current_groundwater - 3:
        risk_score += 25
    else:
        risk_score += 40

    # -------------------------------------------------
    # 3. Rainfall condition
    # -------------------------------------------------
    if rainfall_mm < 25:
        risk_score += 20
    elif rainfall_mm < 50:
        risk_score += 10

    # Keep score between 0 and 100
    risk_score = min(risk_score, 100)

    # -------------------------------------------------
    # 4. Risk classification
    # -------------------------------------------------
    if risk_score >= 70:
        risk_level = "CRITICAL"
    elif risk_score >= 50:
        risk_level = "HIGH"
    elif risk_score >= 25:
        risk_level = "MODERATE"
    else:
        risk_level = "LOW"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level
    }