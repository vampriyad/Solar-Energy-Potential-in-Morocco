import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
CITY_LAT = {"Ouarzazate":30.92,"Dakhla":23.71,"Marrakech":31.63,"Casablanca":33.57,
            "Tangier":35.76,"Tetouan":35.58,"Errachidia":31.93,"Agadir":30.42}
CITY_NAME = {"Tetouan": "Tétouan", "Ouarzazate": "Ouarzazate", "Dakhla": "Dakhla",
             "Marrakech": "Marrakech", "Casablanca": "Casablanca", "Tangier": "Tangier",
             "Errachidia": "Errachidia", "Agadir": "Agadir"}
NORTH = ["Casablanca", "Tangier", "Tetouan"]
df = pd.read_csv("results/daily_all.csv", parse_dates=["date"])
df["lat"] = df["city"].map(CITY_LAT)
FEATURES = ["day_of_year", "temp_mean", "temp_max", "temp_min",
            "rh_mean", "wind_mean", "cloud_mean", "lat"]
TARGET = "ghi_day"
train_mask = df["date"] < "2025-01-01"
test_mask = ~train_mask
X_train, X_test = df.loc[train_mask, FEATURES], df.loc[test_mask, FEATURES]
y_train, y_test = df.loc[train_mask, TARGET], df.loc[test_mask, TARGET]
print(f"Train: {len(X_train)} days | Test: {len(X_test)} days")
models = {
    "Linear regression": LinearRegression(),
    "Random forest": RandomForestRegressor(n_estimators=400, max_depth=15, random_state=42, n_jobs=-1),
    "Gradient boosting": GradientBoostingRegressor(n_estimators=300, max_depth=5,
                                                   learning_rate=0.05, random_state=42),
}

metrics, preds = {}, {}
for name, model in models.items():
    model.fit(X_train, y_train)
    p = model.predict(X_test)
    preds[name] = p
    metrics[name] = {
        "R2": round(r2_score(y_test, p), 3),
        "RMSE": round(np.sqrt(mean_squared_error(y_test, p)), 1),
        "MAE": round(mean_absolute_error(y_test, p), 1),
    }
    print(f"{name}: R2={metrics[name]['R2']}, RMSE={metrics[name]['RMSE']}, MAE={metrics[name]['MAE']}")
base = np.full(len(y_test), y_train.mean())
metrics["Baseline (mean)"] = {
    "R2": round(r2_score(y_test, base), 3),
    "RMSE": round(np.sqrt(mean_squared_error(y_test, base)), 1),
    "MAE": round(mean_absolute_error(y_test, base), 1),
}
print(f"Baseline: R2={metrics['Baseline (mean)']['R2']}, RMSE={metrics['Baseline (mean)']['RMSE']}")
tscv = TimeSeriesSplit(n_splits=4)
cv_scores = {}
for name in ["Linear regression", "Random forest", "Gradient boosting"]:
    r2s = []
    for tr, va in tscv.split(X_train):
        m = models[name]
        m.fit(X_train.iloc[tr], y_train.iloc[tr])
        r2s.append(r2_score(y_train.iloc[va], m.predict(X_train.iloc[va])))
    cv_scores[name] = round(float(np.mean(r2s)), 3)
    print(f"{name} CV (mean R2, 4 folds): {cv_scores[name]}")
df_test = df[test_mask]
per_city = {}
for city in df_test["city"].unique():
    m = (df_test["city"] == city).values
    per_city[city] = {name: round(r2_score(y_test[m], preds[name][m]), 3) for name in preds}
print("\nPer-city R2 (2025):")
for city, v in per_city.items():
    print(f"  {city:12s}", v)
