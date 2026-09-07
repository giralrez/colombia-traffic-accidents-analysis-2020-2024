# Métodos de Imputación de Valores Faltantes

## Guía de Selección

### Variables Numéricas

| Método | Cuándo usarlo | Pros | Contras |
|--------|---------------|------|---------|
| **Media** | Distribución normal, pocos outliers | Simple, preserva media | Sensible a outliers |
| **Mediana** | Distribución sesgada, muchos outliers | Robusta a outliers | Reduce varianza |
| **KNN** | Variables correlacionadas | Usa información multivariada | Lento con muchos datos |
| **Interpolación** | Series temporales con tendencia | Preserva tendencia | Asume continuidad |

### Variables Categóricas

| Método | Cuándo usarlo | Pros | Contras |
|--------|---------------|------|---------|
| **Moda** | Categorías con frecuencias similares | Simple | Ignora relaciones |
| **Constante** | Alta cardinalidad, pocos faltantes | Control total | Requiere conocimiento del dominio |

### Series Temporales

| Método | Cuándo usarlo | Pros | Contras |
|--------|---------------|------|---------|
| **Forward fill** | Datos estacionales, cortos gaps | Preserva estacionalidad | Arrastra valores antiguos |
| **Backward fill** | Datos con tendencia inversa | Usa información futura | No siempre disponible |
| **Interpolación** | Gaps largos, tendencia suave | Estimación precisa | Puede suavizar demasiado |

## Decisión Automática

El script `analyze_missing_values.py` aplica estas reglas:

1. **>70% faltantes**: Eliminar columna
2. **Numérico**: 
   - |skewness| < 0.5 → Media
   - |skewness| ≥ 0.5 → Mediana
3. **Categórico**: Moda
4. **Temporal**: Forward fill
5. **Texto**: 
   - <20% faltantes → Constante "Unknown"
   - ≥20% faltantes → Eliminar columna

## Mejores Prácticas

1. **Documentar** qué métodos se usaron
2. **Validar** que imputaciones son razonables
3. **Comparar** resultados antes/después
4. **Considerar** si la falta de datos es informativa
