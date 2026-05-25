from data.loader import (
    get_survey,
    get_top_questions,
    get_clasificacion,
    get_forecasts,
    get_series_mensuales,
    get_tabla_cruce,
    get_top20,
)

loaders = {
    "survey":          get_survey,
    "top_questions":   get_top_questions,
    "clasificacion":   get_clasificacion,
    "forecasts":       get_forecasts,
    "series_mensuales":get_series_mensuales,
    "tabla_cruce":     get_tabla_cruce,
    "top20":           get_top20,
}

print("\n📦 Probando rutas del loader...\n")
for nombre, fn in loaders.items():
    try:
        df = fn()
        print(f"  ✅ {nombre:20s} → {df.shape[0]} filas, {df.shape[1]} columnas")
    except Exception as e:
        print(f"  ❌ {nombre:20s} → ERROR: {e}")

print("\nListo.\n")