# Solar Energy Potential in Morocco

This repository contains the independent research paper **Solar Energy Potential in Morocco: A Machine Learning Analysis of Eight Cities Using Three Years of Hourly Weather Data**.

## Research

This research examines Morocco's solar energy potential using three years of hourly solar radiation and weather data from eight Moroccan cities.

The study analyzes regional and seasonal variations in solar resources, evaluates machine learning methods for predicting solar radiation, and estimates photovoltaic electricity generation under different locations and conditions.

## Research Paper

**[Read the Full Research Paper](./Solar_Energy_Potential_in_Morocco.pdf)**

The complete research paper is included in this repository together with the supporting materials used in the study.

## Publication

This research has been independently conducted and publicly published through Zenodo.

**DOI:** 10.5281/zenodo.21895488

## Author

**Riyad Khairoun**  
Independent Researcher  
Morocco  
2026

## Copyright and License

This project and its contents are protected by copyright. The research paper, source code, datasets, figures, text, analysis, and other materials contained in this repository may not be copied, reproduced, modified, distributed, republished, or used without prior written permission from the author.

All rights to the original work are reserved by the author.

Permission may be granted by the author for specific uses upon written request.

## Thank You

Thank you for visiting this repository and taking an interest in this research on **solar energy potential in Morocco**.

---

**© 2026 Riyad Khairoun. All Rights Reserved.**

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
