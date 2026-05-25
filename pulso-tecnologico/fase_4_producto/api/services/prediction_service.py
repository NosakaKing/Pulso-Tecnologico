import polars as pl
from prophet import Prophet
from data.loader import get_series_mensuales

def predict_tag(tag: str, periods: int) -> dict | None:
    df = get_series_mensuales()

    # Filter historical data for the requested tag
    df_tag = df.filter(
        pl.col("Tag").str.to_lowercase() == tag.lower()
    ).sort("YearMonth")

    if df_tag.is_empty():
        return None

    # Prophet requires exactly two columns: ds and y
    df_prophet = df_tag.select([
        pl.col("YearMonth").alias("ds"),
        pl.col("Count").cast(pl.Float64).alias("y"),
    ]).to_pandas()

    # Train model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        interval_width=0.90,  # 90% confidence interval
    )
    model.fit(df_prophet)

    # Generate future dates
    future = model.make_future_dataframe(periods=periods, freq="MS")
    forecast = model.predict(future)

    # Return only future months (after last historical date)
    last_date = df_prophet["ds"].max()
    forecast_future = forecast[forecast["ds"] > last_date][
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ]

    records = [
        {
            "ds":          row["ds"].strftime("%Y-%m"),
            "yhat":        round(row["yhat"], 4),
            "yhat_lower":  round(row["yhat_lower"], 4),
            "yhat_upper":  round(row["yhat_upper"], 4),
        }
        for _, row in forecast_future.iterrows()
    ]

    return {
        "tag":                  tag.lower(),
        "periods":              periods,
        "last_historical_date": last_date.strftime("%Y-%m"),
        "data":                 records,
    }