import polars as pl
import pandas as pd
from prophet import Prophet
from data.loader import get_series_mensuales


def predict_tag(tag: str, periods: int) -> dict | None:
    # Load historical monthly series
    df = get_series_mensuales()

    # Filter by tag
    df_tag = df.filter(
        pl.col("Tag").str.to_lowercase() == tag.lower()
    ).sort("YearMonth")

    # If tag does not exist
    if df_tag.is_empty():
        return None

    # Prophet requires columns: ds (date) and y (value)
    df_prophet = df_tag.select([
        pl.col("YearMonth").alias("ds"),
        pl.col("Count").cast(pl.Float64).alias("y"),
    ]).to_pandas()

    # Ensure proper datetime format
    df_prophet["ds"] = pd.to_datetime(
        df_prophet["ds"]
    ).dt.tz_localize(None)

    # Remove duplicate dates
    df_prophet = (
        df_prophet
        .groupby("ds", as_index=False)
        .agg({"y": "sum"})
        .sort_values("ds")
        .reset_index(drop=True)
    )

    # Create Prophet model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        interval_width=0.90,
    )

    # Train model
    model.fit(df_prophet)

    # Generate future dates
    future = model.make_future_dataframe(
        periods=periods,
        freq="MS"
    )

    # Predict future values
    forecast = model.predict(future)

    # Get last historical date
    last_date = df_prophet["ds"].max()

    # Keep only future predictions
    forecast_future = forecast[
        forecast["ds"] > last_date
    ][
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ]

    # Convert to JSON-friendly structure
    records = [
        {
            "ds": row["ds"].strftime("%Y-%m"),
            "yhat": round(float(row["yhat"]), 4),
            "yhat_lower": round(float(row["yhat_lower"]), 4),
            "yhat_upper": round(float(row["yhat_upper"]), 4),
        }
        for _, row in forecast_future.iterrows()
    ]

    return {
        "tag": tag.lower(),
        "periods": periods,
        "last_historical_date": last_date.strftime("%Y-%m"),
        "data": records,
    }