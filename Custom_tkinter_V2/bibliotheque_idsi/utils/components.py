"""
Composants UI modernes pour CustomTkinter
Système de Gestion de Bibliothèque - IDSI

Avec animations et effets visuels
"""

import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import os
from utils.theme import (
    COLORS, FONTS, DIMENSIONS, BUTTON_STYLES, ICONS,
    ANIMATIONS, BACKGROUND_IMAGE
)


class AnimatedButton(ctk.CTkButton):
    """Bouton moderne avec animation au survol"""
    
    def __init__(self, parent, text, command=None, style='primary', icon=None, **kwargs):
        style_config = BUTTON_STYLES.get(style, BUTTON_STYLES['primary'])
        
        # Préparer le texte avec icône
        display_text = f"{icon}  {text}" if icon else text
        
        # Retirer height des kwargs si présent pour éviter le doublon
        height = kwargs.pop('height', DIMENSIONS['button_height'])
        
        super().__init__(
            parent,
            text=display_text,
            command=command,
            font=ctk.CTkFont(family=FONTS['family'], size=14, weight='bold'),
            fg_color=style_config['fg_color'],
            hover_color=style_config['hover_color'],
            text_color=style_config['text_color'],
            border_width=style_config.get('border_width', 0),
            border_color=style_config.get('border_color', COLORS['primary']),
            corner_radius=DIMENSIONS['border_radius'],
            height=height,
            **kwargs
        )
        
        self._original_fg = style_config['fg_color']
        self._hover_fg = style_config['hover_color']


class ModernEntry(ctk.CTkEntry):
    """Champ de saisie moderne avec placeholder"""
    
    def __init__(self, parent, placeholder='', show=None, width=300, **kwargs):
        super().__init__(
            parent,
            placeholder_text=placeholder,
            show=show,
            width=width,
            height=DIMENSIONS['input_height'],
            font=ctk.CTkFont(family=FONTS['family'], size=14),
            fg_color=COLORS['white'],
            border_color=COLORS['border'],
            border_width=2,
            corner_radius=DIMENSIONS['border_radius_sm'],
            text_color=COLORS['text_primary'],
            placeholder_text_color=COLORS['text_disabled'],
            **kwargs
        )
        
        # Animation de focus
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)
    
    def _on_focus_in(self, event):
        self.configure(border_color=COLORS['primary'])
    
    def _on_focus_out(self, event):
        self.configure(border_color=COLORS['border'])


class ModernCard(ctk.CTkFrame):
    """Carte moderne avec ombre et bordures arrondies"""
    
    def __init__(self, parent, title=None, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS['surface'],
            border_width=1,
            border_color=COLORS['border'],
            corner_radius=DIMENSIONS['border_radius'],
            **kwargs
        )
        
        # Titre optionnel
        if title:
            self.title_frame = ctk.CTkFrame(self, fg_color='transparent')
            self.title_frame.pack(fill='x', padx=20, pady=(15, 10))
            
            self.title_label = ctk.CTkLabel(
                self.title_frame,
                text=title,
                font=ctk.CTkFont(family=FONTS['family'], size=18, weight='bold'),
                text_color=COLORS['text_primary']
            )
            self.title_label.pack(side='left')
        
        # Container pour le contenu
        self.content = ctk.CTkFrame(self, fg_color='transparent')
        self.content.pack(fill='both', expand=True, padx=20, pady=15)


