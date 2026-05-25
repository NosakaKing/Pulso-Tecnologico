# fase_4_producto/api/routers/timeseries.py
from fastapi import APIRouter, HTTPException, Query
from services.timeseries_service import obtener_timeseries
from schemas.timeseries import TimeseriesResponse

router = APIRouter()

@router.get("/timeseries", response_model=TimeseriesResponse)
def get_timeseries(
    tags: list[str] = Query(description="Tags a comparar, ej: ?tags=python&tags=javascript"),
):
    """
    Devuelve la serie temporal mensual de una o varias tecnologías.

    Casos de uso:
    - /tags/timeseries?tags=python
    - /tags/timeseries?tags=python&tags=javascript
    - /tags/timeseries?tags=python&tags=javascript&tags=java
    """
    if not tags:
        raise HTTPException(status_code=400, detail="Debes enviar al menos un tag")

    return obtener_timeseries(tags)