# YNM Data

## 🌐 Présentation

**YNM Data** est une application web dédiée à la visualisation et à l'analyse de données relationnelles et multidimensionnelles (OLAP). Elle permet d'explorer, manipuler et auditer efficacement les données au sein d'une interface moderne et dynamique.

## 🔧 Stack Technique

### Architecture Microservices
- **Backend** : Flask (Python)
- **Frontend** : Angular 17
- **Base de données** : MySQL + Data Warehouse

### Interface & Visualisation
- **Tailwind CSS** : Système de design personnalisé
- **Chart.js** : Graphiques interactifs et dynamiques

## 🧩 Fonctionnalités principales

- Navigation et gestion des tables avec opérations CRUD
- Analyse OLAP avec les opérations classiques
- Journalisation complète des actions utilisateurs
- Réinitialisation des jeux de données (reset)

## 🚀 Déploiement

# Cloner le dépôt
git clone https://github.com/Yovanne05/YNM-Data.git
cd YNM-Data

# Lancer le frontend Angular
cd front
npm install
ng serve

# Ouvrir un nouveau terminal pour le backend
cd ../back
pip install -r requirements.txt
python -m flask run

Accès aux services :
Frontend : http://localhost:4200
API : http://localhost:5000

## 💡 Points techniques
- Architecture orientée services
- API REST documentée avec Swagger
- Système de logs centralisé pour un audit complet des actions
