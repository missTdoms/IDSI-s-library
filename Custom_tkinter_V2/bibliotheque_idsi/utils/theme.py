"""
Configuration du thème et des styles
Système de Gestion de Bibliothèque - IDSI

Design System moderne pour CustomTkinter
"""

import os

# ============================================
# CHEMINS DES RESSOURCES
# ============================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
BACKGROUND_IMAGE = os.path.join(ASSETS_DIR, 'background.jpg')

# ============================================
# PALETTE DE COULEURS - Design IDSI
# ============================================

COLORS = {
    # Couleurs principales IDSI
    'primary': '#0D47A1',        # Bleu IDSI profond
    'primary_light': '#1565C0',  # Bleu clair
    'primary_dark': '#002171',   # Bleu très foncé
    
    # Couleurs secondaires
    'secondary': '#FF6F00',      # Orange IDSI
    'secondary_light': '#FFA040',
    'secondary_dark': '#C43E00',
    
    # Couleurs d'accent
    'accent': '#00C853',         # Vert succès
    'accent_light': '#5EFC82',
    'warning': '#FFB300',        # Ambre avertissement
    'danger': '#D50000',         # Rouge erreur
    'info': '#00B8D4',           # Cyan info
    
    # Couleurs neutres
    'white': '#FFFFFF',
    'background': '#F8FAFC',     # Fond gris très clair
    'surface': '#FFFFFF',        # Surface des cartes
    'surface_dark': '#1E293B',   # Surface sombre
    'border': '#E2E8F0',         # Bordures
    'text_primary': '#1E293B',   # Texte principal
    'text_secondary': '#64748B', # Texte secondaire
    'text_disabled': '#94A3B8',  # Texte désactivé
    'dark': '#0F172A',           # Fond sombre
    'overlay': 'rgba(0,0,0,0.5)', # Superposition
    
    # Couleurs de statut
    'status_available': '#00C853',
    'status_borrowed': '#FFB300',
    'status_late': '#D50000',
    'status_reserved': '#7C4DFF',
    
    # Gradients (pour référence CSS)
    'gradient_primary': ('linear-gradient', '#0D47A1', '#1565C0'),
    'gradient_secondary': ('linear-gradient', '#FF6F00', '#FFA040'),
}

# CustomTkinter color mode
CTK_COLORS = {
    'primary': ('#0D47A1', '#1565C0'),
    'secondary': ('#FF6F00', '#FFA040'),
    'success': ('#00C853', '#5EFC82'),
    'danger': ('#D50000', '#FF5252'),
    'warning': ('#FFB300', '#FFCA28'),
    'info': ('#00B8D4', '#18FFFF'),
}

# ============================================
# TYPOGRAPHIE
# ============================================

FONTS = {
    'family': 'Segoe UI',
    'family_alt': 'Roboto',
    'family_mono': 'Consolas',
    
    # Tailles
    'size_h1': 32,
    'size_h2': 26,
    'size_h3': 20,
    'size_h4': 18,
    'size_body': 14,
    'size_small': 12,
    'size_caption': 10,
    
    # Configurations complètes pour Tkinter
    'heading1': ('Segoe UI', 32, 'bold'),
    'heading2': ('Segoe UI', 26, 'bold'),
    'heading3': ('Segoe UI', 20, 'bold'),
    'heading4': ('Segoe UI', 18, 'bold'),
    'body': ('Segoe UI', 14),
    'body_bold': ('Segoe UI', 14, 'bold'),
    'small': ('Segoe UI', 12),
    'caption': ('Segoe UI', 10),
    'button': ('Segoe UI', 14, 'bold'),
    'input': ('Segoe UI', 14),
    
    # Pour CustomTkinter
    'ctk_heading1': ('Segoe UI', 32),
    'ctk_heading2': ('Segoe UI', 26),
    'ctk_heading3': ('Segoe UI', 20),
    'ctk_body': ('Segoe UI', 14),
    'ctk_button': ('Segoe UI', 14),
}

# ============================================
# DIMENSIONS ET ESPACEMENT
# ============================================

