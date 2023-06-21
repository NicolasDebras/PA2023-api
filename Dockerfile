# Utilisez une image Python légère comme base
FROM python:3.8-slim-buster

# Créez un répertoire pour le script
WORKDIR /app

# Copiez le script Python dans l'image Docker
COPY . /app
