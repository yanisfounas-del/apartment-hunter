from pathlib import Path
import json
import math

import joblib
import pandas as pd
from flask import Flask, render_template, request

# 1. Charger le modèle et ses métadonnées
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

modele = joblib.load(MODEL_DIR / "apartment_hunter_model.joblib")

with open(MODEL_DIR / "model_metadata.json", encoding="utf-8") as f:
    metadata = json.load(f)

features = metadata["features"]

app = Flask(__name__)


# 2. Préparer les caractéristiques du logement
def preparer_logement(formulaire):

    champs = [
        "sqft_living", "bedrooms", "bathrooms",
        "grade", "condition", "sqft_lot",
        "floors", "waterfront", "view",
        "renovated", "has_basement", "lat", "long"
    ]

    valeurs = {}

    for champ in champs:
        valeur = float(formulaire[champ])

        if not math.isfinite(valeur):
            raise ValueError(f"Valeur invalide : {champ}")

        valeurs[champ] = valeur

    # Vérifications simples
    if valeurs["sqft_living"] <= 0:
        raise ValueError("La surface habitable doit être positive.")

    if valeurs["sqft_lot"] <= 0:
        raise ValueError("La surface du terrain doit être positive.")

    if not 0 <= valeurs["bedrooms"] < 20:
        raise ValueError("Nombre de chambres incorrect.")

    for champ in ["waterfront", "renovated", "has_basement"]:
        if valeurs[champ] not in (0, 1):
            raise ValueError(f"{champ} doit valoir 0 ou 1.")

    if not 47.1 <= valeurs["lat"] <= 47.9:
        raise ValueError("Latitude hors de la zone prévue.")

    if not -122.6 <= valeurs["long"] <= -121.3:
        raise ValueError("Longitude hors de la zone prévue.")

    annee_construction = int(formulaire["yr_built"])
    annee_reference = int(formulaire["sale_year"])

    if not 1900 <= annee_construction <= 2015:
        raise ValueError("Année de construction invalide.")

    if annee_reference not in (2014, 2015):
        raise ValueError("Année de référence invalide.")

    age_brut = annee_reference - annee_construction

    if age_brut < -1:
        raise ValueError("Construction trop récente pour la période.")

    valeurs["house_age"] = max(0, age_brut)

    # Construire exactement les 14 colonnes du modèle
    logement = pd.DataFrame([valeurs], columns=features)

    return logement


# 3. Route de l'application
@app.route("/", methods=["GET", "POST"])
def accueil():

    prix_estime = None
    erreur = None

    if request.method == "POST":
        try:
            logement = preparer_logement(request.form)

            prediction = float(modele.predict(logement)[0])

            if not math.isfinite(prediction) or prediction <= 0:
                raise ValueError("Prix prédit invalide.")

            prix_estime = round(prediction, 2)

        except (ValueError, KeyError, TypeError) as e:
            erreur = str(e)

    return render_template(
        "index.html",
        prix_estime=prix_estime,
        erreur=erreur,
        donnees=request.form if request.method == "POST" else {}
    )


# 4. Lancer le serveur
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)