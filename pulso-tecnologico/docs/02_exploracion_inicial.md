# 02_exploracion_inicial — Exploración inicial de los datos

## Objetivo

Realizar el primer diagnóstico del fichero `Questions.csv` y otros recursos auxiliares (por ejemplo `Tags.csv`) para identificar volumen, calidad, campos relevantes, tipos de dato, y problemas que afectan el análisis (missing, formato de fechas, separación de tags, duplicates, ruido por etiquetas concatenadas, etc.).

## Entradas

- `data/Questions.csv` (archivo masivo ~3.6M filas)
- `data/Tags.csv` (catalogo de etiquetas, si existe)

## Pasos principales realizados

1. Lectura perezosa y muestreos: usar `polars` con `pl.scan_csv()` para inspecciones rápidas sin materializar todo en memoria.
2. Inspección de esquema: revisar columnas, tipos, valores nulos y conteo de filas por año (extraer año desde `CreationDate`).
3. Limpieza básica: normalizar mayúsculas/minúsculas en `Tags`, eliminar espacios en blanco, y manejar valores nulos en `Title` o `Body` si es necesario.
4. Análisis de tags: separar la columna `Tags` (formato `"tag1|tag2|tag3"`) en múltiples etiquetas usando `split` y `explode` para estimar cardinalidad de la dimensión `dim_tags`.
5. Identificar outliers y problemas: filas con fechas atípicas, puntuaciones muy altas, o tags raros.

## Fragmentos de código clave (explicación)

- Lectura perezosa con Polars: `df = pl.scan_csv('Questions.csv')` — permite encadenar transformaciones y colectar solo al final.
- Extracción del año: `df = df.with_columns(pl.col('CreationDate').str.strptime(pl.Date, fmt='%Y-%m-%d').dt.year().alias('year'))` — facilita agrupaciones por año.
- Separar tags: `df = df.with_columns(pl.col('Tags').str.split('|').explode().str.to_lowercase().str.strip_chars())` — normaliza y descompone la relación M:N.

## Resultados y artefactos

- Reporte con estadísticas iniciales (conteo por año, top tags crudos, porcentaje de nulos).
- Lista de problemas detectados que guiarán el pipeline ETL (por ejemplo: tags mezclados, errores en `CreationDate`).

## Cómo reproducir

1. Activar entorno: `conda activate pulso-tecnologico` (ver `environment.yml`).
2. Abrir el cuaderno en JupyterLab o VSCode y ejecutar secuencialmente las celdas.

## Notas interpretativas

La finalidad es generar un contrato de calidad de datos: saber qué limpiar y cómo particionar para evitar sesgos en análisis posteriores.
