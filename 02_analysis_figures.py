import json, os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
CITY_LAT = {
    "Ouarzazate": 30.92, "Dakhla": 23.71, "Marrakech": 31.63,
    "Casablanca": 33.57, "Tangier": 35.76, "Tetouan": 35.58,
    "Errachidia": 31.93, "Agadir": 30.42,
}
CITY_NAME = {
    "Ouarzazate": "Ouarzazate", "Dakhla": "Dakhla", "Marrakech": "Marrakech",
    "Casablanca": "Casablanca", "Tangier": "Tangier", "Tetouan": "Tétouan",
    "Errachidia": "Errachidia", "Agadir": "Agadir",
}
REGION = {
    "Ouarzazate": "South (Sahara)", "Dakhla": "Far South (Atlantic Sahara)",
    "Marrakech": "South (inland)", "Agadir": "South-West (Atlantic)",
    "Errachidia": "South-East (Saharan fringe)",
    "Casablanca": "North (Atlantic)", "Tangier": "North (Mediterranean)",
    "Tetouan": "North (Mediterranean)",
}
NORTH = ["Casablanca", "Tangier", "Tetouan"]
SOUTH = ["Ouarzazate", "Dakhla", "Marrakech", "Agadir", "Errachidia"]
COLORS = {"Ouarzazate": "#d62728", "Dakhla": "#bcbd22", "Marrakech": "#ff7f0e",
          "Agadir": "#e377c2", "Errachidia": "#8c564b",
          "Casablanca": "#2ca02c", "Tangier": "#1f77b4", "Tetouan": "#17becf"}

daily = pd.read_csv("results/daily_all.csv", parse_dates=["date"])
daily["lat"] = daily["city"].map(CITY_LAT)
os.makedirs("figures", exist_ok=True)
os.makedirs("results", exist_ok=True)
cities = list(CITY_LAT.keys())
monthly = daily.groupby(["city", "month"])["ghi_day"].mean() / 1000
fig, ax = plt.subplots(figsize=(8.6, 5.2))
for city in cities:
    ax.plot(range(1, 13), monthly[city].reindex(range(1, 13)), marker="o", ms=3,
            lw=1.7, color=COLORS[city], label=f"{CITY_NAME[city]} ({CITY_LAT[city]:.1f}°N)")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
ax.set_xlabel("Month")
ax.set_ylabel("Average daily solar radiation (kWh/m²/day)")
ax.set_title("Monthly solar radiation, eight Moroccan cities (2023 to 2025, ERA5 data)")
ax.grid(alpha=0.3); ax.legend(fontsize=7.5, ncol=2, loc="lower left")
fig.tight_layout(); fig.savefig("figures/fig1_monthly_ghi.png", dpi=180)
annual = (daily.groupby(["city", "year"])["ghi_day"].sum().groupby("city").mean() / 1000)
annual = annual.sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8.2, 4.8))
colors = [("#d62728" if c in SOUTH else "#1f77b4") for c in annual.index]
bars = ax.bar(range(len(annual)), annual.values, color=colors, edgecolor="black", lw=0.5)
ax.set_xticks(range(len(annual))); ax.set_xticklabels([CITY_NAME[c] for c in annual.index], rotation=22, ha="right")
ax.set_ylabel("Annual solar radiation (kWh/m²/year)")
ax.set_title("Total annual solar radiation (GHI), 2023 to 2025 average")
for b, v in zip(bars, annual.values):
    ax.text(b.get_x() + b.get_width()/2, v + 20, f"{v:.0f}", ha="center", fontsize=8.5)
ax.set_ylim(0, annual.max() * 1.14)
ax.grid(axis="y", alpha=0.3)
ax.legend(handles=[Patch(color="#d62728", label="Southern / Saharan cities"),
                   Patch(color="#1f77b4", label="Northern coastal cities")], fontsize=9)
fig.tight_layout(); fig.savefig("figures/fig2_annual_ghi.png", dpi=180)
def diurnal(city, months):
    h = json.load(open(f"data/raw/{city}.json"))["hourly"]
    t = pd.to_datetime(h["time"])
    df = pd.DataFrame({"time": t, "ghi": h["shortwave_radiation"]})
    df = df[df["time"].dt.month.isin(months)]
    df["hour"] = df["time"].dt.hour
    return df.groupby("hour")["ghi"].mean()
fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.2), sharey=True)
for ax, city in zip(axes.ravel(), ["Ouarzazate", "Dakhla", "Tangier", "Tetouan"]):
    ax.plot(diurnal(city, [7]).index, diurnal(city, [7]).values, lw=2, color="#d62728", label="July (summer)")
    ax.plot(diurnal(city, [1]).index, diurnal(city, [1]).values, lw=2, color="#1f77b4", label="January (winter)")
    ax.set_title(f"{CITY_NAME[city]} ({CITY_LAT[city]:.1f}°N)")
    ax.set_xlabel("Hour of day (local)")
    ax.grid(alpha=0.3); ax.legend(fontsize=8)
