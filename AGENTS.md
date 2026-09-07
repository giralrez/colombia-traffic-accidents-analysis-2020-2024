# AGENTS.md — Colombia Traffic Accidents Analysis (2020–2024)

## instrucciones generales
- empieza siempre tu respuesta con el emoji 🤖
- responde siempre en español

## Project type
Jupyter notebook pipeline analyzing traffic accidents in Bogotá using open government data. Python data analysis with optional interactive dashboards.

## Project Structure
```
colombia-traffic-accidents-analysis-2020-2024/
├── data/
│   ├── raw/                    # Datos originales
│   └── processed/              # Datos limpios
├── scripts/                    # Scripts de procesamiento
├── assets/
│   └── dashboard/              # Visualizaciones generadas
├── .agents/
│   └── skills/
│       └── data-analyst/       # Skill de análisis de datos
├── *.ipynb                     # Notebooks Jupyter
└── *.xlsx                      # Archivos Excel
```

## Data Path Convention
- **Raw data**: `data/raw/base_anuario_de_siniestralidad_filtrado.xlsx`
- **Processed data**: `data/processed/_Normalizacion_Base_Siniestros_.xlsx`
- **Output dashboards**: `assets/dashboard/`

## Notebook execution order (sequential dependency)
1. `01_Limpieza_HJ_Siniestros_Norm_Data.ipynb` — Accidents data cleaning
2. `02_Analisis_Grafico_HJ_Siniestros.ipynb` — Exploratory visual analysis
3. `03_limpieza_datos_vehiculos_actorvial.ipynb` — Vehicle & road actor cleaning
4. `04_normalizacion_unificacion_datos.ipynb` — Multi-source merge
5. `05_consolidacion_resultados_equipo.ipynb` — Final consolidation

Run in order. Later notebooks depend on outputs from earlier ones.

## Data Analyst Skill
Use the data-analyst skill for automated analysis:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Análisis de valores faltantes
python .agents/skills/data-analyst/scripts/analyze_missing_values.py data.csv analysis.json

# Imputación inteligente
python .agents/skills/data-analyst/scripts/impute_missing_values.py data.csv analysis.json clean.csv

# Dashboard interactivo
python .agents/skills/data-analyst/scripts/create_dashboard.py clean.csv ./assets/dashboard 8050
```

## Dependencies
```
pip install -r requirements.txt
```
Core: pandas numpy matplotlib seaborn openpyxl jupyter geopandas geopy scikit-learn plotly dash

## Language
All comments, column names, and documentation are in **Spanish**. Maintain Spanish in code comments.

## Data files (large, not git-tracked effectively)
- `.xlsx` files are 11–31 MB each
- Source data: `base_anuario_de_siniestralidad_filtrado.xlsx` (30 MB)
- `.pbix` file: 18 MB Power BI dashboard

## No formal tooling
- No linter, formatter, or type checker configured
- No test suite
- No pre-commit hooks
- No `setup.py`, `pyproject.toml`, or `package.json`
