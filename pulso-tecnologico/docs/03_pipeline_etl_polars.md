# 03_pipeline_etl_polars — Pipeline ETL con Polars

## Objetivo

Construir un pipeline reproducible y eficiente para procesar `Questions.csv` y generar artefactos intermedios (parquets) listos para análisis: `survey_unificado.parquet`, `top_questions.parquet`, y tablas intermedias para el modelo relacional.

## Entradas

- `data/Questions.csv`

## Decisiones técnicas clave

- Uso de `polars` y `pl.scan_csv()` para procesamiento perezoso y multihilo.
- Filtrado anticipado por `CreationDate` (ej. desde 2015) para reducir volumen durante joins.
- Normalización de `Tags` usando API moderna (`.str.to_lowercase()`, `.str.strip_chars()`).

## Pasos principales

1. Crear un `LazyFrame` con `pl.scan_csv()`.
2. Aplicar filtros de rango de fecha y columnas relevantes (Id, CreationDate, Title, Score, Tags, Body).
3. Normalizar y explotar `Tags`:
   - `df = df.with_columns(pl.col('Tags').str.split('|').explode())`
   - `df = df.with_columns(pl.col('Tags').str.to_lowercase().str.strip_chars())`
4. Eliminar duplicados y construir `dim_tags` como un catálogo único.
5. Materializar tablas y exportar a Parquet en `data/datos_procesados/`.

## Artefactos generados

- `data/datos_procesados/survey_unificado.parquet` — tabla principal con preguntas normalizadas.
- `data/datos_procesados/top_questions.parquet` — subset de preguntas de mayor interés por score.
- `data/datos_procesados/dim_tags.parquet` — catálogo de tags únicos.

## Reproducción (comandos)

Ejecutar el cuaderno en el entorno con las dependencias instaladas. Alternativa no interactiva:

```bash
conda activate pulso-tecnologico
python -m pip install polars
# desde el directorio del proyecto
jupyter nbconvert --to notebook --execute fase_2_datos/03_pipeline_etl_polars.ipynb --ExecutePreprocessor.timeout=600
```

## Errores comunes y soluciones

- `AttributeError` en métodos `.str.*`: actualizar uso a `to_lowercase()` y `strip_chars()` según la versión de Polars.
- Problemas de memoria: usar `scan_csv()` y evitar `collect()` hasta el final.