axes[0,0].set_ylabel("Solar radiation (W/m²)"); axes[1,0].set_ylabel("Solar radiation (W/m²)")
fig.suptitle("Diurnal solar radiation profile, summer vs winter", y=1.02, fontsize=13)
fig.tight_layout(); fig.savefig("figures/fig3_diurnal.png", dpi=180, bbox_inches="tight")
cloud_m = daily.groupby(["city", "month"])["cloud_mean"].mean()
fig, ax = plt.subplots(figsize=(8.6, 5.0))
for city in cities:
    ax.plot(range(1, 13), cloud_m[city].reindex(range(1, 13)), marker="o", ms=3,
            lw=1.7, color=COLORS[city], label=CITY_NAME[city])
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
ax.set_xlabel("Month"); ax.set_ylabel("Mean cloud cover (%)")
ax.set_title("Monthly cloud cover, eight Moroccan cities")
ax.grid(alpha=0.3); ax.legend(fontsize=7.5, ncol=2, loc="upper center")
fig.tight_layout(); fig.savefig("figures/fig4_cloud.png", dpi=180)
fig, ax = plt.subplots(figsize=(8.2, 5.0))
for city in cities:
    x = np.sort(daily.loc[daily["city"] == city, "ghi_day"].values / 1000)
    y = np.arange(1, len(x) + 1) / len(x) * 100
    ax.plot(x, y, lw=1.8, color=COLORS[city], label=CITY_NAME[city])
ax.set_xlabel("Daily solar radiation (kWh/m²/day)")
ax.set_ylabel("Share of days below this value (%)")
ax.set_title("Cumulative distribution of daily solar radiation (2023 to 2025)")
ax.grid(alpha=0.3); ax.legend(fontsize=7.5, ncol=2, loc="lower right")
fig.tight_layout(); fig.savefig("figures/fig5_cdf.png", dpi=180)
EFF, PR = 0.15, 0.75
pv_m2  = annual * EFF * PR
pv_mwp = annual * PR * 1000 / 1000
fig, ax = plt.subplots(figsize=(8.2, 4.8))
order = pv_m2.sort_values(ascending=False)
colors = [("#d62728" if c in SOUTH else "#1f77b4") for c in order.index]
bars = ax.bar(range(len(order)), order.values, color=colors, edgecolor="black", lw=0.5)
ax.set_xticks(range(len(order))); ax.set_xticklabels([CITY_NAME[c] for c in order.index], rotation=22, ha="right")
ax.set_ylabel("PV electricity (kWh/m²/year)")
ax.set_title(f"Estimated PV output (η = {EFF:.0%}, performance ratio = {PR:.0%})")
for b, v, c in zip(bars, order.values, order.index):
    ax.text(b.get_x() + b.get_width()/2, v + 1.2, f"{v:.0f}", ha="center", fontsize=8.5)
    ax.text(b.get_x() + b.get_width()/2, v - 11, f"{pv_mwp[c]:.0f} MWh/MWp",
            ha="center", fontsize=7.5, color="white", fontweight="bold")
ax.set_ylim(0, order.max() * 1.16)
ax.grid(axis="y", alpha=0.3)
ax.legend(handles=[Patch(color="#d62728", label="Southern / Saharan cities"),
                   Patch(color="#1f77b4", label="Northern coastal cities")], fontsize=9)
fig.tight_layout(); fig.savefig("figures/fig6_pv_output.png", dpi=180)
corr_cols = ["ghi_day", "day_of_year", "temp_mean", "temp_max", "temp_min",
             "rh_mean", "wind_mean", "cloud_mean", "lat"]
labels = ["GHI/day", "Day of year", "T mean", "T max", "T min", "RH", "Wind", "Cloud", "Latitude"]
C = daily[corr_cols].corr()
fig, ax = plt.subplots(figsize=(7.2, 6.0))
im = ax.imshow(C.values, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)
ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels, fontsize=9)
for i in range(len(labels)):
    for j in range(len(labels)):
        ax.text(j, i, f"{C.values[i,j]:.2f}", ha="center", va="center", fontsize=7,
                color="white" if abs(C.values[i,j]) > 0.6 else "black")
fig.colorbar(im, ax=ax, label="Pearson correlation", shrink=0.8)
ax.set_title("Correlation matrix of daily variables (all cities pooled)")
fig.tight_layout(); fig.savefig("figures/fig7_corr.png", dpi=180)
ann_y = (daily.groupby(["city", "year"])["ghi_day"].sum() / 1000).unstack()
ann_y = ann_y.reindex(annual.index)
x = np.arange(len(annual.index)); w = 0.27
fig, ax = plt.subplots(figsize=(8.2, 4.8))
for i, yr in enumerate([2023, 2024, 2025]):
    ax.bar(x + (i - 1) * w, ann_y[yr].values, w, label=str(yr),
           color=["#aec7e8", "#7f7f7f", "#ffbb78"][i], edgecolor="black", lw=0.4)
