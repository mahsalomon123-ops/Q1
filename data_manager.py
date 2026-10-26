import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def charger_cours():
    chemin = os.path.join(DATA_DIR, "cours.json")
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)["classes"]
    except Exception as e:
        print("Erreur lecture cours:", e)
        return []
