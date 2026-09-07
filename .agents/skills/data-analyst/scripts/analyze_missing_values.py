#!/usr/bin/env python3
"""
Análisis de valores faltantes en datasets CSV.
Detecta patrones de datos faltantes y sugiere estrategias de imputación.
"""

import pandas as pd
import numpy as np
import json
import sys
from pathlib import Path


def detect_column_type(series, column_name):
    """Detecta el tipo de dato de una columna."""
    if pd.api.types.is_numeric_dtype(series):
        return 'numeric'
    elif pd.api.types.is_datetime64_any_dtype(series):
        return 'temporal'
    elif pd.api.types.is_bool_dtype(series):
        return 'boolean'
    else:
        # Verificar si es categórico o texto
        n_unique = series.nunique()
        if n_unique < 20 or n_unique / len(series) < 0.1:
            return 'categorical'
        return 'text'


def suggest_imputation_strategy(series, col_type, missing_pct):
    """Sugiere estrategia de imputación basada en tipo y distribución."""
    if missing_pct > 70:
        return 'drop_column', 'Más del 70% de valores faltantes'
    
    if missing_pct == 0:
        return 'none', 'Sin valores faltantes'
    
    if col_type == 'numeric':
        skewness = series.dropna().skew()
        if abs(skewness) < 0.5:
            return 'mean', f'Distribución normal (skewness: {skewness:.2f})'
        else:
            return 'median', f'Distribución sesgada (skewness: {skewness:.2f})'
    
    elif col_type == 'categorical':
        return 'mode', 'Variable categórica'
    
    elif col_type == 'temporal':
        return 'forward_fill', 'Serie temporal'
    
    elif col_type == 'text':
        if missing_pct < 20:
            return 'constant', 'Campo de texto con pocos faltantes'
        else:
            return 'drop_column', 'Campo de texto con muchos faltantes'
    
    return 'mode', 'Estrategia por defecto'


def analyze_missing_values(csv_path, output_json=None):
    """Analiza valores faltantes en un archivo CSV."""
    print(f"\n{'='*60}")
    print(f"ANÁLISIS DE VALORES FALTANTES")
    print(f"{'='*60}")
    
    # Cargar datos
    df = pd.read_csv(csv_path)
    total_rows = len(df)
    total_cols = len(df.columns)
    
    print(f"\nArchivo: {csv_path}")
    print(f"Filas: {total_rows:,}")
    print(f"Columnas: {total_cols}")
    
    results = {
        'file': str(csv_path),
        'total_rows': total_rows,
        'total_cols': total_cols,
        'columns': []
    }
    
    cols_with_missing = 0
    total_missing = 0
    
    print(f"\n{'─'*60}")
    print(f"{'Columna':<25} {'Tipo':<12} {'Nulos':<10} {'% Nulos':<10} {'Estrategia'}")
    print(f"{'─'*60}")
    
    for col in df.columns:
        series = df[col]
        null_count = series.isnull().sum()
        null_pct = (null_count / total_rows) * 100
        col_type = detect_column_type(series, col)
        
        strategy, reason = suggest_imputation_strategy(series, col_type, null_pct)
        
        if null_count > 0:
            cols_with_missing += 1
            total_missing += null_count
        
        col_result = {
            'name': col,
            'type': col_type,
            'null_count': int(null_count),
            'null_percentage': round(null_pct, 2),
            'unique_values': int(series.nunique()),
            'suggested_strategy': strategy,
            'strategy_reason': reason
        }
        results['columns'].append(col_result)
        
        if null_count > 0:
            print(f"{col:<25} {col_type:<12} {null_count:<10} {null_pct:<10.2f} {strategy}")
    
    print(f"{'─'*60}")
    print(f"\nRESUMEN:")
    print(f"  Columnas con valores faltantes: {cols_with_missing}/{total_cols}")
    print(f"  Total de valores faltantes: {total_missing:,}")
    print(f"  Porcentaje total: {(total_missing / (total_rows * total_cols)) * 100:.2f}%")
    
    results['summary'] = {
        'columns_with_missing': cols_with_missing,
        'total_missing': total_missing,
        'missing_percentage': round((total_missing / (total_rows * total_cols)) * 100, 2)
    }
    
    # Guardar JSON si se especifica
    if output_json:
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nResultados guardados en: {output_json}")
    
    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python analyze_missing_values.py <input.csv> [output.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    analyze_missing_values(input_file, output_file)
