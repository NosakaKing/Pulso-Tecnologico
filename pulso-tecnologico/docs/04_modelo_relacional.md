# 04_modelo_relacional — Modelado relacional 3NF

## Objetivo

Normalizar el output del pipeline ETL en un modelo relacional en tercera forma normal (3NF) para facilitar consultas, reducir redundancia y soportar rutas de API eficientes.

## Entidades definidas

- `dim_questions`: preguntas (Id, CreationDate, Title, Score, etc.)
- `dim_tags`: catálogo de tecnologías (Id_tag, tag_name)
- `fact_question_tags`: tabla puente many-to-many (question_id, tag_id)

## Pasos principales

1. Cargar parquets generados por el ETL.
2. Generar `dim_questions` con columnas relevantes y claves primarias.
3. Generar `dim_tags` deduplicando y limpiando strings.
4. Construir `fact_question_tags` uniendo `dim_questions` con `dim_tags` mediante un explode de tags y un join por nombre/slug.
5. Validar integridad: conteos coherentes entre fact y dims, claves únicas, ausencia de nulls en FK.
6. Exportar tablas finales a `data/datos_procesados/` en Parquet.

## Código y consideraciones

- Evitar joins costosos materializando solo cuando sea estrictamente necesario.
- Usar `lru_cache` cuando las funciones de carga se exponen desde `fase_4_producto/api/data/loader.py`.

## Reproducción

Ejecutar el cuaderno y verificar que los parquets resultantes existen y tienen schema esperado.

```bash
jupyter nbconvert --to notebook --execute fase_2_datos/04_modelo_relacional.ipynb --ExecutePreprocessor.timeout=600
ls data/datos_procesados
```

## Notas para la tesis

Este cuaderno muestra cómo pasar de dataframes analíticos a un esquema normalizado adecuado para una API y consultas relacionales: es evidencia de diseño y gobernanza de datos en la tesis.