class ModernTable(ctk.CTkFrame):
    """Tableau moderne avec scrollbar"""
    
    def __init__(self, parent, columns, height=400, **kwargs):
        super().__init__(parent, fg_color=COLORS['surface'], corner_radius=DIMENSIONS['border_radius'])
        
        self.columns = columns
        self.rows = []
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color=COLORS['primary'], corner_radius=0)
        self.header_frame.pack(fill='x')
        
        for i, (col_id, col_config) in enumerate(columns.items()):
            header_label = ctk.CTkLabel(
                self.header_frame,
                text=col_config.get('text', col_id),
                font=ctk.CTkFont(family=FONTS['family'], size=13, weight='bold'),
                text_color=COLORS['white'],
                width=col_config.get('width', 100)
            )
            header_label.grid(row=0, column=i, padx=10, pady=12, sticky='w')
        
        # Scrollable frame pour les données avec hauteur fixe
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color='transparent',
            height=height,
            scrollbar_button_color=COLORS['primary'],
            scrollbar_button_hover_color=COLORS['primary_light']
        )
        self.scroll_frame.pack(fill='both', expand=True)
        
        # Configurer les colonnes
        for i in range(len(columns)):
            self.scroll_frame.columnconfigure(i, weight=1)
    
    def insert(self, values):
        """Insérer une ligne"""
        row_idx = len(self.rows)
        row_bg = COLORS['white'] if row_idx % 2 == 0 else COLORS['background']
        
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color=row_bg, corner_radius=0)
        row_frame.grid(row=row_idx, column=0, columnspan=len(self.columns), sticky='ew', pady=1)
        
        for i, (col_id, col_config) in enumerate(self.columns.items()):
            value = values[i] if i < len(values) else ''
            cell_label = ctk.CTkLabel(
                row_frame,
                text=str(value),
                font=ctk.CTkFont(family=FONTS['family'], size=13),
                text_color=COLORS['text_primary'],
                width=col_config.get('width', 100),
                anchor='w'
            )
            cell_label.grid(row=0, column=i, padx=10, pady=10, sticky='w')
        
        self.rows.append((row_frame, values))
        
        # Effet hover
        row_frame.bind('<Enter>', lambda e, f=row_frame: f.configure(fg_color=COLORS['primary_light']))
        row_frame.bind('<Leave>', lambda e, f=row_frame, bg=row_bg: f.configure(fg_color=bg))
        
        # Bind click
        row_frame.bind('<Button-1>', lambda e, idx=row_idx: self._on_row_click(idx))
        for child in row_frame.winfo_children():
            child.bind('<Button-1>', lambda e, idx=row_idx: self._on_row_click(idx))
    
    def _on_row_click(self, idx):
        """Gérer le clic sur une ligne"""
        self.selected_idx = idx
        # Réinitialiser les couleurs
        for i, (frame, _) in enumerate(self.rows):
            bg = COLORS['white'] if i % 2 == 0 else COLORS['background']
            if i == idx:
                frame.configure(fg_color=COLORS['primary'])
                for child in frame.winfo_children():
                    child.configure(text_color=COLORS['white'])
            else:
                frame.configure(fg_color=bg)
                for child in frame.winfo_children():
                    child.configure(text_color=COLORS['text_primary'])
    
    def clear(self):
        """Vider le tableau"""
        for frame, _ in self.rows:
            frame.destroy()
        self.rows = []
        self.selected_idx = None
    
    def get_selected(self):
        """Obtenir l'élément sélectionné"""
        if hasattr(self, 'selected_idx') and self.selected_idx is not None:
            if self.selected_idx < len(self.rows):
                return self.rows[self.selected_idx][1]
        return None


