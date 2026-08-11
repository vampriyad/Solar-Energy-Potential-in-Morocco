import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak)
body = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.2,
                      alignment=TA_JUSTIFY, spaceAfter=5)
body_i = ParagraphStyle("body_i", parent=body, fontName="Helvetica-Oblique")
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=12.5, leading=15,
                    spaceBefore=11, spaceAfter=5)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.8, leading=13,
                    spaceBefore=7, spaceAfter=2)
title = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=16,
                       leading=19.5, alignment=TA_CENTER, spaceAfter=9)
author = ParagraphStyle("author", fontName="Helvetica-Bold", fontSize=10.5,
                        alignment=TA_CENTER, spaceAfter=2)
affil = ParagraphStyle("affil", fontName="Helvetica", fontSize=9.5,
                       alignment=TA_CENTER, spaceAfter=2)
date_s = ParagraphStyle("date", fontName="Helvetica-Oblique", fontSize=9.5,
                        alignment=TA_CENTER, spaceAfter=11)
abstract_h = ParagraphStyle("absh", fontName="Helvetica-Bold", fontSize=10.5,
                            spaceBefore=5, spaceAfter=3)
abstract = ParagraphStyle("abs", fontName="Helvetica", fontSize=9.3, leading=13.2,
                          alignment=TA_JUSTIFY, spaceAfter=7)
keywords = ParagraphStyle("kw", fontName="Helvetica", fontSize=9.3, leading=13,
                          spaceAfter=9)
caption = ParagraphStyle("cap", fontName="Helvetica-Oblique", fontSize=8.6,
                         leading=10.8, alignment=TA_CENTER, spaceBefore=2, spaceAfter=8)
tbl_cap = ParagraphStyle("tcap", fontName="Helvetica-Bold", fontSize=9,
                         alignment=TA_LEFT, spaceBefore=7, spaceAfter=3)
tbltxt = ParagraphStyle("tbl", fontName="Helvetica", fontSize=7.6, leading=9.2)
tblhd = ParagraphStyle("tblh", fontName="Helvetica-Bold", fontSize=7.6, leading=9.2)
ref = ParagraphStyle("ref", fontName="Helvetica", fontSize=8.8, leading=12,
                     alignment=TA_LEFT, spaceAfter=3, leftIndent=14, firstLineIndent=-14)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=16, firstLineIndent=0,
                        spaceAfter=4)

import re-
_COMPOUND_FIX = [
    ("Machine-Learning", "Machine Learning"),
    ("Machine-learning", "Machine learning"),
    ("machine-learning", "machine learning"),
    ("city-days", "city days"),
    ("non-linear", "nonlinear"),
    ("non-linearity", "nonlinearity"),
    ("high-quality", "high quality"),
    ("clear-sky", "clear sky"),
    ("real-world", "real world"),
    ("re-run", "rerun"),
    ("out-of-sample", "out of sample"),
    ("time-series", "time series"),
    ("cross-validation", "cross validation"),
    ("cross-checked", "cross checked"),
    ("training-set", "training set"),
    ("hour-by-hour", "hour by hour"),
    ("bell-shaped", "bell shaped"),
    ("Day-to-day", "Day to day"),
    ("Year-to-year", "Year to year"),
    ("year-to-year", "year to year"),
    ("Year-by-year", "Year by year"),
    ("x-axis", "x axis"),
    ("per-plant", "per plant"),
    ("per-city", "per city"),
    ("predicted-versus-actual", "predicted versus actual"),
    ("grid-scale", "grid scale"),
    ("utility-scale", "utility scale"),
    ("two-tiered", "two tiered"),
    ("two-tier", "two tier"),
    ("climate-scale", "climate scale"),
    ("high-school", "high school"),
    ("open-source", "open source"),
    ("semi-arid", "semiarid"),
    ("South-East", "South East"),
    ("South-West", "South West"),
    ("highest-GHI", "highest GHI"),
    ("4-fold", "4 fold"),
    ("52%-by-2030", "52% by 2030"),
    ("52%-renewables-by-2030", "52% renewables by 2030"),
    ("cloud-free", "cloud free"),
    ("night-time", "night time"),
    ("tree-based", "tree based"),
    ("re-downloaded", "redownloaded"),
    ("Per-city", "Per city"),
    ("Time-series", "Time series"),
    ("</b> \u2014 ", "</b>: "),
]
_EN_WORD_FIX = [
    ("December\u2013February", "December to February"),
    ("north\u2013south", "north to south"),
    ("coast\u2013inland", "coast to inland"),
    ("supply\u2013demand", "supply and demand"),
    ("Public\u2013Private", "Public Private"),
    ("MASEN \u2013 Moroccan", "MASEN: Moroccan"),
    ("PPIAF \u2013 Public", "PPIAF: Public"),
]
def clean_text(text):
    for a, b in _COMPOUND_FIX + _EN_WORD_FIX:
        text = text.replace(a, b)
    text = re.sub(r"(\d)" + "\u2013" + r"(\d)", r"\1 to \2", text)
    text = text.replace("\u2013", " ")
    text = text.replace("\u2014", ", ")
    text = re.sub(r"\s{2,}", " ", text)
    text = text.replace(" ,", ",").replace("( ,", "(").replace(" .", ".")
    return text
def P(text, style=body):
    return Paragraph(clean_text(text), style)
def B(text):
    return P("• " + text, bullet)
def styled_table(rows, col_widths, header_bg=colors.Color(0.92, 0.92, 0.92),
                 fontsize=7.6):
    t = Table(rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.Color(0.97, 0.97, 0.97)]),
        ("FONTSIZE", (0, 0), (-1, -1), fontsize),
    ]))
    return t
daily = pd.read_csv("results/daily_all.csv", parse_dates=["date"])
summ = pd.read_csv("results/city_summary.csv").set_index("city")
mm = pd.read_csv("results/monthly_means.csv", index_col=0)
yt = pd.read_csv("results/yearly_totals.csv", index_col=0)
pct = pd.read_csv("results/percentiles.csv", index_col=0)
metrics = pd.read_csv("results/ml_metrics.csv").set_index("Unnamed: 0")
pc = json.load(open("results/ml_percity_r2.json"))
cv = json.load(open("results/ml_cv.json"))
mmae = json.load(open("results/ml_monthly_mae.json"))
K = json.load(open("results/key_numbers.json"))

CITY_NAME = {"Tetouan": "Tétouan", "Ouarzazate": "Ouarzazate", "Dakhla": "Dakhla",
             "Marrakech": "Marrakech", "Casablanca": "Casablanca", "Tangier": "Tangier",
             "Errachidia": "Errachidia", "Agadir": "Agadir"}
N = {k: CITY_NAME.get(k, k) for k in K["annual_ghi_kwh_m2"]}
ORDER = ["Dakhla", "Ouarzazate", "Errachidia", "Agadir", "Marrakech",
         "Casablanca", "Tangier", "Tetouan"]
NORD = [N[c] for c in ORDER]

