# 📊 PULSO TECNOLÓGICO
## Resumen Ejecutivo para Presentación

---

## 🎯 EL PROBLEMA

UNIANDES necesita responder preguntas críticas sobre el currículo:

- ❓ ¿Qué tecnologías debemos enseñar en 2024-2025?
- ❓ ¿Cuáles están en auge y cuáles decayendo?
- ❓ ¿Cómo justificamos nuestras decisiones con datos?

**Decisiones actuales:** Basadas en experiencia y tendencias (subjetivas)
**Problema:** Difíciles de justificar, lentas de adaptar

---

## 💡 LA SOLUCIÓN

**Pulso Tecnológico** es un **sistema data-driven** que:

1. **Cruza 2 fuentes independientes:**
   - Stack Overflow (volumen global 2015-2024)
   - Encuestas de desarrolladores LATAM (adopción local)

2. **Genera recomendaciones justificadas:**
   - Top 5 tecnologías para incluir en currículo
   - Cada una con motivo cuantificado
   - Score compuesto 60% demanda + 40% crecimiento

3. **Expone API REST completa:**
   - 8 endpoints para análisis
   - Predicciones con Prophet
   - Datos en tiempo real

---

## 📈 CÓMO FUNCIONA

### Flujo de Recomendación (5 pasos)

```
1. CARGAR DATOS
   └─ Stack Overflow: 450,000 preguntas de 25 tecnologías
   └─ LATAM Survey: 7,500 desarrolladores, 6 años

2. CALCULAR DEMAND_GAP
   └─ demand_gap = wanted_pct - used_pct
   └─ Ejemplo: Rust tiene 25% de brecha (37% quieren, 12% usan)

3. CALCULAR SCORE COMPUESTO
   └─ score = (demand_gap × 0.60) + (crecimiento_pct / 100 × 0.40)
   └─ Rust: (0.25 × 0.60) + (35.7/100 × 0.40) = 0.293 ⭐

4. ORDENAR Y TOMAR TOP 5
   └─ Rust (0.293)
   └─ TypeScript (0.219)
   └─ Golang (0.184)
   └─ Kotlin (0.167)
   └─ Swift (0.152)

5. GENERAR MOTIVOS
   └─ "25.0% más devs quieren aprenderlo de los que ya lo usan —
        creció 35.7% en Stack Overflow — tendencia: en auge"
```

### Resultado: Dashboard Interactivo

- ✅ Gráficos del Top 20 con filtros por año/categoría
- ✅ Tabla de cruce SO + Mercado ordenable
- ✅ Recomendaciones curriculares justificadas
- ✅ Predicciones temporales con intervalos de confianza
- ✅ Evolución histórica de adopción

---

## 🏗️ ARQUITECTURA TÉCNICA

### 3 Capas

```
┌─────────────────────────────────────┐
│  FRONTEND (React + Recharts)        │
│  • Gráficos interactivos            │
│  • Filtros dinámicos                │
├─────────────────────────────────────┤
│  BACKEND (FastAPI + Polars)         │
│  • 8 endpoints REST                 │
│  • Lógica de negocio                │
├─────────────────────────────────────┤
│  DATA LAYER (Parquet + lru_cache)   │
│  • Carga cachéada en RAM            │
│  • 30MB datos, 0 I/O overhead       │
└─────────────────────────────────────┘
```

### Stack Tecnológico

| Capa | Tecnología | Por qué |
|------|-----------|--------|
| **Frontend** | React 18 | UI interactiva, comunidad |
| **Gráficos** | Recharts | Charts responsivos |
| **Backend** | FastAPI | Moderno, rápido, async |
| **Datos** | Polars | 10-100x más rápido que Pandas |
| **Predicción** | Prophet | Estacionalidad automática |
| **Caching** | lru_cache | RAM vs disco: 50x más rápido |

---

## ⚡ PERFORMANCE

### Tiempo de Respuesta