class Sidebar(ctk.CTkFrame):
    """Barre latérale de navigation moderne"""
    
    def __init__(self, parent, items, on_select=None, user_info=None, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS['primary_dark'],
            width=DIMENSIONS['sidebar_width'],
            corner_radius=0
        )
        self.pack_propagate(False)
        
        self.on_select = on_select
        self.buttons = {}
        self.active_item = None
        
        # Logo / Titre
        logo_frame = ctk.CTkFrame(self, fg_color='transparent')
        logo_frame.pack(fill='x', pady=(25, 15))
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="📚",
            font=ctk.CTkFont(size=42)
        )
        logo_label.pack()
        
        title_label = ctk.CTkLabel(
            logo_frame,
            text="IDSI Library",
            font=ctk.CTkFont(family=FONTS['family'], size=20, weight='bold'),
            text_color=COLORS['white']
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text="International Data Science Institute",
            font=ctk.CTkFont(family=FONTS['family'], size=10),
            text_color=COLORS['text_disabled']
        )
        subtitle_label.pack()
        
        # Séparateur
        separator = ctk.CTkFrame(self, fg_color=COLORS['primary'], height=2)
        separator.pack(fill='x', padx=20, pady=15)
        
        # Info utilisateur si fourni
        if user_info:
            user_frame = ctk.CTkFrame(self, fg_color=COLORS['primary'], corner_radius=10)
            user_frame.pack(fill='x', padx=15, pady=(0, 15))
            
            ctk.CTkLabel(
                user_frame,
                text=f"👤 {user_info.get('name', 'Utilisateur')}",
                font=ctk.CTkFont(family=FONTS['family'], size=13, weight='bold'),
                text_color=COLORS['white']
            ).pack(pady=(10, 2))
            
            ctk.CTkLabel(
                user_frame,
                text=user_info.get('role', ''),
                font=ctk.CTkFont(family=FONTS['family'], size=11),
                text_color=COLORS['secondary']
            ).pack(pady=(0, 10))
        
        # Items de navigation
        self.nav_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.nav_frame.pack(fill='x', padx=10)
        
        for item_id, item_config in items.items():
            self._create_nav_item(item_id, item_config)
    
    def _create_nav_item(self, item_id, config):
        """Créer un élément de navigation"""
        btn = ctk.CTkButton(
            self.nav_frame,
            text=f"  {config.get('icon', '')}   {config.get('text', item_id)}",
            font=ctk.CTkFont(family=FONTS['family'], size=14),
            fg_color='transparent',
            hover_color=COLORS['primary'],
            text_color=COLORS['white'],
            anchor='w',
            height=45,
            corner_radius=10,
            command=lambda i=item_id: self._on_click(i)
        )
        btn.pack(fill='x', pady=3)
        
        self.buttons[item_id] = btn
    
    def _on_click(self, item_id):
        # Réinitialiser l'ancien actif
        if self.active_item and self.active_item in self.buttons:
            self.buttons[self.active_item].configure(fg_color='transparent')
        
        # Activer le nouveau
        self.active_item = item_id
        self.buttons[item_id].configure(fg_color=COLORS['primary'])
        
        if self.on_select:
            self.on_select(item_id)
    
    def set_active(self, item_id):
        """Définir l'élément actif"""
        if self.active_item and self.active_item in self.buttons:
            self.buttons[self.active_item].configure(fg_color='transparent')
        
        self.active_item = item_id
        if item_id in self.buttons:
            self.buttons[item_id].configure(fg_color=COLORS['primary'])


class StatCard(ctk.CTkFrame):
    """Carte de statistique moderne"""
    
    def __init__(self, parent, title, value, icon=None, color=None, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS['surface'],
            border_width=1,
            border_color=COLORS['border'],
            corner_radius=DIMENSIONS['border_radius']
        )
        
        color = color or COLORS['primary']
        
        # Container interne
        inner = ctk.CTkFrame(self, fg_color='transparent')
        inner.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Ligne du haut (icône + titre)
        top_frame = ctk.CTkFrame(inner, fg_color='transparent')
        top_frame.pack(fill='x')
        
        if icon:
            icon_label = ctk.CTkLabel(
                top_frame,
                text=icon,
                font=ctk.CTkFont(size=28)
            )
            icon_label.pack(side='left')
        
        title_label = ctk.CTkLabel(
            top_frame,
            text=title,
            font=ctk.CTkFont(family=FONTS['family'], size=12),
            text_color=COLORS['text_secondary']
        )
        title_label.pack(side='right')
        
        # Valeur
        value_label = ctk.CTkLabel(
            inner,
            text=str(value),
            font=ctk.CTkFont(family=FONTS['family'], size=36, weight='bold'),
            text_color=color
        )
        value_label.pack(pady=(15, 0))