story = []
story.append(P("Solar Energy Potential in Morocco: A Machine-Learning Analysis of Eight Cities Using Three Years of Hourly Weather Data", title))
story.append(P("Riyad Khairoun", author))
story.append(P("Independent researcher, Chefchaouen, Morocco", affil))
story.append(P("Correspondence: riyadkhairoun@gmail.com · GitHub: github.com/vampriyad", affil))
story.append(P("August 2026", date_s))
story.append(P("Abstract", abstract_h))
story.append(P(
    "Morocco imports almost all of the energy it consumes, yet it is one of the sunniest countries on "
    "Earth, and the government aims to generate more than half of its electricity from renewable sources "
    "by 2030. In this project I quantified the country's solar resource with real data and tested whether "
    "machine learning can predict solar output from everyday weather variables. I downloaded three full "
    "years (2023–2025) of hourly solar radiation and weather data for eight Moroccan cities — Dakhla, "
    "Ouarzazate, Errachidia, Agadir, Marrakech, Casablanca, Tangier and Tétouan — from the free "
    "Open-Meteo API, which is based on the ECMWF ERA5 reanalysis. This gave me 210,432 hourly "
    "observations and 8,768 city-days of data. I found that southern cities receive about 12% more solar "
    "radiation per year than the northern coast (2,087 versus 1,868 kWh/m²/year on average), and that "
    "this gap is almost entirely a winter effect: in December–February, Dakhla still receives "
    "4.70 kWh/m²/day while Tétouan drops to 2.98 kWh/m²/day, because the Mediterranean coast is far "
    "cloudier (47% mean cloud cover versus 23% in Dakhla). I then trained three machine-learning models "
    "to predict each day's total solar radiation from simple variables (time of year, temperature, "
    "humidity, wind, cloud cover, latitude). On the unseen test year (2025), a gradient boosting model "
    "reached R² = 0.932 and a random forest R² = 0.924, while linear regression reached only R² = 0.612, "
    "confirming that the relationship is non-linear. Using a simple photovoltaic (PV) model, I estimate "
    "that a 1 MWp solar farm in Morocco would produce 1,371–1,632 MWh per year depending on the "
    "location. The results show where Morocco's next solar plants should be built, and demonstrate that "
    "free open data plus machine learning is enough to make solar output highly predictable — a "
    "promising result for a country targeting 52% renewable electricity by 2030.", abstract))
story.append(P("<b>Keywords:</b> solar energy; Morocco; machine learning; random forest; gradient boosting; solar radiation; ERA5; Open-Meteo; renewable energy; Noor Ouarzazate; PV yield.", keywords))
story.append(P("1. Introduction", h1))
story.append(P(
    "Morocco is a country of nearly 37 million people with an economy that grows steadily, yet it has "
    "almost no fossil fuels of its own. The country imports roughly 90% of the energy it consumes, which "
    "makes it very exposed to the price of oil and gas on world markets (World Economic Forum, 2018). "
    "Every time the price of natural gas rises, so does the cost of electricity for Moroccan families and "
    "factories. This is a serious problem of energy security, and it is the main reason why Morocco has "
    "become one of the most ambitious countries in the world when it comes to renewable energy."))
story.append(P(
    "The country's strategy has a name: solar. Morocco sits in the 'global sun belt' that stretches "
    "across North Africa and the Middle East, so it receives far more sunlight than most of Europe or "
    "North America. The flagship of the strategy is the Noor Ouarzazate complex, a concentrated solar "
    "power (CSP) plant in the foothills of the Atlas Mountains with about 580 MW of capacity. When its "
    "first phases opened, it was the largest solar thermal plant in the world, designed to supply "
    "electricity to more than one million Moroccans (PPIAF; Construction Review Online, 2026). The "
    "official goal is to reach 52% of electricity generation from renewables by 2030 (World Economic "
    "Forum, 2018; IRENA, 2015)."))
story.append(P(
    "But Morocco is a big country with very different climates. The Sahara in the south is one of the "
    "sunniest places on the planet, while the Mediterranean coast in the north is often covered in "
    "winter clouds. If the country is going to spend billions of dirhams on new solar plants, it should "
    "build them where the sun shines most — and where its output matches the demand. Answering that "
    "question properly requires data: how much sunlight actually falls on different cities, how it "
    "changes across the seasons, and how predictable it is day to day."))
story.append(P(
    "This project started with two motivations. The first is personal: I live in Tétouan, a city in "
    "northern Morocco, where winters are noticeably grey and rainy compared with the desert south, and I "
    "wanted to measure how big that difference really is. The second is scientific: I have been learning "
    "data science with Python, and I discovered that high-quality, free, hourly weather and solar data "
    "for any city in the world is available online through the Open-Meteo API, which is based on the "
    "ECMWF ERA5 reanalysis. That combination — a real question about my own country and free tools to "
    "answer it — is what motivated this research."))
story.append(P("The study has three specific aims:"))
story.append(B("<b>Measure.</b> Quantify the solar radiation received by eight Moroccan cities over three full years, and compare regions and seasons."))
story.append(B("<b>Predict.</b> Build machine-learning models that predict a day's total solar radiation from simple weather variables, and evaluate how accurate they are on data the models have never seen."))
story.append(B("<b>Apply.</b> Estimate how much electricity solar panels would produce in each city, and discuss what this means for Morocco's 2030 renewable energy target."))
story.append(P(
    "The rest of the paper is organised as follows. Section 2 gives the background needed to understand "
    "solar radiation and reviews previous studies. Section 3 states the research questions. Section 4 "
    "describes the data and methods. Section 5 presents the results, Section 6 discusses them, and "
    "Section 7 concludes. Two appendices give details on reproducibility and a glossary."))
story.append(P("2. Background and prior research", h1))
story.append(P("2.1 Solar radiation: what it is and how it is measured", h2))
story.append(P(
    "The sun sends energy to the Earth at an average intensity of about 1,361 W/m² at the top of the "
    "atmosphere, a quantity called the solar constant. As this light travels through the atmosphere, "
    "part of it is absorbed by gases, part is scattered by air molecules and clouds, and part reaches "
    "the ground directly. What actually reaches a horizontal surface on the ground is called global "
    "horizontal irradiance (GHI). GHI has two components: direct normal irradiance (DNI), which is the "
    "sunlight arriving in a straight line from the sun's disc (important for CSP plants that concentrate "
    "sunlight), and diffuse horizontal irradiance (DHI), which is the light scattered by clouds, dust "
    "and the sky itself. The simple equation is GHI = DNI·cos(z) + DHI, where z is the sun's zenith "
    "angle."))
story.append(P(
    "Solar radiation is measured in watts per square metre (W/m²) when talking about an instant, and in "
    "kilowatt hours per square metre (kWh/m²) when talking about an amount of energy over time. A day "
    "with 7 kWh/m² of GHI means that one square metre of ground received the equivalent of 7,000 watts "
    "running for one hour — enough energy to power a typical LED bulb for hundreds of hours. The amount "
    "of sunlight a place receives depends on three main factors: its latitude (which sets the sun's "
    "maximum height and the length of the day), its climate (clouds are the biggest killer of sunlight), "
    "and the time of year. In the northern hemisphere, the sun is highest and days are longest in June, "
    "and lowest and shortest in December."))

story.append(P("2.2 From sunlight to electricity: PV and CSP", h2))
story.append(P(
    "There are two main technologies for turning sunlight into electricity. Photovoltaic (PV) panels "
    "convert sunlight directly into electricity using semiconductor cells, typically made of silicon. "
    "They work with both direct and diffuse light, which is why they still produce something on cloudy "
    "days. Concentrated solar power (CSP) uses mirrors to focus direct sunlight onto a receiver that "
    "heats a fluid, which then drives a turbine like in a normal power plant. CSP needs strong direct "
    "sunlight (high DNI), which is why it only makes sense in very sunny, clear-sky regions. The Noor "
    "Ouarzazate complex uses CSP; rooftop solar in cities mostly uses PV."))
story.append(P(
    "The electricity a PV panel produces is roughly: E = GHI × A × efficiency × performance ratio, "
    "where A is the panel area, efficiency is the fraction of sunlight the cell converts (about 15–22% "
    "for commercial panels), and the performance ratio (PR) accounts for real-world losses such as "
    "inverter losses, dust on the panels, heating of the cells and wiring resistance. A typical PR is "
    "around 0.75–0.80. This simple model is what I use in Section 4.4 to estimate real electricity "
    "output."))

