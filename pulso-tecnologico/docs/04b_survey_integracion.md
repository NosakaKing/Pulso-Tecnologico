# 04b_survey_integracion — Integración de la encuesta de desarrolladores

## Objetivo

Integrar la encuesta (survey) con el modelo de preguntas para añadir evidencia de uso y preferencia desde la comunidad desarrolladora. Permite contrastar métricas de `used_pct` y `wanted_pct` con el volumen de preguntas en Stack Overflow.

## Entradas

- `data/datos_procesados/survey_unificado.parquet` (o archivo original de encuesta transformado)
- Tablas normalizadas del modelo relacional (`dim_tags`, `dim_questions`).

## Pasos

1. Cargar la tabla de encuesta y normalizar nombres de tags para que coincidan con `dim_tags`.
2. Merge/Join entre encuesta y `dim_tags` por `tag_name`.
3. Calcular métricas derivadas: diferencia entre `used_pct` y `wanted_pct`, tendencias por año.
4. Exportar tabla de cruce para análisis (por ejemplo `tabla_cruce_final.parquet`).

## Interpretación

La integración añade una segunda dimensión de evidencia: no basta con que haya muchas preguntas para suponer demanda. La encuesta aporta la percepción y uso real de tecnologías en la comunidad.

## Reproducción

```bash
jupyter nbconvert --to notebook --execute fase_2_datos/04b_survey_integracion.ipynb
```
