"""
Application principale - Système de Gestion de Bibliothèque IDSI
Version CustomTkinter Moderne

International Data Science Institute (IDSI)
Programmes d'excellence en Data Science, Big Data, IA et Cybersécurité
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.theme import COLORS, FONTS, DIMENSIONS, APP_CONFIG, CTK_THEME
from models.database import init_db
from views.login_view import LoginView
from views.student_dashboard import StudentDashboard
from views.librarian_dashboard import LibrarianDashboard


class BibliothequeApp(ctk.CTk):
    """Application principale de gestion de bibliothèque IDSI"""
    
    def __init__(self):
        super().__init__()
        
        # Configuration CustomTkinter
        ctk.set_appearance_mode(CTK_THEME['appearance_mode'])
        ctk.set_default_color_theme(CTK_THEME['color_theme'])
        
        # Configuration de la fenêtre principale
        self.title(f"{APP_CONFIG['name']} - {APP_CONFIG['institution']}")
        self.geometry(f"{DIMENSIONS['window_width']}x{DIMENSIONS['window_height']}")
        self.minsize(DIMENSIONS['min_width'], DIMENSIONS['min_height'])
        self.configure(fg_color=COLORS['dark'])
        
        # Centrer la fenêtre
        self._center_window()
        
        # Icône (optionnel)
        try:
            if sys.platform == 'win32':
                # Sur Windows, on pourrait utiliser un fichier .ico
                pass
        except:
            pass
        
        # Initialiser la base de données
        try:
            init_db()
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Erreur lors de l'initialisation de la base de données:\n{str(e)}"
            )
            sys.exit(1)
        
        # Variables d'état
        self.current_user = None
        self.current_user_type = None
        self.current_view = None
        
        # Afficher la page de connexion
        self._show_login()
        
        # Gérer la fermeture
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _center_window(self):
        """Centrer la fenêtre sur l'écran"""
        self.update_idletasks()
        width = DIMENSIONS['window_width']
        height = DIMENSIONS['window_height']
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _clear_view(self):
        """Effacer la vue actuelle"""
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
    
    def _show_login(self):
        """Afficher la page de connexion"""
        self._clear_view()
        
        self.current_view = LoginView(self, on_login_success=self._on_login_success)
        self.current_view.pack(fill='both', expand=True)
    
    def _on_login_success(self, user, user_type):
        """Callback après connexion réussie"""
        self.current_user = user
        self.current_user_type = user_type
        
        self._clear_view()
        
        if user_type == 'etudiant':
            self.current_view = StudentDashboard(
                self,
                user=user,
                on_logout=self._on_logout
            )
        else:
            self.current_view = LibrarianDashboard(
                self,
                user=user,
                on_logout=self._on_logout
            )
        
        self.current_view.pack(fill='both', expand=True)
    
    def _on_logout(self):
        """Callback pour la déconnexion"""
        self.current_user = None
        self.current_user_type = None
        self._show_login()
    
    def _on_closing(self):
        """Gérer la fermeture de l'application"""
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter l'application ?"):
            self.destroy()


def main():
    """Point d'entrée de l'application"""
    print(f"""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║   📚 Système de Gestion de Bibliothèque IDSI                        ║
    ║                                                                      ║
    ║   International Data Science Institute                               ║
    ║   Data Science • Big Data • IA • Cybersécurité                      ║
    ║                                                                      ║
    ║   Version: {APP_CONFIG['version']}                                                  ║
    ║                                                                      ║
    ║   Démarrage de l'application...                                      ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    app = BibliothequeApp()
    app.mainloop()


if __name__ == "__main__":
    main()
