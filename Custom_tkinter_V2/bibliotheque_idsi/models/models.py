"""
Modèles de données SQLAlchemy
Système de Gestion de Bibliothèque - ENSEA
"""

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from models.database import Base
import hashlib

# Table d'association Livre-Auteur (relation many-to-many)
livre_auteur = Table(
    'livre_auteur',
    Base.metadata,
    Column('livre_id', Integer, ForeignKey('livres.id'), primary_key=True),
    Column('auteur_id', Integer, ForeignKey('auteurs.id'), primary_key=True)
)


class Auteur(Base):
    """Modèle pour les auteurs"""
    __tablename__ = 'auteurs'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100))
    nationalite = Column(String(50))
    biographie = Column(Text)
    
    # Relation avec les livres
    livres = relationship('Livre', secondary=livre_auteur, back_populates='auteurs')
    
    def __repr__(self):
        return f"<Auteur {self.prenom} {self.nom}>"
    
    @property
    def nom_complet(self):
        if self.prenom:
            return f"{self.prenom} {self.nom}"
        return self.nom


class Livre(Base):
    """Modèle pour les livres"""
    __tablename__ = 'livres'
    
    id = Column(Integer, primary_key=True)
    isbn = Column(String(20), unique=True)
    titre = Column(String(200), nullable=False)
    description = Column(Text)
    categorie = Column(String(100))
    annee_publication = Column(Integer)
    editeur = Column(String(100))
    langue = Column(String(50), default='Français')
    nombre_pages = Column(Integer)
    quantite_totale = Column(Integer, default=1)
    quantite_disponible = Column(Integer, default=1)
    image_url = Column(String(500))
    date_ajout = Column(DateTime, default=datetime.now)
    
    # Relations
    auteurs = relationship('Auteur', secondary=livre_auteur, back_populates='livres')
    emprunts = relationship('Emprunt', back_populates='livre')
    reservations = relationship('Reservation', back_populates='livre')
    
    def __repr__(self):
        return f"<Livre {self.titre}>"
    
    @property
    def est_disponible(self):
        return self.quantite_disponible > 0
    
    @property
    def auteurs_str(self):
        return ", ".join([a.nom_complet for a in self.auteurs])


class Etudiant(Base):
    """Modèle pour les étudiants"""
    __tablename__ = 'etudiants'
    
    id = Column(Integer, primary_key=True)
    matricule = Column(String(50), unique=True, nullable=False)  # Format: ENSEA-XXXX
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    mot_de_passe = Column(String(256), nullable=False)
    filiere = Column(String(100))  # Data Science, Cybersécurité, etc.
    niveau = Column(String(20))  # Master 1, Master 2
    telephone = Column(String(20))
    date_inscription = Column(DateTime, default=datetime.now)
    actif = Column(Boolean, default=True)
    
    # Relations
    emprunts = relationship('Emprunt', back_populates='etudiant')
    reservations = relationship('Reservation', back_populates='etudiant')
    
    def __repr__(self):
        return f"<Etudiant {self.matricule} - {self.nom} {self.prenom}>"
    
    @staticmethod
    def hash_password(password):
        """Hasher le mot de passe"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """Vérifier le mot de passe"""
        return self.mot_de_passe == self.hash_password(password)
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
    
    @property
    def emprunts_en_cours(self):
        return [e for e in self.emprunts if e.date_retour_effective is None]
    
    @property
    def penalites_totales(self):
        return sum([e.penalite for e in self.emprunts if e.penalite > 0])


class Bibliothecaire(Base):
    """Modèle pour les bibliothécaires"""
    __tablename__ = 'bibliothecaires'
    
    id = Column(Integer, primary_key=True)
    identifiant = Column(String(50), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    mot_de_passe = Column(String(256), nullable=False)
    telephone = Column(String(20))
    role = Column(String(50), default='bibliothecaire')  # admin, bibliothecaire
    date_creation = Column(DateTime, default=datetime.now)
    actif = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Bibliothecaire {self.identifiant}>"
    
    @staticmethod
    def hash_password(password):
        """Hasher le mot de passe"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """Vérifier le mot de passe"""
        return self.mot_de_passe == self.hash_password(password)
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class Emprunt(Base):
    """Modèle pour les emprunts"""
    __tablename__ = 'emprunts'
    
    id = Column(Integer, primary_key=True)
    etudiant_id = Column(Integer, ForeignKey('etudiants.id'), nullable=False)
    livre_id = Column(Integer, ForeignKey('livres.id'), nullable=False)
    date_emprunt = Column(DateTime, default=datetime.now)
    date_retour_prevue = Column(DateTime)
    date_retour_effective = Column(DateTime)
    penalite = Column(Float, default=0)  # En francs CFA
    statut = Column(String(20), default='en_cours')  # en_cours, retourne, en_retard
    notes = Column(Text)
    
    # Relations
    etudiant = relationship('Etudiant', back_populates='emprunts')
    livre = relationship('Livre', back_populates='emprunts')
    
    # Constantes
    DUREE_EMPRUNT_JOURS = 14
    PENALITE_PAR_JOUR = 100  # 100 FCFA par jour de retard
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.date_retour_prevue:
            self.date_retour_prevue = datetime.now() + timedelta(days=self.DUREE_EMPRUNT_JOURS)
    
    def __repr__(self):
        return f"<Emprunt {self.id} - {self.livre.titre if self.livre else 'N/A'}>"
    
    @property
    def jours_retard(self):
        """Calculer le nombre de jours de retard"""
        if self.date_retour_effective:
            date_ref = self.date_retour_effective
        else:
            date_ref = datetime.now()
        
        if date_ref > self.date_retour_prevue:
            return (date_ref - self.date_retour_prevue).days
        return 0
    
    @property
    def est_en_retard(self):
        return self.jours_retard > 0
    
    def calculer_penalite(self):
        """Calculer la pénalité en FCFA"""
        self.penalite = self.jours_retard * self.PENALITE_PAR_JOUR
        return self.penalite
    
    def retourner(self):
        """Enregistrer le retour du livre"""
        self.date_retour_effective = datetime.now()
        self.calculer_penalite()
        self.statut = 'retourne'
        
        # Mettre à jour la disponibilité du livre
        if self.livre:
            self.livre.quantite_disponible += 1


class Reservation(Base):
    """Modèle pour les réservations"""
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key=True)
    etudiant_id = Column(Integer, ForeignKey('etudiants.id'), nullable=False)
    livre_id = Column(Integer, ForeignKey('livres.id'), nullable=False)
    date_reservation = Column(DateTime, default=datetime.now)
    date_expiration = Column(DateTime)
    statut = Column(String(20), default='en_attente')  # en_attente, confirmee, annulee, expiree
    
    # Relations
    etudiant = relationship('Etudiant', back_populates='reservations')
    livre = relationship('Livre', back_populates='reservations')
    
    DUREE_RESERVATION_JOURS = 3
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.date_expiration:
            self.date_expiration = datetime.now() + timedelta(days=self.DUREE_RESERVATION_JOURS)
    
    def __repr__(self):
        return f"<Reservation {self.id} - {self.livre.titre if self.livre else 'N/A'}>"
    
    @property
    def est_expiree(self):
        return datetime.now() > self.date_expiration and self.statut == 'en_attente'
