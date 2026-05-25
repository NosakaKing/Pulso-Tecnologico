# fase_4_producto/api/services/timeseries_service.py
import polars as pl
from data.loader import get_series_mensuales

def obtener_timeseries(tags: list[str]) -> dict:
    df = get_series_mensuales()

    tags_lower = [t.lower() for t in tags]

    # Tags que realmente existen en el dataset
    tags_disponibles = (
        df.select(pl.col("Tag").str.to_lowercase())
        .unique()
        .to_series()
        .to_list()
    )

    tags_encontrados     = [t for t in tags_lower if t in tags_disponibles]
    tags_no_encontrados  = [t for t in tags_lower if t not in tags_disponibles]

    series = []
    for tag in tags_encontrados:
        puntos = (
    df.filter(pl.col("Tag").str.to_lowercase() == tag)
    .sort("YearMonth")
    .select([
        pl.col("YearMonth").dt.strftime("%Y-%m").alias("year_month"),  # ← fix aquí
        pl.col("Count").alias("count"),
        pl.col("MA3").alias("ma3"),
    ])
    .to_dicts()
)
        series.append({"tag": tag, "data": puntos})

    return {
        "tags_solicitados":    tags_lower,
        "tags_encontrados":    tags_encontrados,
        "tags_no_encontrados": tags_no_encontrados,
        "series":              series,
    }