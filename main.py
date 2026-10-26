# --- CONFIGURATION PLEIN ECRAN (Doit être tout en haut) ---
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'window_state', 'maximized')

# --- IMPORTS ---
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import webbrowser
import database
import data_manager

Window.clearcolor = (0.08, 0.09, 0.13, 1)
BLEU = (0.3, 0.7, 1, 1)
ORANGE = (1, 0.6, 0.2, 1)


# ==========================================
# ÉCRAN ACCUEIL
# ==========================================
class AccueilScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=15)
        
        self.layout.add_widget(Label(text="Q1", font_size=42, bold=True,
                                color=BLEU, size_hint_y=0.1))
        
        self.statut_label = Label(text="", font_size=16, size_hint_y=0.05)
        self.layout.add_widget(self.statut_label)

        # Zone pour les classes
        scroll = ScrollView(size_hint_y=0.6)
        self.liste_classes = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=10)
        self.liste_classes.bind(minimum_height=self.liste_classes.setter("height"))
        scroll.add_widget(self.liste_classes)
        self.layout.add_widget(scroll)

        # Bouton Premium
        btn_prem = Button(text="Gérer mon abonnement Premium", size_hint_y=None,
                          height=60, font_size=16, background_color=ORANGE)
        btn_prem.bind(on_press=lambda x: setattr(self.manager, "current", "premium"))
        self.layout.add_widget(btn_prem)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        statut = "Statut : PREMIUM" if database.is_premium() else "Statut : GRATUIT"
        self.statut_label.text = statut
        
        self.liste_classes.clear_widgets()
        classes = data_manager.charger_cours()
        for c in classes:
            btn = Button(text=c["nom"], size_hint_y=None, height=80, font_size=20, background_color=(0.2, 0.4, 0.6, 1))
            btn.bind(on_press=lambda x, c=c: self.ouvrir_classe(c))
            self.liste_classes.add_widget(btn)

    def ouvrir_classe(self, classe):
        App.get_running_app().classe_active = classe
        self.manager.current = "matieres"


# ==========================================
# ÉCRAN MATIERES
# ==========================================
class MatieresScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=15)
        
        self.titre = Label(text="", font_size=28, bold=True, color=BLEU, size_hint_y=0.1)
        self.layout.add_widget(self.titre)

        scroll = ScrollView(size_hint_y=0.7)
        self.liste_matieres = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=10)
        self.liste_matieres.bind(minimum_height=self.liste_matieres.setter("height"))
        scroll.add_widget(self.liste_matieres)
        self.layout.add_widget(scroll)

        btn_retour = Button(text="Retour", size_hint_y=None, height=60)
        btn_retour.bind(on_press=lambda x: setattr(self.manager, "current", "accueil"))
        self.layout.add_widget(btn_retour)
        
        self.add_widget(self.layout)

    def on_pre_enter(self):
        classe = App.get_running_app().classe_active
        self.titre.text = f"Classe : {classe['nom']}"
        
        self.liste_matieres.clear_widgets()
        for m in classe["matieres"]:
            btn = Button(text=m["nom"], size_hint_y=None, height=80, font_size=18)
            btn.bind(on_press=lambda x, m=m: self.ouvrir_matiere(m))
            self.liste_matieres.add_widget(btn)

    def ouvrir_matiere(self, matiere):
        App.get_running_app().matiere_active = matiere
        self.manager.current = "cours"


