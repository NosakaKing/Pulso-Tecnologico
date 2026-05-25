# fase_4_producto/api/config.py

from pathlib import Path

# Raíz del proyecto — sube 3 niveles desde api/
BASE_DIR = Path(__file__).resolve().parent  # = /app

# Carpeta base de datos procesados
DATOS = BASE_DIR / "data" / "datos_procesados"

# Archivos en datos_procesados/
SURVEY_PATH            = DATOS / "eda" / "survey_unificado.parquet"
TOP_QUESTIONS_PATH     = DATOS / "eda" / "top_questions.parquet"

# Archivos en datos_procesados/eda/
CLASIFICACION_PATH     = DATOS / "eda" / "clasificacion.parquet"
FORECASTS_PATH         = DATOS / "eda" / "forecasts.parquet"
SERIES_MENSUALES_PATH  = DATOS / "eda" / "series_mensuales.parquet"
TABLA_CRUCE_PATH       = DATOS / "eda" / "tabla_cruce_final.parquet"
TOP20_PATH             = DATOS / "eda" / "top20.parquet"