# 06_clasificacion_auge_declive — Clasificación: en auge / en declive

## Objetivo

Clasificar cada tecnología en categorías de tendencia (por ejemplo: `en auge`, `estable`, `en declive`) usando reglas heurísticas sobre series temporales y métricas de volumen y crecimiento.

## Metodología general

1. Calcular métricas por tag: crecimiento interanual, volumen promedio, varianza.
2. Definir umbrales que separen `en auge` (crecimiento consistente y volumen creciente), `estable` (variaciones pequeñas) y `en declive` (tendencia negativa sostenida).
3. Validar la clasificación con casos de control (ej. tecnologías conocidas que cambiaron recientemente).

## Pasos en el cuaderno

- Cálculo de tasas de crecimiento y smoothing (media móvil).
- Aplicación de reglas y etiquetado.
- Visualización de ejemplos representativos por categoría.

## Uso en tesis

La clasificación sirve para priorizar qué tecnologías recomendar o retirar de un currículo. En la tesis, incluir la lógica de umbrales y la sensibilidad del resultado sería importante para la reproducibilidad.