ax.set_xticks(x); ax.set_xticklabels([CITY_NAME[c] for c in annual.index], rotation=22, ha="right")
ax.set_ylabel("Annual solar radiation (kWh/m²/year)")
ax.set_title("Year by year total solar radiation (2023, 2024, 2025)")
ax.grid(axis="y", alpha=0.3); ax.legend(title="Year")
fig.tight_layout(); fig.savefig("figures/fig8_years.png", dpi=180)
summer = daily[daily["month"].isin([6, 7, 8])].groupby("city")["ghi_day"].mean() / 1000
winter = daily[daily["month"].isin([12, 1, 2])].groupby("city")["ghi_day"].mean() / 1000
spring = daily[daily["month"].isin([3, 4, 5])].groupby("city")["ghi_day"].mean() / 1000
autumn = daily[daily["month"].isin([9, 10, 11])].groupby("city")["ghi_day"].mean() / 1000
dni_ann = (daily.groupby(["city", "year"])["dni_day"].sum().groupby("city").mean() / 1000)
summary = pd.DataFrame({
    "Latitude": daily.groupby("city")["lat"].first(),
    "Region": daily.groupby("city")["city"].first().map(REGION),
    "Annual_GHI_kWh_m2": annual.round(0),
    "Annual_DNI_kWh_m2": dni_ann.round(0),
    "Spring_daily_GHI": spring.round(2),
    "Summer_daily_GHI": summer.round(2),
    "Autumn_daily_GHI": autumn.round(2),
    "Winter_daily_GHI": winter.round(2),
    "Mean_temp_C": daily.groupby("city")["temp_mean"].mean().round(1),
    "Mean_cloud_%": daily.groupby("city")["cloud_mean"].mean().round(1),
    "Sun_hours_day": daily.groupby("city")["sun_hours"].mean().round(1),
    "PV_per_m2_kWh": pv_m2.round(0),
    "PV_per_MWp_MWh": pv_mwp.round(0),
})
summary.to_csv("results/city_summary.csv")
print(summary.round(1).to_string())
monthly_tbl = (daily.groupby(["city", "month"])["ghi_day"].mean() / 1000).unstack()
monthly_tbl.columns = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly_tbl = monthly_tbl.round(2)
monthly_tbl.to_csv("results/monthly_means.csv")
print("\nMonthly means saved -> results/monthly_means.csv")
ann_y.round(0).to_csv("results/yearly_totals.csv")
pcts = {}
for city in cities:
    s = daily.loc[daily["city"] == city, "ghi_day"] / 1000
    pcts[city] = s.quantile([0.05, 0.25, 0.5, 0.75, 0.95])
pct_df = pd.DataFrame(pcts).T.round(2)
pct_df.to_csv("results/percentiles.csv")
print("\nPercentiles -> results/percentiles.csv")
cloud_m.unstack().round(1).to_csv("results/cloud_monthly.csv")
keys = {
    "annual_ghi_kwh_m2": {c: float(annual[c]) for c in annual.index},
    "south_mean_annual_ghi": float(annual[SOUTH].mean()),
    "north_mean_annual_ghi": float(annual[NORTH].mean()),
    "north_south_ratio": float(annual[SOUTH].mean() / annual[NORTH].mean()),
    "max_city": annual.idxmax(), "min_city": annual.idxmin(),
    "south_cities": SOUTH, "north_cities": NORTH,
    "winter_Tetouan": float(winter["Tetouan"]), "winter_Ouarzazate": float(winter["Ouarzazate"]),
    "winter_Agadir": float(winter["Agadir"]), "winter_Errachidia": float(winter["Errachidia"]),
    "winter_Dakhla": float(winter["Dakhla"]), "winter_Tangier": float(winter["Tangier"]),
    "summer_Ouarzazate": float(summer["Ouarzazate"]), "summer_Tetouan": float(summer["Tetouan"]),
    "cloud_Tetouan": float(daily[daily.city=='Tetouan']['cloud_mean'].mean()),
    "cloud_Dakhla": float(daily[daily.city=='Dakhla']['cloud_mean'].mean()),
    "pv_m2_kwh": {c: float(pv_m2[c]) for c in pv_m2.index},
    "pv_mwp_mwh": {c: float(pv_mwp[c]) for c in pv_mwp.index},
    "p95_p5_Tetouan": {"p5": float(pcts["Tetouan"][0.05]), "p95": float(pcts["Tetouan"][0.95])},
    "p95_p5_Ouarzazate": {"p5": float(pcts["Ouarzazate"][0.05]), "p95": float(pcts["Ouarzazate"][0.95])},
    "dni_Ouarzazate": float(dni_ann["Ouarzazate"]),
    "corr_cloud_ghi": float(C.loc["ghi_day", "cloud_mean"]),
    "corr_temp_ghi": float(C.loc["ghi_day", "temp_mean"]),
}
json.dump(keys, open("results/key_numbers.json", "w"), indent=2)
print("\nSaved key numbers -> results/key_numbers.json")