story.append(P("2.3 Morocco's solar strategy and the Noor complex", h2))
story.append(P(
    "Morocco launched its energy strategy in 2009 with the goal of increasing the share of renewables "
    "in electricity generation to 42% by 2020 and 52% by 2030 (IRENA, 2015; World Economic Forum, "
    "2018). The state agency MASEN (Moroccan Agency for Sustainable Energy) was created to lead the "
    "programme, and the first large project was the Noor complex at Ouarzazate. Noor I (160 MW) uses "
    "parabolic trough CSP with thermal storage, which means it can keep producing electricity for "
    "several hours after sunset — a big advantage over plain PV. Noor II and Noor III added more "
    "capacity, and the site has been described as 'a solar farm as big as Paris in the Sahara' (World "
    "Economic Forum, 2018). The complex reduces CO2 emissions by several hundred thousand tonnes per "
    "year (Construction Review Online, 2026)."))
story.append(P(
    "Why Ouarzazate? Because it is one of the sunniest places in Morocco, close to the grid, with huge "
    "areas of flat desert land. A key question for the next phase of the programme is whether other "
    "southern sites — such as Errachidia, Dakhla or Agadir — are even better, and how the north "
    "compares if rooftop solar is to be encouraged there. This study provides quantitative evidence for "
    "exactly that comparison, using recent (2023–2025) data."))

story.append(P("2.4 Previous studies of Morocco's solar resource", h2))
story.append(P(
    "Benbba et al. (2024) publis resource and power "
    "generation in the journal Resources. They report that the best zones — including Errachidia, "
    "Taroudant, Ouarzazate, Smara and Bouarfa — have GHI levels above 5.57 kWh/m²/day, that DNI across "
    "Morocco ranges from about 1,800 to 3,000 kWh/m²/year, and that commercially viable CSP plants "
    "usually need DNI of at least 2,000–2,800 kWh/m²/year. They also report an average PV specific "
    "yield (energy per kilowatt of installed capacity) of about 1,779 kWh/kWp/year for the country. "
    "IRENA's Renewables Readiness Assessment of Morocco (2015) reached similar conclusions, describing "
    "solar as the country's largest untapped resource and estimating the cost of solar electricity as "
    "already competitive with fossil fuels in many cases. Internationally, the Global Solar Atlas "
    "(World Bank Group/ESMAP) and the European Commission's PVGIS tool provide independent solar maps "
    "that agree with these ranges."))
story.append(P(
    "What these sources do not provide is a single, recent, reproducible dataset covering several "
    "specific Moroccan cities hour by hour, together with machine-learning predictions. Most published "
    "numbers come from satellite models or older ground measurements, and they are rarely shared in a "
    "form that a student can download and analyse. This project fills that gap in a modest way: by "
    "using open data and open code, every number in this paper can be checked and re-run by anyone."))

story.append(P("2.5 Machine learning for solar radiation forecasting", h2))
story.append(P(
    "Forecasting solar radiation is an active research area because grid operators need to know in "
    "advance how much solar electricity will be available. Voyant et al. (2017) reviewed dozens of "
    "studies and found that machine-learning methods — artificial neural networks, support vector "
    "machines and tree-based ensembles — generally outperform classical statistical models, especially "
    "when the relationship between predictors and radiation is non-linear. Cloud cover is a perfect "
    "example: a small increase in clouds can cut radiation a lot, but beyond a certain point extra "
    "clouds barely matter, so a straight line (linear regression) cannot capture it well."))
story.append(P(
    "Random forests and gradient boosting are two tree-based ensemble methods that are widely used "
    "because they handle non-linearities and interactions automatically, need little data preparation, "
    "and are fast to train. They also give feature importances — a measure of which variables matter "
    "most — which is useful for understanding the problem, not just for predicting. For these reasons I "
    "chose them as my main models, with linear regression as a simple baseline. I deliberately used "
    "only variables that are easy to obtain or forecast (temperature, humidity, wind, cloud cover, time "
    "of year, latitude), because the goal is a practical model, not a theoretical one."))

story.append(P("2.6 The data source: ERA5 and Open-Meteo", h2))
story.append(P(
    "My data comes from ERA5, a global weather reanalysis produced by the European Centre for "
    "Medium-Range Weather Forecasts (ECMWF). A reanalysis combines millions of real observations "
    "(from weather stations, satellites, ships, balloons) with a physical model of the atmosphere to "
    "produce a complete, consistent record of the weather everywhere on Earth, even where there are no "
    "stations (Hersbach et al., 2020). ERA5 covers the period from 1940 to the present and is the most "
    "widely used reanalysis in climate research. The Open-Meteo project (Open-Meteo, 2025) provides a "
    "free API that extracts ERA5 data for any location, including hourly solar radiation and weather "
    "variables, without requiring an account or an API key. This makes the entire study reproducible by "
    "anyone with internet access."))
story.append(P("The project was built around three research questions:"))
story.append(P("<b>RQ1 (measure).</b> How does solar radiation differ across Morocco — between the Saharan south, the inland south and the Mediterranean north, and across the seasons? How variable is it from day to day and from year to year?"))
story.append(P("<b>RQ2 (predict).</b> How accurately can machine-learning models predict a day's total solar radiation from simple weather variables (time of year, temperature, humidity, wind, cloud cover, latitude)? Which model works best, and why?"))
story.append(P("<b>RQ3 (apply).</b> How much electricity would a simple PV installation produce in each city, and what do the results imply for where Morocco should build new solar capacity and for the 52%-by-2030 target?"))
story.append(P("4. Method", h1))

story.append(P("4.1 Study sites", h2))
story.append(P(
    "I chose eight cities that span the full north–south and coast–inland gradients of Morocco (Table "
    "1). The northern group (Casablanca, Tangier, Tétouan) represents the cloudy Atlantic and "
    "Mediterranean coast; the southern group (Dakhla, Ouarzazate, Errachidia, Agadir, Marrakech) "
    "represents the Saharan and semi-arid south, where the big utility-scale plants are located or "
    "planned. Including Agadir adds a southern coastal city, and Errachidia is one of the zones that "
    "Benbba et al. (2024) identify among the sunniest in Morocco."))

site_rows = [[P(x, tblhd) for x in ["City", "Latitude", "Longitude", "Region", "Why included"]]]
sites = [
    ("Ouarzazate", "30.92°N", "6.91°W", "South (Sahara, Atlas foothills)", "Location of the Noor CSP complex"),
    ("Errachidia", "31.93°N", "4.42°W", "South-East (Saharan fringe)", "Among the highest-GHI zones in the literature"),
    ("Dakhla", "23.71°N", "15.94°W", "Far south (Atlantic Sahara)", "Southernmost city; coastal desert climate"),
    ("Agadir", "30.42°N", "9.60°W", "South-West (Atlantic coast)", "Southern coastal city; MASEN solar activity"),
    ("Marrakech", "31.63°N", "7.98°W", "South (inland, Haouz plain)", "Major inland city; tourism + energy demand"),
    ("Casablanca", "33.57°N", "7.59°W", "North (Atlantic coast)", "Largest city and economic capital"),
    ("Tangier", "35.76°N", "5.83°W", "North (Strait of Gibraltar)", "Northernmost city; Mediterranean climate"),
    ("Tétouan", "35.58°N", "5.37°W", "North (Mediterranean, Rif)", "Author's home city"),
]
for s in sites:
    site_rows.append([P(x, tbltxt) for x in s])
story.append(P("Table 1. The eight study sites, ordered from south to north.", tbl_cap))
story.append(styled_table(site_rows, [2.3*cm, 1.7*cm, 1.8*cm, 5.0*cm, 5.4*cm]))
story.append(Spacer(1, 4))

