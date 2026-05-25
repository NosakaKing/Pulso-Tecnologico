"""
src/forecast.py — Modulo reutilizable de forecasting con Prophet.

Encapsula el entrenamiento, prediccion y evaluacion (R2 historico)
de modelos Prophet sobre series temporales mensuales de Stack Overflow.

Dependencia: pip install prophet
"""
import pandas as pd
from prophet import Prophet
from sklearn.metrics import r2_score

def entrenar_modelo_prophet(df_train: pd.DataFrame) -> Prophet:
    """
    Inicializa y entrena un modelo Prophet con la configuración estratégica:
    - Estacionalidad anual activada (por los ciclos universitarios/laborales).
    - Intervalo de confianza del 90%.
    """
    modelo = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        interval_width=0.90
    )
    modelo.fit(df_train)
    return modelo

def evaluar_ajuste(modelo: Prophet, df_train: pd.DataFrame) -> float:
    """
    Calcula el R² histórico prediciendo sobre los mismos datos de entrenamiento
    para ver qué tan bien Prophet entendió el pasado.
    """
    pred_historica = modelo.predict(df_train[['ds']])
    r2 = r2_score(df_train['y'], pred_historica['yhat'])
    return r2

def proyectar_futuro(modelo: Prophet, meses: int = 36) -> pd.DataFrame:
    """
    Genera el dataframe futuro y realiza la predicción.
    """
    df_futuro = modelo.make_future_dataframe(periods=meses, freq='MS')
    forecast = modelo.predict(df_futuro)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
