# fase_4_producto/api/schemas/clasificacion.py
from pydantic import BaseModel

class ClasificacionItem(BaseModel):
    tag: str
    volumen_total: int
    share_2022: float
    share_2023: float
    crecimiento_pct: float
    pendiente: float
    r2: float
    view_count_promedio: float
    categoria_tendencia: str

class ClasificacionResponse(BaseModel):
    total: int
    categoria: str | None
    data: list[ClasificacionItem]

class CompararResponse(BaseModel):
    tags_solicitados: list[str]
    tags_encontrados: list[str]
    tags_no_encontrados: list[str]
    data: list[ClasificacionItem]