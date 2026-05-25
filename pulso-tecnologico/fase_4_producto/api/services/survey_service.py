# fase_4_producto/api/services/survey_service.py
import polars as pl
from data.loader import get_survey


def obtener_evolucion_todos(
    start_year: int | None = None,
    end_year: int | None = None,
) -> dict:
    df = get_survey()

    if start_year:
        df = df.filter(pl.col("year") >= start_year)
    if end_year:
        df = df.filter(pl.col("year") <= end_year)

    # Agrupamos por tag para devolver una serie por tecnología
    tags = df.select("tag").unique().sort("tag").to_series().to_list()

    series = []
    for tag in tags:
        puntos = (
            df.filter(pl.col("tag") == tag)
            .sort("year")
            .select(["year", "used_pct", "wanted_pct", "n_respondents"])
            .to_dicts()
        )
        series.append({"tag": tag, "data": puntos})

    return {
        "total_tags": len(series),
        "start_year": start_year,
        "end_year": end_year,
        "series": series,
    }

def obtener_evolucion(tag: str) -> dict | None:
    df = get_survey()

    df_tag = df.filter(
        pl.col("tag").str.to_lowercase() == tag.lower()
    ).sort("year")

    if df_tag.is_empty():
        return None

    registros = df_tag.select([
        pl.col("year"),
        pl.col("used_pct"),
        pl.col("wanted_pct"),
        pl.col("n_respondents"),
    ]).to_dicts()

    return {
        "tag": tag.lower(),
        "total_años": len(registros),
        "data": registros,
    }