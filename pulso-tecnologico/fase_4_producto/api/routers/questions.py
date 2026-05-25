# fase_4_producto/api/routers/questions.py
from fastapi import APIRouter, HTTPException, Query
from services.questions_service import obtener_top_questions
from schemas.questions import QuestionsResponse

router = APIRouter()

@router.get("/{tag}/top", response_model=QuestionsResponse)
def get_top_questions(
    tag: str,
):
    """
    Devuelve las preguntas con mayor puntuación de una tecnología.
    
    Casos de uso:
    - /questions/python/top          → top 10 de python
    """
    resultado = obtener_top_questions(tag)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron preguntas para el tag '{tag}'"
        )

    return resultado