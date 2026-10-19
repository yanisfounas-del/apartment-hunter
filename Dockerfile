FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application et le modèle entraîné
COPY app/ ./app/
COPY models/ ./models/

# Hugging Face Spaces utilise le port 7860
EXPOSE 7860

# Lancer Flask avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "--threads", "2", "app.app:app"]