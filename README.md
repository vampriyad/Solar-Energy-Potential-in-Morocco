Solar Energy Potential in Morocco

Research project by **Riyad Khairoun**

A quantitative study of Morocco's solar energy resource using three years (2023–2026) of hourly
meteorological data for eight Moroccan cities, with machine-learning prediction models and a
photovoltaic (PV) yield estimation.

**Paper:** `Paper_Solar_Energy_Morocco.pdf` (19 pages, 13 figures, 8 tables)

## Cities studied

Dakhla, Ouarzazate, Errachidia, Agadir, Marrakech, Casablanca, Tangier, Tétouan.

## Key results

- Annual solar radiation (GHI) ranges from 1,828 kWh/m²/year (Tétouan) to 2,177 kWh/m²/year (Dakhla).
- Southern cities receive ~12% more solar radiation per year than the northern coast, with the gap
  concentrated in winter (driven by cloud cover).
- A gradient boosting model predicts daily solar radiation on unseen data with R² = 0.932
  (random forest: R² = 0.924; linear regression: R² = 0.612).
- A 1 MWp PV plant would produce 1,371–1,632 MWh/year depending on location.

## Repository structure

```
├── Paper_Solar_Energy_Morocco.pdf   ← the paper
├── scripts/
│   ├── 01_daily_dataset.py          ← builds the daily dataset from raw API data
│   ├── 02_analysis_figures.py       ← exploratory analysis and figures
│   ├── 03_ml_models.py              ← machine-learning models and evaluation
│   └── build_paper.py               ← generates the paper PDF
├── data/raw/                        ← raw hourly data (Open-Meteo / ERA5)
├── results/                         ← processed datasets and model outputs
└── figures/                         ← all figures used in the paper
```

## Reproducing the results

```bash
pip install pandas numpy matplotlib scikit-learn requests reportlab pypdf
python3 scripts/01_daily_dataset.py
python3 scripts/02_analysis_figures.py
python3 scripts/03_ml_models.py
python3 scripts/build_paper.py
```

## Data source

All data comes from the free **Open-Meteo Historical Weather API**, based on the ECMWF **ERA5**
reanalysis: https://open-meteo.com/en/docs/historical-weather-api (no account or API key required).
