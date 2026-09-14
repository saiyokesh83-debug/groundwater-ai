def calculate_stress_clock(
    current_groundwater: float,
    predicted_groundwater: float,
    critical_threshold: float = 50.0
) -> dict:

    # Calculate predicted monthly change
    monthly_change = predicted_groundwater - current_groundwater

    # No meaningful decline
    if monthly_change >= 0:
        return {
            "status": "not_declining",
            "months_to_critical": None,
            "critical_threshold": critical_threshold,
            "message": "Current prediction does not show a decline toward the configured threshold."
        }

    # Already at or beyond critical threshold
    if current_groundwater >= critical_threshold:
        return {
            "status": "already_critical",
            "months_to_critical": 0,
            "critical_threshold": critical_threshold,
            "message": "Current groundwater value is already at or beyond the configured threshold."
        }

    # Estimate months to reach threshold
    monthly_decline = abs(monthly_change)

    distance_to_threshold = critical_threshold - current_groundwater

    months = distance_to_threshold / monthly_decline

    return {
        "status": "declining",
        "months_to_critical": round(months, 1),
        "critical_threshold": critical_threshold,
        "estimated_monthly_change": round(monthly_change, 2),
        "message": "Estimated time based on the current predicted trend."
    }