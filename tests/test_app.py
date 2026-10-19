import sys
from pathlib import Path

# Permettre l'importation de app/app.py
RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "app"))

from app import app


def test_accueil():
    client = app.test_client()

    reponse = client.get("/")

    assert reponse.status_code == 200


def test_prediction():
    client = app.test_client()

    maison = {
        "sqft_living": "1680",
        "sqft_lot": "8080",
        "bedrooms": "3",
        "bathrooms": "2",
        "floors": "1",
        "grade": "8",
        "condition": "3",
        "view": "0",
        "yr_built": "1986",
        "sale_year": "2014",
        "waterfront": "0",
        "renovated": "0",
        "has_basement": "0",
        "lat": "47.6168",
        "long": "-122.045"
    }

    reponse = client.post("/", data=maison)

    assert reponse.status_code == 200
    assert b"503,390.37" in reponse.data