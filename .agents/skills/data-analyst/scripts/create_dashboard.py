#!/usr/bin/env python3
"""
Dashboard interactivo con Plotly Dash para análisis de datos.
Genera visualizaciones interactivas de tendencias y patrones.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import sys
from pathlib import Path


def detect_columns(df):
    """Detecta tipos de columnas automáticamente."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = []
    
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            datetime_cols.append(col)
        elif col in categorical_cols:
            try:
                pd.to_datetime(df[col].head(100))
                datetime_cols.append(col)
                categorical_cols.remove(col)
            except:
                pass
    
    return numeric_cols, categorical_cols, datetime_cols


def create_summary_stats(df, numeric_cols):
    """Crea tabla de estadísticas resumen."""
    stats = df[numeric_cols].describe().T
    stats['missing'] = df[numeric_cols].isnull().sum()
    stats['missing_pct'] = (stats['missing'] / len(df) * 100).round(2)
    return stats.reset_index().rename(columns={'index': 'Variable'})


def create_time_series(df, datetime_cols, numeric_cols):
    """Crea gráficos de series temporales."""
    if not datetime_cols:
        return None
    
    fig = make_subplots(
        rows=1, cols=1,
        subplot_titles=['Tendencia Temporal']
    )
    
    for i, dt_col in enumerate(datetime_cols[:2]):
        for num_col in numeric_cols[:3]:
            temp_df = df.groupby(dt_col)[num_col].mean().reset_index()
            temp_df[dt_col] = pd.to_datetime(temp_df[dt_col])
            temp_df = temp_df.sort_values(dt_col)
            
            fig.add_trace(
                go.Scatter(
                    x=temp_df[dt_col],
                    y=temp_df[num_col],
                    name=f'{num_col}',
                    mode='lines+markers'
                ),
                row=1, col=1
            )
    
    fig.update_layout(height=400, title_text="Análisis de Series Temporales")
    return fig


def create_distributions(df, numeric_cols):
    """Crea histogramas de distribución."""
    n_cols = min(3, len(numeric_cols))
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig = make_subplots(
        rows=n_rows, cols=n_cols,
        subplot_titles=[f'Distribución de {col}' for col in numeric_cols[:n_rows*n_cols]]
    )
    
    for i, col in enumerate(numeric_cols[:n_rows*n_cols]):
        row = i // n_cols + 1
        col_pos = i % n_cols + 1
        
        fig.add_trace(
            go.Histogram(x=df[col], name=col, nbinsx=30),
            row=row, col=col_pos
        )
    
    fig.update_layout(
        height=300 * n_rows,
        title_text="Distribución de Variables Numéricas",
        showlegend=False
    )
    return fig


def create_correlation_heatmap(df, numeric_cols):
    """Crea mapa de correlación."""
    if len(numeric_cols) < 2:
        return None
    
    corr_matrix = df[numeric_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu_r',
        zmin=-1, zmax=1,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        title_text="Matriz de Correlación",
        height=500,
        width=700
    )
    return fig


def create_categorical_charts(df, categorical_cols):
    """Crea gráficos de barras para variables categóricas."""
    if not categorical_cols:
        return None
    
    n_cols = min(2, len(categorical_cols))
    n_rows = (len(categorical_cols) + n_cols - 1) // n_cols
    
    fig = make_subplots(
        rows=n_rows, cols=n_cols,
        subplot_titles=[f'Distribución de {col}' for col in categorical_cols[:n_rows*n_cols]]
    )
    
    for i, col in enumerate(categorical_cols[:n_rows*n_cols]):
        row = i // n_cols + 1
        col_pos = i % n_cols + 1
        
        value_counts = df[col].value_counts().head(10)
        
        fig.add_trace(
            go.Bar(x=value_counts.index.astype(str), y=value_counts.values, name=col),
            row=row, col=col_pos
        )
    
    fig.update_layout(
        height=400 * n_rows,
        title_text="Distribución de Variables Categóricas",
        showlegend=False
    )
    return fig


def create_scatter_matrix(df, numeric_cols):
    """Crea matriz de dispersión."""
    cols_for_scatter = numeric_cols[:5]
    
    if len(cols_for_scatter) < 2:
        return None
    
    fig = px.scatter_matrix(
        df[cols_for_scatter],
        dimensions=cols_for_scatter,
        title="Matriz de Dispersión"
    )
    
    fig.update_layout(height=800, width=800)
    return fig


