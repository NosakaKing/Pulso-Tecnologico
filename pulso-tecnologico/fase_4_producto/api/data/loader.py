from functools import lru_cache
import polars as pl
import sys
from pathlib import Path

# Para que encuentre config.py
sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import (
    SURVEY_PATH,
    TOP_QUESTIONS_PATH,
    CLASIFICACION_PATH,
    FORECASTS_PATH,
    SERIES_MENSUALES_PATH,
    TABLA_CRUCE_PATH,
    TOP20_PATH,
)


@lru_cache(maxsize=1)
def get_survey() -> pl.DataFrame:
    return pl.read_parquet(SURVEY_PATH)

@lru_cache(maxsize=1)
def get_top_questions() -> pl.DataFrame:
    return pl.read_parquet(TOP_QUESTIONS_PATH)

@lru_cache(maxsize=1)
def get_clasificacion() -> pl.DataFrame:
    return pl.read_parquet(CLASIFICACION_PATH)

@lru_cache(maxsize=1)
def get_forecasts() -> pl.DataFrame:
    return pl.read_parquet(FORECASTS_PATH)

@lru_cache(maxsize=1)
def get_series_mensuales() -> pl.DataFrame:
    return pl.read_parquet(SERIES_MENSUALES_PATH)

@lru_cache(maxsize=1)
def get_tabla_cruce() -> pl.DataFrame:
    return pl.read_parquet(TABLA_CRUCE_PATH)

@lru_cache(maxsize=1)
def get_top20() -> pl.DataFrame:
    return pl.read_parquet(TOP20_PATH)