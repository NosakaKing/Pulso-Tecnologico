# 09_calidad_por_tecnologia — Calidad por tecnología

## Objetivo

Evaluar la 'calidad' o confiabilidad de la señal para cada tecnología usando métricas como: volumen de preguntas, dispersion de score, proporción de preguntas respondidas, y consistencia temporal.

## Pasos

1. Agregar métricas por `tag` y `year` (count, mean(score), answered_rate).
2. Construir indicadores compuestos que permitan filtrar tags con señales débiles (poco volumen o alta volatilidad).
3. Visualizar el espacio resultado y proponer criterios de corte.

## Uso en el proyecto

Sirve para priorizar qué tags considerar en análisis más profundos (por ejemplo, forecasting) y cuáles descartar por ruido estadístico.