class SearchBar(ctk.CTkFrame):
    """Barre de recherche moderne"""
    
    def __init__(self, parent, placeholder='Rechercher...', on_search=None, **kwargs):
        super().__init__(parent, fg_color='transparent')
        
        self.on_search = on_search
        
        # Container
        container = ctk.CTkFrame(
            self,
            fg_color=COLORS['white'],
            border_width=2,
            border_color=COLORS['border'],
            corner_radius=DIMENSIONS['border_radius']
        )
        container.pack(fill='x')
        
        # Icône de recherche
        icon_label = ctk.CTkLabel(
            container,
            text=ICONS['search'],
            font=ctk.CTkFont(size=16),
            text_color=COLORS['text_secondary']
        )
        icon_label.pack(side='left', padx=(15, 5))
        
        # Entry
        self.entry = ctk.CTkEntry(
            container,
            placeholder_text=placeholder,
            font=ctk.CTkFont(family=FONTS['family'], size=14),
            fg_color='transparent',
            border_width=0,
            text_color=COLORS['text_primary'],
            placeholder_text_color=COLORS['text_disabled'],
            height=40
        )
        self.entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Bouton recherche
        search_btn = ctk.CTkButton(
            container,
            text="Rechercher",
            font=ctk.CTkFont(family=FONTS['family'], size=13, weight='bold'),
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_light'],
            corner_radius=DIMENSIONS['border_radius_sm'],
            width=100,
            height=35,
            command=self._on_search
        )
        search_btn.pack(side='right', padx=5, pady=5)
        
        # Bind Enter
        self.entry.bind('<Return>', lambda e: self._on_search())
    
    def _on_search(self):
        if self.on_search:
            self.on_search(self.entry.get())
    
    def get(self):
        return self.entry.get()


class BackgroundFrame(ctk.CTkFrame):
    """Frame avec image de fond"""
    
    def __init__(self, parent, image_path=None, blur=True, darken=0.5, **kwargs):
        super().__init__(parent, fg_color=COLORS['dark'], **kwargs)
        
        self.image_path = image_path or BACKGROUND_IMAGE
        self.blur = blur
        self.darken = darken
        self._bg_image = None
        self._bg_label = None
        
        # Canvas pour l'image de fond
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Charger et afficher l'image
        self.bind('<Configure>', self._on_resize)
        self._load_background()
    
    def _load_background(self):
        """Charger l'image de fond"""
        try:
            if os.path.exists(self.image_path):
                img = Image.open(self.image_path)
                
                # Appliquer le flou si demandé
                if self.blur:
                    img = img.filter(ImageFilter.GaussianBlur(radius=3))
                
                # Assombrir si demandé
                if self.darken > 0:
                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(1 - self.darken)
                
                self._original_image = img
                self._update_background()
        except Exception as e:
            print(f"Erreur chargement image: {e}")
    
    def _update_background(self):
        """Mettre à jour l'image de fond selon la taille"""
        if hasattr(self, '_original_image'):
            width = self.winfo_width()
            height = self.winfo_height()
            
            if width > 1 and height > 1:
                # Redimensionner en gardant les proportions
                img = self._original_image.copy()
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
                
                self._bg_image = ImageTk.PhotoImage(img)
                self.canvas.delete('bg')
                self.canvas.create_image(0, 0, anchor='nw', image=self._bg_image, tags='bg')
    
    def _on_resize(self, event):
        """Gérer le redimensionnement"""
        self.after(100, self._update_background)


