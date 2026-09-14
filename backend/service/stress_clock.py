# ==================================================
# GROUNDWATER STRESS CLOCK
# ==================================================

def calculate_stress_clock(
    current_groundwater: float,
    predicted_groundwater: float
) -> dict:
    """
    Estimate near-term groundwater trend.

    IMPORTANT:
    The threshold used here is an AI monitoring reference,
    not an official CGWB groundwater classification.
    """

    change = predicted_groundwater - current_groundwater

    # Small changes are treated as approximately stable
    if abs(change) < 0.10:
        status = "stable"

    elif change < 0:
        status = "declining"

    else:
        status = "improving"

    # For the MVP, avoid presenting a misleading
    # long-term threshold-crossing date.
    if status == "declining":
        message = (
            "Groundwater shows a declining trend. "
            "Continue monitoring and verify conditions "
            "through field observations."
        )

    elif status == "improving":
        message = (
            "Groundwater shows an improving trend. "
            "Continue monitoring to confirm whether "
            "the improvement persists."
        )

    else:
        message = (
            "Groundwater is approximately stable over "
            "the forecast interval."
        )

    return {
        "status": status,

        "current_groundwater": round(
            current_groundwater,
            3
        ),

        "predicted_groundwater": round(
            predicted_groundwater,
            3
        ),

        "estimated_change": round(
            change,
            3
        ),

        "threshold_status": (
            "No official critical threshold applied"
        ),

        "message": message,

        "note": (
            "This stress clock is an AI-based trend "
            "monitoring indicator. It is not an official "
            "CGWB groundwater classification or threshold."
        )
    }