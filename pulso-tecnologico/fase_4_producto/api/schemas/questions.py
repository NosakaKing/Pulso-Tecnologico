# fase_4_producto/api/schemas/questions.py
from pydantic import BaseModel

class QuestionItem(BaseModel):
    id: int
    score: int
    view_count: int
    answer_count: int
    url: str

class QuestionsResponse(BaseModel):
    tag: str
    total: int
    data: list[QuestionItem]