
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import webbrowser
import database

Window.clearcolor = (0.08, 0.09, 0.13, 1)
BLEU = (0.3, 0.7, 1, 1)
ORANGE = (1, 0.6, 0.2, 1)


class AccueilScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)
        layout.add_widget(Label(text="Q1", font_size=42, bold=True,
                                color=BLEU, size_hint_y=0.15))
        layout.add_widget(Label(text="Reussis tes examens !", font_size=18,
                                size_hint_y=0.08))

        btn_prem = Button(text="Passer en Premium", size_hint_y=None,
                          height=80, font_size=18, background_color=ORANGE)
        btn_prem.bind(on_press=self.ouvrir_premium)
        layout.add_widget(btn_prem)

        layout.add_widget(Label(text="Statut : " + ("PREMIUM" if database.is_premium() else "GRATUIT"),
                                font_size=16, size_hint_y=0.1))
        self.add_widget(layout)

    def ouvrir_premium(self, *a):
        self.manager.current = "premium"


class PremiumScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)
        layout.add_widget(Label(text="Q1 PREMIUM", font_size=30, bold=True,
                                color=ORANGE, size_hint_y=0.12))
        layout.add_widget(Label(text="Debloque tous les cours, quiz et exercices.",
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
        # Ouvre le navigateur vers ton lien de paiement
        webbrowser.open("https://pay.wave.com/m/ton-lien-wave-ici")

    def entrer_code(self, *a):
        content = BoxLayout(orientation="vertical", padding=15, spacing=15)
        content.add_widget(Label(text="Entre ton code recu apres paiement :"))
        champ = TextInput(multiline=False, hint_text="Ex: Q1-PREMIUM-2024", font_size=20)
        content.add_widget(champ)
        btn_valider = Button(text="Valider", size_hint_y=None, height=50)
        content.add_widget(btn_valider)
        popup = Popup(title="Code d'activation", content=content,
                      size_hint=(0.9, 0.4))

        def verifier(*args):
            code = champ.text.strip().upper()
            codes_valides = ["Q1-PREMIUM-2024", "Q1-VIP-001", "Q1-BEPC-2025"]
            if code in codes_valides:
                database.set_premium(True)
                popup.dismiss()
                Popup(title="Succes !",
                      content=Label(text="Mode Premium active !"),
                      size_hint=(0.8, 0.3)).open()
                self.manager.current = "accueil"
            else:
                champ.text = ""
                champ.hint_text = "Code invalide"

        btn_valider.bind(on_press=verifier)
        popup.open()


class Q1App(App):
    def build(self):
        database.init_db()
        sm = ScreenManager()
        sm.add_widget(AccueilScreen(name="accueil"))
        sm.add_widget(PremiumScreen(name="premium"))
        return sm


if __name__ == "__main__":
    Q1App().run
