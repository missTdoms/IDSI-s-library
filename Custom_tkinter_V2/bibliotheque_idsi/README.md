# 📚 Système de Gestion de Bibliothèque - IDSI

## Application Desktop Moderne avec CustomTkinter

**Institution:** International Data Science Institute (IDSI)  
**Programmes:** Data Science • Big Data • IA • Cybersécurité  
**Version:** 3.0.0

---

## 📋 Description

Application de gestion de bibliothèque complète développée en Python avec CustomTkinter. Cette application permet la gestion des livres, des emprunts, des étudiants et inclut un système de recommandation basé sur le Machine Learning.

### ✨ Nouveautés v3.0

- 🎨 **Interface moderne** avec CustomTkinter
- 🖼️ **Image de fond** sur la page de connexion
- 🔐 **Gestion de profil** - Les utilisateurs peuvent modifier leurs informations
- 🔑 **Changement de mot de passe** - Sécurité renforcée
- 📱 **Design responsive** et animations fluides
- 🌙 Support du mode clair/sombre

### Fonctionnalités principales

#### 👨‍🎓 Espace Étudiant
- ✅ Consultation du catalogue de livres
- ✅ Recherche par titre, auteur, catégorie
- ✅ Gestion des emprunts personnels
- ✅ Suivi des pénalités de retard
- ✅ **Modification du profil**
- ✅ **Changement de mot de passe**

#### 👨‍💼 Espace Bibliothécaire
- ✅ Tableau de bord avec statistiques
- ✅ Gestion complète des livres (CRUD)
- ✅ Gestion des étudiants
- ✅ Suivi des emprunts et retours
- ✅ Gestion des pénalités (FCFA)
- ✅ **Modification du profil**
- ✅ **Changement de mot de passe**

---

## 🚀 Installation

### Prérequis
- Python 3.9 ou supérieur
- pip (gestionnaire de packages Python)

### Étapes d'installation

```bash
# 1. Cloner ou télécharger le projet
cd bibliotheque_ensea

# 2. Créer un environnement virtuel (recommandé)
python -m venv venv

# 3. Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Linux/Mac:
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Initialiser la base de données avec des données de test
python init_data.py

# 6. Lancer l'application
python main.py
```

---

## 🔐 Comptes de test

### Bibliothécaire (Admin)
- **Identifiant:** `admin`
- **Mot de passe:** `admin123`

### Étudiant
- **Matricule:** `IDSI-2024-001`
- **Mot de passe:** `etudiant123`

---

## 📁 Structure du Projet

```
bibliotheque_ensea/
│
├── main.py                 # Point d'entrée de l'application
├── init_data.py            # Script d'initialisation des données
├── requirements.txt        # Dépendances Python
├── README.md               # Documentation
│
├── models/                 # Modèles de données
│   ├── __init__.py
│   ├── database.py         # Configuration SQLAlchemy
│   └── models.py           # Modèles (Livre, Etudiant, Emprunt, etc.)
│
├── views/                  # Interfaces utilisateur
│   ├── __init__.py
│   ├── login_view.py       # Page de connexion
│   ├── student_dashboard.py    # Dashboard étudiant
│   └── librarian_dashboard.py  # Dashboard bibliothécaire
│
├── utils/                  # Utilitaires
│   ├── __init__.py
│   ├── theme.py            # Design system (couleurs, fonts, etc.)
│   ├── components.py       # Composants UI réutilisables
│   └── recommendation.py   # Système de recommandation ML
│
├── maquettes_figma/        # Maquettes HTML/CSS pour Figma
│   └── maquettes_complete.html
│
└── assets/                 # Ressources (images, icônes)
```

---

## 🎨 Design System

### Palette de couleurs

| Couleur | Hex | Usage |
|---------|-----|-------|
| Primary | `#1E3A5F` | Bleu marine ENSEA |
| Secondary | `#F7941D` | Orange accent |
| Success | `#27AE60` | Disponible, succès |
| Warning | `#F39C12` | Avertissements |
| Danger | `#E74C3C` | Erreurs, retards |
| Background | `#F5F7FA` | Fond principal |

### Maquettes Figma

Les maquettes sont disponibles dans le fichier `maquettes_figma/maquettes_complete.html`. Ouvrez ce fichier dans un navigateur pour visualiser toutes les interfaces :

1. Page de connexion
2. Dashboard Étudiant - Accueil
3. Catalogue des livres
4. Mes Emprunts
5. Recommandations ML
6. Dashboard Bibliothécaire
7. Modal Ajouter un livre
8. Design System complet

---

## 💰 Système de Pénalités

- **Durée d'emprunt:** 14 jours
- **Pénalité par jour de retard:** 100 FCFA
- **Devise:** Franc CFA (FCFA)

---

## 📊 Base de Données

### Tables principales

- **etudiants** - Informations des étudiants
- **bibliothecaires** - Comptes bibliothécaires
- **livres** - Catalogue des livres
- **auteurs** - Liste des auteurs
- **livre_auteur** - Relation many-to-many
- **emprunts** - Historique des emprunts
- **reservations** - Réservations en cours

### Catégories de livres

- Data Science
- Intelligence Artificielle
- Machine Learning
- Deep Learning
- Big Data
- Cybersécurité
- Statistiques
- Programmation
- Base de données
- Et plus...

---

## 🔧 Configuration

### Modifier les paramètres

Éditez le fichier `utils/theme.py` pour personnaliser :

```python
APP_CONFIG = {
    'name': 'Bibliothèque ENSEA',
    'version': '2.0.0',
    'loan_duration_days': 14,
    'penalty_per_day': 100,  # FCFA
    'max_loans_per_student': 3,
}
```

---

## 🤖 Système de Recommandation

Le système utilise :

1. **Filtrage collaboratif** - Basé sur les emprunts d'étudiants similaires
2. **Coefficient de Jaccard** - Pour calculer la similarité entre livres
3. **Clustering** - Regroupement des utilisateurs par préférences

### Comment ça fonctionne

```python
from utils.recommendation import RecommendationSystem

# Créer une instance
rec_system = RecommendationSystem(db_session)

# Obtenir des recommandations pour un étudiant
recommendations = rec_system.recommander_pour_etudiant(
    etudiant_id=1,
    n_recommendations=5
)
```

---

## 📧 Support

Pour toute question ou problème :
- Email: aymy.doma@ensea.edu.ci
- Institution: ENSEA, Abidjan, Côte d'Ivoire

---

## 📄 Licence

Ce projet est développé dans le cadre d'un mémoire de Master à l'ENSEA.

---

© 2024-2025 Aymy Doma - ENSEA
