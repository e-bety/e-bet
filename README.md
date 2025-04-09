# 🎰 E.Bet — Le jeu où chaque mise peut tout changer !

Bienvenue sur **E.Bet**, une application de jeu en ligne où vous pouvez miser sur des lots de numéros et tenter de remporter des gains selon un système intelligent et ludique !

---

## 🚀 Déploiement en production

🔗 Accéder à la version en ligne : [https://e-bet-1.onrender.com](https://e-bet-1.onrender.com)

---

## 🛠️ Technologies utilisées

- **Backend** : FastAPI (Python 3.11)
- **Base de données** : PostgreSQL 16
- **Frontend** : React.js (PWA compatible)
- **Déploiement** : Render

---

## 📦 Fonctionnalités principales

- 🔐 Inscription et connexion des utilisateurs
- 💰 Dépôts et retraits avec historique
- 🎮 Jeu de hasard avec système de mise intelligent
- 🏆 Récompenses calculées selon plusieurs critères :
  - Position dans les groupes de numéros
  - Ordre respecté (bonus multiplicateur)
- 👥 Système de parrainage multi-niveaux
- 📊 Tableau de bord administrateur pour suivre les transactions
- 📱 Interface mobile optimisée (PWA installable)

---

## 💻 Lancer l'application en local

### 1. Backend (FastAPI)

```bash
# Crée un environnement virtuel
python -m venv env
source env/bin/activate  # ou `env\Scripts\activate` sous Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le backend
uvicorn app.main:app --reload
