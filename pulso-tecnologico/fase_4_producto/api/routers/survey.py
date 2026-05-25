# fase_4_producto/api/routers/survey.py
from fastapi import APIRouter, HTTPException, Query
from services.survey_service import obtener_evolucion, obtener_evolucion_todos
from schemas.survey import SurveyEvolucionResponse

router = APIRouter()

@router.get("/evolucion", response_model=None)
def get_evolucion_todos(
    start_year: int | None = Query(default=None, description="Año inicial, ej: 2020"),
    end_year:   int | None = Query(default=None, description="Año final, ej: 2024"),
):
    """
    Evolución de TODOS los tags con rango de años opcional.

    Casos de uso:
    - /survey/evolucion                             → todos los años
    - /survey/evolucion?start_year=2020             → desde 2020
    - /survey/evolucion?start_year=2020&end_year=2023 → rango específico
    """
    return obtener_evolucion_todos(start_year, end_year)

@router.get("/{tag}/evolucion", response_model=SurveyEvolucionResponse)
def get_evolucion(tag: str):
    """
    Evolución histórica de used_pct y wanted_pct de una tecnología.

    Casos de uso:
    - /survey/python/evolucion
    - /survey/rust/evolucion
    - /survey/typescript/evolucion
    """
    resultado = obtener_evolucion(tag)

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail=f"Tag '{tag}' no encontrado en survey"
        )

    return resultado