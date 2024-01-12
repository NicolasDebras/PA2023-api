# Utilisez une image Python officielle comme image parente
FROM python:3.9-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Installez les dépendances nécessaires pour mysqlclient
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev build-essential pkg-config

# Copie les fichiers de dépendances et installe les packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code source de l'application dans le conteneur
COPY . .

# Expose le port sur lequel l'application s'exécute
EXPOSE 8000

# Définit la commande pour démarrer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
