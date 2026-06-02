# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Umgebungsvariablen setzen (verhindert .pyc Dateien und puffert Logs nicht)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System-Abhängigkeiten installieren (wichtig für Pillow/Bildverarbeitung und C-Pakete)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Python-Abhängigkeiten installieren
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Gunicorn für den produktiven Betrieb installieren
RUN pip install gunicorn

# Projektdateien kopieren
COPY . /app/

# Beim Starten des Containers:
# 1. Statische Dateien sammeln (collectstatic)
# 2. Datenbank-Migrationen ausführen (migrate)
# 3. Server mit Gunicorn starten (Port 8000)
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8000"]