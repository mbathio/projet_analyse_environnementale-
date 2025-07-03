"""
Module de chargement et nettoyage des données
"""
import pandas as pd
import numpy as np
from datetime import datetime
from config import DATA_DIR, DATA_FILE, EDUCATION_LEVELS, AGE_GROUPS

def load_data():
    """Charge les données depuis le fichier Excel"""
    file_path = DATA_DIR / DATA_FILE
    try:
        df = pd.read_excel(file_path)
        print(f"✓ Données chargées: {len(df)} enregistrements")
        return df
    except Exception as e:
        print(f"✗ Erreur lors du chargement: {e}")
        return None

def clean_age_data(df):
    """Nettoie et convertit les données d'âge"""
    # Convertir les dates en âge
    def convert_to_age(val):
        if pd.isna(val):
            return np.nan
        if isinstance(val, str) and 'T' in val:
            try:
                birth_date = pd.to_datetime(val)
                age = (datetime.now() - birth_date).days / 365.25
                return int(age)
            except:
                return np.nan
        try:
            return int(val)
        except:
            return np.nan
    
    df['Age_clean'] = df['Age'].apply(convert_to_age)
    
    # Créer les groupes d'âge
    def assign_age_group(age):
        if pd.isna(age):
            return 'Non spécifié'
        for group, (min_age, max_age) in AGE_GROUPS.items():
            if min_age <= age <= max_age:
                return group
        return 'Non spécifié'
    
    df['Age_group'] = df['Age_clean'].apply(assign_age_group)
    return df

def clean_education_data(df):
    """Nettoie les données d'éducation"""
    df['Education_level'] = df["niveau d'instruction "].map(EDUCATION_LEVELS)
    df['Education_level'].fillna(0, inplace=True)
    return df

def clean_water_data(df):
    """Nettoie les données de consommation d'eau"""
    water_mapping = {
        '<10000m3': 8000,
        '10000-13000m3': 11500,
        '13001-16250m3': 14625,
        '>16250m3': 20000
    }
    
    df['Water_consumption_m3'] = df["Quantité d'eau utilisée/ha en cas de pompage"].map(water_mapping)
    df['Water_consumption_m3'].fillna(0, inplace=True)
    return df

def clean_pesticide_data(df):
    """Nettoie les données sur les pesticides"""
    # Indicateur d'utilisation de pesticides
    pesticide_cols = [
        "quels sont  les intrants  et  fertilisants que vous recevez ou utilisez/Herbicide",
        "quels sont  les intrants  et  fertilisants que vous recevez ou utilisez/biopesticide"
    ]
    
    df['Uses_pesticides'] = df[pesticide_cols].sum(axis=1) > 0
    
    # Score d'exposition (basé sur plusieurs facteurs)
    df['Pesticide_exposure_score'] = 0
    
    # Facteurs d'exposition
    if 'sur une echelle de 1 a 100 notez la présence des pesticides dans les canaux' in df.columns:
        df['Pesticide_exposure_score'] += df['sur une echelle de 1 a 100 notez la présence des pesticides dans les canaux'].fillna(0)
    
    # Protection utilisée
    protection_map = {
        'habit_lourd': 0.5,
        'Voile': 0.7,
        'Négligeable': 1.0,
        'neant': 1.0
    }
    
    df['Protection_factor'] = df['quels equipements de protection utilisez vous lors de l\'application de pesticides ou d\'engrais?'].map(protection_map)
    df['Protection_factor'].fillna(1.0, inplace=True)
    
    # Score final d'exposition
    df['Pesticide_exposure_score'] = df['Pesticide_exposure_score'] * df['Protection_factor']
    
    return df

def clean_environmental_data(df):
    """Nettoie les données environnementales"""
    # Impact sur la biodiversité
    biodiversity_keywords = ['disparition', 'diminution', 'prolifération']
    df['Biodiversity_impact'] = df['depuis l\'installation de la rizière, avez vous constaté une diminution, une prolifération ou une disparition des espèces végétales ou animale'].apply(
        lambda x: any(keyword in str(x).lower() for keyword in biodiversity_keywords) if pd.notna(x) else False
    )
    
    # Déforestation
    deforestation_keywords = ['déforestation', 'coupe', 'arbres']
    df['Deforestation_mentioned'] = df['comment ca se manifeste'].apply(
        lambda x: any(keyword in str(x).lower() for keyword in deforestation_keywords) if pd.notna(x) else False
    )
    
    # Érosion des sols
    erosion_map = {
        'epuises': 4,
        'Pauvre': 3,
        'moyen': 2,
        'bon': 1
    }
    
    df['Soil_erosion_score'] = df['comment evaluez vous l\'etat des sols'].map(erosion_map)
    df['Soil_erosion_score'].fillna(2, inplace=True)
    
    return df

def prepare_data():
    """Fonction principale pour préparer toutes les données"""
    print("Chargement et nettoyage des données...")
    
    # Charger les données
    df = load_data()
    if df is None:
        return None
    
    # Nettoyer chaque catégorie
    df = clean_age_data(df)
    df = clean_education_data(df)
    df = clean_water_data(df)
    df = clean_pesticide_data(df)
    df = clean_environmental_data(df)
    
    print(f"✓ Données nettoyées: {len(df)} enregistrements")
    
    # Afficher un résumé
    print("\nRésumé des données:")
    print(f"- Âge moyen: {df['Age_clean'].mean():.1f} ans")
    print(f"- Utilisation de pesticides: {df['Uses_pesticides'].sum()} agriculteurs ({df['Uses_pesticides'].mean()*100:.1f}%)")
    print(f"- Consommation d'eau moyenne: {df['Water_consumption_m3'].mean():.0f} m³/ha")
    print(f"- Impact sur la biodiversité: {df['Biodiversity_impact'].sum()} cas reportés")
    
    return df

if __name__ == "__main__":
    df = prepare_data()
    if df is not None:
        # Sauvegarder les données nettoyées
        df.to_csv(DATA_DIR / "cleaned_data.csv", index=False)
        print("✓ Données sauvegardées dans 'cleaned_data.csv'")