class PasswordChangeDialog(ctk.CTkToplevel):
    """Dialog pour changer le mot de passe"""
    
    def __init__(self, parent, user, user_type, on_success=None):
        super().__init__(parent)
        
        self.user = user
        self.user_type = user_type
        self.on_success = on_success
        
        # Configuration de la fenêtre
        self.title("Modifier le mot de passe")
        self.geometry("450x400")
        self.resizable(False, False)
        
        # Centrer
        self.transient(parent)
        self.grab_set()
        
        self._create_ui()
    
    def _create_ui(self):
        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['surface'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Titre
        ctk.CTkLabel(
            main_frame,
            text="🔐 Modifier le mot de passe",
            font=ctk.CTkFont(family=FONTS['family'], size=22, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(pady=(0, 25))
        
        # Mot de passe actuel
        ctk.CTkLabel(
            main_frame,
            text="Mot de passe actuel",
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['text_secondary'],
            anchor='w'
        ).pack(fill='x')
        
        self.current_password = ModernEntry(
            main_frame,
            placeholder="Entrez votre mot de passe actuel",
            show="•",
            width=350
        )
        self.current_password.pack(pady=(5, 15))
        
        # Nouveau mot de passe
        ctk.CTkLabel(
            main_frame,
            text="Nouveau mot de passe",
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['text_secondary'],
            anchor='w'
        ).pack(fill='x')
        
        self.new_password = ModernEntry(
            main_frame,
            placeholder="Minimum 8 caractères",
            show="•",
            width=350
        )
        self.new_password.pack(pady=(5, 15))
        
        # Confirmer le mot de passe
        ctk.CTkLabel(
            main_frame,
            text="Confirmer le mot de passe",
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['text_secondary'],
            anchor='w'
        ).pack(fill='x')
        
        self.confirm_password = ModernEntry(
            main_frame,
            placeholder="Répétez le nouveau mot de passe",
            show="•",
            width=350
        )
        self.confirm_password.pack(pady=(5, 25))
        
        # Boutons
        btn_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        btn_frame.pack(fill='x')
        
        AnimatedButton(
            btn_frame,
            text="Annuler",
            style='outline',
            command=self.destroy,
            width=150
        ).pack(side='left')
        
        AnimatedButton(
            btn_frame,
            text="Enregistrer",
            style='primary',
            icon=ICONS['check'],
            command=self._save_password,
            width=180
        ).pack(side='right')
    
    def _save_password(self):
        """Enregistrer le nouveau mot de passe"""
        from models.database import get_db
        from models.models import Etudiant, Bibliothecaire
        from tkinter import messagebox
        
        current = self.current_password.get()
        new = self.new_password.get()
        confirm = self.confirm_password.get()
        
        # Validations
        if not current or not new or not confirm:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
        
        if len(new) < 8:
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 8 caractères.")
            return
        
        if new != confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return
        
        # Vérifier le mot de passe actuel
        if not self.user.verify_password(current):
            messagebox.showerror("Erreur", "Mot de passe actuel incorrect.")
            return
        
        # Mettre à jour en base
        db = get_db()
        try:
            if self.user_type == 'etudiant':
                user = db.query(Etudiant).filter(Etudiant.id == self.user.id).first()
                user.mot_de_passe = Etudiant.hash_password(new)
            else:
                user = db.query(Bibliothecaire).filter(Bibliothecaire.id == self.user.id).first()
                user.mot_de_passe = Bibliothecaire.hash_password(new)
            
            db.commit()
            messagebox.showinfo("Succès", "Mot de passe modifié avec succès !")
            
            if self.on_success:
                self.on_success()
            
            self.destroy()
            
        except Exception as e:
            db.rollback()
            messagebox.showerror("Erreur", f"Erreur: {e}")
        finally:
            db.close()


class ProfileEditDialog(ctk.CTkToplevel):
    """Dialog pour modifier le profil"""
    
    def __init__(self, parent, user, user_type, on_success=None):
        super().__init__(parent)
        
        self.user = user
        self.user_type = user_type
        self.on_success = on_success
        
        # Configuration de la fenêtre
        self.title("Modifier le profil")
        self.geometry("500x550")
        self.resizable(False, False)
        
        # Centrer
        self.transient(parent)
        self.grab_set()
        
        self._create_ui()
    
    def _create_ui(self):
        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['surface'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Titre
        ctk.CTkLabel(
            main_frame,
            text="✏️ Modifier le profil",
            font=ctk.CTkFont(family=FONTS['family'], size=22, weight='bold'),
            text_color=COLORS['text_primary']
        ).pack(pady=(0, 25))
        
        # Prénom
        ctk.CTkLabel(
            main_frame,
            text="Prénom",
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['text_secondary'],
            anchor='w'
        ).pack(fill='x')
        
        self.prenom_entry = ModernEntry(main_frame, width=400)
        self.prenom_entry.insert(0, self.user.prenom or '')
        self.prenom_entry.pack(pady=(5, 15))
        
        # Nom
        ctk.CTkLabel(
            main_frame,
            text="Nom",
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['text_secondary'],
            anchor='w'
        ).pack(fill='x')
        
        self.nom_entry = ModernEntry(main_frame, width=400)
        self.nom_entry.insert(0, self.user.nom or '')
        self.nom_entry.pack(pady=(5, 15))
        
        # Email
        ctk.CTkLabel(
            main_frame,
            text="Email",
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['text_secondary'],
            anchor='w'
        ).pack(fill='x')
        
        self.email_entry = ModernEntry(main_frame, width=400)
        self.email_entry.insert(0, self.user.email or '')
        self.email_entry.pack(pady=(5, 15))
        
        # Téléphone
        ctk.CTkLabel(
            main_frame,
            text="Téléphone",
            font=ctk.CTkFont(family=FONTS['family'], size=13),
            text_color=COLORS['text_secondary'],
            anchor='w'
        ).pack(fill='x')
        
        self.telephone_entry = ModernEntry(main_frame, width=400)
        self.telephone_entry.insert(0, self.user.telephone or '')
        self.telephone_entry.pack(pady=(5, 25))
        
        # Boutons
        btn_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        btn_frame.pack(fill='x')
        
        AnimatedButton(
            btn_frame,
            text="Annuler",
            style='outline',
            command=self.destroy,
            width=150
        ).pack(side='left')
        
        AnimatedButton(
            btn_frame,
            text="Enregistrer",
            style='success',
            icon=ICONS['check'],
            command=self._save_profile,
            width=180
        ).pack(side='right')
    
    def _save_profile(self):
        """Enregistrer les modifications du profil"""
        from models.database import get_db
        from models.models import Etudiant, Bibliothecaire
        from tkinter import messagebox
        
        prenom = self.prenom_entry.get().strip()
        nom = self.nom_entry.get().strip()
        email = self.email_entry.get().strip()
        telephone = self.telephone_entry.get().strip()
        
        # Validations
        if not prenom or not nom or not email:
            messagebox.showerror("Erreur", "Prénom, nom et email sont obligatoires.")
            return
        
        if '@' not in email:
            messagebox.showerror("Erreur", "Email invalide.")
            return
        
        # Mettre à jour en base
        db = get_db()
        try:
            if self.user_type == 'etudiant':
                user = db.query(Etudiant).filter(Etudiant.id == self.user.id).first()
            else:
                user = db.query(Bibliothecaire).filter(Bibliothecaire.id == self.user.id).first()
            
            user.prenom = prenom
            user.nom = nom
            user.email = email
            user.telephone = telephone
            
            db.commit()
            
            # Mettre à jour l'objet local
            self.user.prenom = prenom
            self.user.nom = nom
            self.user.email = email
            self.user.telephone = telephone
            
            messagebox.showinfo("Succès", "Profil mis à jour avec succès !")
            
            if self.on_success:
                self.on_success()
            
            self.destroy()
            
        except Exception as e:
            db.rollback()
            messagebox.showerror("Erreur", f"Erreur: {e}")
        finally:
            db.close()
