---
title: apartment-hunter
emoji: 🏠
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Apartment Hunter

Application Flask d'estimation immobiliere avec Random Forest.

## Dataset
King County House Sales (2014-2015).

## Technologies
Python, scikit-learn, Flask, Docker et Hugging Face.

## Performances sur le jeu de test
- MAE : 70 510,41 $
- RMSE : 126 780,75 $
- R2 : 0,8842

## Utilisation
Remplir le formulaire et cliquer sur Estimer le prix immobilier.

Les estimations sont basees sur des ventes historiques.
Elles ne correspondent pas aux prix actuels.

## Application en ligne

https://huggingface.co/spaces/FOUNAS/apartment-hunter

Application Flask déployée avec Docker sur Hugging Face Spaces.
Le modèle Random Forest prédit les prix historiques des
logements de King County en dollars américains.
