# Fase 1: Comprensión del dominio y formulación de hipótesis

**Proyecto:** Pulso Tecnológico  
**Framework:** Intelligence-to-Action (I2A)  

---

## 1. Resumen del caso

El ecosistema de desarrollo de software evoluciona a un ritmo acelerado, lo que genera un desafío crítico para las instituciones académicas: la rápida obsolescencia de sus mallas curriculares frente a las demandas de la industria. El proyecto "Pulso Tecnológico" aborda este problema transformando un volumen masivo de datos crudos extraídos de Stack Overflow (una muestra de más de 16 millones de preguntas) en inteligencia de mercado. Al procesar de manera escalable las interacciones de los desarrolladores a nivel global, el proyecto identifica las trayectorias reales de adopción, estancamiento o declive de lenguajes, herramientas y frameworks.

Este producto analítico funciona como un termómetro en tiempo real de la demanda tecnológica. Su objetivo fundamental es proporcionar evidencia empírica innegable para fundamentar decisiones de actualización académica, garantizando que los nuevos profesionales de ingeniería de software en UNIANDES y adquieran competencias alineadas estrictamente con las exigencias del mercado laboral contemporáneo.

---

## 2. Contexto del dominio y mercado

### 2.1. Dinámica del negocio
* **Función del negocio:** Diseño estratégico y actualización curricular para programas de educación superior en Ingeniería de Software.
* **Tomador de decisiones:** Director de Carrera y el Comité Curricular Universitario (autoridades responsables de validar y aprobar las modificaciones a los sílabos formativos).
* **Incentivos:** Aumentar agresivamente la tasa de empleabilidad de los egresados, mitigar la brecha de habilidades digitales y elevar el prestigio de la institución para atraer más postulantes.

### 2.2. Stack Overflow como indicador líder
En el contexto de la inteligencia tecnológica, Stack Overflow no es un simple repositorio pasivo; es un **"indicador líder" (leading indicator) y un sensor cuantitativo en tiempo real**. La actividad en la plataforma refleja la fricción cognitiva que enfrentan los equipos de ingeniería a nivel global. Existe una relación causal comprobable entre la latencia de resolución de consultas en la plataforma y la probabilidad de adopción tecnológica a nivel corporativo: las tecnologías con ecosistemas de soporte robustos experimentan curvas de adopción más aceleradas.

### 2.3. Contexto corporativo, académico y regional
Para que la extracción de conocimiento sea procesable, las métricas globales deben anclarse a realidades empíricas y regionales:

* **Obsolescencia del talento:** El Foro Económico Mundial (*Future of Jobs Report 2025*) proyecta que el 39% de las habilidades tecnológicas actuales se volverán obsoletas para el 2030, destacando a los especialistas en Big Data e Inteligencia Artificial como los roles de mayor crecimiento.
* **La brecha de contratación:** Investigaciones de Gartner (2023) advierten que el 86% de los líderes tecnológicos (CIOs) lidian directamente con una escasez crítica de talento que posea habilidades en frameworks modernos.
* **Validez de la fuente:** Un análisis publicado por el IEEE (*Unveiling Research Trends in Stack Overflow*, 2024) valida científicamente a la plataforma como un indicador dinámico que refleja la adopción real de paradigmas de la industria.
* **Ecuador y Latinoamérica:** La región se ha consolidado como un hub estratégico de *Nearshoring*. Localmente, el avance está propulsado por el comercio electrónico (proyectado en **$6,500 millones USD para 2025**) y una adopción de Inteligencia Artificial en el sector corporativo que ya alcanza el **40%**.
* **Hegemonía técnica:** Python domina el sector de datos e IA (presente en >30% de ofertas laborales), mientras que React lidera el frontend abarcando más del 60% de las vacantes regionales.

---

## 3. Preguntas de negocio

* **Pregunta Principal:** ¿Qué tecnologías, lenguajes o frameworks deben integrarse obligatoriamente o eliminarse de la malla curricular de Ingeniería de Software para maximizar la empleabilidad de los egresados en los próximos tres años?
* **Pregunta Secundaria 1:** ¿Cuáles son las tecnologías del ecosistema de datos e infraestructura (ej. Machine Learning, Cloud) que presentan una aceleración de adopción tan alta que justifique la creación de nuevas asignaturas de especialización?
* **Pregunta Secundaria 2:** ¿Existen lenguajes de programación backend de enseñanza tradicional en fase de declive sostenido cuyo tiempo en el sílabo deba reducirse?

---

## 4. Métrica de éxito

* **KPI Principal:** Tasa de Alineación Curricular (TAC).
* **Dirección y Cambio:** **Incremento**. Se busca aumentar significativamente el porcentaje de coincidencia entre las tecnologías enseñadas en las materias troncales y el "Top 20 de tecnologías de mayor crecimiento" identificado empíricamente por el dashboard.

---

## 5. Diccionario de variables

Estructura de los datos en la capa relacional antes de derivar métricas complejas:

| Nombre de la Variable | Tipo de Dato | Descripción | Rango / Valores | % Nulos | Observaciones |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Id` | `int` | Identificador numérico único de la pregunta en la plataforma. | 1 al ~80,000,000+ | 0% | Llave primaria (PK) para la dimensión de preguntas. |
| `Title` | `str` | Título literal de la duda técnica del desarrollador. | Texto libre | 0% | Base para previsualización o futuro análisis NLP. |
| `CreationDate` | `datetime` | Marca temporal exacta de publicación de la consulta. | 2015-01-01 a hoy | 0% | Fundamental para agrupar series de tiempo. |
| `Score` | `int` | Puntuación neta comunitaria (votos a favor - en contra). | -100 a 10,000+ | 0% | Permite extraer las dudas mejor valoradas. |
| `Tags` | `str` | Etiquetas crudas asociadas, en un solo string. | N/A | 0% | Destruida en el ETL tras aplicar `.explode()` (1NF). |
| `ClosedDate` | `datetime` | Marca temporal en la que se inhabilitaron nuevas respuestas. | $\ge$ `CreationDate` | ~80-90% | Se descarta tras procesar la variable derivada. |
| `es_cerrada` | `bool` | Variable derivada en Polars; indica el estatus de la consulta. | `True` o `False` | 0% | Reemplaza a `ClosedDate` para permitir agrupaciones. |

---

## 6. Hipótesis iniciales (Falsificables)

Estas premisas están diseñadas como constructos falsificables para ser validadas o refutadas en la Fase 3 utilizando los datos purificados:

1. **Evolución Backend/Datos:** El volumen de preguntas mensuales relacionadas con **Python** experimentó un punto de cruce, superando a Java de manera definitiva a partir del año 2018 debido a la demanda en ciencia de datos.
2. **Evolución Frontend:** La interacción comunitaria sobre **React** superó en volumen absoluto a la de Angular entre los años 2019 y 2020.
3. **Tecnologías de Datos e IA:** El crecimiento de las consultas sobre herramientas de **Machine Learning** ha mantenido una trayectoria ascendente y sostenida (sin años de contracción) desde el año 2016.
4. **Infraestructura e Implementación:** Las consultas asociadas a la orquestación de contenedores (específicamente **Docker**) muestran un crecimiento interanual consistente superior al 25% a partir de 2019.
5. **Bases de Datos Modernas:** El ecosistema de **PostgreSQL** presenta una tasa de crecimiento transaccional significativamente mayor que ecosistemas tradicionales como MySQL en el período 2021-2024.