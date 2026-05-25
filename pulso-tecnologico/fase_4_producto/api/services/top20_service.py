# fase_4_producto/api/services/top20_service.py
import polars as pl
from data.loader import get_top20

def obtener_top20(
    start_year: int | None = None,
    end_year: int | None = None,
    categoria: str | None = None,
) -> dict:
    df = get_top20()

    # Filtro de rango de años
    if start_year:
        df = df.filter(pl.col("Year") >= start_year)
    if end_year:
        df = df.filter(pl.col("Year") <= end_year)

    # Filtro de categoría
    if categoria:
        df = df.filter(pl.col("Categoria").str.to_lowercase() == categoria.lower())

    # Acumular conteos por Tag + Categoria (pueden venir varios años)
    df = (
        df.group_by(["Tag", "Categoria"])
        .agg(pl.col("Count").sum().alias("count"))
        .sort("count", descending=True)
        .head(20)
    )

    registros = df.select([
        pl.col("Tag").alias("tag"),
        pl.col("count"),
        pl.col("Categoria").alias("categoria"),
    ]).to_dicts()

    return {
        "total": len(registros),
        "start_year": start_year,
        "end_year": end_year,
        "categoria": categoria,
        "data": registros,
    }