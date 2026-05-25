from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    tag: str
    periods: int = Field(default=12, ge=1, le=36, description="Months to predict, max 36")

class PredictionPoint(BaseModel):
    ds: str
    yhat: float
    yhat_lower: float
    yhat_upper: float

class PredictionResponse(BaseModel):
    tag: str
    periods: int
    last_historical_date: str
    data: list[PredictionPoint]