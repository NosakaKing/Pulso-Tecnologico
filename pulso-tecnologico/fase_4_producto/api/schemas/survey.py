# fase_4_producto/api/schemas/survey.py
from pydantic import BaseModel

class SurveyPoint(BaseModel):
    year: int
    used_pct: float
    wanted_pct: float
    n_respondents: int

class SurveyEvolucionResponse(BaseModel):
    tag: str
    total_años: int
    data: list[SurveyPoint]