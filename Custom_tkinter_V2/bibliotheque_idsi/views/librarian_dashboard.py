"""
Dashboard Bibliothécaire Moderne
Système de Gestion de Bibliothèque - IDSI

Avec CustomTkinter, animations et gestion du profil
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from utils.theme import (
    COLORS, FONTS, DIMENSIONS, ICONS, APP_CONFIG, 
    BOOK_CATEGORIES, PROGRAMMES, NIVEAUX
)
from utils.components import (
    AnimatedButton, ModernEntry, ModernCard, ModernTable, 
    Sidebar, SearchBar, StatCard, PasswordChangeDialog, ProfileEditDialog
)
from models.database import get_db
from models.models import Livre, Auteur, Etudiant, Bibliothecaire, Emprunt, Reservation


class LibrarianDashboard(ctk.CTkFrame):
    """Dashboard principal pour les bibliothécaires"""
    
    def __init__(self, parent, user, on_logout):
        super().__init__(parent, fg_color=COLORS['background'])
        self.parent = parent
        self.user = user
        self.on_logout = on_logout
        
        self._create_ui()
        self.sidebar.set_active('home')
        self._show_home()
    
    def _create_ui(self):
        # Sidebar avec info utilisateur
        nav_items = {
            'home': {'text': 'Tableau de bord', 'icon': ICONS['home']},
            'books': {'text': 'Gestion Livres', 'icon': ICONS['book']},
            'students': {'text': 'Étudiants', 'icon': ICONS['users']},
            'loans': {'text': 'Emprunts', 'icon': ICONS['loan']},
            'returns': {'text': 'Retours', 'icon': ICONS['return']},
            'settings': {'text': 'Paramètres', 'icon': ICONS['settings']},
        }
        
        user_info = {
            'name': f"{self.user.prenom} {self.user.nom}",
            'role': f"{self.user.role.upper()}"
        }
        
        self.sidebar = Sidebar(self, nav_items, on_select=self._on_nav_select, user_info=user_info)
        self.sidebar.pack(side='left', fill='y')
        
        # Bouton déconnexion
        logout_frame = ctk.CTkFrame(self.sidebar, fg_color='transparent')
        logout_frame.pack(side='bottom', fill='x', pady=20, padx=15)
        
        logout_btn = AnimatedButton(
            logout_frame,
            text="Déconnexion",
            style='danger',
            icon=ICONS['logout'],
            command=self._confirm_logout
        )
        logout_btn.pack(fill='x')
        
        # Zone de contenu
        self.content_area = ctk.CTkFrame(self, fg_color=COLORS['background'])
        self.content_area.pack(side='left', fill='both', expand=True)
        
        # Header
        self._create_header()
        
        # Main content
        self.main_content = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color=COLORS['background'],
            scrollbar_button_color=COLORS['primary'],
            scrollbar_button_hover_color=COLORS['primary_light']
        )
        self.main_content.pack(fill='both', expand=True, padx=30, pady=20)
    
    def _create_header(self):
        """Créer l'en-tête"""
        header = ctk.CTkFrame(self.content_area, fg_color=COLORS['surface'], height=70, corner_radius=0)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Titre admin
        admin_frame = ctk.CTkFrame(header, fg_color='transparent')
        admin_frame.pack(side='left', padx=30, pady=15)
        
        ctk.CTkLabel(
            admin_frame,
            text=f"Administration - {self.user.nom_complet}",
            font=ctk.CTkFont(family=FONTS['family'], size=22, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(side='left')
        
        # Badge admin
        badge = ctk.CTkFrame(admin_frame, fg_color=COLORS['secondary'], corner_radius=10)
        badge.pack(side='left', padx=15)
        
        ctk.CTkLabel(
            badge,
            text=f"  {self.user.role.upper()}  ",
            font=ctk.CTkFont(family=FONTS['family'], size=11, weight='bold'),
            text_color=COLORS['white']
        ).pack(padx=8, pady=4)
        
        # Date
        date_frame = ctk.CTkFrame(header, fg_color='transparent')
        date_frame.pack(side='right', padx=30, pady=15)
        
        ctk.CTkLabel(
            date_frame,
            text=f"{ICONS['calendar']}  {datetime.now().strftime('%d/%m/%Y')}",
            font=ctk.CTkFont(family=FONTS['family'], size=14),
            text_color=COLORS['text_secondary']
        ).pack()
    
    def _clear_content(self):
        """Effacer le contenu actuel"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def _confirm_logout(self):
        """Confirmer la déconnexion"""
        if messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter ?"):
            self.on_logout()
    
    def _on_nav_select(self, item_id):
        """Gérer la navigation"""
        self._clear_content()
        
        if item_id == 'home':
            self._show_home()
        elif item_id == 'books':
            self._show_books()
        elif item_id == 'students':
            self._show_students()
        elif item_id == 'loans':
            self._show_loans()
        elif item_id == 'returns':
            self._show_returns()
        elif item_id == 'settings':
            self._show_settings()
    
    def _show_home(self):
        """Afficher le tableau de bord"""
        ctk.CTkLabel(
            self.main_content,
            text=f"{ICONS['chart']}  Tableau de bord",
            font=ctk.CTkFont(family=FONTS['family'], size=26, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(anchor='w', pady=(0, 25))
        
        # Récupérer les statistiques
        db = get_db()
        try:
            total_livres = db.query(Livre).count()
            total_etudiants = db.query(Etudiant).count()
            emprunts_en_cours = db.query(Emprunt).filter(
                Emprunt.date_retour_effective.is_(None)
            ).count()
            emprunts = db.query(Emprunt).filter(
                Emprunt.date_retour_effective.is_(None)
            ).all()
            emprunts_retard = sum(1 for e in emprunts if e.est_en_retard)
        except:
            total_livres = 0
            total_etudiants = 0
            emprunts_en_cours = 0
            emprunts_retard = 0
        finally:
            db.close()
        
        # Statistiques
        stats_frame = ctk.CTkFrame(self.main_content, fg_color='transparent')
        stats_frame.pack(fill='x', pady=(0, 25))
        
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)
        
        stats = [
            ('Total Livres', total_livres, ICONS['book'], COLORS['primary']),
            ('Étudiants', total_etudiants, ICONS['users'], COLORS['info']),
            ('Emprunts en cours', emprunts_en_cours, ICONS['loan'], COLORS['secondary']),
            ('En retard', emprunts_retard, ICONS['warning'], COLORS['danger']),
        ]
        
        for i, (title, value, icon, color) in enumerate(stats):
            stat_card = StatCard(stats_frame, title, value, icon, color)
            stat_card.grid(row=0, column=i, padx=8, pady=5, sticky='nsew')
        
        # Section emprunts en retard
        retard_title = f"⚠️  Emprunts en retard ({emprunts_retard})" if emprunts_retard > 0 else "✅  Aucun emprunt en retard"
        retard_card = ModernCard(self.main_content, title=retard_title)
        retard_card.pack(fill='x', pady=(0, 20))
        
        if emprunts_retard > 0:
            columns = {
                'etudiant': {'text': 'Étudiant', 'width': 180},
                'livre': {'text': 'Livre', 'width': 280},
                'jours': {'text': 'Jours de retard', 'width': 120},
                'penalite': {'text': 'Pénalité', 'width': 120},
            }
            
            table = ModernTable(retard_card.content, columns, height=200)
            table.pack(fill='both', expand=True)
            
            db = get_db()
            try:
                emprunts = db.query(Emprunt).filter(
                    Emprunt.date_retour_effective.is_(None)
                ).all()
                
                for emprunt in emprunts:
                    if emprunt.est_en_retard:
                        table.insert((
                            emprunt.etudiant.matricule if emprunt.etudiant else 'N/A',
                            emprunt.livre.titre[:40] + '...' if emprunt.livre and len(emprunt.livre.titre) > 40 else (emprunt.livre.titre if emprunt.livre else 'N/A'),
                            f"{emprunt.jours_retard} jours",
                            f"{emprunt.calculer_penalite():,.0f} FCFA"
                        ))
            finally:
                db.close()
        else:
            ctk.CTkLabel(
                retard_card.content,
                text="🎉 Tous les emprunts sont dans les délais !",
                font=ctk.CTkFont(family=FONTS['family'], size=14),
                text_color=COLORS['accent']
            ).pack(pady=20)
        
        # Section emprunts récents
        recent_card = ModernCard(self.main_content, title="📖  Emprunts récents")
        recent_card.pack(fill='both', expand=True)
        
        columns_recent = {
            'etudiant': {'text': 'Étudiant', 'width': 150},
            'livre': {'text': 'Livre', 'width': 280},
            'date_emprunt': {'text': 'Date emprunt', 'width': 120},
            'date_retour': {'text': 'Retour prévu', 'width': 120},
            'statut': {'text': 'Statut', 'width': 100},
        }
        
        table_recent = ModernTable(recent_card.content, columns_recent, height=200)
        table_recent.pack(fill='both', expand=True)
        
        db = get_db()
        try:
            emprunts_recents = db.query(Emprunt).order_by(
                Emprunt.date_emprunt.desc()
            ).limit(10).all()
            
            for emprunt in emprunts_recents:
                if emprunt.date_retour_effective:
                    statut = '✅ Retourné'
                elif emprunt.est_en_retard:
                    statut = '⚠️ En retard'
                else:
                    statut = '📖 En cours'
                
                table_recent.insert((
                    emprunt.etudiant.matricule if emprunt.etudiant else 'N/A',
                    emprunt.livre.titre[:35] + '...' if emprunt.livre and len(emprunt.livre.titre) > 35 else (emprunt.livre.titre if emprunt.livre else 'N/A'),
                    emprunt.date_emprunt.strftime('%d/%m/%Y'),
                    emprunt.date_retour_prevue.strftime('%d/%m/%Y'),
                    statut
                ))
        except Exception as e:
            print(f"Erreur: {e}")
        finally:
            db.close()
    
    def _show_books(self):
        """Afficher la gestion des livres"""
        # Header
        header_frame = ctk.CTkFrame(self.main_content, fg_color='transparent')
        header_frame.pack(fill='x', pady=(0, 25))
        
        ctk.CTkLabel(
            header_frame,
            text=f"{ICONS['book']}  Gestion des Livres",
            font=ctk.CTkFont(family=FONTS['family'], size=26, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(side='left')
        
        # Boutons actions
        btn_frame = ctk.CTkFrame(header_frame, fg_color='transparent')
        btn_frame.pack(side='right')
        
        AnimatedButton(
            btn_frame,
            text="Ajouter un livre",
            style='success',
            icon=ICONS['add'],
            command=self._show_add_book_modal,
            width=180
        ).pack(side='left', padx=5)
        
        AnimatedButton(
            btn_frame,
            text="Supprimer",
            style='danger',
            icon=ICONS['delete'],
            command=self._delete_book,
            width=140
        ).pack(side='left', padx=5)
        
        # Recherche
        search_frame = ctk.CTkFrame(self.main_content, fg_color='transparent')
        search_frame.pack(fill='x', pady=(0, 20))
        
        self.book_search = SearchBar(
            search_frame,
            placeholder="Rechercher un livre...",
            on_search=self._search_books_admin
        )
        self.book_search.pack(fill='x')
        
        # Table des livres
        columns = {
            'id': {'text': 'ID', 'width': 50},
            'titre': {'text': 'Titre', 'width': 300},
            'auteurs': {'text': 'Auteur(s)', 'width': 180},
            'categorie': {'text': 'Catégorie', 'width': 150},
            'quantite': {'text': 'Qté dispo', 'width': 90},
        }
        
        self.books_table = ModernTable(self.main_content, columns)
        self.books_table.pack(fill='both', expand=True)
        
        self._load_books()
    
    def _load_books(self, search_term=None):
        """Charger les livres"""
        self.books_table.clear()
        
        db = get_db()
        try:
            query = db.query(Livre)
            
            if search_term:
                search_term = f"%{search_term}%"
                query = query.filter(
                    Livre.titre.ilike(search_term) |
                    Livre.categorie.ilike(search_term)
                )
            
            livres = query.all()
            
            for livre in livres:
                auteurs = ", ".join([a.nom_complet for a in livre.auteurs]) if livre.auteurs else "N/A"
                qte = f"{livre.quantite_disponible}/{livre.quantite_totale}"
                
                self.books_table.insert((
                    livre.id,
                    livre.titre,
                    auteurs,
                    livre.categorie or "N/A",
                    qte
                ))
        finally:
            db.close()
    
    def _search_books_admin(self, search_term):
        """Rechercher des livres (admin)"""
        self._load_books(search_term if search_term else None)
    
    def _show_add_book_modal(self):
        """Afficher le modal d'ajout de livre"""
        modal = ctk.CTkToplevel(self.parent)
        modal.title("Ajouter un livre")
        modal.geometry("550x700")
        modal.resizable(False, False)
        modal.transient(self.parent)
        modal.grab_set()
        
        # Container principal
        main_frame = ctk.CTkScrollableFrame(modal, fg_color=COLORS['surface'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Titre
        ctk.CTkLabel(
            main_frame,
            text=f"{ICONS['add']}  Nouveau Livre",
            font=ctk.CTkFont(family=FONTS['family'], size=22, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(pady=(0, 25))
        
        # Champs
        fields = {}
        
        # Titre
        ctk.CTkLabel(main_frame, text="Titre *", font=ctk.CTkFont(size=13), text_color=COLORS['text_secondary']).pack(anchor='w')
        fields['titre'] = ModernEntry(main_frame, placeholder="Titre du livre", width=480)
        fields['titre'].pack(pady=(5, 15))
        
        # ISBN
        ctk.CTkLabel(main_frame, text="ISBN", font=ctk.CTkFont(size=13), text_color=COLORS['text_secondary']).pack(anchor='w')
        fields['isbn'] = ModernEntry(main_frame, placeholder="978-...", width=480)
        fields['isbn'].pack(pady=(5, 15))
        
        # Auteur
        ctk.CTkLabel(main_frame, text="Auteur *", font=ctk.CTkFont(size=13), text_color=COLORS['text_secondary']).pack(anchor='w')
        fields['auteur'] = ModernEntry(main_frame, placeholder="Prénom Nom", width=480)
        fields['auteur'].pack(pady=(5, 15))
        
        # Catégorie
        ctk.CTkLabel(main_frame, text="Catégorie", font=ctk.CTkFont(size=13), text_color=COLORS['text_secondary']).pack(anchor='w')
        fields['categorie'] = ctk.CTkComboBox(
            main_frame,
            values=BOOK_CATEGORIES,
            font=ctk.CTkFont(family=FONTS['family'], size=14),
            width=480,
            height=40,
            dropdown_font=ctk.CTkFont(family=FONTS['family'], size=13)
        )
        fields['categorie'].pack(pady=(5, 15))
        
        # Éditeur
        ctk.CTkLabel(main_frame, text="Éditeur", font=ctk.CTkFont(size=13), text_color=COLORS['text_secondary']).pack(anchor='w')
        fields['editeur'] = ModernEntry(main_frame, placeholder="Nom de l'éditeur", width=480)
        fields['editeur'].pack(pady=(5, 15))
        
        # Année et Quantité sur la même ligne
        row_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        row_frame.pack(fill='x', pady=(0, 15))
        
        # Année
        left_col = ctk.CTkFrame(row_frame, fg_color='transparent')
        left_col.pack(side='left', fill='x', expand=True, padx=(0, 10))
        ctk.CTkLabel(left_col, text="Année", font=ctk.CTkFont(size=13), text_color=COLORS['text_secondary']).pack(anchor='w')
        fields['annee'] = ModernEntry(left_col, placeholder="2024", width=220)
        fields['annee'].pack(pady=(5, 0))
        
        # Quantité
        right_col = ctk.CTkFrame(row_frame, fg_color='transparent')
        right_col.pack(side='left', fill='x', expand=True, padx=(10, 0))
        ctk.CTkLabel(right_col, text="Quantité", font=ctk.CTkFont(size=13), text_color=COLORS['text_secondary']).pack(anchor='w')
        fields['quantite'] = ModernEntry(right_col, placeholder="1", width=220)
        fields['quantite'].pack(pady=(5, 0))
        
        # Description
        ctk.CTkLabel(main_frame, text="Description", font=ctk.CTkFont(size=13), text_color=COLORS['text_secondary']).pack(anchor='w')
        fields['description'] = ctk.CTkTextbox(
            main_frame,
            height=80,
            width=480,
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            fg_color=COLORS['white'],
            border_width=2,
            border_color=COLORS['border']
        )
        fields['description'].pack(pady=(5, 20))
        
        def save_book():
            titre = fields['titre'].get().strip()
            auteur = fields['auteur'].get().strip()
            
            if not titre:
                messagebox.showerror("Erreur", "Le titre est obligatoire.")
                return
            
            if not auteur:
                messagebox.showerror("Erreur", "L'auteur est obligatoire.")
                return
            
            db = get_db()
            try:
                # Créer ou récupérer l'auteur
                parts = auteur.split(' ', 1)
                prenom = parts[0] if len(parts) > 0 else ''
                nom = parts[1] if len(parts) > 1 else parts[0]
                
                auteur_obj = db.query(Auteur).filter(
                    Auteur.nom == nom,
                    Auteur.prenom == prenom
                ).first()
                
                if not auteur_obj:
                    auteur_obj = Auteur(nom=nom, prenom=prenom)
                    db.add(auteur_obj)
                    db.flush()
                
                # Créer le livre
                try:
                    quantite = int(fields['quantite'].get() or 1)
                except:
                    quantite = 1
                
                try:
                    annee = int(fields['annee'].get()) if fields['annee'].get() else None
                except:
                    annee = None
                
                livre = Livre(
                    titre=titre,
                    isbn=fields['isbn'].get().strip() or None,
                    categorie=fields['categorie'].get(),
                    editeur=fields['editeur'].get().strip() or None,
                    annee_publication=annee,
                    quantite_totale=quantite,
                    quantite_disponible=quantite,
                    description=fields['description'].get("1.0", "end-1c").strip() or None
                )
                
                livre.auteurs.append(auteur_obj)
                
                db.add(livre)
                db.commit()
                
                messagebox.showinfo("Succès", f"Le livre '{titre}' a été ajouté.")
                modal.destroy()
                self._load_books()
            except Exception as e:
                db.rollback()
                messagebox.showerror("Erreur", f"Erreur: {e}")
            finally:
                db.close()
        
        # Boutons
        btn_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        btn_frame.pack(fill='x', pady=(10, 0))
        
        AnimatedButton(
            btn_frame,
            text="Annuler",
            style='outline',
            command=modal.destroy,
            width=150
        ).pack(side='left')
        
        AnimatedButton(
            btn_frame,
            text="Enregistrer",
            style='success',
            icon=ICONS['check'],
            command=save_book,
            width=180
        ).pack(side='right')
    
    def _delete_book(self):
        """Supprimer un livre"""
        selected = self.books_table.get_selected()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un livre.")
            return
        
        livre_id = selected[0]
        titre = selected[1]
        
        if messagebox.askyesno("Confirmation", f"Supprimer le livre '{titre}' ?"):
            db = get_db()
            try:
                livre = db.query(Livre).filter(Livre.id == livre_id).first()
                if livre:
                    db.delete(livre)
                    db.commit()
                    messagebox.showinfo("Succès", "Livre supprimé.")
                    self._load_books()
            except Exception as e:
                db.rollback()
                messagebox.showerror("Erreur", f"Erreur: {e}")
            finally:
                db.close()
    
    def _show_students(self):
        """Afficher la liste des étudiants"""
        # Header avec compteur
        header_frame = ctk.CTkFrame(self.main_content, fg_color='transparent')
        header_frame.pack(fill='x', pady=(0, 20))
        
        db = get_db()
        try:
            total_etudiants = db.query(Etudiant).count()
        except:
            total_etudiants = 0
        finally:
            db.close()
        
        ctk.CTkLabel(
            header_frame,
            text=f"{ICONS['users']}  Gestion des Étudiants ({total_etudiants})",
            font=ctk.CTkFont(family=FONTS['family'], size=26, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(side='left')
        
        # Barre de recherche
        search_frame = ctk.CTkFrame(self.main_content, fg_color='transparent')
        search_frame.pack(fill='x', pady=(0, 15))
        
        self.student_search = SearchBar(
            search_frame,
            placeholder="Rechercher un étudiant par nom, matricule ou filière...",
            on_search=self._search_students
        )
        self.student_search.pack(fill='x')
        
        columns = {
            'matricule': {'text': 'Matricule', 'width': 120},
            'nom': {'text': 'Nom', 'width': 150},
            'prenom': {'text': 'Prénom', 'width': 200},
            'programme': {'text': 'Programme', 'width': 320},
            'niveau': {'text': 'Niveau', 'width': 100},
        }
        
        # Table avec hauteur de 450px pour voir plus d'étudiants
        self.students_table = ModernTable(self.main_content, columns, height=450)
        self.students_table.pack(fill='both', expand=True)
        
        self._load_students()
    
    def _load_students(self, search_term=None):
        """Charger les étudiants dans la table"""
        self.students_table.clear()
        
        db = get_db()
        try:
            query = db.query(Etudiant)
            
            if search_term:
                search_term = f"%{search_term}%"
                query = query.filter(
                    Etudiant.nom.ilike(search_term) |
                    Etudiant.prenom.ilike(search_term) |
                    Etudiant.matricule.ilike(search_term) |
                    Etudiant.filiere.ilike(search_term)
                )
            
            etudiants = query.order_by(Etudiant.nom).all()
            
            for etudiant in etudiants:
                # Raccourcir le nom de la filière pour l'affichage
                filiere = etudiant.filiere or "N/A"
                if len(filiere) > 45:
                    filiere = filiere[:42] + "..."
                
                self.students_table.insert((
                    etudiant.matricule,
                    etudiant.nom,
                    etudiant.prenom,
                    filiere,
                    etudiant.niveau or "N/A"
                ))
        except Exception as e:
            print(f"Erreur chargement étudiants: {e}")
        finally:
            db.close()
    
    def _search_students(self, search_term):
        """Rechercher des étudiants"""
        self._load_students(search_term if search_term else None)
    
    def _show_loans(self):
        """Afficher tous les emprunts"""
        ctk.CTkLabel(
            self.main_content,
            text=f"{ICONS['loan']}  Tous les Emprunts",
            font=ctk.CTkFont(family=FONTS['family'], size=26, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(anchor='w', pady=(0, 25))
        
        columns = {
            'id': {'text': 'ID', 'width': 50},
            'etudiant': {'text': 'Étudiant', 'width': 150},
            'livre': {'text': 'Livre', 'width': 230},
            'date_emprunt': {'text': 'Date emprunt', 'width': 110},
            'date_retour': {'text': 'Retour prévu', 'width': 110},
            'statut': {'text': 'Statut', 'width': 100},
        }
        
        table = ModernTable(self.main_content, columns)
        table.pack(fill='both', expand=True)
        
        db = get_db()
        try:
            emprunts = db.query(Emprunt).order_by(Emprunt.date_emprunt.desc()).all()
            for emprunt in emprunts:
                if emprunt.date_retour_effective:
                    statut = '✅ Retourné'
                elif emprunt.est_en_retard:
                    statut = '⚠️ En retard'
                else:
                    statut = '📖 En cours'
                
                table.insert((
                    emprunt.id,
                    emprunt.etudiant.matricule if emprunt.etudiant else 'N/A',
                    emprunt.livre.titre if emprunt.livre else 'N/A',
                    emprunt.date_emprunt.strftime('%d/%m/%Y'),
                    emprunt.date_retour_prevue.strftime('%d/%m/%Y'),
                    statut
                ))
        finally:
            db.close()
    
    def _show_returns(self):
        """Gérer les retours de livres"""
        ctk.CTkLabel(
            self.main_content,
            text=f"{ICONS['return']}  Retours de Livres",
            font=ctk.CTkFont(family=FONTS['family'], size=26, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(anchor='w', pady=(0, 25))
        
        columns = {
            'id': {'text': 'ID', 'width': 50},
            'etudiant': {'text': 'Étudiant', 'width': 150},
            'livre': {'text': 'Livre', 'width': 230},
            'date_retour': {'text': 'Retour prévu', 'width': 110},
            'retard': {'text': 'Retard', 'width': 100},
            'penalite': {'text': 'Pénalité', 'width': 100},
        }
        
        self.returns_table = ModernTable(self.main_content, columns)
        self.returns_table.pack(fill='both', expand=True)
        
        self._load_returns()
        
        # Bouton retourner
        btn_frame = ctk.CTkFrame(self.main_content, fg_color='transparent')
        btn_frame.pack(fill='x', pady=(25, 0))
        
        AnimatedButton(
            btn_frame,
            text="Enregistrer le retour",
            style='success',
            icon=ICONS['check'],
            command=self._process_return,
            width=220
        ).pack(side='left')
    
    def _load_returns(self):
        """Charger les emprunts en cours pour retour"""
        self.returns_table.clear()
        
        db = get_db()
        try:
            emprunts = db.query(Emprunt).filter(
                Emprunt.date_retour_effective.is_(None)
            ).all()
            
            for emprunt in emprunts:
                retard = f"⚠️ {emprunt.jours_retard} jours" if emprunt.est_en_retard else "✅ Aucun"
                penalite = f"{emprunt.calculer_penalite():,.0f} FCFA"
                
                self.returns_table.insert((
                    emprunt.id,
                    emprunt.etudiant.matricule if emprunt.etudiant else 'N/A',
                    emprunt.livre.titre if emprunt.livre else 'N/A',
                    emprunt.date_retour_prevue.strftime('%d/%m/%Y'),
                    retard,
                    penalite
                ))
        finally:
            db.close()
    
    def _process_return(self):
        """Traiter un retour de livre"""
        selected = self.returns_table.get_selected()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un emprunt.")
            return
        
        emprunt_id = selected[0]
        
        db = get_db()
        try:
            emprunt = db.query(Emprunt).filter(Emprunt.id == emprunt_id).first()
            if emprunt:
                emprunt.retourner()
                db.commit()
                
                penalite = emprunt.penalite
                if penalite > 0:
                    messagebox.showinfo(
                        "Retour enregistré",
                        f"Retour enregistré avec succès.\nPénalité: {penalite:,.0f} FCFA"
                    )
                else:
                    messagebox.showinfo("Succès", "Retour enregistré avec succès.")
                
                self._load_returns()
        except Exception as e:
            db.rollback()
            messagebox.showerror("Erreur", f"Erreur: {e}")
        finally:
            db.close()
    
    def _show_settings(self):
        """Afficher les paramètres"""
        ctk.CTkLabel(
            self.main_content,
            text=f"{ICONS['settings']}  Paramètres",
            font=ctk.CTkFont(family=FONTS['family'], size=26, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(anchor='w', pady=(0, 25))
        
        # Carte sécurité
        security_card = ModernCard(self.main_content, title=f"{ICONS['lock']}  Sécurité du compte")
        security_card.pack(fill='x', pady=(0, 20))
        
        ctk.CTkLabel(
            security_card.content,
            text="Gérez vos informations de connexion et la sécurité de votre compte.",
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['text_secondary']
        ).pack(anchor='w', pady=(0, 20))
        
        AnimatedButton(
            security_card.content,
            text="Modifier le mot de passe",
            style='primary',
            icon=ICONS['key'],
            command=self._open_password_dialog,
            width=250
        ).pack(anchor='w')
        
        # Carte profil
        profile_card = ModernCard(self.main_content, title=f"{ICONS['edit']}  Modifier le profil")
        profile_card.pack(fill='x', pady=(0, 20))
        
        ctk.CTkLabel(
            profile_card.content,
            text="Mettez à jour vos informations personnelles.",
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['text_secondary']
        ).pack(anchor='w', pady=(0, 20))
        
        AnimatedButton(
            profile_card.content,
            text="Modifier mes informations",
            style='secondary',
            icon=ICONS['edit'],
            command=self._open_profile_dialog,
            width=250
        ).pack(anchor='w')
        
        # Informations système
        info_card = ModernCard(self.main_content, title=f"{ICONS['info']}  À propos du système")
        info_card.pack(fill='x')
        
        about_text = f"""
        {APP_CONFIG['name']} - Version {APP_CONFIG['version']}
        
        {APP_CONFIG['institution']}
        {APP_CONFIG['description']}
        
        Configuration:
        • Durée d'emprunt: {APP_CONFIG['loan_duration_days']} jours
        • Pénalité de retard: {APP_CONFIG['penalty_per_day']} {APP_CONFIG['currency']}/jour
        • Maximum d'emprunts par étudiant: {APP_CONFIG['max_loans_per_student']} livres
        • Durée de réservation: {APP_CONFIG['reservation_duration_days']} jours
        """
        
        ctk.CTkLabel(
            info_card.content,
            text=about_text,
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['text_secondary'],
            justify='left'
        ).pack(anchor='w')
    
    def _open_password_dialog(self):
        """Ouvrir le dialog de changement de mot de passe"""
        PasswordChangeDialog(self.parent, self.user, 'bibliothecaire')
    
    def _open_profile_dialog(self):
        """Ouvrir le dialog de modification du profil"""
        ProfileEditDialog(
            self.parent, 
            self.user, 
            'bibliothecaire',
            on_success=self._refresh_ui
        )
    
    def _refresh_ui(self):
        """Rafraîchir l'interface après modification"""
        self._on_nav_select(self.sidebar.active_item)