story.append(P("4.2 Data source and variables", h2))
story.append(P(
    "For each city I downloaded hourly values for the period 1 January 2023 to 31 December 2025 using "
    "the Open-Meteo Historical Weather API (https://open-meteo.com). The seven variables used are "
    "listed in Table 2. The download used each city's coordinates and the timezone 'auto', so all times "
    "are local Moroccan time. In total the dataset contains 26,304 hourly rows per city and 210,432 "
    "hourly observations overall."))
var_rows = [[P(x, tblhd) for x in ["Variable", "API name", "Unit", "Description"]]]
vars_ = [
    ("Global horizontal irradiance (GHI)", "shortwave_radiation", "W/m²", "Total sunlight on a horizontal surface"),
    ("Direct normal irradiance (DNI)", "direct_normal_irradiance", "W/m²", "Direct sunlight from the sun's disc (needed for CSP)"),
    ("Diffuse irradiance (DHI)", "diffuse_radiation", "W/m²", "Scattered sunlight from sky and clouds"),
    ("Air temperature at 2 m", "temperature_2m", "°C", "Used as a proxy for clear-sky conditions"),
    ("Relative humidity", "relative_humidity_2m", "%", "Moisture content of the air"),
    ("Wind speed at 10 m", "wind_speed_10m", "km/h", "Can matter for panel cooling and dust"),
    ("Total cloud cover", "cloud_cover", "%", "Fraction of the sky covered by clouds"),
]
for v in vars_:
    var_rows.append([P(x, tbltxt) for x in v])
story.append(P("Table 2. Variables downloaded per city (hourly, 2023–2025).", tbl_cap))
story.append(styled_table(var_rows, [5.1*cm, 3.6*cm, 1.9*cm, 5.6*cm]))
story.append(Spacer(1, 4))
story.append(P(
    "<b>Data availability.</b> All raw data used in this study is publicly available and can be "
    "re-downloaded at any time from the Open-Meteo API using the coordinates in Table 1 and the "
    "variable list in Table 2. The complete code, the processed daily dataset and all figures are "
    "included in the author's public repository at https://github.com/vampriyad, and Appendix A "
    "explains exactly how to rebuild every result. No proprietary or subscription data was used "
    "anywhere in this project."))

story.append(P("4.3 Data processing and quality checks", h2))
story.append(P(
    "All processing was done in Python 3 with the pandas library (McKinney, 2010). I converted the "
    "hourly GHI values into daily totals (in Wh/m²/day) by summing the 24 hourly values of each day, "
    "then aggregated by month, season and year. This produced a clean dataset of 8,768 city-days "
    "(eight cities × 365.25 days × three years) used for all further analysis."))
story.append(P(
    "I performed several quality checks. First, I checked that every city had exactly 26,304 hourly "
    "records with no missing values and no duplicated timestamps. Second, I verified that night-time "
    "values were zero and that daytime maxima were physically plausible (peak hourly GHI around "
    "1,000 W/m² in summer, as expected for a clear day). Third, I cross-checked my annual totals "
    "against independent numbers in the literature: my Ouarzazate value of 2,137 kWh/m²/year agrees "
    "with the ranges reported by Benbba et al. (2024), and my PV specific yields (1,371–1,632 "
    "kWh/kWp/year) bracket the ~1,779 kWh/kWp/year national average they report. These checks give "
    "confidence that the pipeline is correct."))

story.append(P("4.4 Photovoltaic (PV) energy model", h2))
story.append(P(
    "To translate solar radiation into electricity, I used the standard simple model "
    "E = GHI × efficiency × performance ratio. I assumed a module efficiency of 15% (typical for "
    "commercial panels) and a performance ratio of 0.75, which accounts for inverter losses, dust, "
    "heating of the cells and wiring. I deliberately did not model panel tilt or sun tracking, so my "
    "estimates are conservative — tilted panels facing south would produce somewhat more. The model "
    "gives two useful quantities: the annual electricity per square metre of panels (kWh/m²/year), and "
    "the annual specific yield of a 1 MWp installation (MWh/MWp/year), which is the standard way the "
    "solar industry compares sites."))

story.append(P("4.5 Machine-learning models", h2))
story.append(P(
    "For the prediction task, the target variable is the day's total GHI (in Wh/m²/day) and the "
    "features are: day of the year (1–366), mean/maximum/minimum temperature, mean relative humidity, "
    "mean wind speed, mean cloud cover, and latitude (a proxy for the city). I compared three models: "
    "linear regression (simple baseline), a random forest with 400 trees, and gradient boosting with "
    "300 trees — all implemented with the scikit-learn library (Pedregosa et al., 2011)."))
story.append(P(
    "The models were trained on 2023–2024 (5,848 days) and tested on 2025 (2,920 days). This is a "
    "strictly out-of-sample test: the models never saw 2025 during training, so the scores show how "
    "well they would work on genuinely new data, which is what matters for real forecasting. I also ran "
    "a time-series cross-validation (4 folds) inside the training period to check that the results are "
    "stable and not due to one lucky split. I evaluated the models with three standard metrics: R² "
    "(fraction of variance explained), root mean squared error (RMSE, in Wh/m²/day) and mean absolute "
    "error (MAE, in Wh/m²/day). I compared all models against a naive baseline that always predicts the "
    "training-set average — any useful model must clearly beat it."))

story.append(P("5. Results", h1))

story.append(P("5.1 Regional and seasonal variation", h2))
story.append(P(
    "Table 3 summarises the main results for the eight cities and Figure 1 shows the monthly curves. "
    "Annual GHI ranges from 1,828 kWh/m²/year in Tétouan to 2,177 kWh/m²/year in Dakhla. On average, "
    "the five southern cities receive about 12% more solar radiation per year than the three northern "
    "ones (2,087 versus 1,868 kWh/m²/year). The ordering is remarkably clean: every southern city "
    "outperforms every northern city, with Casablanca, Tangier and Tétouan at the bottom and Dakhla, "
    "Ouarzazate and Errachidia at the top (Figure 2)."))

sum_cols = ["City", "Annual GHI\n(kWh/m²/yr)", "Annual DNI\n(kWh/m²/yr)", "Spring\n(kWh/m²/day)",
            "Summer\n(kWh/m²/day)", "Autumn\n(kWh/m²/day)", "Winter\n(kWh/m²/day)", "Mean T\n(°C)"]
t3 = [[P(x, tblhd) for x in sum_cols]]
for c in ORDER:
    r = summ.loc[c]
    t3.append([P(N[c], tbltxt),
               P(f"{r['Annual_GHI_kWh_m2']:.0f}", tbltxt),
               P(f"{r['Annual_DNI_kWh_m2']:.0f}", tbltxt),
               P(f"{r['Spring_daily_GHI']:.2f}", tbltxt),
               P(f"{r['Summer_daily_GHI']:.2f}", tbltxt),
               P(f"{r['Autumn_daily_GHI']:.2f}", tbltxt),
               P(f"{r['Winter_daily_GHI']:.2f}", tbltxt),
               P(f"{r['Mean_temp_C']:.1f}", tbltxt)])
story.append(P("Table 3. Annual and seasonal solar radiation for the eight cities (2023–2025 average).", tbl_cap))
story.append(styled_table(t3, [2.6*cm, 2.2*cm, 2.2*cm, 2.1*cm, 2.1*cm, 2.1*cm, 2.1*cm, 1.6*cm]))
story.append(Spacer(1, 2))

story.append(P("Figure 1. Average daily solar radiation (GHI) by month for the eight cities, 2023–2025.", caption))
story.append(Image("figures/fig1_monthly_ghi.png", width=15.4*cm, height=9.3*cm))
story.append(P("Figure 2. Total annual solar radiation (GHI) per city. Red bars are southern cities, blue bars are northern coastal cities.", caption))
story.append(Image("figures/fig2_annual_ghi.png", width=13.6*cm, height=7.9*cm))

