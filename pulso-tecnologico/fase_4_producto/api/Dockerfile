# ── Imagen base ──────────────────────────────────────────────
FROM python:3.11-slim

# ── Variables de entorno ──────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# ── Directorio de trabajo ─────────────────────────────────────
WORKDIR /app

# ── Dependencias del sistema (prophet necesita estas) ─────────
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ── Instalar dependencias Python ──────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copiar código fuente ──────────────────────────────────────
COPY . .

# ── Puerto expuesto ───────────────────────────────────────────
EXPOSE 8000

# ── Comando de arranque ───────────────────────────────────────
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]