DIMENSIONS = {
    # Fenêtre principale
    'window_width': 1400,
    'window_height': 800,
    'min_width': 1200,
    'min_height': 700,
    
    # Sidebar
    'sidebar_width': 280,
    'sidebar_collapsed': 70,
    
    # Composants
    'button_height': 45,
    'button_width': 150,
    'input_height': 45,
    'card_padding': 24,
    'border_radius': 12,
    'border_radius_lg': 16,
    'border_radius_sm': 8,
    
    # Espacement
    'spacing_xs': 4,
    'spacing_sm': 8,
    'spacing_md': 16,
    'spacing_lg': 24,
    'spacing_xl': 32,
    'spacing_2xl': 48,
    
    # Modal
    'modal_width': 500,
    'modal_height': 600,
}

# ============================================
# ICÔNES (Unicode améliorées)
# ============================================

ICONS = {
    'home': '🏠',
    'book': '📚',
    'book_open': '📖',
    'user': '👤',
    'users': '👥',
    'search': '🔍',
    'add': '➕',
    'edit': '✏️',
    'delete': '🗑️',
    'check': '✓',
    'cross': '✕',
    'arrow_left': '←',
    'arrow_right': '→',
    'arrow_down': '↓',
    'calendar': '📅',
    'clock': '🕐',
    'warning': '⚠️',
    'info': 'ℹ️',
    'success': '✅',
    'error': '❌',
    'logout': '🚪',
    'settings': '⚙️',
    'chart': '📊',
    'star': '⭐',
    'star_filled': '★',
    'loan': '📖',
    'return': '↩️',
    'reserve': '🔖',
    'notification': '🔔',
    'email': '📧',
    'phone': '📞',
    'lock': '🔒',
    'unlock': '🔓',
    'eye': '👁️',
    'eye_off': '🙈',
    'refresh': '🔄',
    'download': '⬇️',
    'upload': '⬆️',
    'filter': '🔽',
    'sort': '↕️',
    'menu': '☰',
    'close': '✖',
    'ai': '🤖',
    'data': '📈',
    'security': '🛡️',
    'certificate': '📜',
    'graduation': '🎓',
    'library': '🏛️',
    'key': '🔑',
    'profile': '👤',
    'password': '🔐',
}

# ============================================
# STYLES DES COMPOSANTS
# ============================================

BUTTON_STYLES = {
    'primary': {
        'fg_color': COLORS['primary'],
        'hover_color': COLORS['primary_light'],
        'text_color': COLORS['white'],
        'border_width': 0,
    },
    'secondary': {
        'fg_color': COLORS['secondary'],
        'hover_color': COLORS['secondary_light'],
        'text_color': COLORS['white'],
        'border_width': 0,
    },
    'success': {
        'fg_color': COLORS['accent'],
        'hover_color': COLORS['accent_light'],
        'text_color': COLORS['white'],
        'border_width': 0,
    },
    'danger': {
        'fg_color': COLORS['danger'],
        'hover_color': '#FF5252',
        'text_color': COLORS['white'],
        'border_width': 0,
    },
    'warning': {
        'fg_color': COLORS['warning'],
        'hover_color': '#FFCA28',
        'text_color': COLORS['dark'],
        'border_width': 0,
    },
    'outline': {
        'fg_color': 'transparent',
        'hover_color': COLORS['background'],
        'text_color': COLORS['primary'],
        'border_width': 2,
        'border_color': COLORS['primary'],
    },
    'ghost': {
        'fg_color': 'transparent',
        'hover_color': COLORS['background'],
        'text_color': COLORS['text_primary'],
        'border_width': 0,
    },
}

INPUT_STYLES = {
    'default': {
        'fg_color': COLORS['white'],
        'border_color': COLORS['border'],
        'text_color': COLORS['text_primary'],
        'placeholder_text_color': COLORS['text_disabled'],
    },
    'focused': {
        'fg_color': COLORS['white'],
        'border_color': COLORS['primary'],
        'text_color': COLORS['text_primary'],
    },
    'error': {
        'fg_color': '#FEF2F2',
        'border_color': COLORS['danger'],
        'text_color': COLORS['text_primary'],
    },
}