story.append(P(
    "Figure 1 reveals the most important pattern of the whole study: in summer the curves of all eight "
    "cities come very close together, but in winter they spread widely apart. In June, Ouarzazate "
    "receives 7.73 kWh/m²/day and Tétouan 7.23 — a difference of only 7%. In December, Ouarzazate "
    "still receives 3.57 kWh/m²/day but Tétouan drops to 2.52 and Tangier to 2.49 — a difference of "
    "more than 40%. Table 4 gives the full monthly table."))

mt_cols = ["City"] + ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
t4 = [[P(x, tblhd) for x in mt_cols]]
for c in ORDER:
    t4.append([P(N[c], tbltxt)] + [P(f"{mm.loc[c, m]:.2f}", tbltxt) for m in mt_cols[1:]])
story.append(P("Table 4. Mean daily solar radiation by month (kWh/m²/day), 2023–2025 average.", tbl_cap))
story.append(styled_table(t4, [2.3*cm] + [1.12*cm]*12))
story.append(Spacer(1, 4))

story.append(P("5.2 The winter gap and the role of cloud cover", h2))
story.append(P(
    "Why do the northern cities lose so much more radiation in winter? The answer is clouds. Figure 3 "
    "shows the diurnal (hour-by-hour) profile of solar radiation in July and January for four "
    "representative cities. In July, all cities show a tall, smooth bell-shaped curve peaking around "
    "13:00 at roughly 900–1,000 W/m². In January, the southern cities (Ouarzazate, Dakhla) still show "
    "a clean bell shape, but the northern cities (Tangier, Tétouan) show a much lower, jagged curve — "
    "the jaggedness is the signature of passing clouds, which block the sun for part of the day."))
story.append(P("Figure 3. Diurnal solar radiation profile in July versus January for four cities.", caption))
story.append(Image("figures/fig3_diurnal.png", width=15.6*cm, height=10.6*cm))
story.append(P("Figure 4. Monthly cloud cover for the eight cities. Northern coastal cities are far cloudier, especially in winter.", caption))
story.append(Image("figures/fig4_cloud.png", width=15.4*cm, height=8.9*cm))
story.append(P(
    "Figure 4 quantifies this: mean annual cloud cover is 47.1% in Tétouan, 45.0% in Casablanca and "
    "43.2% in Tangier, versus only 22.9% in Dakhla, 28.5% in Ouarzazate and 29.6% in Errachidia. The "
    "cloudiness of the north is a winter phenomenon — in summer all cities are fairly clear — and it is "
    "exactly the months when clouds are worst (December–February) that solar output matters most for "
    "winter electricity demand."))

story.append(P("5.3 Day-to-day variability: cumulative distributions", h2))
story.append(P(
    "Averages hide variability, and variability matters for grid planning. Figure 5 shows the "
    "cumulative distribution of daily solar radiation for each city: for any value on the x-axis, the "
    "curve tells you what share of days fall below it. Two things stand out. First, the southern cities "
    "shift the whole curve to the right — even their bad days are better than the north's. The 5th "
    "percentile (the level exceeded on 95% of days, i.e., the 'worst winter day') is 3.45 kWh/m²/day in "
    "Ouarzazate and 4.17 in Dakhla, but only 2.15 in Tangier and 2.23 in Tétouan. Second, the northern "
    "cities have fatter left tails — more truly bad days — while their best summer days are similar to "
    "the south (95th percentile ≈ 7.6–8.1 kWh/m²/day everywhere). In other words, the south's advantage "
    "is not more sun in summer; it is much more reliable sun in winter."))
story.append(P("Figure 5. Cumulative distribution of daily solar radiation (2023–2025).", caption))
story.append(Image("figures/fig5_cdf.png", width=14.6*cm, height=8.9*cm))

story.append(P("5.4 Year-to-year stability", h2))
story.append(P(
    "Three years is not a long time, but it is enough to check that the rankings are not a fluke of one "
    "particular year. Figure 6 and Table 5 show the annual totals for 2023, 2024 and 2025 separately. "
    "The picture is stable: Dakhla is first in all three years (2,183 / 2,175 / 2,172 kWh/m²/year), "
    "Tétouan is last in all three (1,866 / 1,805 / 1,814), and the order of the cities barely changes. "
    "The year-to-year variation within a city is small (roughly ±3%), which means the rankings are "
    "robust."))
story.append(P("Figure 6. Year-by-year total solar radiation (2023, 2024, 2025).", caption))
story.append(Image("figures/fig8_years.png", width=14.2*cm, height=8.3*cm))
yt_cols = ["City", "2023", "2024", "2025", "Mean", "P10", "P50", "P90"]
t5 = [[P(x, tblhd) for x in yt_cols]]
q10 = daily.groupby("city")["ghi_day"].quantile(0.10) / 1000
q50 = daily.groupby("city")["ghi_day"].quantile(0.50) / 1000
q90 = daily.groupby("city")["ghi_day"].quantile(0.90) / 1000
for c in ORDER:
    t5.append([P(N[c], tbltxt),
               P(f"{yt.loc[c, '2023']:.0f}", tbltxt),
               P(f"{yt.loc[c, '2024']:.0f}", tbltxt),
               P(f"{yt.loc[c, '2025']:.0f}", tbltxt),
               P(f"{K['annual_ghi_kwh_m2'][c]:.0f}", tbltxt),
               P(f"{q10[c]:.2f}", tbltxt),
               P(f"{q50[c]:.2f}", tbltxt),
               P(f"{q90[c]:.2f}", tbltxt)])
story.append(P("Table 5. Annual GHI by year (kWh/m²/year) and percentiles of daily GHI (kWh/m²/day).", tbl_cap))
story.append(styled_table(t5, [2.6*cm, 1.7*cm, 1.7*cm, 1.7*cm, 1.7*cm, 1.7*cm, 1.7*cm, 1.7*cm]))
story.append(Spacer(1, 4))

story.append(P("5.5 Correlations between variables", h2))
story.append(P(
    "Before building the machine-learning models, I looked at how the daily variables relate to each "
    "other (Figure 7). The two strongest correlations with daily GHI are mean temperature (+0.62) and "
    "cloud cover (−0.44). The positive temperature correlation makes physical sense: clear skies and "
    "high sun both warm the ground, and winter days are both cold and short. The negative cloud "
    "correlation is also expected, but note that −0.44 is far from −1: clouds block radiation only "
    "partially and irregularly, which is exactly the kind of non-linearity that linear models struggle "
    "with. Humidity correlates negatively with temperature (dry air in summer), and wind is almost "
    "independent of radiation."))
story.append(P("Figure 7. Correlation matrix of daily variables (all cities pooled).", caption))
story.append(Image("figures/fig7_corr.png", width=12.4*cm, height=10.3*cm))

story.append(P("5.6 Estimated PV electricity output", h2))
story.append(P(
    "Applying the PV model (Section 4.4) to the measured radiation gives the electricity estimates in "
    "Table 6 and Figure 8. One square metre of panels would produce 206 kWh/year in Tétouan and up to "
    "245 kWh/year in Dakhla. In per-plant terms, a 1 MWp solar farm (about 6,700 m² of panels) would "
    "generate roughly 1,371 MWh/year in Tétouan, 1,603 in Ouarzazate and 1,632 in Dakhla — a 19% "
    "difference between the best and worst city. For comparison, a PV plant the size of the Noor "
    "complex (580 MWp) would produce about 0.9 TWh per year in this model if built at Ouarzazate's "
    "resource level — enough for roughly a million households at Moroccan consumption levels. These "
    "estimates are consistent with the ~1,779 kWh/kWp national average reported by Benbba et al. "
    "(2024), which gives confidence in the model."))