rf = models["Random forest"]
p = preds["Random forest"]
df_test2 = df_test.copy()
df_test2["month"] = df_test2["date"].dt.month
df_test2["pred"] = p
monthly_mae = df_test2.groupby("month").apply(lambda g: mean_absolute_error(g[TARGET], g["pred"]), include_groups=False)
print("\nMonthly MAE (Wh/m2/day):", monthly_mae.round(0).to_dict())
pd.DataFrame(metrics).T.to_csv("results/ml_metrics.csv")
json.dump({c: v for c, v in per_city.items()}, open("results/ml_percity_r2.json", "w"), indent=2)
json.dump({k: round(v, 0) for k, v in monthly_mae.items()}, open("results/ml_monthly_mae.json", "w"))
json.dump(cv_scores, open("results/ml_cv.json", "w"), indent=2)
fig, ax = plt.subplots(figsize=(6.6, 6.2))
sc = ax.scatter(y_test / 1000, p / 1000, s=6, alpha=0.45, c=df.loc[test_mask, "lat"], cmap="viridis_r")
lim = [0, y_test.max() / 1000 * 1.05]
ax.plot(lim, lim, "--", color="black", lw=1, label="Perfect prediction")
ax.set_xlabel("Actual daily solar radiation (kWh/m²/day)")
ax.set_ylabel("Predicted (kWh/m²/day)")
ax.set_title(f"Random forest, test year 2025, R² = {metrics['Random forest']['R2']}")
ax.grid(alpha=0.3)
fig.colorbar(sc, ax=ax, label="Latitude (°N)")
ax.legend(fontsize=9)
fig.tight_layout(); fig.savefig("figures/fig9_scatter.png", dpi=180)
resid = (y_test - p) / 1000
fig, ax = plt.subplots(figsize=(6.6, 5.0))
sc = ax.scatter(p / 1000, resid, s=6, alpha=0.5, c=df.loc[test_mask, "lat"], cmap="viridis_r")
ax.axhline(0, color="black", lw=1)
ax.set_xlabel("Predicted daily solar radiation (kWh/m²/day)")
ax.set_ylabel("Residual (actual minus predicted, kWh/m²/day)")
ax.set_title("Residuals of the random forest (test year 2025)")
ax.grid(alpha=0.3)
fig.colorbar(sc, ax=ax, label="Latitude (°N)")
fig.tight_layout(); fig.savefig("figures/fig10_residuals.png", dpi=180)
imps = pd.Series(rf.feature_importances_, index=FEATURES).sort_values()
fig, ax = plt.subplots(figsize=(6.8, 4.2))
ax.barh([f.replace("_", " ") for f in imps.index], imps.values, color="#2a9d8f", edgecolor="black", lw=0.4)
ax.set_xlabel("Importance (random forest)")
ax.set_title("Which weather variables matter most for predicting solar radiation?")
ax.grid(axis="x", alpha=0.3)
fig.tight_layout(); fig.savefig("figures/fig11_importances.png", dpi=180)
pc = pd.DataFrame(per_city).T
pc = pc.reindex(df["city"].unique())
x = np.arange(len(pc)); w = 0.26
fig, ax = plt.subplots(figsize=(8.2, 4.6))
colors = {"Linear regression": "#aec7e8", "Random forest": "#2a9d8f", "Gradient boosting": "#ffbb78"}
for i, model in enumerate(["Linear regression", "Random forest", "Gradient boosting"]):
    ax.bar(x + (i - 1) * w, pc[model], w, label=model, color=colors[model], edgecolor="black", lw=0.4)
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(x); ax.set_xticklabels([CITY_NAME[c] for c in pc.index], rotation=22, ha="right")
ax.set_ylabel("R² (test year 2025)")
ax.set_title("Model performance by city (out of sample)")
ax.grid(axis="y", alpha=0.3); ax.legend(fontsize=8.5)
fig.tight_layout(); fig.savefig("figures/fig12_city_r2.png", dpi=180)
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
fig, ax = plt.subplots(figsize=(7.6, 4.2))
ax.bar(range(1, 13), monthly_mae.reindex(range(1, 13)) / 1000, color="#e76f51", edgecolor="black", lw=0.4)
ax.set_xticks(range(1, 13)); ax.set_xticklabels(months)
ax.set_ylabel("Mean absolute error (kWh/m²/day)")
ax.set_xlabel("Month (test year 2025)")
ax.set_title("How prediction error changes across the year (random forest)")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig("figures/fig13_monthly_mae.png", dpi=180)
out = df.loc[test_mask, ["city", "date", TARGET]].copy()
out["predicted_ghi"] = p.round(0)
out.to_csv("results/predictions_2025.csv", index=False)
print("\nSaved: ml_metrics.csv, ml_percity_r2.json, ml_cv.json, ml_monthly_mae.json, figures 9-13")
