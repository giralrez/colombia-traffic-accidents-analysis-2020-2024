<div align="center">

# 🚦 Road Safety Analytics — Bogotá, Colombia (2020–2024)

**End-to-end data analytics project on traffic accident patterns in Bogotá using open government data**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=flat-square&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org)
[![Status](https://img.shields.io/badge/Status-Complete-2ea44f?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

</div>

---

## 📌 Overview

This project performs a **complete end-to-end data analysis** of road traffic accidents (siniestros viales) in Bogotá, Colombia between 2020 and 2024. Using open data from the Secretaría Distrital de Movilidad, the analysis spans data ingestion, multi-source cleaning and normalization, exploratory analysis, and a fully interactive Power BI dashboard for decision-support.

The goal is to identify **temporal patterns, high-risk road actors, accident severity trends, and geographic concentrations** that can inform public safety policy and urban mobility planning.

---

## 🎯 Key Questions Answered

- How have traffic accident rates evolved year-over-year from 2020 to 2024?
- Which vehicle types and road actors are most frequently involved in serious incidents?
- Are there seasonal or day-of-week patterns in accident frequency?
- How did mobility restrictions during 2020–2021 affect accident rates?
- What accident categories show the highest severity (deaths and injuries)?

---

## 🗂️ Project Structure

```
colombia-traffic-accidents-analysis-2020-2024/
│
├── 📓 01_Limpieza_HJ_Siniestros_Norm_Data.ipynb       # Accidents dataset: cleaning & normalization
├── 📓 02_Analisis_Grafico_HJ_Siniestros.ipynb          # Exploratory visual analysis
├── 📓 03_limpieza_datos_vehiculos_actorvial.ipynb      # Vehicle & road actor data cleaning
├── 📓 04_normalizacion_unificacion_datos.ipynb         # Multi-source normalization & merge
├── 📓 05_consolidacion_resultados_equipo.ipynb         # Final consolidation & team results
│
├── 📊 Siniestralidad vial Bogotá.pbix                  # Interactive Power BI dashboard
├── 📄 Siniestralidad vial Bogotá.pdf                   # Exported dashboard (PDF)
├── 📋 Siniestralidad vial Bogotá.pptx                  # Project presentation
├── 📝 Informe_Accidentes Viales en Bogota_...pdf       # Full analytical report
│
├── 📁 _Normalizacion_Base_Siniestros_.xlsx             # Normalized accidents base
├── 📁 base_anuario_de_siniestralidad_filtrado.xlsx     # Filtered annual dataset
└── 📁 Paleta de colores - proyecto.pptx                # Visual design guidelines
```

---

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Language | Python 3.10+ | Core analysis engine |
| Data manipulation | Pandas, NumPy | Cleaning, transformation, aggregation |
| Visualization | Matplotlib, Seaborn | EDA charts and distribution analysis |
| BI Dashboard | Power BI Desktop | Interactive business intelligence report |
| Data formats | Excel (.xlsx), CSV | Source data ingestion |
| Environment | Jupyter Notebook | Reproducible analysis workflow |
| Version control | Git & GitHub | Collaboration and versioning |

---

## 🔄 Data Pipeline

The project follows a structured 5-stage pipeline:

```
Raw Open Data (SDM Bogotá)
        │
        ▼
[01] Cleaning & Normalization       ← Handle nulls, fix dtypes, standardize columns
        │
        ▼
[02] Exploratory Visual Analysis    ← Distributions, trends, outliers, correlations
        │
        ▼
[03] Vehicle & Actor Data Cleaning  ← Secondary dataset: vehicle types & road actors
        │
        ▼
[04] Multi-source Normalization     ← Schema alignment, key unification, data merge
        │
        ▼
[05] Results Consolidation          ← Final dataset ready for dashboard & report
        │
        ▼
Power BI Dashboard + Analytical Report
```

---

## 🧹 Data Cleaning Highlights

The raw datasets required significant preparation before analysis:

- **Multi-year consolidation:** Integrated annual accident records across 5 years (2020–2024) into a unified schema
- **Missing value treatment:** Applied column-specific strategies — median imputation for numeric fields, mode for categorical, row removal for critical nulls
- **Data type normalization:** Standardized date/time formats, encoded accident severity categories, harmonized column naming conventions across annual files
- **Duplicate detection:** Identified and removed duplicate incident records caused by multi-source ingestion
- **Secondary dataset join:** Cleaned and merged vehicle/road-actor datasets using standardized accident identifiers
- **Categorical encoding:** Normalized Spanish-language category values with inconsistent spelling across years (e.g., accented vs. unaccented entries)

---

## 📊 Dashboard — Power BI

The interactive dashboard covers:

- 📈 **Annual trend line** — accident volume 2020–2024 with COVID-19 period annotation
- 🗓️ **Temporal heatmap** — accident frequency by day of week and hour
- 🚗 **Road actor breakdown** — cyclists, motorcyclists, pedestrians, drivers
- ⚠️ **Severity distribution** — fatalities, serious injuries, minor injuries by year
- 📍 **Geographic concentration** — accident density by Bogotá locality *(if applicable)*
- 🔍 **Interactive filters** — year, accident type, severity, vehicle type

> 📥 **Download the dashboard:** [`Siniestralidad vial Bogotá.pbix`](./Siniestralidad%20vial%20Bogot%C3%A1.pbix)
>
> 📄 **View as PDF:** [`Siniestralidad vial Bogotá.pdf`](./Siniestralidad%20vial%20Bogot%C3%A1.pdf)

---


<!-- ## 📸 Dashboard Preview

> *Add screenshots of your Power BI dashboard here for maximum visual impact*
>
> Suggested captures:
> - Main KPI overview page
> - Temporal trend chart
> - Road actor breakdown chart
>
> `![Dashboard Overview](./assets/dashboard_overview.png)`

---
-->

## 📦 Data Sources

| Dataset | Source | Coverage |
|---------|--------|----------|
| Anuario de Siniestralidad Vial | Secretaría Distrital de Movilidad — Bogotá | 2020–2024 |
| Vehículos y actores viales | Datos Abiertos Colombia | 2020–2024 |

> Open data available at: [datos.gov.co](https://www.datos.gov.co) and [datosabiertos.bogota.gov.co](https://datosabiertos.bogota.gov.co)

---

## 🚀 How to Run

### Prerequisites
```bash
Python 3.10+
pip
Power BI Desktop (for .pbix file)
```

### Setup
```bash
# 1. Clone the repository
git clone https://github.com/giralrez/colombia-traffic-accidents-analysis-2020-2024.git
cd colombia-traffic-accidents-analysis-2020-2024

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install pandas numpy matplotlib seaborn openpyxl jupyter

# 4. Launch Jupyter
jupyter notebook
```

### Run notebooks in order:
| Step | Notebook | Description |
|------|----------|-------------|
| 1 | `01_Limpieza_HJ_Siniestros_Norm_Data.ipynb` | Clean & normalize accidents data |
| 2 | `02_Analisis_Grafico_HJ_Siniestros.ipynb` | Exploratory visual analysis |
| 3 | `03_limpieza_datos_vehiculos_actorvial.ipynb` | Clean vehicle & actor data |
| 4 | `04_normalizacion_unificacion_datos.ipynb` | Merge & unify all sources |
| 5 | `05_consolidacion_resultados_equipo.ipynb` | Final results consolidation |

### Power BI Dashboard
Open `Siniestralidad vial Bogotá.pbix` in **Power BI Desktop** (free download from Microsoft).

---

## 📚 Deliverables

| Deliverable | File | Description |
|-------------|------|-------------|
| 📓 Analysis notebooks | `01` – `05` `.ipynb` | Full reproducible pipeline |
| 📊 Interactive dashboard | `.pbix` | Power BI report with filters |
| 📄 Dashboard export | `.pdf` | Static version for sharing |
| 📋 Presentation | `.pptx` | Executive summary slides |
| 📝 Full report | `Informe_...pdf` | Detailed analytical report |

---

## 👤 Author

**Andrés Giraldo Ramírez**
Software Engineer · Data Analytics · ML · Bogotá, Colombia 🇨🇴

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/andres-giraldo-ramirez-a21190341)
[![GitHub](https://img.shields.io/badge/GitHub-@giralrez-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/giralrez)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:andresras103@gmail.com)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
<i>If this project was useful or interesting to you, consider giving it a ⭐</i>
</div>
