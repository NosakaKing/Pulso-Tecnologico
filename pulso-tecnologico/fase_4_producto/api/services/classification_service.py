# fase_4_producto/api/services/clasificacion_service.py
import polars as pl
from data.loader import get_clasificacion

def _formatear(df: pl.DataFrame) -> list[dict]:
    return df.select([
        pl.col("Tag").alias("tag"),
        pl.col("Volumen_Total").alias("volumen_total"),
        pl.col("Share_2022").alias("share_2022"),
        pl.col("Share_2023").alias("share_2023"),
        pl.col("Crecimiento_Pct").alias("crecimiento_pct"),
        pl.col("Pendiente").alias("pendiente"),
        pl.col("R2").alias("r2"),
        pl.col("ViewCount_Promedio").alias("view_count_promedio"),
        pl.col("Categoria_Tendencia").alias("categoria_tendencia"),
    ]).to_dicts()


def obtener_clasificacion(categoria: str | None = None) -> dict:
    df = get_clasificacion()

    if categoria:
        df = df.filter(
            pl.col("Categoria_Tendencia").str.to_lowercase() == categoria.lower()
        )

    df = df.sort("Volumen_Total", descending=True)

    return {
        "total": len(df),
        "categoria": categoria,
        "data": _formatear(df),
    }


def obtener_clasificacion_tag(tag: str) -> dict | None:
    df = get_clasificacion()

    resultado = df.filter(
        pl.col("Tag").str.to_lowercase() == tag.lower()
    )

    if resultado.is_empty():
        return None

    return _formatear(resultado)[0]


def comparar_tags(tags: list[str]) -> dict:
    df = get_clasificacion()

    tags_lower = [t.lower() for t in tags]

    tags_disponibles = (
        df.select(pl.col("Tag").str.to_lowercase())
        .unique()
        .to_series()
        .to_list()
    )

    tags_encontrados    = [t for t in tags_lower if t in tags_disponibles]
    tags_no_encontrados = [t for t in tags_lower if t not in tags_disponibles]

    df_filtrado = df.filter(
        pl.col("Tag").str.to_lowercase().is_in(tags_encontrados)
    ).sort("Crecimiento_Pct", descending=True)

    return {
        "tags_solicitados":    tags_lower,
        "tags_encontrados":    tags_encontrados,
        "tags_no_encontrados": tags_no_encontrados,
        "data": _formatear(df_filtrado),
    }