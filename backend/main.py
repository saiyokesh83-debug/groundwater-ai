from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.service.prediction import predict_groundwater
from backend.service.risk_engine import calculate_risk
from backend.service.advisory import generate_advisory
from backend.service.data_service import (
    get_stations,
    get_station_data,
    get_station_reliability
)
from backend.service.forecast import generate_forecast
from backend.service.explainability import explain_prediction
from backend.service.stress_clock import calculate_stress_clock


# ==================================================
# FASTAPI APP
# ==================================================

app = FastAPI(
    title="Groundwater AI",
    description="AI-based groundwater risk prediction system",
    version="1.0.0"
)


# ==================================================
# REQUEST MODEL
# ==================================================

class PredictionRequest(BaseModel):

    gw_lag_1: float
    gw_lag_2: float
    gw_lag_3: float

    gw_rolling_3: float
    gw_change_1m: float

    rainfall_mm: float

    rain_lag_1: float
    rain_lag_2: float
    rain_lag_3: float

    rain_rolling_3: float

    month_num: int
    year: int

    current_groundwater: float


# ==================================================
# ROOT
# ==================================================

@app.get("/")
def root():

    return {
        "status": "success",
        "message": "Groundwater AI API is running"
    }


# ==================================================
# GET ALL STATIONS
# ==================================================

@app.get("/stations")
def stations():

    return {
        "status": "success",
        "stations": get_stations()
    }


# ==================================================
# GET STATION INFORMATION
# ==================================================

@app.get("/stations/{station_name}")
def station_information(station_name: str):

    data = get_station_data(station_name)

    if data is None:

        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    return {
        "status": "success",
        "data": data
    }


# ==================================================
# STATION PREDICTION
# ==================================================

@app.get("/stations/{station_name}/predict")
def station_prediction(station_name: str):

    # --------------------------------------------------
    # GET STATION DATA
    # --------------------------------------------------

    data = get_station_data(station_name)

    if data is None:

        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    # --------------------------------------------------
    # GET RELIABILITY
    # --------------------------------------------------

    reliability = get_station_reliability(
        station_name
    )

    # --------------------------------------------------
    # PREPARE MODEL INPUT
    # --------------------------------------------------

    input_data = data.copy()

    # --------------------------------------------------
    # PREDICTION
    # --------------------------------------------------

    prediction_result = predict_groundwater(
        input_data
    )

    predicted_groundwater = (
        prediction_result["prediction"]
    )

    # --------------------------------------------------
    # FORECAST
    # --------------------------------------------------

    forecast = generate_forecast(
        predicted_groundwater
    )

    # --------------------------------------------------
    # RISK ENGINE
    # --------------------------------------------------

    risk = calculate_risk(
        predicted_groundwater=predicted_groundwater,
        current_groundwater=data["current_groundwater"],
        gw_change_1m=data["gw_change_1m"],
        rainfall_mm=data["rainfall_mm"],
        reliability=reliability["reliability"]
    )

    # --------------------------------------------------
    # EXPLAINABILITY
    # --------------------------------------------------

    why = explain_prediction(
        input_data
    )

    # --------------------------------------------------
    # STRESS CLOCK
    # --------------------------------------------------

    stress_clock = calculate_stress_clock(
        current_groundwater=data["current_groundwater"],
        predicted_groundwater=predicted_groundwater
    )

    # --------------------------------------------------
    # ADVISORY
    # --------------------------------------------------

    advisory = generate_advisory(
        risk["risk_level"],
        data["gw_change_1m"]
    )

    # --------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------

    return {

        "status": "success",

        "station":
            data["station"],

        "current_groundwater":
            data["current_groundwater"],

        "prediction": {

            "predicted_groundwater":
                predicted_groundwater,

            "unit":
                "meters"
        },

        "reliability":
            reliability,

        "forecast":
            forecast,

        "risk":
            risk,

        "why":
            why,

        "stress_clock":
            stress_clock,

        "advisory":
            advisory,

        "debug": {

            "model_inputs":
                prediction_result["model_inputs"],

            "medians_used":
                prediction_result["medians_used"],

            "model_features":
                list(
                    prediction_result["model_inputs"].keys()
                )
        }
    }


# ==================================================
# MANUAL PREDICTION
# ==================================================

@app.post("/predict")
def manual_prediction(
    request: PredictionRequest
):

    # --------------------------------------------------
    # CONVERT REQUEST TO DICTIONARY
    # --------------------------------------------------

    input_data = request.model_dump()

    # --------------------------------------------------
    # PREDICTION
    # --------------------------------------------------

    prediction_result = predict_groundwater(
        input_data
    )

    predicted_groundwater = (
        prediction_result["prediction"]
    )

    # --------------------------------------------------
    # RISK
    # --------------------------------------------------

    risk = calculate_risk(
        predicted_groundwater=predicted_groundwater,
        current_groundwater=
            request.current_groundwater,
        gw_change_1m=
            request.gw_change_1m,
        rainfall_mm=
            request.rainfall_mm,
        reliability="normal"
    )

    # --------------------------------------------------
    # FORECAST
    # --------------------------------------------------

    forecast = generate_forecast(
        predicted_groundwater
    )

    # --------------------------------------------------
    # EXPLAINABILITY
    # --------------------------------------------------

    why = explain_prediction(
        input_data
    )

    # --------------------------------------------------
    # STRESS CLOCK
    # --------------------------------------------------

    stress_clock = calculate_stress_clock(
        current_groundwater=
            request.current_groundwater,
        predicted_groundwater=
            predicted_groundwater
    )

    # --------------------------------------------------
    # ADVISORY
    # --------------------------------------------------

    advisory = generate_advisory(
        risk["risk_level"],
        request.gw_change_1m
    )

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------

    return {

        "status":
            "success",

        "prediction": {

            "predicted_groundwater":
                predicted_groundwater,

            "unit":
                "meters"
        },

        "forecast":
            forecast,

        "risk":
            risk,

        "why":
            why,

        "stress_clock":
            stress_clock,

        "advisory":
            advisory,

        "debug": {

            "model_inputs":
                prediction_result["model_inputs"],

            "medians_used":
                prediction_result["medians_used"],

            "model_features":
                list(
                    prediction_result["model_inputs"].keys()
                )
        }
    }