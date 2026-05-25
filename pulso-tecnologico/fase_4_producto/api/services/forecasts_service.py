# fase_4_producto/api/services/forecasts_service.py
import polars as pl
from data.loader import get_forecasts

def obtener_forecasts(tags: list[str] | None = None) -> dict:
    df = get_forecasts()

    tags_disponibles = (
        df.select(pl.col("tag").str.to_lowercase())
        .unique()
        .to_series()
        .to_list()
    )

    # Si no se pasan tags devolvemos todos
    if not tags:
        tags_lower         = tags_disponibles
        tags_encontrados   = tags_disponibles
        tags_no_encontrados = []
    else:
        tags_lower          = [t.lower() for t in tags]
        tags_encontrados    = [t for t in tags_lower if t in tags_disponibles]
        tags_no_encontrados = [t for t in tags_lower if t not in tags_disponibles]

    series = []
    for tag in tags_encontrados:
        puntos = (
            df.filter(pl.col("tag").str.to_lowercase() == tag)
            .sort("ds")
            .select([
                pl.col("ds").dt.strftime("%Y-%m").alias("ds"),  # date → string
                pl.col("yhat"),
                pl.col("yhat_lower"),
                pl.col("yhat_upper"),
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