# WildLens – README principal

WildLens est une application web permettant d’identifier des espèces animales à partir d’empreintes, grâce à un modèle d’intelligence artificielle. Ce projet est composé de trois parties principales : un front-end développé en PHP, un back-end sous Flask en Python, et un modèle IA séquentiel créé avec TensorFlow.

## Structure du projet

```
MSPR_WILDLENS-MAIN/
|
├── api/                   # Back-end Flask (routes, prédiction, auth)
├── model/                 # Modèle IA et métriques associées
├── script/                # Scripts de traitement et entraînement
├── Views/                 # Pages front-end PHP
├── assets/                # Fichiers statiques (CSS, JS, images)
├── uploads/               # Images envoyées par les utilisateurs
├── data/                  # Données IA (brutes / nettoyées)
├── TEST/                  # Scripts de test
├── README.md              # Documentation principale
└── index.php              # Point d’entrée du site
```

## Installation

1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/wildlens.git
cd wildlens
```

2. Installer les dépendances Python

```bash
python -m venv venv
source venv/bin/activate  # sous Windows : venv\Scripts\activate
pip install -r requirements.txt
```

3. Lancer le back-end

```bash
cd api
python main.py
```

4. Lancer le front-end PHP via un serveur Apache (WAMP, XAMPP, etc.).

## Fonctionnalités globales

* Identification d'espèces par empreinte
* Authentification sécurisée avec tokens
* Historique personnel de scans
* Affichage d’erreurs centralisé
* Monitoring IA (matrice de confusion, courbes)
* Tests unitaires intégrés

---

Ce README a été rédigé par Nihel Hammouche pour la coordination du projet WildLens.

---

# Front-end - WildLens

Le front-end a été conçu pour offrir une expérience utilisateur fluide et intuitive permettant l’interrogation de l’IA via un formulaire image, la consultation de l’historique de scans, et la gestion du profil utilisateur.

## Technologies utilisées

* HTML / CSS / Bootstrap
* PHP 8
* JavaScript (AJAX, cURL)
* Intégration REST avec API Flask
* Conformité RGAA (accessibilité)

## Structure

```
Views/
├── login.php
├── register.php
├── profil.php
├── historique.php
├── animaux.php
assets/
├── CSS/
├── JS/
uploads/
```

## Fonctionnalités principales

* Formulaires d’authentification (inscription, connexion)
* Envoi d’empreintes pour analyse
* Affichage du résultat de la prédiction
* Historique utilisateur avec les anciennes analyses
* Modification de profil
* Gestion des erreurs via log.php

Cette partie a été réalisée par lORIS TERRY et NIHEL HAMMOUCHE dans le cadre du développement front-end du projet.

---

# Back-end - WildLens API

Le back-end Flask fournit une API RESTful centralisant la logique métier, l’authentification, la communication avec le modèle IA séquentiel, et l’accès à la base de données.

## Technologies

* Python 3.11
* Flask & Flask-CORS
* SQLAlchemy (connexion MySQL)
* TensorFlow/Keras (modèle séquentiel pour classification)
* JSON Web Token (JWT) pour sécurité
* Logging personnalisé

## Fonctionnalités clés du back-end

**Routes RESTful**

* /users : création d’utilisateur
* /login : authentification
* /predict : envoi d’image pour prédiction
* /animals : exploration des espèces
* /scan-history : historique personnel

**Sécurité**

* Authentification par tokens UUID
* Protection des routes sensibles

**Journalisation**

* Erreurs enregistrées dans wildlens\_api.log
* Fichier log.php utilisé pour transmettre les messages côté front-end

**Prédiction IA**
Le modèle est un réseau neuronal séquentiel entraîné avec TensorFlow sur un jeu de données d’empreintes. Il reçoit une image et retourne la classe d’animal prédit.

**Tests**
Des tests unitaires ont été réalisés avec Pytest dans le dossier TEST/.

Cette API a été développée par \[Ton Nom] pour la partie back-end.

---

# Intelligence Artificielle - Modèle IA

Le modèle IA repose sur une architecture séquentielle construite avec TensorFlow/Keras. Il s’agit d’un classificateur d’images destiné à identifier des espèces animales à partir d’empreintes.

## Données

* Dataset nettoyé et augmenté dans le dossier `data/`
* Images prétraitées (resize, grayscale, normalisation)

## Modèle

* Architecture : Conv2D -> MaxPooling -> Dense
* Fonction d’activation : ReLU / Softmax
* Entraînement sur 30 epochs avec validation croissée

## Résultats

* Sauvegarde du modèle : `model_trained.h5`
* Visualisation : `confusion_matrix.png`, `training_curves.png`

Cette partie IA a été développée par SAMAR HTIRA et NIHEL HAMMOUCHE dans le cadre du développement machine learning du projet WildLens.
```
    pip install mysql-connector-python
```

