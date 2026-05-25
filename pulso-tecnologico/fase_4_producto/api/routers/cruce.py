# fase_4_producto/api/routers/cruce.py
from fastapi import APIRouter, Query
from services.cruce_service import obtener_cruce, obtener_recomendaciones
from schemas.cruce import CruceResponse, RecomendacionesResponse

router = APIRouter()

@router.get("/recomendaciones", response_model=RecomendacionesResponse)
def get_recomendaciones():
    """
    Tecnologías recomendadas para incluir en el currículo.
    Criterio: Demand_Gap > 0 y Crecimiento_Pct > 0.
    Ordenadas por mayor brecha de demanda.
    """
    return obtener_recomendaciones()


@router.get("/", response_model=CruceResponse)
def get_cruce(
    orden: str | None = Query(
        default=None,
        description="Ordenar por: demand_gap, crecimiento, used, wanted, views"
    ),
    categoria: str | None = Query(
        default=None,
        description="Filtrar por tendencia: en auge, madurando, en declive"
    ),
):
    """
    Tabla completa del cruce SO + mercado laboral.

    Casos de uso:
    - /cruce                          → todo ordenado por demand_gap
    - /cruce?orden=crecimiento        → ordenado por crecimiento en SO
    - /cruce?categoria=en auge        → solo tecnologías en auge
    """
    return obtener_cruce(orden, categoria)