# 📊 Pulso Tecnológico — Stack Overflow Dashboard

> Proyecto analítico bajo el framework **Intelligence-to-Action (I2A)**: un sistema que convierte señales de datos en decisiones institucionales y recomendaciones curriculares para UNIANDES.

---

## 👥 Equipo de desarrollo

| Nombre | Rol |
|--------|-----|
| **Justin Moreira** | Data Engineer — Carga, filtrado y pipeline de datos |
| **Raul Durán** | Backend Developer — API FastAPI |
| **Ricardo Vaca** | Frontend Developer — Dashboard Streamlit |

---

## 🎯 Objetivo del proyecto

Ir más allá de la analítica descriptiva para entregar un producto que cruce la realidad del **mercado laboral de Ecuador y LATAM** con el volumen de tendencias globales de Stack Overflow (2015-2024). El fin último es derivar recomendaciones curriculares accionables (tecnologías que entran, salen o se actualizan) justificadas por partida doble.

---

## 🏗️ Fases del framework I2A

| Fase | Descripción |
|------|-------------|
| **Fase 1** | Comprensión del dominio y formulación de hipótesis |
| **Fase 2** | Preparación y estrategia de datos (Polars ETL) |
| **Fase 3** | Análisis de tendencias (Descriptivo + Prescriptivo) |
| **Fase 4** | Arquitectura del producto (FastAPI + Streamlit) |
| **Fase 5** | Informe de interpretación y comunicación |

---

## 🗂️ Estructura del proyecto

```text
pulso-tecnologico/
│
├── data/
│   └── datos_procesados/            # Archivos .parquet procesados
│       ├── survey_unificado.parquet
│       ├── top_questions.parquet
│       └── eda/
│           ├── clasificacion.parquet
│           ├── forecasts.parquet
│           ├── series_mensuales.parquet
│           ├── tabla_cruce_final.parquet
│           └── top20.parquet
│
├── fase_1_dominio/
├── fase_2_datos/
├── fase_3_analisis/
├── fase_4_producto/
│   └── api/
│       ├── main.py                  # Punto de entrada FastAPI
│       ├── config.py                # Rutas y configuración global
│       ├── data/
│       │   └── loader.py            # Carga de parquets con lru_cache
│       ├── routers/
│       │   ├── top20.py
│       │   ├── questions.py
│       │   ├── timeseries.py
│       │   ├── cruce.py
│       │   ├── clasificacion.py
│       │   ├── survey.py
│       │   ├── forecasts.py
│       │   └── prediccion.py
│       ├── services/
│       │   ├── top20_service.py
│       │   ├── questions_service.py
│       │   ├── timeseries_service.py
│       │   ├── cruce_service.py
│       │   ├── clasificacion_service.py
│       │   ├── survey_service.py
│       │   ├── forecasts_service.py
│       │   └── prediccion_service.py
│       └── schemas/
│           ├── top20.py
│           ├── questions.py
│           ├── timeseries.py
│           ├── cruce.py
│           ├── clasificacion.py
│           ├── survey.py
│           ├── forecasts.py
│           └── prediccion.py
├── fase_5_informe/
├── notebooks/
└── environment.yml
```

---

## 🚀 Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/<tu-usuario>/pulso-tecnologico.git
cd pulso-tecnologico
```

### 2. Crear y activar el entorno

```bash
conda env create -f environment.yml
conda activate pulso-tecnologico
```

### 3. Instalar dependencias de la API

```bash
pip install fastapi uvicorn polars prophet pydantic-settings
```

### 4. Configurar los datos

Coloca los archivos `.parquet` procesados en la siguiente estructura:

```
data/datos_procesados/
├── dim_tags.parquet
├── survey_unificado.parquet
├── top_questions.parquet
└── eda/
    ├── clasificacion.parquet
    ├── forecasts.parquet
    ├── series_mensuales.parquet
    ├── tabla_cruce_final.parquet
    └── top20.parquet
```

### 5. Levantar la API

```bash
cd fase_4_producto/api
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`

Documentación interactiva en `http://localhost:8000/docs`

---

## 📡 Endpoints de la API

### Top 20 Tecnologías
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/top20?start_year=2023&end_year=2023&categoria=backend` | Top 20 por categoría y año |

### Preguntas
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/questions/{tag}/top` | Top preguntas por score de un tag |

### Series Temporales
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/tags/timeseries?tags=python&tags=javascript` | Comparativa mensual de múltiples tecnologías |

### Clasificación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/clasificacion` | Listado completo ordenado por volumen |
| GET | `/clasificacion?categoria=en auge` | Filtrado por categoría de tendencia |
| GET | `/clasificacion/{tag}` | Detalle completo de una tecnología |
| GET | `/clasificacion/comparar?tags=python&tags=java` | Comparativa lado a lado |

### Cruce de Mercado
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/cruce` | Cruce completo SO + mercado LATAM |
| GET | `/cruce?orden=crecimiento` | Ordenado por: demand_gap, crecimiento, used, wanted, views |
| GET | `/cruce?categoria=en auge` | Filtrado por tendencia |
| GET | `/cruce/recomendaciones` | **Recomendaciones curriculares** (top 5 por score compuesto) |

### Encuesta de Desarrolladores
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/survey/{tag}/evolucion` | Evolución histórica used_pct vs wanted_pct de un tag |
| GET | `/survey/evolucion` | Evolución de todos los tags |
| GET | `/survey/evolucion?start_year=2020&end_year=2024` | Filtrado por rango de años |

### Forecasts Pre-calculados
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/forecasts` | Todos los forecasts pre-calculados (2024-2027) |
| GET | `/forecasts?tags=python&tags=reactjs` | Filtrado por tags |

### Predicción en Vivo (Prophet)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/prediccion` | Entrena Prophet en tiempo real y devuelve la proyección |

**Cuerpo de la solicitud:**
```json
{
  "tag": "python",
  "periods": 12
}
```

**Tags disponibles para predicción:** `angular`, `java`, `javascript`, `mongodb`, `mysql`, `postgresql`, `python`, `reactjs`, `vue.js`

**periods:** entre 1 y 36 meses

---

## 🛠️ Stack tecnológico

| Capa | Tecnología |
|------|------------|
| ETL | Polars (lazy evaluation) |
| API | FastAPI + Uvicorn |
| Predicción | Prophet (Meta) |
| Validación de datos | Pydantic v2 |
| Dashboard | React + Plotly |
| Entorno | Anaconda |

---

## ⚙️ Decisiones de arquitectura

**Polars sobre Pandas** — implementado con `lru_cache` en todos los loaders para que los archivos `.parquet` se lean del disco una sola vez y queden en RAM para las solicitudes posteriores.

**Estrategia pre-filtrado** — los filtros de año se aplican antes de los joins para minimizar el tamaño de los dataframes a lo largo del pipeline.

**Justificación dual** — todas las recomendaciones curriculares (`/cruce/recomendaciones`) están respaldadas tanto por el volumen de Stack Overflow como por una fuente independiente del mercado laboral LATAM.

**El orden de los routers importa** — en cada router de FastAPI, las rutas fijas (ej. `/comparar`, `/evolucion`) se registran antes que las rutas dinámicas (ej. `/{tag}`) para evitar conflictos de paths.

---

## 📦 Despliegue (Docker + Azure VM)

Próximamente en [`fase_4_producto/README_deploy.md`](fase_4_producto/README_deploy.md)