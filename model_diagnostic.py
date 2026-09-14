import pandas as pd
import joblib
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = (
    BASE_DIR
    / "backend"
    / "data"
    / "Salem_ML_Ready_Monthly.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "backend"
    / "model"
    / "salem_xgboost_groundwater.joblib"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading data...")

df = pd.read_csv(CSV_PATH)

print("Data loaded successfully!")


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading model...")

package = joblib.load(MODEL_PATH)

model = package["model"]
FEATURES = package["features"]

print("Model loaded successfully!")


# ============================================================
# BASIC DATA INFORMATION
# ============================================================

print("\n========== DATA INFO ==========")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumns:")

for column in df.columns:
    print(" -", column)


# ============================================================
# TARGET STATISTICS
# ============================================================

print("\n========== TARGET STATISTICS ==========")

print(
    df["target_gw_next_month"].describe()
)


# ============================================================
# AMARAM_1 MODEL TEST
# ============================================================

print("\n========== AMARAM_1 TEST ==========")

station_df = df[
    df["Station"].str.lower() == "amaram_1"
].copy()

station_df = station_df.sort_values("month")


# Model input features
X = station_df[FEATURES]

# Actual target
y = station_df["target_gw_next_month"]


# Make predictions
predictions = model.predict(X)


# Add predictions to dataframe
station_df["prediction"] = predictions


# Calculate absolute error
station_df["absolute_error"] = (
    station_df["target_gw_next_month"]
    - station_df["prediction"]
).abs()


# Display results
print(
    station_df[
        [
            "month",
            "groundwater_level_m",
            "target_gw_next_month",
            "prediction",
            "absolute_error"
        ]
    ].to_string(index=False)
)


# ============================================================
# AMARAM_1 METRICS
# ============================================================

mae = mean_absolute_error(
    y,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y,
        predictions
    )
)


print("\n========== AMARAM_1 METRICS ==========")

print("MAE :", round(mae, 4))
print("RMSE:", round(rmse, 4))


# ============================================================
# EXTREME GROUNDWATER VALUES
# ============================================================

print("\n========== EXTREME VALUES ==========")


print("\nHighest groundwater values:")

highest_values = df.nlargest(
    10,
    "groundwater_level_m"
)

print(
    highest_values[
        [
            "Station",
            "month",
            "groundwater_level_m"
        ]
    ].to_string(index=False)
)


print("\nLowest groundwater values:")

lowest_values = df.nsmallest(
    10,
    "groundwater_level_m"
)

print(
    lowest_values[
        [
            "Station",
            "month",
            "groundwater_level_m"
        ]
    ].to_string(index=False)
)


# ============================================================
# STATION-WISE GROUNDWATER RANGE
# ============================================================

print(
    "\n========== STATION-WISE GROUNDWATER RANGE =========="
)


station_stats = (
    df.groupby("Station")["groundwater_level_m"]
    .agg(
        [
            "count",
            "min",
            "median",
            "max",
            "mean"
        ]
    )
    .sort_values(
        "max",
        ascending=False
    )
)


print(
    station_stats.to_string()
)


# ============================================================
# STATIONS WITH VERY LARGE VALUES
# ============================================================

print(
    "\n========== STATIONS WITH VERY LARGE VALUES =========="
)


large_stations = station_stats[
    (station_stats["max"] > 100)
    |
    (station_stats["min"] < -50)
]


print(
    large_stations.to_string()
)


# ============================================================
# FINISHED
# ============================================================

print("\n========== DONE ==========")