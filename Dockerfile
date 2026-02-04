# Étape 1 : Builder / installer les dépendances
FROM python:3.12-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crée le répertoire de l'application
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier tout le code
COPY auth_service/ ./auth_service/

# Crée le dossier pour collectstatic si besoin
RUN mkdir -p /app/static

# Expose le port
EXPOSE 8000

# Commande par défaut
CMD ["gunicorn", "auth_service.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
