def generate_advisory(risk_level: str, gw_change_1m: float) -> dict:
    """
    Generate farmer and officer advisory based on groundwater risk.
    """

    if risk_level == "LOW":
        english = (
            "Groundwater condition is currently stable. "
            "Continue monitoring and use water efficiently."
        )

        tamil = (
            "நிலத்தடி நீர் நிலை தற்போது சீராக உள்ளது. "
            "தொடர்ந்து கண்காணித்து நீரை திறமையாக பயன்படுத்தவும்."
        )

        officer_action = (
            "Continue routine monitoring."
        )

    elif risk_level == "MODERATE":
        english = (
            "Groundwater shows moderate stress. "
            "Review irrigation schedules and monitor the trend closely."
        )

        tamil = (
            "நிலத்தடி நீரில் மிதமான அழுத்தம் காணப்படுகிறது. "
            "நீர்ப்பாசன அட்டவணையை மறுபரிசீலனை செய்து நிலையை தொடர்ந்து கண்காணிக்கவும்."
        )

        officer_action = (
            "Increase monitoring frequency and review irrigation demand."
        )

    elif risk_level == "HIGH":
        english = (
            "Groundwater decline is significant. "
            "Reduce unnecessary irrigation and prioritize efficient water use."
        )

        tamil = (
            "நிலத்தடி நீர் அளவு குறிப்பிடத்தக்க அளவில் குறைந்து வருகிறது. "
            "தேவையற்ற நீர்ப்பாசனத்தை குறைத்து நீர் பயன்பாட்டு திறனை மேம்படுத்தவும்."
        )

        officer_action = (
            "Prioritize the block for field verification and water-management intervention."
        )

    else:
        english = (
            "Critical groundwater stress detected. "
            "Immediate field verification, extraction review and recharge measures are recommended."
        )

        tamil = (
            "நிலத்தடி நீரில் தீவிரமான அழுத்தம் கண்டறியப்பட்டுள்ளது. "
            "உடனடி கள ஆய்வு, நீர் எடுப்பு மதிப்பாய்வு மற்றும் நீர் சேமிப்பு நடவடிக்கைகள் மேற்கொள்ள பரிந்துரைக்கப்படுகிறது."
        )

        officer_action = (
            "Immediate field verification and priority groundwater-management action required."
        )

    # Additional warning for rapid decline
    rapid_decline_alert = None

    if gw_change_1m < -2:
        rapid_decline_alert = (
            "Groundwater is declining rapidly compared with the recent trend."
        )

    return {
        "english": english,
        "tamil": tamil,
        "officer_action": officer_action,
        "rapid_decline_alert": rapid_decline_alert
    }