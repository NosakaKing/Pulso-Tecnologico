# 07b_forecast_prophet — Proyecciones con Prophet

## Objetivo

Entrenar modelos de serie temporal (Prophet) para proyectar la evolución futura de la popularidad de tecnologías y obtener intervalos de confianza sobre las predicciones.

## Pasos

1. Preparar series con columnas `ds` (fecha) y `y` (valor: conteo o índice).
2. Entrenar `Prophet()` con parámetros por defecto o ajustados (seasonality, changepoints).
3. Predecir para el horizonte deseado (p.ej. 12-36 meses).
4. Visualizar predicción con intervalos de incertidumbre.

## Artefactos

- Modelos serializados y dataframes con `forecast` para varias tecnologías.
- Gráficos con `plotly` o `matplotlib` para mostrar tendencias proyectadas.

## Reproducir

```bash
conda activate pulso-tecnologico
jupyter nbconvert --to notebook --execute fase_3_analisis/07b_forecast_prophet.ipynb
```

## Notas

Prophet requiere series limpias y suficientes observaciones; validar supuestos antes de presentar proyecciones en la tesis.
