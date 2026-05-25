# fase_4_producto/api/services/cruce_service.py
import polars as pl
from data.loader import get_tabla_cruce

COLUMNAS_ORDEN = {
    "demand_gap":     "Demand_Gap",
    "crecimiento":    "Crecimiento_Pct",
    "used":           "used_pct",
    "wanted":         "wanted_pct",
    "views":          "ViewCount_Promedio",
}

def obtener_cruce(
    orden: str | None = None,
    categoria: str | None = None,
) -> dict:
    df = get_tabla_cruce()

    if categoria:
        df = df.filter(
            pl.col("Categoria_Tendencia").str.to_lowercase() == categoria.lower()
        )

    col_orden = COLUMNAS_ORDEN.get(orden, "Demand_Gap")
    df = df.sort(col_orden, descending=True)

    registros = df.select([
        pl.col("Tag").alias("tag"),
        pl.col("Categoria_Tendencia").alias("categoria_tendencia"),
        pl.col("used_pct"),
        pl.col("wanted_pct"),
        pl.col("Demand_Gap").alias("demand_gap"),
        pl.col("Crecimiento_Pct").alias("crecimiento_pct"),
        pl.col("Pendiente").alias("pendiente"),
        pl.col("R2").alias("r2"),
        pl.col("ViewCount_Promedio").alias("view_count_promedio"),
        pl.col("n_respondents"),
    ]).to_dicts()

    return {
        "total": len(registros),
        "orden": orden,
        "categoria": categoria,
        "data": registros,
    }



def obtener_recomendaciones() -> dict:
    df = get_tabla_cruce()

    # Score compuesto: normaliza ambas métricas y las combina
    # Demand_Gap pesa 60% (más importante para currículo)
    # Crecimiento_Pct pesa 40%
    df = df.with_columns([
        (
            pl.col("Demand_Gap") * 0.6 +
            (pl.col("Crecimiento_Pct") / 100) * 0.4
        ).alias("score")
    ]).sort("score", descending=True).head(5)

    registros = df.select([
        pl.col("Tag").alias("tag"),
        pl.col("Categoria_Tendencia").alias("categoria_tendencia"),
        pl.col("Demand_Gap").alias("demand_gap"),
        pl.col("Crecimiento_Pct").alias("crecimiento_pct"),
        pl.col("used_pct"),
        pl.col("wanted_pct"),
    ]).to_dicts()

    for row in registros:
        row["motivo"] = _generar_motivo(row)

    return {"total": len(registros), "data": registros}


def _generar_motivo(row: dict) -> str:
    partes = []

    if row["demand_gap"] > 0:
        partes.append(f"{row['demand_gap']*100:.1f}% más devs quieren aprenderlo de los que ya lo usan")
    else:
        partes.append(f"tecnología consolidada con {row['used_pct']*100:.1f}% de adopción actual")

    if row["crecimiento_pct"] > 0:
        partes.append(f"creció {row['crecimiento_pct']:.1f}% en Stack Overflow")
    else:
        partes.append(f"actividad estable en Stack Overflow")

    partes.append(f"tendencia: {row['categoria_tendencia']}")

    return " — ".join(partes)