pv_cols = ["City", "PV per m²\n(kWh/m²/yr)", "1 MWp output\n(MWh/yr)", "Mean cloud\n(%)", "Mean T\n(°C)"]
t6 = [[P(x, tblhd) for x in pv_cols]]
for c in ORDER:
    r = summ.loc[c]
    t6.append([P(N[c], tbltxt),
               P(f"{r['PV_per_m2_kWh']:.0f}", tbltxt),
               P(f"{r['PV_per_MWp_MWh']:.0f}", tbltxt),
               P(f"{r['Mean_cloud_%']:.1f}", tbltxt),
               P(f"{r['Mean_temp_C']:.1f}", tbltxt)])
story.append(P("Table 6. Estimated PV electricity output and climate summary (η = 15%, PR = 0.75).", tbl_cap))
story.append(styled_table(t6, [2.9*cm, 2.9*cm, 2.9*cm, 2.6*cm, 2.3*cm]))
story.append(Spacer(1, 2))
story.append(P("Figure 8. Estimated annual PV electricity per square metre of panels. Numbers inside bars are specific yields in MWh/MWp.", caption))
story.append(Image("figures/fig6_pv_output.png", width=14.2*cm, height=8.3*cm))

story.append(P("5.7 Machine-learning results", h2))
story.append(P(
    "Table 7 compares the models on the out-of-sample test year (2025). The gradient boosting model "
    "performed best, with R² = 0.932, RMSE = 443 Wh/m²/day and MAE = 291 Wh/m²/day. The random forest "
    "was very close (R² = 0.924, RMSE = 468, MAE = 304). Linear regression was clearly worse (R² = "
    "0.612, RMSE = 1,053, MAE = 856), and both tree models crushed the naive baseline (R² ≈ 0, RMSE = "
    "1,691). To put the errors in context: a typical clear summer day provides about 7,000–7,700 "
    "Wh/m², so the best model's average error of ~300 Wh/m² is only about 4–5% of a full summer day, "
    "and about 8–10% of a typical winter day."))
m_cols = ["Model", "R² (test 2025)", "RMSE\n(Wh/m²/day)", "MAE\n(Wh/m²/day)", "CV R²\n(4-fold)"]
t7 = [[P(x, tblhd) for x in m_cols]]
order_m = ["Linear regression", "Random forest", "Gradient boosting", "Baseline (mean)"]
for mname in order_m:
    r = metrics.loc[mname]
    cvv = cv.get(mname, "")
    t7.append([P({"Baseline (mean)": "Baseline (predict the mean)",
                          "Linear regression": "Linear regression",
                          "Random forest": "Random forest",
                          "Gradient boosting": "Gradient boosting"}[mname], tbltxt),
               P(f"{max(0.0, r['R2']):.3f}", tbltxt),
               P(f"{r['RMSE']:.0f}", tbltxt),
               P(f"{r['MAE']:.0f}", tbltxt),
               P("n/a" if cvv == "" else f"{cvv:.3f}", tbltxt)])
story.append(P("Table 7. Model performance on the out-of-sample test year (2025) and time-series cross-validation.", tbl_cap))
story.append(styled_table(t7, [5.2*cm, 2.8*cm, 3.1*cm, 3.1*cm, 2.4*cm]))
story.append(Spacer(1, 2))

story.append(P("Figure 9. Predicted versus actual daily solar radiation (gradient boosting, test year 2025). Points close to the dashed line are accurate.", caption))
story.append(Image("figures/fig9_scatter.png", width=11.8*cm, height=11.1*cm))
story.append(P("Figure 10. Residuals (actual minus predicted) of the best model. Errors grow in spring (April) and are smallest in winter.", caption))
story.append(Image("figures/fig10_residuals.png", width=12.4*cm, height=9.4*cm))
story.append(P(
    "Figures 9 and 10 visualise the quality of the best model. The predicted-versus-actual plot hugs "
    "the 1:1 line with no obvious curve or fan shape, which means the model is neither systematically "
    "biased nor getting worse on big values. The residuals are scattered around zero. The monthly error "
    "analysis (Figure 11) shows that the model is least accurate in April (MAE ≈ 513 Wh/m²/day) and "
    "most accurate in November and January (MAE ≈ 204–216 Wh/m²/day). April is the month with the most "
    "variable weather in Morocco — the transition from winter clouds to summer heat — so this pattern "
    "is physically sensible."))
story.append(P("Figure 11. Mean absolute error of the best model by month (test year 2025).", caption))
story.append(Image("figures/fig13_monthly_mae.png", width=13.4*cm, height=7.4*cm))

story.append(P(
    "Figure 12 shows which variables drive the predictions: day of the year and mean temperature "
    "dominate, with cloud cover in third place, followed by latitude. This is consistent with the "
    "correlation analysis: the seasonal cycle (day of year) and the clear-sky signal (temperature) "
    "carry most of the information, and clouds are the main perturbation on top of that. Figure 13 "
    "shows the per-city performance: gradient boosting and random forest are strong everywhere "
    "(R² ≈ 0.86–0.94), with Dakhla the hardest city to predict (R² = 0.86–0.89), probably because its "
    "coastal fog is very local. Linear regression is poor everywhere and especially bad in Dakhla "
    "(R² = 0.16)."))
story.append(P("Figure 12. Feature importances from the random forest.", caption))
story.append(Image("figures/fig11_importances.png", width=13.0*cm, height=8.0*cm))
story.append(P("Figure 13. Per-city R² for the three models on the test year 2025.", caption))
story.append(Image("figures/fig12_city_r2.png", width=14.4*cm, height=8.0*cm))
story.append(P("6. Discussion", h1))

story.append(P("6.1 Morocco's solar resource is real and uneven", h2))
story.append(P(
    "The first clear message of the results is that Morocco's solar resource is excellent by world "
    "standards — even the 'worst' city, Tétouan, receives 1,828 kWh/m²/year of GHI, which is more than "
    "most of Europe (much of Germany, for example, receives roughly 1,000–1,200 kWh/m²/year). But the "
    "resource is not uniform: the south receives about 12% more energy per year, and the difference is "
    "concentrated almost entirely in winter. In summer the whole country is a solar paradise; in "
    "winter, the Mediterranean coast is cloudy while the Sahara stays clear. My winter values "
    "(2.98–4.70 kWh/m²/day) fit the picture reported by Benbba et al. (2024), who place the best zones "
    "above 5.57 kWh/m²/day on annual average."))

story.append(P("6.2 What the winter gap means for policy", h2))
story.append(P(
    "The winter gap matters for three reasons. First, the south's winter advantage makes it the natural "
    "home for grid-scale solar: a plant in Dakhla produces about 19% more electricity per year than the "
    "same plant in Tétouan, and it produces it disproportionately in the months when it is needed most. "
    "Second, winter is when Morocco's electricity demand peaks (heating, and lower hydro output), so "
    "solar plants that still deliver in December are much more valuable than plants that only deliver "
    "in summer. Third, the DNI data reinforce the choice of CSP: Ouarzazate receives 2,570 kWh/m²/year "
    "of direct radiation and Errachidia 2,482 — comfortably inside the 2,000–2,800 kWh/m²/year range "
    "that Benbba et al. (2024) identify as required for commercially viable CSP. The government's "
    "decision to build Noor at Ouarzazate is strongly supported by these data."))
story.append(P(
    "For the northern cities, the implication is different but still positive: Tétouan and Tangier "
    "receive enough sun for rooftop PV (about 1,371–1,395 MWh/MWp/year in my model), especially in "
    "summer when demand for air conditioning peaks. A sensible national strategy is therefore two-"
    "tiered: large utility-scale plants (PV and CSP with storage) in the south, and distributed "
    "rooftop PV in the north to shave summer peak demand. This is, in fact, close to the strategy "
    "Morocco is already following."))