def create_dashboard(csv_path, output_dir='./visualizations', port=8050):
    """Crea dashboard interactivo con Plotly Dash."""
    print(f"\n{'='*60}")
    print(f"CREANDO DASHBOARD INTERACTIVO")
    print(f"{'='*60}")
    
    # Cargar datos
    df = pd.read_csv(csv_path)
    print(f"\nArchivo: {csv_path}")
    print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
    
    # Detectar columnas
    numeric_cols, categorical_cols, datetime_cols = detect_columns(df)
    print(f"\nColumnas detectadas:")
    print(f"  Numéricas: {len(numeric_cols)}")
    print(f"  Categóricas: {len(categorical_cols)}")
    print(f"  Temporales: {len(datetime_cols)}")
    
    # Crear directorio de salida
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Guardar gráficos estáticos como HTML
    print(f"\nGenerando visualizaciones estáticas...")
    
    # Estadísticas resumen
    stats = create_summary_stats(df, numeric_cols)
    stats_html = stats.to_html(index=False, classes='table table-striped')
    
    # Series temporales
    ts_fig = create_time_series(df, datetime_cols, numeric_cols)
    if ts_fig:
        ts_fig.write_html(str(output_path / 'time_series.html'))
        print(f"  ✓ time_series.html")
    
    # Distribuciones
    dist_fig = create_distributions(df, numeric_cols)
    dist_fig.write_html(str(output_path / 'distributions.html'))
    print(f"  ✓ distributions.html")
    
    # Mapa de correlación
    corr_fig = create_correlation_heatmap(df, numeric_cols)
    if corr_fig:
        corr_fig.write_html(str(output_path / 'correlation_heatmap.html'))
        print(f"  ✓ correlation_heatmap.html")
    
    # Gráficos categóricos
    cat_fig = create_categorical_charts(df, categorical_cols)
    if cat_fig:
        cat_fig.write_html(str(output_path / 'categorical_charts.html'))
        print(f"  ✓ categorical_charts.html")
    
    # Matriz de dispersión
    scatter_fig = create_scatter_matrix(df, numeric_cols)
    if scatter_fig:
        scatter_fig.write_html(str(output_path / 'scatter_matrix.html'))
        print(f"  ✓ scatter_matrix.html")
    
    # Crear app Dash
    print(f"\nIniciando servidor Dash en puerto {port}...")
    
    app = dash.Dash(__name__)
    
    app.layout = html.Div([
        html.H1("Dashboard de Análisis de Datos", 
                style={'textAlign': 'center', 'color': '#2c3e50'}),
        
        html.Div([
            html.H2("Estadísticas Resumen"),
            html.Div(html.Table([
                html.Tr([html.Th(col) for col in stats.columns])
            ] + [
                html.Tr([html.Td(stats.iloc[i][col]) for col in stats.columns])
                for i in range(min(10, len(stats)))
            ], className='table table-striped'))
        ], style={'padding': '20px'}),
        
        html.Div([
            html.H2("Series Temporales"),
            dcc.Graph(figure=ts_fig) if ts_fig else html.P("No hay columnas temporales")
        ], style={'padding': '20px'}),
        
        html.Div([
            html.H2("Distribuciones"),
            dcc.Graph(figure=dist_fig)
        ], style={'padding': '20px'}),
        
        html.Div([
            html.H2("Correlaciones"),
            dcc.Graph(figure=corr_fig) if corr_fig else html.P("No hay suficientes columnas numéricas")
        ], style={'padding': '20px'}),
        
        html.Div([
            html.H2("Variables Categóricas"),
            dcc.Graph(figure=cat_fig) if cat_fig else html.P("No hay columnas categóricas")
        ], style={'padding': '20px'}),
        
        html.Div([
            html.H2("Matriz de Dispersión"),
            dcc.Graph(figure=scatter_fig) if scatter_fig else html.P("No hay suficientes columnas numéricas")
        ], style={'padding': '20px'})
        
    ], style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '1200px', 'margin': '0 auto'})
    
    print(f"\nDashboard listo en: http://127.0.0.1:{port}")
    print(f"Archivos estáticos guardados en: {output_dir}/")
    
    app.run(debug=False, port=port)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python create_dashboard.py <input.csv> [output_dir] [port]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_directory = sys.argv[2] if len(sys.argv) > 2 else './visualizations'
    server_port = int(sys.argv[3]) if len(sys.argv) > 3 else 8050
    
    create_dashboard(input_file, output_directory, server_port)
