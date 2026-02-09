"""
Script d'initialisation de la base de données avec les vrais étudiants
Système de Gestion de Bibliothèque - IDSI

INP-HB - Master Data Science & Cybersécurité
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from models.database import init_db, get_db
from models.models import Etudiant, Bibliothecaire, Livre, Auteur, Emprunt, Reservation


# ============================================
# DONNÉES DES ÉTUDIANTS (depuis le fichier Excel)
# ============================================

ETUDIANTS_DATA = [
    # Master 1 - Data Sciences
    {"matricule": "25INP00193", "nom": "AKROMAN", "prenom": "CHARLES ARISTIDE KACOU", "email": "charles.akroman25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00254", "nom": "AYEMOU", "prenom": "BAHE MARIE LAURE THERESE", "email": "bahe.ayemou25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00250", "nom": "BAMBA", "prenom": "DRISSA FRANCIS JUNIOR", "email": "drissa.bamba25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00195", "nom": "BROU", "prenom": "KOUAKOU CEPHAS", "email": "cephas.brou25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00200", "nom": "DABIRE", "prenom": "SAABETERFAA JOEL", "email": "saabeterfaa.dabire25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "BURKINABE"},
    {"matricule": "25INP00253", "nom": "DAH", "prenom": "BOBO SAMUEL", "email": "bobo.dah25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00256", "nom": "DIABAGATE", "prenom": "SOUMAHILA", "email": "soumahila.diabagate25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00249", "nom": "DJE", "prenom": "KOFFI JEAN EUDES", "email": "koffi.dje25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00029", "nom": "DOUKROU", "prenom": "DODJI MARIE JOLIANA", "email": "dodji.doukrou25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00190", "nom": "DRABO", "prenom": "SEYDOU", "email": "seydou.drabo25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "BURKINABE"},
    {"matricule": "25INP00201", "nom": "EZEJIDEAKU", "prenom": "CHUKWUDOBELU EMMANUEL", "email": "chukwudobelu.ezejideaku25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "NIGERIANNE"},
    {"matricule": "25INP00248", "nom": "GBAH", "prenom": "KAPEU FABIEN", "email": "kapeu.gbah25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00197", "nom": "GOLI", "prenom": "YAO JEAN-JAURES", "email": "yao.goli25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00188", "nom": "KANRAH", "prenom": "MAXIME ADONLIN", "email": "maxime.kanrah25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00192", "nom": "KOFFI", "prenom": "KONAN HIPPOLITE EVRARD", "email": "hippolite.koffi25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00267", "nom": "KOFFI", "prenom": "MARC JOEL", "email": "marc.koffi25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00247", "nom": "KONAN", "prenom": "KOFFI DENIS", "email": "koffi.konan25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00189", "nom": "KOUAKOU", "prenom": "KOFFI HONORE", "email": "koffi.kouakou25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00252", "nom": "KOUAME", "prenom": "KOMOE FERDINAND", "email": "komoe.kouame25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00191", "nom": "KOUAME", "prenom": "KOUAKOU ELVIS JUNIOR", "email": "kouakou.kouame25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00251", "nom": "OUATTARA", "prenom": "ALMAMY ALI", "email": "almamy.ouattara25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00194", "nom": "SORO", "prenom": "TCHEWA AMY DOMA", "email": "tchewa.soro25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "22INP01073", "nom": "TOURÉ", "prenom": "MAMADOU", "email": "mamadou.toure22@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00255", "nom": "YAO", "prenom": "RYAN ANGE EMMANUEL", "email": "ryan.yao25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00196", "nom": "YAO", "prenom": "YAO YANNICK", "email": "yannick.yao25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00198", "nom": "YEO", "prenom": "TENEGNIGUI", "email": "tenegnigui.yeo25@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    
    # Master 1 - Cybersécurité
    {"matricule": "25INP00266", "nom": "BROU", "prenom": "VANESSA REISHANA", "email": "vanessa.brou25@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "22INP00198", "nom": "CODJEAU", "prenom": "NELOUM GRACE EMMANUELLE LYDIE", "email": "neloum.codjeau22@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00257", "nom": "DIARRASSOUBA", "prenom": "ZANWA", "email": "zanwa.diarrassouba25@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00265", "nom": "GAKPA", "prenom": "ESSAIE SOPHONIE", "email": "essaie.gakpa25@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00262", "nom": "GBA", "prenom": "MINCA YANN ARMEL", "email": "minca.gba25@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "22INP00394", "nom": "KANON", "prenom": "PRINCE ELIHU JOSEPH CHRISTIAN", "email": "prince.kanon22@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00259", "nom": "KOPE", "prenom": "JEAN PAUL DAVID", "email": "jean.kope25@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00261", "nom": "SAMAKE", "prenom": "CHEIKH OMAR", "email": "cheikh.samake25@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "21INP00711", "nom": "SILUÉ", "prenom": "DOLOUROU ANTONI", "email": "dolourou.silue21@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00260", "nom": "SYLLA", "prenom": "ABDOUL AZIZ INZA MOUMINE", "email": "abdoul.sylla25@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP01027", "nom": "TIHO", "prenom": "GNIMETA", "email": "gnimeta.tiho24@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00264", "nom": "TRAORE", "prenom": "HABIBA YASMINE", "email": "habiba.traore25@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00258", "nom": "TRAORE", "prenom": "IBRAHIM", "email": "ibrahim.traore25@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    {"matricule": "25INP00263", "nom": "YAO", "prenom": "ALLE EMMANUEL FLAURIAN", "email": "alle.yao25@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 1", "nationalite": "IVOIRIENNE"},
    
    # Master 2 - Data Sciences
    {"matricule": "24INP01010", "nom": "ADJINDA", "prenom": "ADEKIN OLAKEMI LUCIA", "email": "adkin.adjinda24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "BENINOISE"},
    {"matricule": "24INP00990", "nom": "ALUI", "prenom": "ANGE-ELVIS", "email": "ange-elvis.alui24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "21INP00973", "nom": "CAMARA", "prenom": "FAROUCK MUHAMMAD BACHIR", "email": "farouck.camara21@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP00991", "nom": "COULIBALY", "prenom": "FOUNGNIGUE ADELE", "email": "foungnigue.coulibaly24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP00992", "nom": "COULIBALY", "prenom": "SEGNINDENIN OUMAR", "email": "segnindenin.coulibaly24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "23INP00917", "nom": "FOFANA", "prenom": "ABOUBACAR CYRILLE", "email": "aboubacar.fofana23@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP00994", "nom": "FOFANA", "prenom": "NDANFOLY ADELPHE VIANNEY", "email": "ndanfoly.fofana24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP00995", "nom": "GBE", "prenom": "VEH MINQUE EDDY ARISTIDE", "email": "veh.gbe24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP00996", "nom": "KOFFI", "prenom": "JUDE", "email": "jude.koffi24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP01276", "nom": "KONAN", "prenom": "N'GUESSAN ESAÏE", "email": "nguessan.konan24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP00998", "nom": "KOUIAHON", "prenom": "TOSSEU LARISSA DORINE", "email": "tosseu.kouiahon24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "23INP00923", "nom": "MABIALA", "prenom": "BERGIN", "email": "bergin.mabiala23@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "CONGOLAISE"},
    {"matricule": "24INP01002", "nom": "MOUHI", "prenom": "CHRIST-EMMANUEL", "email": "christ.mouhi24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP01055", "nom": "NIADA", "prenom": "ULRICH BORIS", "email": "ulrich.niada24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "BURKINABE"},
    {"matricule": "24INP01008", "nom": "VE", "prenom": "TOKPA NATHANAEL JUNIOR", "email": "nathanael.ve24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP01009", "nom": "ZONGO", "prenom": "MESSOU ALPHEE COLOMBE", "email": "messou.zongo24@inphb.ci", "filiere": "DATA SCIENCES-BIG DATA ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    
    # Master 2 - Cybersécurité
    {"matricule": "24INP01058", "nom": "ADJETEY TOGLOZOMBIO", "prenom": "ADJE MICHEL", "email": "adje.adjeteytoglozombio24@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "TOGOLAISE"},
    {"matricule": "21INP00276", "nom": "ASSANVO", "prenom": "DELI YANN HOREB", "email": "deli.assanvo21@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP01015", "nom": "DIABY", "prenom": "ABOUBACAR SIDIKI", "email": "aboubacar.diaby24@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP01017", "nom": "GOUET", "prenom": "GNANGNAN GRACE ESTHER", "email": "gnangnan.gouet24@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "21INP00595", "nom": "KONAN", "prenom": "GUILLAUME DAVID", "email": "guillaume.konan21@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP01057", "nom": "KONE", "prenom": "ISSOUF", "email": "issouf.kone24@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP01020", "nom": "KONE", "prenom": "KADER", "email": "kader.kone24@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP01022", "nom": "KOUAKOU", "prenom": "MARCEL JUNIOR", "email": "marcel.kouakou24@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP01023", "nom": "KOUAME", "prenom": "ESDRAS JONATHAN", "email": "esdras.kouame24@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP01024", "nom": "N'GUESSAN", "prenom": "CURTIS SYLVAIN", "email": "curtis.nguessan24@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "21INP00893", "nom": "SAGOE", "prenom": "CHRISTIAN BRICE-YVAN", "email": "christian.sagoe21@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
    {"matricule": "24INP01028", "nom": "TOURE", "prenom": "MAMINIGNAN ZAHRA", "email": "maminignan.toure24@inphb.ci", "filiere": "SECURITE, CYBERSECURITE ET INTELLIGENCE ARTIFICIELLE", "niveau": "MASTER 2", "nationalite": "IVOIRIENNE"},
]


def create_sample_data():
    """Créer les données pour l'application"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║   📚 IDSI Library - Initialisation de la base de données            ║
    ║   INP-HB - Master Data Science & Cybersécurité                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    print("🔧 Initialisation de la base de données...")
    init_db()
    
    db = get_db()
    
    try:
        # Vérifier si des données existent déjà
        if db.query(Bibliothecaire).count() > 0:
            print("⚠️  Des données existent déjà. Voulez-vous les réinitialiser ?")
            response = input("Tapez 'oui' pour confirmer: ")
            if response.lower() != 'oui':
                print("Annulé.")
                return
            
            # Supprimer les données existantes
            db.query(Emprunt).delete()
            db.query(Reservation).delete()
            db.query(Livre).delete()
            db.query(Auteur).delete()
            db.query(Etudiant).delete()
            db.query(Bibliothecaire).delete()
            db.commit()
        
        print("\n📝 Création des bibliothécaires...")
        
        # Bibliothécaires
        bibliothecaires = [
            Bibliothecaire(
                identifiant='admin',
                nom='Administrateur',
                prenom='Principal',
                email='admin@inphb.ci',
                mot_de_passe=Bibliothecaire.hash_password('admin123'),
                telephone='+225 07 00 00 00 01',
                role='admin'
            ),
            Bibliothecaire(
                identifiant='biblio1',
                nom='DIALLO',
                prenom='Aminata',
                email='aminata.diallo@inphb.ci',
                mot_de_passe=Bibliothecaire.hash_password('biblio123'),
                telephone='+225 07 00 00 00 02',
                role='bibliothecaire'
            ),
        ]
        
        for b in bibliothecaires:
            db.add(b)
        
        print("✅ Bibliothécaires créés")
        print("   - admin / admin123 (Administrateur)")
        print("   - biblio1 / biblio123 (Bibliothécaire)")
        
        print(f"\n📝 Création de {len(ETUDIANTS_DATA)} étudiants...")
        
        # Étudiants (mot de passe = matricule)
        for etud_data in ETUDIANTS_DATA:
            etudiant = Etudiant(
                matricule=etud_data['matricule'],
                nom=etud_data['nom'],
                prenom=etud_data['prenom'],
                email=etud_data['email'],
                mot_de_passe=Etudiant.hash_password(etud_data['matricule']),  # Mot de passe = matricule
                filiere=etud_data['filiere'],
                niveau=etud_data['niveau'],
                telephone=''
            )
            db.add(etudiant)
        
        db.flush()
        
        # Compter par filière
        ds_m1 = len([e for e in ETUDIANTS_DATA if 'DATA SCIENCES' in e['filiere'] and e['niveau'] == 'MASTER 1'])
        ds_m2 = len([e for e in ETUDIANTS_DATA if 'DATA SCIENCES' in e['filiere'] and e['niveau'] == 'MASTER 2'])
        cyber_m1 = len([e for e in ETUDIANTS_DATA if 'SECURITE' in e['filiere'] and e['niveau'] == 'MASTER 1'])
        cyber_m2 = len([e for e in ETUDIANTS_DATA if 'SECURITE' in e['filiere'] and e['niveau'] == 'MASTER 2'])
        
        print(f"✅ {len(ETUDIANTS_DATA)} étudiants créés:")
        print(f"   - Data Sciences M1: {ds_m1} étudiants")
        print(f"   - Data Sciences M2: {ds_m2} étudiants")
        print(f"   - Cybersécurité M1: {cyber_m1} étudiants")
        print(f"   - Cybersécurité M2: {cyber_m2} étudiants")
        
        print("\n📝 Création des auteurs...")
        
        # Auteurs
        auteurs_data = [
            ('Aurélien', 'Géron', 'Française'),
            ('François', 'Chollet', 'Française'),
            ('Ian', 'Goodfellow', 'Américaine'),
            ('Yoshua', 'Bengio', 'Canadienne'),
            ('Andrew', 'Ng', 'Américaine'),
            ('Jake', 'VanderPlas', 'Américaine'),
            ('Wes', 'McKinney', 'Américaine'),
            ('Bruce', 'Schneier', 'Américaine'),
            ('Ross', 'Anderson', 'Britannique'),
            ('Hadley', 'Wickham', 'Néo-Zélandaise'),
            ('Thomas', 'Cormen', 'Américaine'),
            ('Martin', 'Kleppmann', 'Allemande'),
            ('Christopher', 'Bishop', 'Britannique'),
        ]
        
        auteurs = {}
        for prenom, nom, nationalite in auteurs_data:
            auteur = Auteur(nom=nom, prenom=prenom, nationalite=nationalite)
            db.add(auteur)
            auteurs[f"{prenom} {nom}"] = auteur
        
        db.flush()
        print(f"✅ {len(auteurs)} auteurs créés")
        
        print("\n📝 Création des livres...")
        
        # Livres
        livres_data = [
            {
                'titre': "Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow",
                'isbn': '978-1492032649',
                'categorie': 'Machine Learning',
                'auteurs': ['Aurélien Géron'],
                'editeur': "O'Reilly Media",
                'annee': 2022,
                'pages': 856,
                'quantite': 5,
                'description': "Guide pratique du Machine Learning avec des exemples concrets en Python."
            },
            {
                'titre': "Deep Learning with Python",
                'isbn': '978-1617296864',
                'categorie': 'Deep Learning',
                'auteurs': ['François Chollet'],
                'editeur': 'Manning Publications',
                'annee': 2021,
                'pages': 504,
                'quantite': 4,
                'description': "Introduction au Deep Learning par le créateur de Keras."
            },
            {
                'titre': "Deep Learning",
                'isbn': '978-0262035613',
                'categorie': 'Deep Learning',
                'auteurs': ['Ian Goodfellow', 'Yoshua Bengio'],
                'editeur': 'MIT Press',
                'annee': 2016,
                'pages': 800,
                'quantite': 3,
                'description': "Le livre de référence sur le Deep Learning."
            },
            {
                'titre': "Python Data Science Handbook",
                'isbn': '978-1491912058',
                'categorie': 'Data Science',
                'auteurs': ['Jake VanderPlas'],
                'editeur': "O'Reilly Media",
                'annee': 2016,
                'pages': 548,
                'quantite': 6,
                'description': "Guide complet de la Data Science avec Python."
            },
            {
                'titre': "Python for Data Analysis",
                'isbn': '978-1491957660',
                'categorie': 'Data Science',
                'auteurs': ['Wes McKinney'],
                'editeur': "O'Reilly Media",
                'annee': 2017,
                'pages': 544,
                'quantite': 4,
                'description': "Analyse de données avec Pandas par son créateur."
            },
            {
                'titre': "Applied Cryptography",
                'isbn': '978-1119096726',
                'categorie': 'Cybersécurité',
                'auteurs': ['Bruce Schneier'],
                'editeur': 'Wiley',
                'annee': 2015,
                'pages': 1136,
                'quantite': 3,
                'description': "Protocoles et algorithmes de cryptographie."
            },
            {
                'titre': "Security Engineering",
                'isbn': '978-1119642787',
                'categorie': 'Cybersécurité',
                'auteurs': ['Ross Anderson'],
                'editeur': 'Wiley',
                'annee': 2020,
                'pages': 1232,
                'quantite': 2,
                'description': "Guide complet de la sécurité informatique."
            },
            {
                'titre': "R for Data Science",
                'isbn': '978-1491910399',
                'categorie': 'Statistiques',
                'auteurs': ['Hadley Wickham'],
                'editeur': "O'Reilly Media",
                'annee': 2017,
                'pages': 522,
                'quantite': 4,
                'description': "Introduction à la Data Science avec R."
            },
            {
                'titre': "Introduction to Algorithms",
                'isbn': '978-0262033848',
                'categorie': 'Algorithmique',
                'auteurs': ['Thomas Cormen'],
                'editeur': 'MIT Press',
                'annee': 2009,
                'pages': 1312,
                'quantite': 5,
                'description': "Le livre de référence sur les algorithmes."
            },
            {
                'titre': "Machine Learning Yearning",
                'isbn': '978-9999999999',
                'categorie': 'Machine Learning',
                'auteurs': ['Andrew Ng'],
                'editeur': 'Deeplearning.ai',
                'annee': 2018,
                'pages': 118,
                'quantite': 10,
                'description': "Guide pratique pour les projets ML."
            },
            {
                'titre': "Designing Data-Intensive Applications",
                'isbn': '978-1449373320',
                'categorie': 'Big Data',
                'auteurs': ['Martin Kleppmann'],
                'editeur': "O'Reilly Media",
                'annee': 2017,
                'pages': 616,
                'quantite': 4,
                'description': "Architecture des systèmes Big Data."
            },
            {
                'titre': "Pattern Recognition and Machine Learning",
                'isbn': '978-0387310732',
                'categorie': 'Intelligence Artificielle',
                'auteurs': ['Christopher Bishop'],
                'editeur': 'Springer',
                'annee': 2006,
                'pages': 738,
                'quantite': 3,
                'description': "Fondements mathématiques du ML."
            },
        ]
        
        livres = []
        for livre_data in livres_data:
            livre = Livre(
                titre=livre_data['titre'],
                isbn=livre_data['isbn'],
                categorie=livre_data['categorie'],
                editeur=livre_data['editeur'],
                annee_publication=livre_data['annee'],
                nombre_pages=livre_data['pages'],
                quantite_totale=livre_data['quantite'],
                quantite_disponible=livre_data['quantite'],
                description=livre_data['description']
            )
            
            for auteur_nom in livre_data['auteurs']:
                if auteur_nom in auteurs:
                    livre.auteurs.append(auteurs[auteur_nom])
            
            db.add(livre)
            livres.append(livre)
        
        db.flush()
        print(f"✅ {len(livres)} livres créés")
        
        # Commit final
        db.commit()
        
        print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║   ✅ BASE DE DONNÉES INITIALISÉE AVEC SUCCÈS !                       ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║                                                                      ║
    ║   📋 Identifiants de connexion:                                      ║
    ║                                                                      ║
    ║   🔑 Bibliothécaires:                                                ║
    ║      - Identifiant: admin      | Mot de passe: admin123              ║
    ║      - Identifiant: biblio1    | Mot de passe: biblio123             ║
    ║                                                                      ║
    ║   🔑 Étudiants:                                                      ║
    ║      - Email: [votre email @inphb.ci]                                ║
    ║      - Mot de passe: [votre matricule]                               ║
    ║                                                                      ║
    ║   📧 Exemple: tchewa.soro25@inphb.ci / 25INP00194                    ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
        """)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erreur: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()
