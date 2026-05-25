# fase_4_producto/api/routers/top20.py
from fastapi import APIRouter, Query
from services.top20_service import obtener_top20
from schemas.top20 import Top20Response

router = APIRouter()

@router.get("/", response_model=Top20Response)
def get_top20(
    start_year: int | None = Query(default=None, description="Año inicial del rango, ej: 2020"),
    end_year:   int | None = Query(default=None, description="Año final del rango, ej: 2023"),
    categoria:  str | None = Query(default=None, description="Filtrar por categoría, ej: backend"),
):
    """
    Devuelve el Top 20 de tecnologías acumulado.

    Casos de uso:
    - /top20?start_year=2020&end_year=2023       → rango de años acumulado
    - /top20?year=2023&categoria=backend         → top de una categoría en un año
    - /top20?start_year=2020&end_year=2023&categoria=backend → combinado
    """
    return obtener_top20(start_year, end_year, categoria)