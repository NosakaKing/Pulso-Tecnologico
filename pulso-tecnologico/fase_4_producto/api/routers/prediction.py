from fastapi import APIRouter, HTTPException
from services.prediction_service import predict_tag
from schemas.predicction import PredictionRequest, PredictionResponse

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
def post_prediction(body: PredictionRequest):
    """
    Entrena Prophet con el histórico de un tag y devuelve la proyección.

    Casos de uso:
    - { "tag": "python", "periods": 12 }  → próximos 12 meses
    - { "tag": "reactjs", "periods": 24 } → próximos 24 meses
    - { "tag": "java", "periods": 36 }    → próximos 36 meses

    Tags disponibles: angular, java, javascript, mongodb,
                      mysql, postgresql, python, reactjs, vue.js
    """
    result = predict_tag(body.tag, body.periods)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Tag '{body.tag}' not found in historical data"
        )

    return result