import pandas as pd
from pathlib import Path


# ============================================================
# DATA PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = (
    BASE_DIR
    / "backend"
    / "data"
    / "Salem_ML_Ready_Monthly.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading CSV...")

df = pd.read_csv(CSV_PATH)

print("CSV loaded!")
print("Rows:", len(df))


# ============================================================
# STATIONS TO INSPECT
# ============================================================

stations = [
    "Ammapet_1",
    "Avaniperur Keelmugam",
    "Illupanatham_1"
]


# ============================================================
# INSPECT EACH STATION
# ============================================================

for station in stations:

    print("\n" + "=" * 70)
    print(f"STATION: {station}")
    print("=" * 70)

    station_df = df[
        df["Station"].str.lower()
        == station.lower()
    ].copy()

    station_df = station_df.sort_values("month")

    print(
        station_df[
            [
                "month",
                "groundwater_level_m",
                "gw_lag_1",
                "gw_lag_2",
                "gw_lag_3",
                "gw_rolling_3",
                "gw_change_1m",
                "target_gw_next_month"
            ]
        ].to_string(index=False)
    )


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("INSPECTION COMPLETE")
print("=" * 70)