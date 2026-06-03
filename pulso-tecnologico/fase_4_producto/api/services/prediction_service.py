import polars as pl
import pandas as pd
from prophet import Prophet
from data.loader import get_series_mensuales


def _calcular_market_share(df: pl.DataFrame) -> pl.DataFrame:
    """
    Calcula el Market Share mensual de cada tag.

    Market_Share = (Count del tag en ese mes / Total de preguntas de TODOS los tags ese mes) * 100

    Esto elimina el sesgo del volumen absoluto — si Stack Overflow
    recibe menos preguntas en 2023 por ChatGPT, el market share
    de Python puede mantenerse aunque el Count baje.
    """
    # Total de preguntas por mes (suma de todos los tags)
    total_por_mes = (
        df.group_by("YearMonth")
        .agg(pl.col("Count").sum().alias("Total_Mes"))
    )

    # Join con el dataframe original
    df_con_total = df.join(total_por_mes, on="YearMonth", how="left")

    # Calcular market share como porcentaje
    df_con_share = df_con_total.with_columns(
        (pl.col("Count") / pl.col("Total_Mes") * 100)
        .alias("Market_Share")
    )

    return df_con_share


def predict_tag(tag: str, periods: int) -> dict | None:
    """
    Entrena Prophet con el Market Share histórico de un tag
    y devuelve la proyección futura.

    Usamos Market Share en vez de Count absoluto porque:
    - El volumen total de SO varía por eventos externos (ChatGPT, etc.)
    - El Market Share refleja la participación relativa real
    - Es comparable entre tecnologías independientemente del volumen
    """

    # ── 1. Cargar serie histórica completa (TODOS los tags) ───────────
    # Necesitamos todos los tags para calcular el total mensual
    df_completo = get_series_mensuales()

    # ── 2. Calcular Market Share ──────────────────────────────────────
    df_con_share = _calcular_market_share(df_completo)

    # ── 3. Filtrar el tag solicitado ──────────────────────────────────
    df_tag = (
        df_con_share
        .filter(pl.col("Tag").str.to_lowercase() == tag.lower())
        .sort("YearMonth")
    )

    if df_tag.is_empty():
        return None

    # ── 4. Preparar para Prophet: ds + y (Market Share) ──────────────
    df_prophet = df_tag.select([
        pl.col("YearMonth").alias("ds"),
        pl.col("Market_Share").alias("y"),   # ← market share, no Count
    ]).to_pandas()

    # Asegurar formato datetime correcto sin timezone
    df_prophet["ds"] = pd.to_datetime(
        df_prophet["ds"]
    ).dt.tz_localize(None)

    # Eliminar duplicados de fecha (por si hay filas repetidas)
    df_prophet = (
        df_prophet
        .groupby("ds", as_index=False)
        .agg({"y": "sum"})
        .sort_values("ds")
        .reset_index(drop=True)
    )

    # ── 5. Crear y entrenar Prophet ───────────────────────────────────
    model = Prophet(
        yearly_seasonality=True,   # Detecta patrones anuales en SO
        weekly_seasonality=False,  # Datos mensuales — no aplica
        daily_seasonality=False,   # Datos mensuales — no aplica
        interval_width=0.90,       # Banda de confianza del 90%
    )

    model.fit(df_prophet)

    # ── 6. Generar fechas futuras ─────────────────────────────────────
    future = model.make_future_dataframe(
        periods=periods,
        freq="MS"   # Month Start — frecuencia mensual
    )

    # ── 7. Predecir ───────────────────────────────────────────────────
    forecast = model.predict(future)

    # ── 8. Separar solo el futuro ─────────────────────────────────────
    last_date = df_prophet["ds"].max()

    forecast_future = forecast[
        forecast["ds"] > last_date
    ][["ds", "yhat", "yhat_lower", "yhat_upper"]]

    # ── 9. Serializar a JSON ──────────────────────────────────────────
    records = [
        {
            "ds":          row["ds"].strftime("%Y-%m"),
            "yhat":        round(float(row["yhat"]),       4),
            "yhat_lower":  round(float(row["yhat_lower"]), 4),
            "yhat_upper":  round(float(row["yhat_upper"]), 4),
        }
        for _, row in forecast_future.iterrows()
    ]

    return {
        "tag":                  tag.lower(),
        "periods":              periods,
        "last_historical_date": last_date.strftime("%Y-%m"),
        "unit":                 "market_share_pct",  # ← documenta la unidad
        "data":                 records,
    }