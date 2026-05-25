from fastapi import FastAPI
from routers import top20, questions, timeseries, cruce, classification, survey, forecasts, prediction
from fastapi.middleware.cors import CORSMiddleware  # ← faltaba este import

app = FastAPI(title="Pulso Tecnológico API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(top20.router,         prefix="/top20",         tags=["Top 20"])
app.include_router(questions.router,     prefix="/questions",     tags=["Questions"])
app.include_router(timeseries.router,    prefix="/tags",          tags=["Timeseries"])
app.include_router(cruce.router,         prefix="/cruce",         tags=["Cruce Mercado"])
app.include_router(classification.router, prefix="/classification", tags=["Clasificación"])
app.include_router(survey.router,        prefix="/survey",        tags=["Survey"])
app.include_router(forecasts.router,     prefix="/forecasts",     tags=["Forecasts"])
app.include_router(prediction.router,    prefix="/prediction",    tags=["Prediction"])


