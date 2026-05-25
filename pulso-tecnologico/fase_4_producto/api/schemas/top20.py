# fase_4_producto/api/schemas/top20.py
from pydantic import BaseModel

class Top20Item(BaseModel):
    tag: str
    count: int
    categoria: str

class Top20Response(BaseModel):
    total: int
    start_year: int | None
    end_year: int | None
    categoria: str | None
    data: list[Top20Item]