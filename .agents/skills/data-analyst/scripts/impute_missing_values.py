#!/usr/bin/env python3
"""
Imputación inteligente de valores faltantes.
Aplica métodos estadísticos apropiados según el tipo de dato.
"""

import pandas as pd
import numpy as np
import json
import sys
from pathlib import Path
from sklearn.impute import KNNImputer


def impute_numeric_mean(series):
    """Imputa valores numéricos con la media."""
    return series.fillna(series.mean())


def impute_numeric_median(series):
    """Imputa valores numéricos con la mediana."""
    return series.fillna(series.median())


def impute_categorical_mode(series):
    """Imputa valores categóricos con la moda."""
    mode_val = series.mode()
    if len(mode_val) > 0:
        return series.fillna(mode_val[0])
    return series


def impute_forward_fill(series):
    """Imputa con forward fill para series temporales."""
    return series.fillna(method='ffill')


def impute_constant(series, fill_value='Unknown'):
    """Imputa con un valor constante."""
    return series.fillna(fill_value)


def impute_knn(df, columns, n_neighbors=5):
    """Imputa valores numéricos usando KNN."""
    imputer = KNNImputer(n_neighbors=n_neighbors)
    df[columns] = imputer.fit_transform(df[columns])
    return df


def impute_missing_values(csv_path, analysis_json=None, output_csv=None):
    """Imputa valores faltantes basándose en el análisis."""
    print(f"\n{'='*60}")
    print(f"IMPUTACIÓN DE VALORES FALTANTES")
    print(f"{'='*60}")
    
    # Cargar datos
    df = pd.read_csv(csv_path)
    original_shape = df.shape
    print(f"\nArchivo original: {csv_path}")
    print(f"Dimensiones: {original_shape[0]} filas x {original_shape[1]} columnas")
    
    # Cargar o realizar análisis
    if analysis_json and Path(analysis_json).exists():
        with open(analysis_json, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
    else:
        from analyze_missing_values import analyze_missing_values
        analysis = analyze_missing_values(csv_path)
    
    # Estadísticas antes de imputación
    missing_before = df.isnull().sum().sum()
    print(f"\nValores faltantes antes: {missing_before:,}")
    
    # Separar columnas numéricas para KNN
    numeric_cols_for_knn = []
    
    print(f"\n{'─'*60}")
    print(f"{'Columna':<25} {'Método':<20} {'Valores imputados'}")
    print(f"{'─'*60}")
    
    for col_info in analysis['columns']:
        col_name = col_info['name']
        strategy = col_info['suggested_strategy']
        null_count = col_info['null_count']
        
        if null_count == 0:
            continue
        
        if strategy == 'drop_column':
            df = df.drop(columns=[col_name])
            print(f"{col_name:<25} {'DROP COLUMN':<20} {null_count}")
        elif strategy == 'mean':
            df[col_name] = impute_numeric_mean(df[col_name])
            print(f"{col_name:<25} {'MEDIA':<20} {null_count}")
        elif strategy == 'median':
            df[col_name] = impute_numeric_median(df[col_name])
            print(f"{col_name:<25} {'MEDIANA':<20} {null_count}")
        elif strategy == 'mode':
            df[col_name] = impute_categorical_mode(df[col_name])
            print(f"{col_name:<25} {'MODA':<20} {null_count}")
        elif strategy == 'forward_fill':
            df[col_name] = impute_forward_fill(df[col_name])
            print(f"{col_name:<25} {'FORWARD FILL':<20} {null_count}")
        elif strategy == 'constant':
            df[col_name] = impute_constant(df[col_name])
            print(f"{col_name:<25} {'CONSTANTE':<20} {null_count}")
        elif strategy == 'knn':
            numeric_cols_for_knn.append(col_name)
        elif strategy == 'none':
            continue
    
    # Aplicar KNN si hay columnas numéricas correlacionadas
    if numeric_cols_for_knn:
        numeric_available = [c for c in numeric_cols_for_knn if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
        if len(numeric_available) >= 2:
            df = impute_knn(df, numeric_available)
            print(f"{'KNN (lote)':<25} {'KNN':<20} {len(numeric_available)} columnas")
    
    print(f"{'─'*60}")
    
    # Estadísticas después de imputación
    missing_after = df.isnull().sum().sum()
    print(f"\nValores faltantes después: {missing_after:,}")
    print(f"Valores imputados: {missing_before - missing_after:,}")
    print(f"Dimensiones finales: {df.shape[0]} filas x {df.shape[1]} columnas")
    
    # Guardar resultado
    if output_csv:
        df.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"\nArchivo guardado: {output_csv}")
    
    return df


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python impute_missing_values.py <input.csv> [analysis.json] [output.csv]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    analysis_file = sys.argv[2] if len(sys.argv) > 2 else None
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    impute_missing_values(input_file, analysis_file, output_file)
