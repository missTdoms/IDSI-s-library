"""
Système de Recommandation ML
Système de Gestion de Bibliothèque - ENSEA
"""

import numpy as np
from collections import defaultdict
from datetime import datetime
import pickle
import os


class RecommendationSystem:
    """
    Système de recommandation basé sur le filtrage collaboratif
    et le clustering des utilisateurs
    """
    
    def __init__(self, db_session):
        self.db = db_session
        self.user_item_matrix = None
        self.item_similarity = None
        self.user_clusters = None
    
    def _get_emprunt_data(self):
        """Récupérer les données d'emprunts pour l'analyse"""
        from models.models import Emprunt, Etudiant, Livre
        
        emprunts = self.db.query(Emprunt).all()
        
        # Créer une matrice utilisateur-livre
        user_books = defaultdict(list)
        book_users = defaultdict(list)
        
        for emprunt in emprunts:
            user_books[emprunt.etudiant_id].append(emprunt.livre_id)
            book_users[emprunt.livre_id].append(emprunt.etudiant_id)
        
        return user_books, book_users
    
    def calculer_similarite_livres(self, livre_id1, livre_id2):
        """
        Calculer la similarité entre deux livres basée sur les co-emprunts
        Utilise le coefficient de Jaccard
        """
        _, book_users = self._get_emprunt_data()
        
        users1 = set(book_users.get(livre_id1, []))
        users2 = set(book_users.get(livre_id2, []))
        
        if not users1 or not users2:
            return 0.0
        
        intersection = len(users1 & users2)
        union = len(users1 | users2)
        
        return intersection / union if union > 0 else 0.0
    
    def recommander_pour_etudiant(self, etudiant_id, n_recommendations=5):
        """
        Recommander des livres pour un étudiant basé sur ses emprunts précédents
        et ceux des étudiants similaires
        """
        from models.models import Livre, Emprunt
        
        user_books, book_users = self._get_emprunt_data()
        
        # Livres déjà empruntés par l'étudiant
        livres_empruntes = set(user_books.get(etudiant_id, []))
        
        if not livres_empruntes:
            # Si l'étudiant n'a pas d'historique, recommander les livres populaires
            return self.livres_populaires(n_recommendations)
        
        # Trouver les étudiants similaires (qui ont emprunté les mêmes livres)
        etudiants_similaires = defaultdict(int)
        for livre_id in livres_empruntes:
            for autre_etudiant in book_users.get(livre_id, []):
                if autre_etudiant != etudiant_id:
                    etudiants_similaires[autre_etudiant] += 1
        
        # Trier par similarité
        etudiants_similaires = sorted(
            etudiants_similaires.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]  # Top 10 étudiants similaires
        
        # Collecter les livres recommandés
        livres_recommandes = defaultdict(float)
        for autre_etudiant, score_similarite in etudiants_similaires:
            for livre_id in user_books.get(autre_etudiant, []):
                if livre_id not in livres_empruntes:
                    livres_recommandes[livre_id] += score_similarite
        
        # Trier et retourner les top N
        recommendations = sorted(
            livres_recommandes.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n_recommendations]
        
        # Récupérer les objets Livre
        livre_ids = [lid for lid, _ in recommendations]
        if not livre_ids:
            return self.livres_populaires(n_recommendations)
        
        livres = self.db.query(Livre).filter(Livre.id.in_(livre_ids)).all()
        return livres
    
    def livres_populaires(self, n=5):
        """Retourner les livres les plus empruntés"""
        from models.models import Livre, Emprunt
        from sqlalchemy import func
        
        # Compter les emprunts par livre
        popular = self.db.query(
            Livre,
            func.count(Emprunt.id).label('nb_emprunts')
        ).outerjoin(Emprunt).group_by(Livre.id).order_by(
            func.count(Emprunt.id).desc()
        ).limit(n).all()
        
        return [livre for livre, _ in popular]
    
    def livres_par_categorie(self, categorie, n=5):
        """Recommander des livres d'une catégorie spécifique"""
        from models.models import Livre
        
        return self.db.query(Livre).filter(
            Livre.categorie == categorie,
            Livre.quantite_disponible > 0
        ).limit(n).all()
    
    def clustering_etudiants(self, n_clusters=3):
        """
        Regrouper les étudiants en clusters basés sur leurs habitudes d'emprunt
        Utilise un algorithme simple de clustering basé sur les catégories
        """
        from models.models import Etudiant, Emprunt, Livre
        
        etudiants = self.db.query(Etudiant).all()
        
        # Créer un profil pour chaque étudiant basé sur les catégories empruntées
        profils = {}
        categories = set()
        
        for etudiant in etudiants:
            cat_count = defaultdict(int)
            for emprunt in etudiant.emprunts:
                if emprunt.livre and emprunt.livre.categorie:
                    cat_count[emprunt.livre.categorie] += 1
                    categories.add(emprunt.livre.categorie)
            profils[etudiant.id] = cat_count
        
        categories = list(categories)
        
        if not categories:
            return {}
        
        # Créer la matrice de features
        features = []
        etudiant_ids = []
        for etudiant_id, cat_count in profils.items():
            if sum(cat_count.values()) > 0:
                feature_vector = [cat_count.get(cat, 0) for cat in categories]
                features.append(feature_vector)
                etudiant_ids.append(etudiant_id)
        
        if not features:
            return {}
        
        # Clustering simple (k-means simplifié)
        features = np.array(features)
        n_clusters = min(n_clusters, len(features))
        
        # Initialisation aléatoire des centres
        np.random.seed(42)
        indices = np.random.choice(len(features), n_clusters, replace=False)
        centres = features[indices]
        
        # Itérations
        for _ in range(10):
            # Assigner chaque point au cluster le plus proche
            clusters = []
            for f in features:
                distances = [np.linalg.norm(f - c) for c in centres]
                clusters.append(np.argmin(distances))
            
            # Mettre à jour les centres
            for i in range(n_clusters):
                cluster_points = features[np.array(clusters) == i]
                if len(cluster_points) > 0:
                    centres[i] = cluster_points.mean(axis=0)
        
        # Retourner les assignations
        result = {}
        for i, etudiant_id in enumerate(etudiant_ids):
            result[etudiant_id] = clusters[i]
        
        return result
    
    def statistiques_emprunts(self):
        """Générer des statistiques sur les emprunts"""
        from models.models import Emprunt, Livre
        from sqlalchemy import func
        
        stats = {}
        
        # Total emprunts
        stats['total_emprunts'] = self.db.query(Emprunt).count()
        
        # Emprunts en cours
        stats['emprunts_en_cours'] = self.db.query(Emprunt).filter(
            Emprunt.date_retour_effective.is_(None)
        ).count()
        
        # Emprunts en retard
        emprunts_en_cours = self.db.query(Emprunt).filter(
            Emprunt.date_retour_effective.is_(None)
        ).all()
        stats['emprunts_en_retard'] = sum(1 for e in emprunts_en_cours if e.est_en_retard)
        
        # Pénalités totales
        stats['penalites_totales'] = self.db.query(
            func.sum(Emprunt.penalite)
        ).scalar() or 0
        
        # Catégories les plus empruntées
        cat_emprunts = self.db.query(
            Livre.categorie,
            func.count(Emprunt.id).label('count')
        ).join(Emprunt).group_by(Livre.categorie).order_by(
            func.count(Emprunt.id).desc()
        ).limit(5).all()
        stats['categories_populaires'] = [(cat, count) for cat, count in cat_emprunts if cat]
        
        return stats
