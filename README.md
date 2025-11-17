

flask_project

Application web **Flask** interactive pour explorer la base **Ensembl**. Elle affiche les parties d’organisme, les gènes et transcrits, avec des fiches détaillées et permet l’édition de gènes. Utilise **SQLite/SQL** pour la base de données, des templates HTML/CSS pour l’interface, et est déployée sur **Render**.

---

## Table des matières

1. [À propos](#à-propos)  
2. [Fonctionnalités](#fonctionnalités)  
3. [Architecture & Structure du projet](#architecture--structure-du-projet)  
4. [Installation & Exécution](#installation--exécution)  
5. [Configuration](#configuration)  
6. [Base de données](#base-de-données)  
7. [Routes / API](#routes--api)  
8. [Front‑end](#front-end)  
9. [Déploiement](#déploiement)  
10. [Contribuer](#contribuer)  
11. [Roadmap / Améliorations futures](#roadmap--améliorations-futures)  
12. [Licence](#licence)  
13. [Contact](#contact)

---

## À propos

Cette application web permet d’explorer une version simplifiée de la base **Ensembl** (modèle humain HS63 dans ce cas), en naviguant :

- par **organismes / parties d’organisme**  
- par **gènes**, avec des fiches détaillées  
- par **transcrits**, liés aux gènes  
- édition des gènes (ajout / modification) via l’interface  

Elle utilise **SQLite** comme base de données légère, et des templates **Flask / Jinja2** pour le rendu HTML. Le but est d’avoir une interface simple mais puissante pour visualiser et manipuler des données génomiques.

---

## Fonctionnalités

- Navigation hiérarchique : organisme → gène → transcrit  
- Fiches détaillées pour chaque gène et transcrit  
- Formulaire d’édition / mise à jour des gènes  
- Interface web responsive (HTML + CSS)  
- API simple pour certaines opérations (GET, POST)  
- Base de données SQLite embarquée  
- Déploiement possible sur Render ou autre plateforme cloud  

---

## Architecture & Structure du projet

```

flask_project/
│
├── api.py                   # définition des routes API
├── ensembl_hs63_simple.sqlite  # base de données SQLite
├── requirements.txt         # dépendances Python
├── Procfile.txt             # pour déploiement (Render)
│
├── templates/               # templates HTML (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── gene_detail.html
│   └── ...
│
└── static/                   # fichiers statiques : CSS, JS, images
├── css/
└── js/

````

- `api.py` : routes backend (vues + API)  
- `templates/` : vues HTML  
- `static/` : ressources CSS / JS  
- `ensembl_hs63_simple.sqlite` : base de données SQLite  

---

## Installation & Exécution

1. **Cloner le répertoire**  
   ```bash
   git clone https://github.com/kounourizkiath/flask_project.git
   cd flask_project
````

2. **Créer un environnement virtuel**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # mac/linux
   # Windows : venv\Scripts\activate
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l’application**

   ```bash
   export FLASK_APP=api.py
   export FLASK_ENV=development  # optionnel : mode debug
   flask run
   ```

   Accéder ensuite à `http://127.0.0.1:5000`.

---

## Configuration

* Pour changer de base de données, adapter l’URI SQLite dans le code Flask.
* Variables d’environnement possibles : `FLASK_ENV`, `FLASK_DEBUG`.
* `Procfile.txt` : utilisé pour le déploiement sur Render, indique la commande de lancement.

---

## Base de données

* Base SQLite : `ensembl_hs63_simple.sqlite`.
* Contient les tables pour les organismes, gènes et transcrits.
* Pour modifier la base : utiliser DB Browser for SQLite ou tout autre outil compatible.

---

## Routes / API

* `/` : page d’accueil, liste des organismes
* `/gene/<gene_id>` : fiche d’un gène spécifique
* `/transcript/<transcript_id>` : fiche d’un transcrit
* `/edit_gene/<gene_id>` : formulaire d’édition d’un gène
* `/api/...` : routes API REST selon implémentation

---

## Front‑end

* Templates **Jinja2** héritant de `base.html`.
* CSS et JS dans `static/`.
* Formulaires pour ajout / édition de gènes.

---

## Déploiement

* Déploiement possible sur **Render** :

  1. Créer un compte Render
  2. Créer une Web Service et lier ton dépôt GitHub
  3. Définir le **Procfile** pour démarrage Flask
  4. Définir les variables d’environnement
  5. Déployer et vérifier l’URL fournie

* Possibilité de déploiement sur **Heroku** ou **Docker**.

---

## Contribuer

* Ouvrir des **issues** pour bugs ou suggestions.
* Fork → branch → Pull Request.
* Respecter les standards PEP8 et docstrings.
* Ajouter des tests unitaires si possible (pytest / unittest).

---

## Roadmap / Améliorations futures

* Ajouter tests unitaires et d’intégration
* Authentification / gestion utilisateurs
* API CRUD complète pour gènes et transcrits
* Migration vers PostgreSQL ou MySQL
* Amélioration UI/UX : recherche, filtres, design responsive
* Importer une version plus complète de la base Ensembl
* Déploiement avec Docker + CI/CD

---

## Licence

À définir (MIT, Apache 2.0, etc.)

---

## Contact

* **Auteur** : Rizkiath Kounou
* **GitHub** : [kounourizkiath](https://github.com/kounourizkiath)
* **Email** : kounourizkiath@gmail.com
* **Live Demo** : https://flask-project-bj1e.onrender.com/

```


