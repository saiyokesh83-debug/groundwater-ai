import pandas as pd
from pathlib import Path


# ==================================================
# BASE DIRECTORY
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# DATA PATH
# ==================================================

DATA_PATH = (
    BASE_DIR
    / "data"
    / "Salem_ML_Ready_Monthly.csv"
)


# ==================================================
# LOAD CSV
# ==================================================

print("Loading CSV...")
print("CSV path:", DATA_PATH)

df = pd.read_csv(DATA_PATH)

print("CSV loaded!")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ==================================================
# CONVERT MONTH TO DATETIME
# ==================================================

df["month"] = pd.to_datetime(df["month"])


# ==================================================
# GET ALL STATIONS
# ==================================================

def get_stations():

    return sorted(
        df["Station"]
        .dropna()
        .unique()
        .tolist()
    )


# ==================================================
# GET LATEST STATION DATA
# ==================================================

def get_station_data(station_name: str):

    station_df = df[
        df["Station"].str.lower()
        == station_name.lower()
    ]

    if station_df.empty:

        return None

    # Get latest available observation
    latest = (
        station_df
        .sort_values("month")
        .iloc[-1]
    )

    return {

        "station":
            latest["Station"],

        "month":
            latest["month"].strftime("%Y-%m-%d"),

        "latitude":
            float(latest["latitude"]),

        "longitude":
            float(latest["longitude"]),

        "current_groundwater":
            float(latest["groundwater_level_m"]),

        "rainfall_mm":
            float(latest["rainfall_mm"]),

        "gw_lag_1":
            float(latest["gw_lag_1"]),

        "gw_lag_2":
            float(latest["gw_lag_2"]),

        "gw_lag_3":
            float(latest["gw_lag_3"]),

        "gw_rolling_3":
            float(latest["gw_rolling_3"]),

        "gw_change_1m":
            float(latest["gw_change_1m"]),

        "rain_lag_1":
            float(latest["rain_lag_1"]),

        "rain_lag_2":
            float(latest["rain_lag_2"]),

        "rain_lag_3":
            float(latest["rain_lag_3"]),

        "rain_rolling_3":
            float(latest["rain_rolling_3"]),

        "month_num":
            int(latest["month_num"]),

        "year":
            int(latest["year"])
    }


# ==================================================
# STATION RELIABILITY
# ==================================================

def get_station_reliability(station_name: str):

    # --------------------------------------------------
    # GET STATION DATA
    # --------------------------------------------------

    station_df = df[
        df["Station"].str.lower()
        == station_name.lower()
    ].copy()

    if station_df.empty:

        return None

    # --------------------------------------------------
    # MODEL TRAINING PERIOD
    # --------------------------------------------------

    training_df = station_df[
        station_df["month"]
        <= pd.Timestamp("2024-12-01")
    ].copy()

    training_rows = len(training_df)

    # --------------------------------------------------
    # TRAINING GROUNDWATER RANGE
    # --------------------------------------------------

    if training_rows > 0:

        training_min = float(
            training_df[
                "groundwater_level_m"
            ].min()
        )

        training_max = float(
            training_df[
                "groundwater_level_m"
            ].max()
        )

    else:

        training_min = None
        training_max = None

    # --------------------------------------------------
    # LATEST OBSERVATION
    # --------------------------------------------------

    latest = (
        station_df
        .sort_values("month")
        .iloc[-1]
    )

    current_groundwater = float(
        latest["groundwater_level_m"]
    )

    # --------------------------------------------------
    # CHECK TRAINING RANGE
    # --------------------------------------------------

    outside_training_range = False

    if (
        training_min is not None
        and training_max is not None
    ):

        outside_training_range = (
            current_groundwater < training_min
            or current_groundwater > training_max
        )

    # --------------------------------------------------
    # RELIABILITY CLASSIFICATION
    # --------------------------------------------------

    if training_rows < 5:

        reliability = "very_low"

    elif training_rows < 10:

        reliability = "low"

    elif outside_training_range:

        reliability = "low"

    else:

        reliability = "normal"

    # --------------------------------------------------
    # RETURN RELIABILITY INFORMATION
    # --------------------------------------------------

    return {

        "training_rows":
            training_rows,

        "training_groundwater_min":
            training_min,

        "training_groundwater_max":
            training_max,

        "current_groundwater":
            current_groundwater,

        "outside_training_range":
            outside_training_range,

        "reliability":
            reliability
    }