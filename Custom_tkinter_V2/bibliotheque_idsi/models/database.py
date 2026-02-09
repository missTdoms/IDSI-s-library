"""
Configuration de la base de données SQLAlchemy
Système de Gestion de Bibliothèque - ENSEA
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Chemin de la base de données
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'bibliotheque_ensea.db')

# Configuration SQLAlchemy
engine = create_engine(f'sqlite:///{DATABASE_PATH}', echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Obtenir une session de base de données"""
    db = SessionLocal()
    try:
        return db
    except:
        db.close()
        raise

def init_db():
    """Initialiser la base de données"""
    from models.models import Etudiant, Bibliothecaire, Livre, Auteur, livre_auteur, Emprunt, Reservation
    Base.metadata.create_all(bind=engine)