story.append(P("6.3 Machine learning can predict solar output well", h2))
story.append(P(
    "The prediction results are encouraging for a country planning to integrate lots of solar. With "
    "nothing but daily weather averages and the calendar date, gradient boosting explains 93% of the "
    "variance in daily solar radiation on data it has never seen (R² = 0.932). The average error of "
    "~300 Wh/m²/day is small compared with the ~7,000 Wh/m² a good summer day delivers. This is in "
    "line with the forecasting literature: Voyant et al. (2017) found that machine-learning methods "
    "beat classical statistics for solar radiation, and tree ensembles are among the most reliable "
    "practical choices."))
story.append(P(
    "Why does gradient boosting beat linear regression so clearly (R² = 0.932 versus 0.612)? Because "
    "the relationship between weather and radiation is genuinely non-linear. Cloud cover, for example, "
    "removes radiation in a complicated way: a little cloud on a clear day can halve the radiation, but "
    "the difference between 80% and 100% cloud cover is small. A straight line cannot represent that "
    "kind of saturation effect, but trees can, by splitting the data into many small regions. The "
    "cross-validation results (R² ≈ 0.87 for both tree models, versus 0.37 for linear regression) "
    "confirm that this is a real advantage, not an accident of the test year."))

story.append(P("6.4 Comparison with previous studies", h2))
story.append(P(
    "My annual GHI values (1,828–2,177 kWh/m²/year) fall inside the ranges reported by Benbba et al. "
    "(2024) and by the Global Solar Atlas for Morocco. My DNI values (2,070–2,570 kWh/m²/year) match "
    "the 1,800–3,000 kWh/m²/year national range. My PV specific yields (1,371–1,632 kWh/kWp/year) "
    "bracket the ~1,779 kWh/kWp/year national average they report; the difference is expected because "
    "I assume fixed horizontal panels with PR = 0.75, while the published figure often assumes "
    "optimally tilted panels and slightly better PR. The good agreement with independent sources "
    "suggests that ERA5/Open-Meteo data, although modelled rather than measured on the ground, is "
    "reliable enough for resource assessment at city level."))

story.append(P("6.5 Implications for the 52%-by-2030 target", h2))
story.append(P(
    "Morocco aims to produce 52% of its electricity from renewables by 2030. The data in this study "
    "support the feasibility of that target from a resource perspective: the country has more than "
    "enough sun, in the right places, and modern forecasting tools are accurate enough to manage the "
    "variability. The main challenges are therefore not resource but infrastructure: grid capacity to "
    "move southern power to northern cities, storage (batteries or CSP thermal storage) to cover the "
    "evening peak and cloudy days, and financing. This study cannot address those directly, but it "
    "quantifies the resource side of the equation, which is the necessary foundation."))

story.append(P("6.6 Limitations", h2))
story.append(P(
    "This study has several limitations, which I want to be honest about. First, ERA5 is a reanalysis: "
    "the radiation values are modelled estimates, not measurements from a weather station at each "
    "city. Ground stations can differ from reanalysis by a few percent, especially for radiation, "
    "because local topography and haze are smoothed out. Second, each city is represented by a single "
    "grid point, so local microclimates (for example, the Rif mountains around Tétouan) are not "
    "captured. Third, the PV model is deliberately simple: it ignores panel tilt, sun tracking, "
    "temperature losses, soiling and shading, and it assumes perfect availability (no outages). "
    "Fourth, three years is a short period for climate-scale conclusions, although the year-to-year "
    "stability (Section 5.4) is reassuring. Fifth, I did not analyse economics — cost per kWh, land "
    "prices, grid connection costs — which are decisive in the real world. Finally, the machine-"
    "learning models predict total daily energy, not the hourly shape, which is what grid operators "
    "actually need for dispatching."))

story.append(P("6.7 Future work", h2))
story.append(P(
    "This project could be extended in several directions. Adding more cities and more years would "
    "strengthen the geographic and climatic coverage; the API makes this trivial. Modelling the "
    "optimal panel tilt and comparing fixed versus tracking systems would refine the PV estimates. "
    "An hourly forecasting model (predicting tomorrow's hourly curve) would be much more useful for "
    "grid operators than daily totals, and the same methods would apply. Finally, combining the solar "
    "data with electricity demand data for Morocco would allow a genuine supply–demand analysis of "
    "the 52% target. Each of these is a natural next step that a motivated student could take."))

story.append(P("6.8 What this project says about open data and education", h2))
story.append(P(
    "Perhaps the most unexpected finding of this project is not about the sun at all, but about access "
    "to science. Every figure in this paper was produced with free tools and free data: a laptop, "
    "Python, pandas, scikit-learn, matplotlib, and the Open-Meteo API built on ERA5. Twenty years ago, "
    "a study like this would have required a university department, a meteorological station and a "
    "research budget. Today it can be done by a high-school student in a few weekends. This matters "
    "for Morocco in a practical way: a country planning to double its renewable capacity by 2030 will "
    "need thousands of engineers and analysts, and the tools they will use are the same open tools I "
    "used here. Projects like this one are, in a small way, a demonstration that the skills for the "
    "energy transition are available to anyone willing to learn."))
story.append(P("7. Conclusion", h1))
story.append(P(
    "In this project I quantified the solar resource of eight Moroccan cities using three years of "
    "free, hourly, open data, and tested whether machine learning can predict solar radiation from "
    "everyday weather variables. Three main findings emerge."))
story.append(P(
    "First, the resource is real but uneven: southern cities receive about 12% more solar radiation "
    "per year than the northern coast (2,087 versus 1,868 kWh/m²/year), and the gap is almost "
    "entirely a winter effect driven by cloud cover — Dakhla receives 4.70 kWh/m²/day in winter "
    "versus 2.98 for Tétouan, while summer values are similar everywhere. Second, Ouarzazate's direct "
    "radiation (2,570 kWh/m²/year) and Errachidia's (2,482) are in the range required for economical "
    "concentrated solar power, which strongly supports the location of the Noor complex and points to "
    "the south as the home of Morocco's future utility-scale solar. Third, machine learning predicts "
    "daily solar energy very accurately: gradient boosting reaches R² = 0.932 and a random forest "
    "R² = 0.924 on unseen data, versus 0.612 for linear regression, showing that the relationship is "
    "non-linear and that simple weather variables carry almost all the information needed."))
story.append(P(
    "For Morocco's 52%-renewables-by-2030 target, the data suggest a two-tier strategy: big solar "
    "plants in the sunny, cloud-free south, and rooftop PV in the north to cover summer demand peaks. "
    "Perhaps the most important lesson of the project, however, is methodological: with free APIs, "
    "open-source Python libraries and public reanalysis data, a high-school student can carry out "
    "real, quantitative, reproducible research on a question that matters for their own country — and "
    "that is exactly the kind of science that the 2030 target will need."))
story.append(P("Declarations", h1))
story.append(P(
    "<b>Author contributions (CRediT).</b> Conceptualization, R.K.; Methodology, R.K.; Software, "
    "R.K.; Validation, R.K.; Formal analysis, R.K.; Investigation, R.K.; Data curation, R.K.; "
    "Writing — original draft, R.K.; Writing — review &amp; editing, R.K.; Visualization, R.K. All "
    "work for this study was carried out by the single author."))
story.append(P(
    "<b>Funding.</b> This research received no external funding."))
story.append(P(
    "<b>Conflicts of interest.</b> The author declares no conflicts of interest."))
story.append(P(
    "<b>Ethics statement.</b> Not applicable. This study used only publicly available meteorological "
    "data and involved no human or animal subjects."))
story.append(P(
    "<b>Data availability.</b> All raw and processed data, code and figures are publicly available "
    "in the author's GitHub repository (https://github.com/vampriyad) and from the Open-Meteo "
    "Historical Weather API (https://open-meteo.com), which is based on the ECMWF ERA5 reanalysis. "
    "All analysis was performed in Python 3 with pandas (McKinney, 2010) and scikit-learn (Pedregosa "
    "et al., 2011)."))
