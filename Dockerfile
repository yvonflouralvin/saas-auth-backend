FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ⬇️ Copier le contenu du projet, pas le dossier parent
COPY auth_service/ .

RUN mkdir -p /app/static

EXPOSE 8000
# Commande par défaut
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "auth_service.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
