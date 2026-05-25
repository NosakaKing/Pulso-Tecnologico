# despliegue.md

# 📊 Pulso Tecnológico — Dockerización y Despliegue Fullstack en Azure VM

## 📌 Introducción

Pulso Tecnológico es una aplicación fullstack desarrollada para el análisis y visualización de tendencias tecnológicas utilizando datos de Stack Overflow.

El objetivo del despliegue fue contenerizar tanto el frontend como el backend utilizando Docker, permitiendo ejecutar toda la aplicación dentro de una máquina virtual Ubuntu en Microsoft Azure mediante Docker Compose.

La arquitectura final permite:

- Separar frontend y backend en contenedores independientes.
- Ejecutar ambos servicios simultáneamente.
- Facilitar despliegues futuros.
- Mantener portabilidad entre entornos.
- Automatizar la ejecución completa del sistema.

---

# 🏗️ Arquitectura General del Sistema

El sistema se compone de:

| Componente | Tecnología |
|---|---|
| Frontend | React + Vite |
| Backend | FastAPI |
| Procesamiento de datos | Polars |
| Contenedores | Docker |
| Orquestación | Docker Compose |
| Servidor frontend | Nginx |
| Hosting | Azure Virtual Machine |
| Sistema operativo | Ubuntu Linux |

---

# 📁 Estructura Final del Proyecto

La estructura final del proyecto quedó organizada de la siguiente manera:

```text
Seminario 2026/
│
├── docker-compose.yml
├── .gitignore
├── README.md
│
├── pulso-tecnologico/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   ├── routers/
│   ├── services/
│   ├── data/
│   │   └── datos_procesados/
│   └── ...
│
└── pulso_tecnologico_frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.ts
    ├── src/
    ├── public/
    ├── .env
    └── ...