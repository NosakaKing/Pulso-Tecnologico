# fase_4_producto/api/schemas/forecasts.py
from pydantic import BaseModel

class ForecastPoint(BaseModel):
    ds: str
    yhat: float
    yhat_lower: float
    yhat_upper: float

class ForecastSerie(BaseModel):
    tag: str
    data: list[ForecastPoint]

class ForecastResponse(BaseModel):
    tags_solicitados: list[str]
    tags_encontrados: list[str]
    tags_no_encontrados: list[str]
    series: list[ForecastSerie]