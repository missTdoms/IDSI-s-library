"""
Page de connexion moderne
Système de Gestion de Bibliothèque - IDSI

Avec image de fond, animations et design glassmorphism
"""

import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import os
from utils.theme import (
    COLORS, FONTS, DIMENSIONS, ICONS, APP_CONFIG,
    BACKGROUND_IMAGE, MESSAGES
)
from utils.components import ModernEntry, AnimatedButton
from models.database import get_db
from models.models import Etudiant, Bibliothecaire


class LoginView(ctk.CTkFrame):
    """Page de connexion moderne avec image de fond"""
    
    def __init__(self, parent, on_login_success):
        super().__init__(parent, fg_color=COLORS['dark'])
        self.parent = parent
        self.on_login_success = on_login_success
        
        self._bg_image = None
        self._bg_photo = None
        
        self._create_ui()
        self.bind('<Configure>', self._on_resize)
    
    def _load_background(self, width, height):
        """Charger et traiter l'image de fond"""
        try:
            if os.path.exists(BACKGROUND_IMAGE) and width > 1 and height > 1:
                img = Image.open(BACKGROUND_IMAGE)
                
                # Redimensionner pour couvrir
                img_ratio = img.width / img.height
                frame_ratio = width / height
                
                if frame_ratio > img_ratio:
                    new_width = width
                    new_height = int(width / img_ratio)
                else:
                    new_height = height
                    new_width = int(height * img_ratio)
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Centrer et découper
                left = (new_width - width) // 2
                top = (new_height - height) // 2
                img = img.crop((left, top, left + width, top + height))
                
                # Appliquer un léger flou
                img = img.filter(ImageFilter.GaussianBlur(radius=2))
                
                # Assombrir
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(0.4)
                
                self._bg_image = img
                self._bg_photo = ImageTk.PhotoImage(img)
                
                self.bg_label.configure(image=self._bg_photo)
        except Exception as e:
            print(f"Erreur chargement image: {e}")
    
    def _on_resize(self, event):
        """Gérer le redimensionnement"""
        self.after(100, lambda: self._load_background(event.width, event.height))
    
    def _create_ui(self):
        # Label pour l'image de fond
        self.bg_label = ctk.CTkLabel(self, text='', fg_color=COLORS['dark'])
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Container principal centré
        main_container = ctk.CTkFrame(self, fg_color='transparent')
        main_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Carte de connexion (glassmorphism effect)
        login_card = ctk.CTkFrame(
            main_container,
            fg_color=('#FFFFFF', '#1E293B'),
            corner_radius=20,
            border_width=1,
            border_color=COLORS['border']
        )
        login_card.pack(padx=40, pady=40)
        
        # Contenu de la carte
        content = ctk.CTkFrame(login_card, fg_color='transparent')
        content.pack(padx=50, pady=50)
        
        # Logo et titre
        logo_frame = ctk.CTkFrame(content, fg_color='transparent')
        logo_frame.pack(pady=(0, 10))
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="📚",
            font=ctk.CTkFont(size=60)
        )
        logo_label.pack()
        
        title_label = ctk.CTkLabel(
            content,
            text=APP_CONFIG['name'],
            font=ctk.CTkFont(family=FONTS['family'], size=28, weight='bold'),
            text_color=COLORS['primary']
        )
        title_label.pack()
        
        # Sous-titre IDSI
        subtitle_label = ctk.CTkLabel(
            content,
            text=APP_CONFIG['institution'],
            font=ctk.CTkFont(family=FONTS['family'], size=12),
            text_color=COLORS['text_secondary']
        )
        subtitle_label.pack(pady=(5, 5))
        
        # Description
        desc_label = ctk.CTkLabel(
            content,
            text="Data Science • Big Data • IA • Cybersécurité",
            font=ctk.CTkFont(family=FONTS['family'], size=11),
            text_color=COLORS['secondary']
        )
        desc_label.pack(pady=(0, 30))
        
        # Sélection du type d'utilisateur
        user_type_frame = ctk.CTkFrame(content, fg_color='transparent')
        user_type_frame.pack(pady=(0, 20))
        
        self.user_type = ctk.StringVar(value='etudiant')
        
        student_radio = ctk.CTkRadioButton(
            user_type_frame,
            text="  Étudiant",
            variable=self.user_type,
            value='etudiant',
            font=ctk.CTkFont(family=FONTS['family'], size=14),
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_light'],
            command=self._on_user_type_change
        )
        student_radio.pack(side='left', padx=20)
        
        librarian_radio = ctk.CTkRadioButton(
            user_type_frame,
            text="  Bibliothécaire",
            variable=self.user_type,
            value='bibliothecaire',
            font=ctk.CTkFont(family=FONTS['family'], size=14),
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_light'],
            command=self._on_user_type_change
        )
        librarian_radio.pack(side='left', padx=20)
        
        # Champs de saisie
        fields_frame = ctk.CTkFrame(content, fg_color='transparent')
        fields_frame.pack(fill='x')
        
        # Identifiant (Email pour étudiants, Identifiant pour bibliothécaires)
        self.id_label = ctk.CTkLabel(
            fields_frame,
            text=f"{ICONS['email']}  Email",
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        self.id_label.pack(fill='x', pady=(0, 5))
        
        self.id_entry = ModernEntry(
            fields_frame,
            placeholder="Entrez votre email @inphb.ci",
            width=350
        )
        self.id_entry.pack(pady=(0, 20))
        
        # Mot de passe
        pwd_label = ctk.CTkLabel(
            fields_frame,
            text=f"{ICONS['lock']}  Mot de passe",
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        pwd_label.pack(fill='x', pady=(0, 5))
        
        self.pwd_entry = ModernEntry(
            fields_frame,
            placeholder="Entrez votre mot de passe",
            show="•",
            width=350
        )
        self.pwd_entry.pack(pady=(0, 10))
        
        # Message d'erreur (caché par défaut)
        self.error_label = ctk.CTkLabel(
            content,
            text="",
            font=ctk.CTkFont(family=FONTS['family'], size=12),
            text_color=COLORS['danger']
        )
        self.error_label.pack(pady=(5, 10))
        
        # Bouton de connexion
        self.login_btn = AnimatedButton(
            content,
            text="Se connecter",
            style='primary',
            icon=ICONS['unlock'],
            command=self._on_login,
            width=350,
            height=50
        )
        self.login_btn.pack(pady=(10, 20))
        
        # Bind Enter key
        self.pwd_entry.bind('<Return>', lambda e: self._on_login())
        self.id_entry.bind('<Return>', lambda e: self.pwd_entry.focus())
        
        # Footer
        footer_label = ctk.CTkLabel(
            content,
            text=f"Version {APP_CONFIG['version']} • SORO & TRAORE 2025-2026 IDSI",
            font=ctk.CTkFont(family=FONTS['family'], size=10),
            text_color=COLORS['text_disabled']
        )
        footer_label.pack()
    
    def _on_user_type_change(self):
        """Mettre à jour le label selon le type d'utilisateur"""
        if self.user_type.get() == 'etudiant':
            self.id_label.configure(text=f"{ICONS['email']}  Email")
            self.id_entry.configure(placeholder_text="Entrez votre email @inphb.ci")
        else:
            self.id_label.configure(text=f"{ICONS['user']}  Identifiant")
            self.id_entry.configure(placeholder_text="Entrez votre identifiant")
    
    def _show_error(self, message):
        """Afficher un message d'erreur"""
        self.error_label.configure(text=message)
        
        # Animation de shake
        original_x = 0.5
        shake_distance = 0.01
        
        def shake(count=0):
            if count < 6:
                offset = shake_distance if count % 2 == 0 else -shake_distance
                self.after(50, lambda: shake(count + 1))
    
    def _on_login(self):
        """Gérer la connexion"""
        identifier = self.id_entry.get().strip()
        password = self.pwd_entry.get()
        user_type = self.user_type.get()
        
        # Validation
        if not identifier:
            self._show_error("Veuillez entrer votre identifiant")
            return
        
        if not password:
            self._show_error("Veuillez entrer votre mot de passe")
            return
        
        # Vérification en base de données
        db = get_db()
        try:
            if user_type == 'etudiant':
                # Pour les étudiants: identifier par email, mot de passe = matricule
                user = db.query(Etudiant).filter(
                    Etudiant.email == identifier
                ).first()
            else:
                # Pour les bibliothécaires: identifier par identifiant
                user = db.query(Bibliothecaire).filter(
                    Bibliothecaire.identifiant == identifier
                ).first()
            
            if user and user.verify_password(password):
                if hasattr(user, 'actif') and not user.actif:
                    self._show_error("Ce compte est désactivé")
                    return
                
                # Connexion réussie
                self.error_label.configure(text="")
                self.on_login_success(user, user_type)
            else:
                self._show_error(MESSAGES['login_error'])
                
        except Exception as e:
            self._show_error(f"Erreur de connexion: {str(e)}")
        finally:
            db.close()
