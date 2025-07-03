"""
Analyse des impacts environnementaux des pratiques agricoles
"""
import pandas as pd
import numpy as np
from collections import Counter
import re

def analyze_harmful_practices(df):
    """Identifie les pratiques agricoles nuisibles"""
    
    harmful_practices = {
        'pesticides_chimiques': {
            'column': 'quels sont  les intrants  et  fertilisants que vous recevez ou utilisez/Herbicide',
            'description': 'Utilisation d\'herbicides chimiques',
            'impact': 'Pollution des sols et de l\'eau, risques sanitaires'
        },
        'engrais_chimiques': {
            'column': 'quels sont  les intrants  et  fertilisants que vous recevez ou utilisez/engrais chimiques(uree, NPk...)',
            'description': 'Utilisation d\'engrais chimiques (urée, NPK)',
            'impact': 'Eutrophisation, pollution des nappes phréatiques'
        },
        'brulage_dechets': {
            'indicator': lambda row: 'brûl' in str(row['que faites vous des contenants vides de produits agrochimiques (sacs, bidons) après usage']).lower(),
            'description': 'Brûlage des contenants de produits chimiques',
            'impact': 'Pollution atmosphérique, émission de dioxines'
        },
        'pas_de_protection': {
            'indicator': lambda row: row['Protection_factor'] >= 0.7,
            'description': 'Absence ou insuffisance d\'équipements de protection',
            'impact': 'Exposition directe aux produits toxiques'
        },
        'surconsommation_eau': {
            'indicator': lambda row: row['Water_consumption_m3'] > 16250,
            'description': 'Surconsommation d\'eau (>16250 m³/ha)',
            'impact': 'Épuisement des ressources hydriques'
        },
        'pas_de_rotation': {
            'column': 'utilisez vous des pratiques pour limiter l\'impact de la riziculture sur l\'environnement en adoptant ces mesures/rotation ',
            'description': 'Absence de rotation des cultures',
            'impact': 'Épuisement des sols, prolifération des ravageurs',
            'inverse': True  # 0 signifie pas de rotation
        }
    }
    
    results = {}
    
    for practice, config in harmful_practices.items():
        if 'column' in config:
            if config.get('inverse', False):
                count = (df[config['column']] == 0).sum()
            else:
                count = df[config['column']].sum()
        else:
            count = df.apply(config['indicator'], axis=1).sum()
        
        percentage = (count / len(df)) * 100
        
        results[practice] = {
            'count': count,
            'percentage': percentage,
            'description': config['description'],
            'impact': config['impact']
        }
    
    return results

def analyze_deforestation_evolution(df):
    """Analyse l'évolution de la déforestation"""
    
    # Analyser les mentions de déforestation
    deforestation_indicators = []
    
    # Colonnes contenant des informations sur la déforestation
    text_columns = [
        'depuis l\'installation de la rizière, avez vous constaté une diminution, une prolifération ou une disparition des espèces végétales ou animale',
        'comment ca se manifeste',
        'Avez vous beneficié d\'une extention de vos surfaces rizicoles, si oui expliquez'
    ]
    
    deforestation_keywords = ['déforestation', 'coupe', 'arbres', 'défrichement', 'déboisement']
    
    for _, row in df.iterrows():
        mentions = []
        for col in text_columns:
            if pd.notna(row[col]):
                text = str(row[col]).lower()
                for keyword in deforestation_keywords:
                    if keyword in text:
                        mentions.append({
                            'keyword': keyword,
                            'context': text[:100],
                            'column': col
                        })
        
        deforestation_indicators.append({
            'has_deforestation': len(mentions) > 0,
            'mentions': mentions,
            'surface_2023': row.get('Surperficie cultivée en 2023', 0),
            'surface_2024': row.get('Superficie cultivée en 2024', 0),
            'surface_2025': row.get('Superficie cultivée en 2025', 0)
        })
    
    # Calculer les statistiques
    df_defor = pd.DataFrame(deforestation_indicators)
    
    results = {
        'total_mentions': df_defor['has_deforestation'].sum(),
        'percentage': (df_defor['has_deforestation'].sum() / len(df)) * 100,
        'surface_evolution': {
            '2023': df['Surperficie cultivée en 2023'].sum(),
            '2024': df['Superficie cultivée en 2024'].sum(),
            '2025': df['Superficie cultivée en 2025'].sum()
        },
        'keywords_frequency': Counter([m['keyword'] for ind in deforestation_indicators for m in ind['mentions']])
    }
    
    return results

