# fase_4_producto/api/schemas/cruce.py
from pydantic import BaseModel

class CruceItem(BaseModel):
    tag: str
    categoria_tendencia: str
    used_pct: float
    wanted_pct: float
    demand_gap: float
    crecimiento_pct: float
    pendiente: float
    r2: float
    view_count_promedio: float
    n_respondents: int

class CruceResponse(BaseModel):
    total: int
    orden: str | None
    categoria: str | None
    data: list[CruceItem]

class RecomendacionItem(BaseModel):
    tag: str
    categoria_tendencia: str
    demand_gap: float
    crecimiento_pct: float
    used_pct: float
    wanted_pct: float
    motivo: str          # ← texto explicativo generado automáticamente

class RecomendacionesResponse(BaseModel):
    total: int
    data: list[RecomendacionItem]