CARD_STYLES = {
    'default': {
        'fg_color': COLORS['surface'],
        'border_width': 1,
        'border_color': COLORS['border'],
        'corner_radius': DIMENSIONS['border_radius'],
    },
    'elevated': {
        'fg_color': COLORS['surface'],
        'border_width': 0,
        'corner_radius': DIMENSIONS['border_radius_lg'],
    },
    'dark': {
        'fg_color': COLORS['surface_dark'],
        'border_width': 0,
        'corner_radius': DIMENSIONS['border_radius'],
    },
}

# ============================================
# CONFIGURATION DE L'APPLICATION
# ============================================

APP_CONFIG = {
    'name': 'Bibliothèque IDSI',
    'full_name': 'International Data Science Institute',
    'version': '3.0.0',
    'author': 'IDSI Development Team',
    'institution': 'International Data Science Institute (IDSI)',
    'description': 'Programmes d\'excellence en Data Science, Big Data, IA et Cybersécurité',
    'currency': 'FCFA',
    'loan_duration_days': 14,
    'penalty_per_day': 100,  # FCFA
    'max_loans_per_student': 5,
    'reservation_duration_days': 3,
    'logo_text': '📚 IDSI Library',
}

# ============================================
# CATÉGORIES DE LIVRES (adaptées IDSI)
# ============================================

BOOK_CATEGORIES = [
    'Data Science',
    'Intelligence Artificielle',
    'Machine Learning',
    'Deep Learning',
    'Big Data',
    'Cybersécurité',
    'Sécurité Informatique',
    'Statistiques',
    'Programmation Python',
    'Programmation R',
    'Base de données',
    'Cloud Computing',
    'Data Engineering',
    'MLOps',
    'Natural Language Processing',
    'Computer Vision',
    'Réseaux de Neurones',
    'Analyse de Données',
    'Visualisation de Données',
    'Éthique de l\'IA',
    'Autre',
]

# ============================================
# PROGRAMMES IDSI
# ============================================

PROGRAMMES = [
    'Data Science & Big Data',
    'Intelligence Artificielle',
    'Machine Learning Engineering',
    'Cybersécurité',
    'Data Engineering',
    'Business Intelligence',
]

NIVEAUX = [
    'Certificate',
    'Diploma',
    'Bachelor 1',
    'Bachelor 2', 
    'Bachelor 3',
    'Master 1',
    'Master 2',
    'PhD',
]

# Compatibilité avec l'ancien code
FILIERES = PROGRAMMES

# ============================================
# ANIMATIONS
# ============================================

ANIMATIONS = {
    'fade_duration': 300,  # ms
    'slide_duration': 250,  # ms
    'bounce_duration': 400,  # ms
    'hover_scale': 1.02,
    'press_scale': 0.98,
}

# ============================================
# MESSAGES ET TEXTES
# ============================================

MESSAGES = {
    'welcome': 'Bienvenue à la Bibliothèque IDSI',
    'login_title': 'Connexion',
    'login_subtitle': 'Accédez à votre espace personnel',
    'login_success': 'Connexion réussie !',
    'login_error': 'Identifiant ou mot de passe incorrect',
    'logout': 'Vous avez été déconnecté',
    'logout_confirm': 'Voulez-vous vraiment vous déconnecter ?',
    'loan_success': 'Emprunt enregistré avec succès',
    'return_success': 'Retour enregistré avec succès',
    'book_added': 'Livre ajouté avec succès',
    'book_updated': 'Livre mis à jour',
    'book_deleted': 'Livre supprimé',
    'student_added': 'Étudiant ajouté avec succès',
    'no_books': 'Aucun livre trouvé',
    'book_unavailable': 'Ce livre n\'est pas disponible',
    'max_loans': 'Nombre maximum d\'emprunts atteint',
    'confirm_delete': 'Êtes-vous sûr de vouloir supprimer ?',
    'penalty_warning': 'Attention : Vous avez des pénalités impayées',
    'password_changed': 'Mot de passe modifié avec succès',
    'profile_updated': 'Profil mis à jour avec succès',
    'password_mismatch': 'Les mots de passe ne correspondent pas',
    'password_weak': 'Le mot de passe doit contenir au moins 8 caractères',
    'current_password_wrong': 'Mot de passe actuel incorrect',
}

# ============================================
# THEME CUSTOMTKINTER
# ============================================

CTK_THEME = {
    'appearance_mode': 'light',  # 'light', 'dark', 'system'
    'color_theme': 'blue',
}
