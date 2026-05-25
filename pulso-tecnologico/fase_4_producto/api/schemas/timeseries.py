# fase_4_producto/api/schemas/timeseries.py
from pydantic import BaseModel

class TimeseriesPoint(BaseModel):
    year_month: str
    count: int
    ma3: float | None  

class TimeseriesSerie(BaseModel):
    tag: str
    data: list[TimeseriesPoint]

class TimeseriesResponse(BaseModel):
    tags_solicitados: list[str]
    tags_encontrados: list[str]
    tags_no_encontrados: list[str]
    series: list[TimeseriesSerie]