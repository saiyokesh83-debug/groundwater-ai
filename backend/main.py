from fastapi import FastAPI
from pydantic import BaseModel

from backend.service.prediction import predict_groundwater
from backend.service.risk_engine import calculate_risk
from backend.service.advisory import generate_advisory

app = FastAPI()


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


@app.get("/")
def home():
    return {
        "message": "Groundwater AI Backend is running!",
        "status": "success"
    }


@app.post("/predict")
def predict(request: PredictionRequest):

    input_data = request.model_dump()

    # 1. XGBoost prediction
    predicted_groundwater = predict_groundwater(input_data)

    # 2. Risk calculation
    risk = calculate_risk(
        predicted_groundwater=predicted_groundwater,
        current_groundwater=request.current_groundwater,
        gw_change_1m=request.gw_change_1m,
        rainfall_mm=request.rainfall_mm
    )

    # 3. Advisory generation
    advisory = generate_advisory(
        risk_level=risk["risk_level"],
        gw_change_1m=request.gw_change_1m
    )

    # 4. Final API response
    return {
        "prediction": {
            "predicted_groundwater": predicted_groundwater,
            "unit": "meters"
        },
        "risk": risk,
        "advisory": advisory
    }