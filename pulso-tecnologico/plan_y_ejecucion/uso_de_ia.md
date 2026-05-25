# Bitacora de IA Nro. 01
**Fecha:** 2026-04-28  
**Herramientas IA utilizadas:** Gemini 3 Pro (Google)  
**Integrante:** Justin Moreira  
**Tarea:** Construir y ejecutar un pipeline ETL altamente optimizado utilizando la librería **Polars**.

## Prompt resumido – Fase 2, Cuaderno 03

- **Rol:** Ingeniero de Datos de Alto Rendimiento, experto en `polars` y Lazy Evaluation.
- **Tarea:** Construir y ejecutar el pipeline ETL masivo sobre `Questions.csv` (~3.6M filas).
- **Objetivo:** Resolver ruptura de 1NF con procesamiento columnar y multihilo, evitando OOM.
- **Directrices:**
  1. **Ingesta perezosa:** `pl.scan_csv()` (no usar `read_csv`).
  2. **Filtrado anticipado:** Retener solo preguntas desde 2015 (`CreationDate`).
  3. **Explode y normalización:** `Tags.str.split("|").explode().str.lower().str.strip()`.
  4. **Materialización controlada:** `.collect()` + documentación de volúmenes (shape en 3 etapas).
  5. **Benchmark:** Medir tiempo y memoria, justificar Polars sobre Pandas.
- **Documentación:** Explicar la lógica del filtrado transaccional analítico temporal obligatorio.
- **Formato:** Código limpio, encadenado idiomáticamente en Polars, altamente comentado.  
  *No se guardan archivos físicos en este cuaderno (los Parquet se exportan en el Cuaderno 04).*

## Observaciones

### Problema
Hubo un conflicto con la libreria polars ya que el agente usó metodos que se usaban en una version anterior de polars a la que se tiene instalada.  
`AttributeError: 'ExprStringNameSpace' object has no attribute 'lower'`

### Solución
En las versiones recientes, la API de cadenas (strings) fue actualizada, por lo que `.str.lower()` se reemplazó por `.str.to_lowercase()`, y `.str.strip()` se cambió a `.str.strip_chars()`.

**Revisado, corregido y ejecutado por Justin Moreira.**  

---

# Bitacora de IA Nro. 02
**Fecha:** 2026-05-04  
**Herramientas IA utilizadas:** Gemini 3 Pro (Google)  
**Integrante:** Justin Moreira  
**Tarea:** Tomar el pipeline ETL masivo validado en la sección anterior y aplicar los principios estrictos de **Modelado Dimensional (Tercera Forma Normal - 3NF)**.  
# Prompt resumido – Fase 2, Cuaderno 04

- **Rol:** Ingeniero de Datos experto en 3NF y `polars`.
- **Tarea:** Normalizar el DataFrame masivo en un modelo relacional y documentarlo.
- **Entidades:**
  - `dim_questions`: preguntas únicas (Id, CreationDate, Title, Score).
  - `dim_tags`: catálogo único de tecnologías.
  - `fact_question_tags`: tabla puente que resuelve la relación M:N.
- **Exportación:** Guardar en formato Parquet (`data/datos_procesados/`).
- **Documentación:** ERD en Mermaid + explicación de eficiencia para FastAPI.
- **Formato:** Código modular, comentado, tono ejecutivo y referencial.

## Observaciones
Ninguna, se aceptaron todas las entradas del agente. El codigo y la generacion de archivos se hizo sin ningun tipo de error.  
  
**Revisado y ejecutado por Justin Moreira.**  