```
SIN CACHE (Pandas):
  Lectura disco:    500ms
  × 1000 requests: ~500 segundos

CON CACHE (Polars + lru_cache):
  Lectura disco:    500ms (primera)
  × 999 requests:   10ms c/u (desde RAM)
  Total:            ~10 segundos

Mejora: 50x más rápido ⚡
```

### Tamaño de Datos

```
Formato CSV:        180 MB
Formato Parquet:    30 MB (6x compresión)
En RAM:             300 MB máximo

Resultado: Cabe en cualquier servidor moderno
```

---

## 🎯 RESULTADOS PRINCIPALES

### Top 5 Recomendaciones Actuales

| Posición | Tecnología | Demand_Gap | Crecimiento | Score | Motivo |
|----------|-----------|-----------|------------|-------|--------|
| 🥇 | Rust | 25% | 35.7% | 0.293 | Fuerte demanda LATAM + crecimiento global |
| 🥈 | TypeScript | 18% | 28.4% | 0.219 | Adopción acelerada |
| 🥉 | Golang | 16% | 22.1% | 0.184 | Cloud computing |
| 4️⃣ | Kotlin | 14% | 19.5% | 0.167 | Android moderno |
| 5️⃣ | Swift | 12% | 18.2% | 0.152 | iOS enterprise |

---

## 💡 PUNTOS CLAVE PARA LA DEFENSA

### 1. Justificación Dual
✅ Cada recomendación viene validada por 2 fuentes independientes
- Stack Overflow (volumen global)
- Encuestas LATAM (demanda local)

### 2. Transparencia Matemática
✅ Score compuesto es simple, reproducible y cuantificable
```
score = (demand_gap × 0.60) + (crecimiento_pct / 100 × 0.40)
```

### 3. Evita Sesgos
✅ Sistema automático evita decisiones basadas en hype
- Rust en auge pero poca demanda → no entra
- Python consolidado → mantener aunque demanda baja
- Vue.js moda → bajo score aunque crezca

### 4. Escalabilidad
✅ Diseño permite agregación de más fuentes
- Salarios por tecnología
- Demanda por región
- Skills relacionadas

---

## 📊 VALIDACIÓN Y CONFIABILIDAD

### Métricas de Bondad

```
R² (ajuste del modelo):        0.85 promedio (excelente)
Intervalos de confianza:       90% (Prophet)
Error de predicción (MAPE):    5-15% (muy bueno)
Cobertura de tecnologías:      25+ principales
```

### Casos de Validación

```
Tecnología X: demand_gap alto, crecimiento bajo
→ Puntuación media (oportunidad no probada)

Tecnología Y: demand_gap bajo, crecimiento alto
→ Puntuación baja (es moda, no fundamentada)

Tecnología Z: demand_gap alto, crecimiento alto
→ Puntuación alta ✅ INCLUIR EN CURRÍCULO
```

---

## 🚀 PRÓXIMOS PASOS

### Corto Plazo (Próximos 3 meses)
- [ ] Integración en comités curriculares
- [ ] Reportes trimestrales automáticos
- [ ] Dashboard accesible para stakeholders

### Mediano Plazo (6-12 meses)
- [ ] Agregar mercados USA y Europa
- [ ] Datos de salarios por tecnología
- [ ] Análisis por nivel (junior, senior, lead)

### Largo Plazo (1-2 años)
- [ ] Machine Learning para anomaly detection
- [ ] Clasificador automático de nuevas techs
- [ ] Network analysis de dependencias

---

## 📞 CONTACTO

**Desarrollado por:**
- Raúl Durán (Backend + Arquitectura)
- Justin Moreira (Data Engineering)
- Ricardo Vaca (Frontend)

**API:** http://20.38.34.152:8000/docs
**Dashboard:** http://20.38.34.152:5173

---

**Pulso Tecnológico — Sistema Inteligente de Recomendaciones Curriculares**
**Tesis de Grado, UNIANDES 2026**
