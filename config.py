"""
Configuration du projet d'analyse environnementale
"""
import os
from pathlib import Path

# Chemins du projet
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "resultats"
GRAPHS_DIR = RESULTS_DIR / "graphiques"
REPORTS_DIR = RESULTS_DIR / "rapports"

# Créer les dossiers s'ils n'existent pas
for directory in [DATA_DIR, RESULTS_DIR, GRAPHS_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Fichier de données
DATA_FILE = "Evaluation_environnementale_du_projet_TAAT2__all_versions__Français_fr__20250703101247.xlsx"

# Configuration des graphiques
GRAPH_CONFIG = {
    'figure_size': (10, 6),
    'dpi': 300,
    'font_size': 12,
    'title_size': 14,
    'label_size': 12,
    'legend_size': 10,
    'colors': ['#2E86AB', '#E63946', '#F77F00', '#06D6A0', '#7209B7', '#F72585']
}

# Seuils d'analyse
THRESHOLDS = {
    'water_consumption_high': 16250,  # m³/ha
    'pesticide_exposure_risk': 50,    # échelle 1-100
    'soil_erosion_severe': 3,         # échelle 1-5
    'biodiversity_impact_high': 0.7   # proportion
}

# Catégories d'analyse
EDUCATION_LEVELS = {
    'Non scolarise': 0,
    'Coranique': 1,
    'Primaire': 2,
    'Secondaire': 3,
    'Superieur': 4
}

AGE_GROUPS = {
    'Jeune (18-35)': (18, 35),
    'Adulte (36-50)': (36, 50),
    'Senior (>50)': (51, 100)
}

# Messages et labels en français
LABELS = {
    'water_usage': "Consommation d'eau (m³/ha)",
    'pesticide_exposure': "Exposition aux pesticides",
    'deforestation': "Impact sur la déforestation",
    'biodiversity': "Impact sur la biodiversité",
    'education': "Niveau d'éducation",
    'age': "Groupe d'âge",
    'marital_status': "Situation matrimoniale"
}