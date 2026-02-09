"""
Dashboard Étudiant Moderne
Système de Gestion de Bibliothèque - IDSI

Avec CustomTkinter, animations et gestion du profil
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from utils.theme import (
    COLORS, FONTS, DIMENSIONS, ICONS, APP_CONFIG, PROGRAMMES, NIVEAUX
)
from utils.components import (
    AnimatedButton, ModernCard, ModernTable, Sidebar, 
    SearchBar, StatCard, PasswordChangeDialog, ProfileEditDialog
)
from models.database import get_db
from models.models import Livre, Emprunt, Reservation, Auteur


class StudentDashboard(ctk.CTkFrame):
    """Dashboard principal pour les étudiants"""
    
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
            'home': {'text': 'Accueil', 'icon': ICONS['home']},
            'catalog': {'text': 'Catalogue', 'icon': ICONS['book']},
            'loans': {'text': 'Mes Emprunts', 'icon': ICONS['loan']},
            'profile': {'text': 'Mon Profil', 'icon': ICONS['user']},
            'settings': {'text': 'Paramètres', 'icon': ICONS['settings']},
        }
        
        user_info = {
            'name': f"{self.user.prenom} {self.user.nom}",
            'role': f"{self.user.filiere or 'Étudiant'}"
        }
        
        self.sidebar = Sidebar(self, nav_items, on_select=self._on_nav_select, user_info=user_info)
        self.sidebar.pack(side='left', fill='y')
        
        # Bouton déconnexion en bas de la sidebar
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
        
        # Zone de contenu principal
        self.content_area = ctk.CTkFrame(self, fg_color=COLORS['background'])
        self.content_area.pack(side='left', fill='both', expand=True)
        
        # Header
        self._create_header()
        
        # Main content container
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
        
        # Bienvenue
        welcome_frame = ctk.CTkFrame(header, fg_color='transparent')
        welcome_frame.pack(side='left', padx=30, pady=15)
        
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text=f"Bienvenue, {self.user.prenom} ! 👋",
            font=ctk.CTkFont(family=FONTS['family'], size=22, weight='bold'),
            text_color=COLORS['text_primary']
        )
        welcome_label.pack(side='left')
        
        # Info utilisateur à droite
        user_frame = ctk.CTkFrame(header, fg_color='transparent')
        user_frame.pack(side='right', padx=30, pady=15)
        
        # Badge matricule
        badge = ctk.CTkFrame(user_frame, fg_color=COLORS['primary'], corner_radius=20)
        badge.pack(side='right')
        
        ctk.CTkLabel(
            badge,
            text=f"  {ICONS['user']}  {self.user.matricule}  ",
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['white']
        ).pack(padx=10, pady=5)
    
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
        elif item_id == 'catalog':
            self._show_catalog()
        elif item_id == 'loans':
            self._show_loans()
        elif item_id == 'profile':
            self._show_profile()
        elif item_id == 'settings':
            self._show_settings()
    
    def _show_home(self):
        """Afficher la page d'accueil"""
        # Titre
        title_frame = ctk.CTkFrame(self.main_content, fg_color='transparent')
        title_frame.pack(fill='x', pady=(0, 25))
        
        ctk.CTkLabel(
            title_frame,
            text=f"{ICONS['home']}  Tableau de bord",
            font=ctk.CTkFont(family=FONTS['family'], size=26, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(side='left')
        
        # Récupérer les statistiques
        db = get_db()
        try:
            emprunts_en_cours = db.query(Emprunt).filter(
                Emprunt.etudiant_id == self.user.id,
                Emprunt.date_retour_effective.is_(None)
            ).count()
            
            emprunts = db.query(Emprunt).filter(
                Emprunt.etudiant_id == self.user.id,
                Emprunt.date_retour_effective.is_(None)
            ).all()
            emprunts_retard = sum(1 for e in emprunts if e.est_en_retard)
            
            penalites = sum(e.calculer_penalite() for e in emprunts if e.est_en_retard)
            
            total_emprunts = db.query(Emprunt).filter(
                Emprunt.etudiant_id == self.user.id
            ).count()
        except Exception as e:
            emprunts_en_cours = 0
            emprunts_retard = 0
            penalites = 0
            total_emprunts = 0
        finally:
            db.close()
        
        # Statistiques
        stats_frame = ctk.CTkFrame(self.main_content, fg_color='transparent')
        stats_frame.pack(fill='x', pady=(0, 25))
        
        stats = [
            ('Emprunts en cours', emprunts_en_cours, ICONS['book'], COLORS['primary']),
            ('En retard', emprunts_retard, ICONS['warning'], COLORS['danger']),
            ('Pénalités', f"{penalites:,.0f} FCFA", ICONS['info'], COLORS['secondary']),
            ('Total emprunts', total_emprunts, ICONS['chart'], COLORS['accent']),
        ]
        
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)
        
        for i, (title, value, icon, color) in enumerate(stats):
            stat_card = StatCard(stats_frame, title, value, icon, color)
            stat_card.grid(row=0, column=i, padx=8, pady=5, sticky='nsew')
        
        # Alerte si pénalités
        if penalites > 0:
            alert_frame = ctk.CTkFrame(
                self.main_content,
                fg_color='#FEF2F2',
                border_width=1,
                border_color=COLORS['danger'],
                corner_radius=DIMENSIONS['border_radius']
            )
            alert_frame.pack(fill='x', pady=(0, 25))
            
            ctk.CTkLabel(
                alert_frame,
                text=f"  {ICONS['warning']}  Attention : Vous avez {penalites:,.0f} FCFA de pénalités à régler",
                font=ctk.CTkFont(family=FONTS['family'], size=14, weight='bold'),
                text_color=COLORS['danger']
            ).pack(pady=15)
        
        # Section emprunts récents
        recent_card = ModernCard(self.main_content, title=f"{ICONS['clock']}  Emprunts récents")
        recent_card.pack(fill='both', expand=True)
        
        # Table des emprunts récents
        columns = {
            'livre': {'text': 'Livre', 'width': 300},
            'date_emprunt': {'text': 'Date emprunt', 'width': 150},
            'date_retour': {'text': 'À rendre le', 'width': 150},
            'statut': {'text': 'Statut', 'width': 120},
        }
        
        table = ModernTable(recent_card.content, columns)
        table.pack(fill='both', expand=True)
        
        db = get_db()
        try:
            emprunts = db.query(Emprunt).filter(
                Emprunt.etudiant_id == self.user.id
            ).order_by(Emprunt.date_emprunt.desc()).limit(5).all()
            
            for emprunt in emprunts:
                if emprunt.date_retour_effective:
                    statut = '✅ Retourné'
                elif emprunt.est_en_retard:
                    statut = '⚠️ En retard'
                else:
                    statut = '📖 En cours'
                
                livre_titre = emprunt.livre.titre if emprunt.livre else 'N/A'
                date_emprunt = emprunt.date_emprunt.strftime('%d/%m/%Y') if emprunt.date_emprunt else 'N/A'
                date_retour = emprunt.date_retour_prevue.strftime('%d/%m/%Y') if emprunt.date_retour_prevue else 'N/A'
                
                table.insert((livre_titre, date_emprunt, date_retour, statut))
        except Exception as e:
            print(f"Erreur chargement emprunts: {e}")
        finally:
            db.close()
    
    def _show_catalog(self):
        """Afficher le catalogue de livres"""
        # Header avec recherche
        header_frame = ctk.CTkFrame(self.main_content, fg_color='transparent')
        header_frame.pack(fill='x', pady=(0, 25))
        
        ctk.CTkLabel(
            header_frame,
            text=f"{ICONS['book']}  Catalogue des livres",
            font=ctk.CTkFont(family=FONTS['family'], size=26, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(side='left')
        
        # Barre de recherche
        search_frame = ctk.CTkFrame(self.main_content, fg_color='transparent')
        search_frame.pack(fill='x', pady=(0, 20))
        
        self.search_var = ctk.StringVar()
        search_bar = SearchBar(
            search_frame,
            placeholder="Rechercher un livre par titre, auteur ou catégorie...",
            on_search=self._search_books
        )
        search_bar.pack(fill='x')
        self.search_entry = search_bar
        
        # Table des livres
        columns = {
            'titre': {'text': 'Titre', 'width': 350},
            'auteurs': {'text': 'Auteur(s)', 'width': 200},
            'categorie': {'text': 'Catégorie', 'width': 180},
            'disponible': {'text': 'Disponible', 'width': 100},
        }
        
        self.books_table = ModernTable(self.main_content, columns)
        self.books_table.pack(fill='both', expand=True)
        
        self._load_books()
        
        # Bouton emprunter
        btn_frame = ctk.CTkFrame(self.main_content, fg_color='transparent')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        emprunt_btn = AnimatedButton(
            btn_frame,
            text="Emprunter le livre sélectionné",
            style='success',
            icon=ICONS['add'],
            command=self._emprunter_livre,
            width=280
        )
        emprunt_btn.pack(side='left')
    
    def _load_books(self, search_term=None):
        """Charger les livres dans la table"""
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
                disponible = "✅ Oui" if livre.quantite_disponible > 0 else "❌ Non"
                
                self.books_table.insert((
                    livre.titre,
                    auteurs,
                    livre.categorie or "N/A",
                    disponible
                ))
        except Exception as e:
            print(f"Erreur chargement livres: {e}")
        finally:
            db.close()
    
    def _search_books(self, search_term=None):
        """Rechercher des livres"""
        if search_term is None:
            search_term = self.search_entry.get()
        self._load_books(search_term if search_term else None)
    
    def _emprunter_livre(self):
        """Emprunter un livre sélectionné"""
        selected = self.books_table.get_selected()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un livre.")
            return
        
        titre = selected[0]
        disponible = selected[3]
        
        if "Non" in disponible:
            messagebox.showwarning("Indisponible", "Ce livre n'est pas disponible.")
            return
        
        db = get_db()
        try:
            livre = db.query(Livre).filter(Livre.titre == titre).first()
            
            if livre and livre.quantite_disponible > 0:
                # Vérifier le nombre max d'emprunts
                emprunts_en_cours = db.query(Emprunt).filter(
                    Emprunt.etudiant_id == self.user.id,
                    Emprunt.date_retour_effective.is_(None)
                ).count()
                
                if emprunts_en_cours >= APP_CONFIG['max_loans_per_student']:
                    messagebox.showwarning(
                        "Limite atteinte",
                        f"Vous avez atteint le nombre maximum d'emprunts ({APP_CONFIG['max_loans_per_student']})."
                    )
                    return
                
                # Créer l'emprunt
                emprunt = Emprunt(
                    etudiant_id=self.user.id,
                    livre_id=livre.id
                )
                livre.quantite_disponible -= 1
                
                db.add(emprunt)
                db.commit()
                
                messagebox.showinfo(
                    "Succès",
                    f"Vous avez emprunté '{titre}'.\n"
                    f"À rendre avant le {emprunt.date_retour_prevue.strftime('%d/%m/%Y')}"
                )
                
                self._load_books()
        except Exception as e:
            db.rollback()
            messagebox.showerror("Erreur", f"Erreur lors de l'emprunt: {e}")
        finally:
            db.close()
    
    def _show_loans(self):
        """Afficher les emprunts de l'étudiant"""
        ctk.CTkLabel(
            self.main_content,
            text=f"{ICONS['loan']}  Mes Emprunts",
            font=ctk.CTkFont(family=FONTS['family'], size=26, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(anchor='w', pady=(0, 25))
        
        # Table des emprunts
        columns = {
            'livre': {'text': 'Livre', 'width': 280},
            'date_emprunt': {'text': 'Date emprunt', 'width': 120},
            'date_retour': {'text': 'À rendre le', 'width': 120},
            'statut': {'text': 'Statut', 'width': 110},
            'penalite': {'text': 'Pénalité', 'width': 110},
        }
        
        self.loans_table = ModernTable(self.main_content, columns)
        self.loans_table.pack(fill='both', expand=True)
        
        db = get_db()
        try:
            emprunts = db.query(Emprunt).filter(
                Emprunt.etudiant_id == self.user.id
            ).order_by(Emprunt.date_emprunt.desc()).all()
            
            for emprunt in emprunts:
                if emprunt.date_retour_effective:
                    statut = '✅ Retourné'
                elif emprunt.est_en_retard:
                    statut = '⚠️ En retard'
                else:
                    statut = '📖 En cours'
                
                penalite = f"{emprunt.calculer_penalite():,.0f} FCFA"
                livre_titre = emprunt.livre.titre if emprunt.livre else 'N/A'
                
                self.loans_table.insert((
                    livre_titre,
                    emprunt.date_emprunt.strftime('%d/%m/%Y'),
                    emprunt.date_retour_prevue.strftime('%d/%m/%Y'),
                    statut,
                    penalite
                ))
        except Exception as e:
            print(f"Erreur: {e}")
        finally:
            db.close()
        
        # Résumé pénalités
        summary_card = ModernCard(self.main_content, title="💰 Résumé des pénalités")
        summary_card.pack(fill='x', pady=(25, 0))
        
        db = get_db()
        try:
            emprunts = db.query(Emprunt).filter(
                Emprunt.etudiant_id == self.user.id,
                Emprunt.date_retour_effective.is_(None)
            ).all()
            
            total_penalites = sum(e.calculer_penalite() for e in emprunts if e.est_en_retard)
        except:
            total_penalites = 0
        finally:
            db.close()
        
        color = COLORS['danger'] if total_penalites > 0 else COLORS['accent']
        
        ctk.CTkLabel(
            summary_card.content,
            text=f"Total pénalités en cours: {total_penalites:,.0f} FCFA",
            font=ctk.CTkFont(family=FONTS['family'], size=20, weight='bold'),
            text_color=color
        ).pack(pady=15)
    
    def _show_profile(self):
        """Afficher le profil de l'étudiant"""
        ctk.CTkLabel(
            self.main_content,
            text=f"{ICONS['user']}  Mon Profil",
            font=ctk.CTkFont(family=FONTS['family'], size=26, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(anchor='w', pady=(0, 25))
        
        # Carte profil
        profile_card = ModernCard(self.main_content)
        profile_card.pack(fill='x')
        
        # Avatar
        avatar_frame = ctk.CTkFrame(profile_card.content, fg_color='transparent')
        avatar_frame.pack(pady=20)
        
        avatar_bg = ctk.CTkFrame(
            avatar_frame,
            fg_color=COLORS['primary'],
            corner_radius=60,
            width=120,
            height=120
        )
        avatar_bg.pack()
        avatar_bg.pack_propagate(False)
        
        ctk.CTkLabel(
            avatar_bg,
            text="👤",
            font=ctk.CTkFont(size=50),
            text_color=COLORS['white']
        ).place(relx=0.5, rely=0.5, anchor='center')
        
        ctk.CTkLabel(
            avatar_frame,
            text=f"{self.user.prenom} {self.user.nom}",
            font=ctk.CTkFont(family=FONTS['family'], size=24, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(pady=(15, 5))
        
        # Badge programme
        ctk.CTkLabel(
            avatar_frame,
            text=f"🎓 {self.user.filiere or 'Étudiant IDSI'}",
            font=ctk.CTkFont(family=FONTS['family'], size=14),
            text_color=COLORS['secondary']
        ).pack()
        
        # Informations
        info_frame = ctk.CTkFrame(profile_card.content, fg_color='transparent')
        info_frame.pack(fill='x', pady=25, padx=50)
        
        infos = [
            (ICONS['user'], "Matricule", self.user.matricule),
            (ICONS['email'], "Email", self.user.email),
            (ICONS['graduation'], "Programme", self.user.filiere or "N/A"),
            (ICONS['certificate'], "Niveau", self.user.niveau or "N/A"),
            (ICONS['phone'], "Téléphone", self.user.telephone or "N/A"),
        ]
        
        for icon, label, value in infos:
            row = ctk.CTkFrame(info_frame, fg_color='transparent')
            row.pack(fill='x', pady=8)
            
            ctk.CTkLabel(
                row,
                text=f"{icon}  {label}:",
                font=ctk.CTkFont(family=FONTS['family'], size=14, weight='bold'),
                text_color=COLORS['text_secondary'],
                width=180,
                anchor='e'
            ).pack(side='left', padx=(0, 15))
            
            ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(family=FONTS['family'], size=14),
                text_color=COLORS['text_primary'],
                anchor='w'
            ).pack(side='left')
    
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
        
        # Bouton modifier le mot de passe
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
        info_card = ModernCard(self.main_content, title=f"{ICONS['info']}  À propos")
        info_card.pack(fill='x')
        
        about_text = f"""
        {APP_CONFIG['name']} - Version {APP_CONFIG['version']}
        
        {APP_CONFIG['institution']}
        {APP_CONFIG['description']}
        
        • Durée d'emprunt: {APP_CONFIG['loan_duration_days']} jours
        • Pénalité de retard: {APP_CONFIG['penalty_per_day']} {APP_CONFIG['currency']}/jour
        • Maximum d'emprunts: {APP_CONFIG['max_loans_per_student']} livres
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
        PasswordChangeDialog(self.parent, self.user, 'etudiant')
    
    def _open_profile_dialog(self):
        """Ouvrir le dialog de modification du profil"""
        ProfileEditDialog(
            self.parent, 
            self.user, 
            'etudiant',
            on_success=self._refresh_ui
        )
    
    def _refresh_ui(self):
        """Rafraîchir l'interface après modification"""
        # Recharger la vue courante
        self._on_nav_select(self.sidebar.active_item)
