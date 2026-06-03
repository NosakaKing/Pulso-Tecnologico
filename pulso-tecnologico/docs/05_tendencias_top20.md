# 05_tendencias_top20 — Tendencias Top20

## Objetivo

Identificar las 20 tecnologías más relevantes por año y categoría (frontend, backend, data, infra, etc.) y visualizar su evolución temporal para detectar ganadores y perdedores en el ecosistema técnico.

## Entradas

- `data/datos_procesados/top20.parquet` o salida agregada del pipeline.

## Pasos

1. Cargar la tabla de top20.
2. Agregar por `tag` y `year` para construir series temporales.
3. Visualizar con `plotly` o `matplotlib` para mostrar ranking o heatmaps.
4. Guardar figuras y tablas resumen.

## Artefactos

- Gráficos interactivos (Plotly) embebibles en dashboard.
- Tablas con rank por año para ser usadas en el informe final.

## Reproducción

```bash
jupyter nbconvert --to notebook --execute fase_3_analisis/05_tendencias_top20.ipynb
```

## Observaciones para tesis

Este cuaderno resume el resultado más directo y comunicable del proyecto: ¿qué tecnologías tienen peso en cada año? En la tesis puede usarse como evidencia empírica al argumentar recomendaciones curriculares.
