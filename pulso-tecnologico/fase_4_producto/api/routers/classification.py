# fase_4_producto/api/routers/clasificacion.py
from fastapi import APIRouter, HTTPException, Query
from services.classification_service import (
    obtener_clasificacion,
    obtener_clasificacion_tag,
    comparar_tags,
)
from schemas.classification import (
    ClasificacionResponse,
    ClasificacionItem,
    CompararResponse,
)

router = APIRouter()


@router.get("/comparar", response_model=CompararResponse)
def get_comparar(
    tags: list[str] = Query(description="Tags a comparar: ?tags=python&tags=java"),
):
    """
    Compara los indicadores de varias tecnologías lado a lado.

    Casos de uso:
    - /clasificacion/comparar?tags=python&tags=java
    - /clasificacion/comparar?tags=python&tags=javascript&tags=react
    """
    if not tags:
        raise HTTPException(status_code=400, detail="Debes enviar al menos un tag")

    return comparar_tags(tags)


@router.get("/{tag}", response_model=ClasificacionItem)
def get_clasificacion_tag(tag: str):
    """
    Detalle completo de una tecnología específica.

    Casos de uso:
    - /clasificacion/python
    - /clasificacion/javascript
    """
    resultado = obtener_clasificacion_tag(tag)

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail=f"Tag '{tag}' no encontrado en clasificación"
        )

    return resultado


@router.get("/", response_model=ClasificacionResponse)
def get_clasificacion(
    categoria: str | None = Query(
        default=None,
        description="Filtrar por: en auge, madurando, en declive"
    ),
):
    """
    Listado completo de clasificación ordenado por volumen.

    Casos de uso:
    - /clasificacion                      → todas
    - /clasificacion?categoria=en auge    → solo las que están creciendo
    - /clasificacion?categoria=en declive → candidatas a salir del currículo
    """
    return obtener_clasificacion(categoria)