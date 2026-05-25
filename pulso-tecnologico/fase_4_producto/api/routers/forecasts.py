# fase_4_producto/api/routers/forecasts.py
from fastapi import APIRouter, Query
from services.forecasts_service import obtener_forecasts
from schemas.forecasts import ForecastResponse

router = APIRouter()

@router.get("/", response_model=ForecastResponse)
def get_forecasts(
    tags: list[str] | None = Query(
        default=None,
        description="Tags a consultar: ?tags=python&tags=reactjs. Sin filtro devuelve todos."
    ),
):
    """
    Proyección mensual de preguntas en Stack Overflow (2024-2027).

    Casos de uso:
    - /forecasts                          → todos los tags
    - /forecasts?tags=python              → solo python
    - /forecasts?tags=python&tags=reactjs → comparativa
    """
    return obtener_forecasts(tags)