def analyze_biodiversity_loss(df):
    """Analyse la perte de biodiversité"""
    
    biodiversity_column = 'depuis l\'installation de la rizière, avez vous constaté une diminution, une prolifération ou une disparition des espèces végétales ou animale'
    
    # Catégoriser les impacts
    impact_categories = {
        'disparition': ['disparition', 'disparu'],
        'diminution': ['diminution', 'réduit', 'baisse'],
        'proliferation_negative': ['prolifération', 'herbe', 'adventice', 'mauvaise'],
        'pas_de_changement': ['pas de changement', 'rien', 'néant', 'non']
    }
    
    impacts = []
    
    for _, row in df.iterrows():
        response = str(row[biodiversity_column]).lower() if pd.notna(row[biodiversity_column]) else ''
        
        impact_type = 'non_specifie'
        details = ''
        
        for category, keywords in impact_categories.items():
            if any(keyword in response for keyword in keywords):
                impact_type = category
                details = response
                break
        
        impacts.append({
            'type': impact_type,
            'details': details,
            'uses_pesticides': row.get('Uses_pesticides', False),
            'water_consumption': row.get('Water_consumption_m3', 0)
        })
    
    df_impacts = pd.DataFrame(impacts)
    
    # Calculer les statistiques
    results = {
        'impact_distribution': df_impacts['type'].value_counts().to_dict(),
        'percentage_negative_impact': (
            (df_impacts['type'].isin(['disparition', 'diminution', 'proliferation_negative']).sum() / len(df)) * 100
        ),
        'correlation_with_pesticides': {
            'with_pesticides': df_impacts[df_impacts['uses_pesticides']]['type'].isin(['disparition', 'diminution']).mean() * 100,
            'without_pesticides': df_impacts[~df_impacts['uses_pesticides']]['type'].isin(['disparition', 'diminution']).mean() * 100
        }
    }
    
    return results

def generate_impact_report(df):
    """Génère un rapport complet sur les impacts environnementaux"""
    
    print("Analyse des impacts environnementaux...")
    
    # Analyser les pratiques nuisibles
    harmful_practices = analyze_harmful_practices(df)
    
    # Analyser la déforestation
    deforestation = analyze_deforestation_evolution(df)
    
    # Analyser la biodiversité
    biodiversity = analyze_biodiversity_loss(df)
    
    report = {
        'harmful_practices': harmful_practices,
        'deforestation': deforestation,
        'biodiversity': biodiversity,
        'summary': {
            'total_farmers': len(df),
            'main_harmful_practice': max(harmful_practices.items(), key=lambda x: x[1]['percentage'])[0],
            'deforestation_rate': deforestation['percentage'],
            'biodiversity_impact_rate': biodiversity['percentage_negative_impact']
        }
    }
    
    # Afficher le résumé
    print("\n=== RÉSUMÉ DES IMPACTS ENVIRONNEMENTAUX ===")
    print(f"\n1. Pratiques agricoles nuisibles identifiées:")
    for practice, data in harmful_practices.items():
        if data['percentage'] > 30:  # Seuil significatif
            print(f"   - {data['description']}: {data['percentage']:.1f}% des agriculteurs")
            print(f"     Impact: {data['impact']}")
    
    print(f"\n2. Déforestation:")
    print(f"   - {deforestation['percentage']:.1f}% des agriculteurs mentionnent la déforestation")
    print(f"   - Évolution des surfaces cultivées: {deforestation['surface_evolution']}")
    
    print(f"\n3. Biodiversité:")
    print(f"   - {biodiversity['percentage_negative_impact']:.1f}% reportent un impact négatif")
    print(f"   - Corrélation avec pesticides: {biodiversity['correlation_with_pesticides']}")
    
    return report

if __name__ == "__main__":
    # Charger les données nettoyées
    from data_loader import prepare_data
    df = prepare_data()
    
    if df is not None:
        report = generate_impact_report(df)