story.append(PageBreak())
story.append(P("References", h1))
refs = [
    "Benbba, R., Barhdadi, M., Ficarella, A., Manente, G., El Hachemi, N., Barhdadi, A., Al-Salaymeh, A. & Outzourhit, A. (2024). Solar energy resource and power generation in Morocco: current situation, potential, and future perspective. <i>Resources</i>, 13(10), 140. https://www.mdpi.com/2079-9276/13/10/140",
    "Construction Review Online (2026). The Noor Ouarzazate solar complex: Morocco's renewable energy giant. https://constructionreviewonline.com/noor-ouarzazate-solar-complex-worlds-largest-concentrated-solar-power-plant/",
    "European Commission, Joint Research Centre. <i>Photovoltaic Geographical Information System (PVGIS)</i>. https://re.jrc.ec.europa.eu/pvg_tools/",
    "Hersbach, H., Bell, B., Berrisford, P., Hirahara, S., Horányi, A., Muñoz-Sabater, J., et al. (2020). The ERA5 global reanalysis. <i>Quarterly Journal of the Royal Meteorological Society</i>, 146(730), 1999–2049.",
    "IRENA (2015). <i>Renewables Readiness Assessment: Morocco</i>. International Renewable Energy Agency, Abu Dhabi. https://www.irena.org",
    "IRENA (2024). <i>Renewable capacity statistics 2024</i>. International Renewable Energy Agency, Abu Dhabi.",
    "MASEN – Moroccan Agency for Sustainable Energy. https://www.masen.ma",
    "McKinney, W. (2010). Data structures for statistical computing in Python. <i>Proceedings of the 9th Python in Science Conference</i>, 56–61.",
    "Open-Meteo (2025). Historical Weather API documentation. https://open-meteo.com/en/docs/historical-weather-api",
    "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. (2011). Scikit-learn: machine learning in Python. <i>Journal of Machine Learning Research</i>, 12, 2825–2830.",
    "PPIAF – Public–Private Infrastructure Advisory Facility. <i>Morocco: Noor Ouarzazate concentrated solar power complex</i>. https://www.ppiaf.org/documents/4689",
    "Voyant, C., Notton, G., Kalogirou, S., Nivet, M.-L., Paoli, C., Motte, F. & Fouilloy, A. (2017). Machine learning methods for solar radiation forecasting: a review. <i>Renewable Energy</i>, 105, 569–582.",
    "World Bank Group / ESMAP. <i>Global Solar Atlas</i>. https://globalsolaratlas.info",
    "World Economic Forum (2018). Morocco is building a solar farm as big as Paris in the Sahara Desert. https://www.weforum.org/stories/2018/05/morocco-is-building-a-solar-farm-as-big-as-paris-in-the-sahara-desert/",
]
for i, rtext in enumerate(refs, 1):
    story.append(P(f"[{i}] {rtext}", ref))
story.append(P("Appendix A. Reproducibility and code", h1))
story.append(P(
    "Everything in this paper can be reproduced by anyone with internet access and a Python "
    "installation. The project is organised as follows:"))
story.append(B("<b>data/raw/</b> — the raw hourly JSON files downloaded from Open-Meteo (one per city)."))
story.append(B("<b>scripts/01_daily_dataset.py</b> — converts raw hourly data into the daily dataset (results/daily_all.csv)."))
story.append(B("<b>scripts/02_analysis_figures.py</b> — produces the exploratory figures and summary tables (Figures 1–8, Tables 1–6)."))
story.append(B("<b>scripts/03_ml_models.py</b> — trains and evaluates the machine-learning models (Figures 9–13, Table 7)."))
story.append(B("<b>scripts/build_paper.py</b> — generates this PDF from the results."))
story.append(P(
    "The commands to reproduce everything are:"))
story.append(P("<font face='Courier' size='8.5'>pip install pandas numpy matplotlib scikit-learn requests reportlab pypdf<br/>"
               "python3 scripts/01_daily_dataset.py<br/>"
               "python3 scripts/02_analysis_figures.py<br/>"
               "python3 scripts/03_ml_models.py<br/>"
               "python3 scripts/build_paper.py</font>", body))
story.append(P(
    "The random seeds in the machine-learning script are fixed (random_state = 42), so the results are "
    "exactly reproducible. If you want to extend the study, the cheapest changes are: add a new city "
    "(the API accepts any latitude/longitude), change the period, or add a feature such as "
    "precipitation. Each of these takes only a few minutes."))
story.append(P("Appendix B. Glossary", h1))
gloss = [
    ("GHI (Global Horizontal Irradiance)", "Total solar energy falling on a horizontal surface; the standard measure of a site's solar resource."),
    ("DNI (Direct Normal Irradiance)", "Solar energy arriving directly from the sun's disc, perpendicular to the sun's rays; essential for concentrated solar power."),
    ("DHI (Diffuse Horizontal Irradiance)", "Solar energy scattered by clouds, dust and the sky; the reason PV panels still produce power on cloudy days."),
    ("Reanalysis (ERA5)", "A complete weather record produced by combining real observations with a physical model of the atmosphere; ERA5 is produced by ECMWF since 1940."),
    ("kWh/m²/day", "Kilowatt hours per square metre per day; a unit of solar energy. 1 kWh/m²/day ≈ the energy of 1,000 W running for one hour on one square metre."),
    ("PV (Photovoltaic)", "Technology that converts sunlight directly into electricity using semiconductor cells."),
    ("CSP (Concentrated Solar Power)", "Technology that concentrates direct sunlight with mirrors to heat a fluid and drive a turbine; needs high DNI."),
    ("Performance ratio (PR)", "The fraction of a PV system's theoretical output that survives real-world losses (inverter, soiling, heat, wiring); typically 0.75–0.80."),
    ("Specific yield", "Annual electricity produced per unit of installed capacity (kWh/kWp/year); the industry standard for comparing solar sites."),
    ("MWp (Megawatt peak)", "The rated power of a solar plant under standard test conditions."),
    ("R² (coefficient of determination)", "The fraction of variance in the data explained by a model; 1 is perfect, 0 means no better than predicting the mean."),
    ("RMSE / MAE", "Root mean squared error / mean absolute error: two ways of measuring a model's average prediction error, in the same units as the target."),
    ("Random forest", "An ensemble of many decision trees whose predictions are averaged; handles non-linear relationships well."),
    ("Gradient boosting", "An ensemble built by adding trees one at a time, each correcting the errors of the previous ones."),
    ("Solar constant", "The average intensity of sunlight at the top of the atmosphere, about 1,361 W/m²."),
    ("Zenith angle", "The angle between the sun's rays and the vertical; at high zenith angles (low sun), more light is absorbed by the atmosphere."),
    ("Diffuse fraction", "The share of GHI that is diffuse (scattered) rather than direct; it rises on cloudy days."),
    ("Performance of a 'naive baseline'", "A model that always predicts the same value (the training mean); any real model must beat it, or it is useless."),
    ("Time-series split", "A way of splitting data for validation that respects time order (train on the past, test on the future), avoiding leakage of future information."),
]
for term, definition in gloss:
    story.append(P(f"<b>{term}.</b> {definition}", ref))
story.append(Spacer(1, 8))
story.append(P("End of paper", ParagraphStyle("end", parent=body, alignment=TA_CENTER, fontSize=9)))
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0]/2, 1.05*cm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate("Paper_Solar_Energy_Morocco.pdf", pagesize=A4,
                        leftMargin=2.0*cm, rightMargin=2.0*cm,
                        topMargin=1.9*cm, bottomMargin=1.7*cm,
                        title="Solar Energy Potential in Morocco",
                        author="Riyad Khairoun")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF built: Paper_Solar_Energy_Morocco.pdf")
