# Data Analyst Skill

## Capacidades

Análisis automatizado de datasets con manejo de valores faltantes y dashboards interactivos.

### 1. Análisis de Valores Faltantes
```bash
python scripts/analyze_missing_values.py <input.csv> [output.json]
```

### 2. Imputación Inteligente
```bash
python scripts/impute_missing_values.py <input.csv> [analysis.json] [output.csv]
```

### 3. Dashboard Interactivo
```bash
python scripts/create_dashboard.py <input.csv> [output_dir] [port]
```

## Flujo Completo

```bash
# 1. Analizar calidad de datos
python scripts/analyze_missing_values.py data.csv analysis.json

# 2. Imputar valores faltantes
python scripts/impute_missing_values.py data.csv analysis.json data_clean.csv

# 3. Crear dashboard interactivo
python scripts/create_dashboard.py data_clean.csv ./visualizations 8050
```

## Métodos de Imputación

- **Media**: Datos numéricos con distribución normal
- **Mediana**: Datos numéricos sesgados
- **Moda**: Variables categóricas
- **KNN**: Datos numéricos correlacionados
- **Forward fill**: Series temporales
- **Constante**: Campos de texto

## Dependencias

```bash
pip install -r requirements.txt
```