# ==========================================
# ÉCRAN COURS
# ==========================================
class CoursScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=15)
        
        self.titre = Label(text="", font_size=24, bold=True, color=BLEU, size_hint_y=0.1)
        self.layout.add_widget(self.titre)

        scroll = ScrollView(size_hint_y=0.7)
        self.liste_cours = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=10)
        self.liste_cours.bind(minimum_height=self.liste_cours.setter("height"))
        scroll.add_widget(self.liste_cours)
        self.layout.add_widget(scroll)

        btn_retour = Button(text="Retour", size_hint_y=None, height=60)
        btn_retour.bind(on_press=lambda x: setattr(self.manager, "current", "matieres"))
        self.layout.add_widget(btn_retour)
        
        self.add_widget(self.layout)

    def on_pre_enter(self):
        matiere = App.get_running_app().matiere_active
        self.titre.text = f"Matière : {matiere['nom']}"
        
        self.liste_cours.clear_widgets()
        premium = database.is_premium()
        
        for c in matiere["cours"]:
            if c.get("premium") and not premium:
                texte = f"[PREMIUM] {c['titre']}"
                couleur = (0.4, 0.4, 0.4, 1)
            else:
                texte = f"{c['titre']}"
                couleur = (0.2, 0.6, 0.3, 1)
                
            btn = Button(text=texte, size_hint_y=None, height=80, font_size=16, background_color=couleur)
            btn.bind(on_press=lambda x, c=c: self.ouvrir_cours(c))
            self.liste_cours.add_widget(btn)

    def ouvrir_cours(self, cours):
        if cours.get("premium") and not database.is_premium():
            Popup(title="Contenu Premium",
                  content=Label(text="Ce cours est réservé aux membres Premium.\nVa dans 'Gérer mon abonnement'."),
                  size_hint=(0.9, 0.3)).open()
        else:
            Popup(title=cours["titre"],
                  content=Label(text=cours["contenu"], text_size=(Window.width*0.8, None)),
                  size_hint=(0.9, 0.5)).open()


# ==========================================
# ÉCRAN PREMIUM
# ==========================================
class PremiumScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)
        layout.add_widget(Label(text="Q1 PREMIUM", font_size=30, bold=True,
                                color=ORANGE, size_hint_y=0.12))
        layout.add_widget(Label(text="Débloque tous les cours, quiz et exercices.",
                                font_size=15, size_hint_y=0.1))

        btn_payer = Button(text="Payer 5000 FCFA", size_hint_y=None, height=80,
                           font_size=18, background_color=(0.2, 0.7, 0.3, 1))
        btn_payer.bind(on_press=self.payer)
        layout.add_widget(btn_payer)

        btn_code = Button(text="J'ai un code d'activation", size_hint_y=None,
                          height=70, font_size=16, background_color=BLEU)
        btn_code.bind(on_press=self.entrer_code)
        layout.add_widget(btn_code)

        btn_retour = Button(text="Retour", size_hint_y=None, height=60)
        btn_retour.bind(on_press=lambda x: setattr(self.manager, "current", "accueil"))
        layout.add_widget(btn_retour)
        self.add_widget(layout)

    def payer(self, *a):
        webbrowser.open("https://pay.wave.com/m/ton-lien-wave-ici")

    def entrer_code(self, *a):
        content = BoxLayout(orientation="vertical", padding=15, spacing=15)
        content.add_widget(Label(text="Entre ton code reçu après paiement :"))
        champ = TextInput(multiline=False, hint_text="Ex: Q1-PREMIUM-2024", font_size=20)
        content.add_widget(champ)
        btn_valider = Button(text="Valider", size_hint_y=None, height=50)
        content.add_widget(btn_valider)
        popup = Popup(title="Code d'activation", content=content, size_hint=(0.9, 0.4))

        def verifier(*args):
            code = champ.text.strip().upper()
            codes_valides = ["Q1-PREMIUM-2024", "Q1-VIP-001", "Q1-BEPC-2025"]
            if code in codes_valides:
                database.set_premium(True)
                popup.dismiss()
                Popup(title="Succès !", content=Label(text="Mode Premium activé !"), size_hint=(0.8, 0.3)).open()
                self.manager.current = "accueil"
            else:
                champ.text = ""
                champ.hint_text = "Code invalide"

        btn_valider.bind(on_press=verifier)
        popup.open()


# ==========================================
# APP PRINCIPALE
# ==========================================
class Q1App(App):
    classe_active = None
    matiere_active = None

    def build(self):
        database.init_db()
        sm = ScreenManager()
        sm.add_widget(AccueilScreen(name="accueil"))
        sm.add_widget(MatieresScreen(name="matieres"))
        sm.add_widget(CoursScreen(name="cours"))
        sm.add_widget(PremiumScreen(name="premium"))
        return sm

if __name__ == "__main__":
    Q1App().run()
