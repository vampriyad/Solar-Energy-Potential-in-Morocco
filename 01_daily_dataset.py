Data source: Open-Meteo Historical Weather API
https://open-meteo.com/en/docs/historical-weather-api
"""
import json
import glob
import os
import pandas as pd

RAW_DIR = "data/raw"
OUT = "results/daily_all.csv"
os.makedirs("results", exist_ok=True)

frames = []
for path in sorted(glob.glob(f"{RAW_DIR}/*.json")):
    city = os.path.basename(path)[:-5]  # strip ".json"
    data = json.load(open(path))
    h = data["hourly"]
    df = pd.DataFrame({
        "time": pd.to_datetime(h["time"]),
        "ghi":  h["shortwave_radiation"],        # W/m2, global horizontal irradiance
        "dni":  h["direct_normal_irradiance"],   # W/m2, direct normal irradiance
        "dhi":  h["diffuse_radiation"],          # W/m2, diffuse irradiance
        "temp": h["temperature_2m"],             # deg C
        "rh":   h["relative_humidity_2m"],       # %
        "wind": h["wind_speed_10m"],             # km/h
        "cloud": h["cloud_cover"],               # %
    })
    df["city"] = city
    df["date"] = df["time"].dt.date
    frames.append(df)

hourly = pd.concat(frames, ignore_index=True)

# Aggregate hourly rows into daily rows
daily = hourly.groupby(["city", "date"]).agg(
    ghi_day   = ("ghi", "sum"),              # Wh/m2 per day
    dni_day   = ("dni", "sum"),
    dhi_day   = ("dhi", "sum"),
    temp_mean = ("temp", "mean"),
    temp_max  = ("temp", "max"),
    temp_min  = ("temp", "min"),
    rh_mean   = ("rh", "mean"),
    wind_mean = ("wind", "mean"),
    cloud_mean = ("cloud", "mean"),
    sun_hours = ("ghi", lambda s: (s > 5).sum()),   # hours with real sunshine
).reset_index()

daily["date"] = pd.to_datetime(daily["date"])
daily["year"] = daily["date"].dt.year
daily["month"] = daily["date"].dt.month
daily["day_of_year"] = daily["date"].dt.dayofyear

def season(m):
    return {12: "Winter", 1: "Winter", 2: "Winter",
            3: "Spring", 4: "Spring", 5: "Spring",
            6: "Summer", 7: "Summer", 8: "Summer",
            9: "Autumn", 10: "Autumn", 11: "Autumn"}[m]
daily["season"] = daily["month"].map(season)

daily.to_csv(OUT, index=False)
print(f"Saved {len(daily):,} daily rows ({daily['city'].nunique()} cities x 3 years) -> {OUT}")

ann = (daily.groupby(["city", "year"])["ghi_day"].sum().groupby("city").mean() / 1000)
print("\nAnnual solar radiation per city (kWh/m2/year):")
print(ann.round(0))
