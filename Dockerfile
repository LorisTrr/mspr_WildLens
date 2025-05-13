# Utilise une image Python légère
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers dans le conteneur
COPY . .

# Installer Flask (à adapter si plus de dépendances)
RUN pip install flask

# Exposer le port utilisé par l'application Flask
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python", "main.py"]
