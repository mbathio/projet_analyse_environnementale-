"""
Analyse de l'exposition humaine aux pesticides et engrais
"""
import pandas as pd
import numpy as np

def analyze_pesticide_exposure(df):
    """Analyse l'exposition aux pesticides"""
    
    # Types de pesticides utilisés
    pesticides_mentioned = []
    pesticide_column = 'quels sont les pesticides que vous  utiliser '
    
    for _, row in df.iterrows():
        if pd.notna(row[pesticide_column]):
            pesticides = str(row[pesticide_column]).lower().split(',')
            pesticides_mentioned.extend([p.strip() for p in pesticides])
    
    # Compter les types de pesticides
    from collections import Counter
    pesticide_counts = Counter(pesticides_mentioned)
    
    # Analyser les cas d'intoxication
    intoxication_column = 'pouvez vous raconter un cas d\'accident ou d\'intoxication lie à l\'usage des produits chimiques? _1'
    intoxication_cases = df[intoxication_column].notna().sum()
    
    # Analyser les maladies liées
    disease_column = 'avez vous constaté une émergence de maladie liés à la production rizicole_1'
    disease_cases = (df[disease_column] == 'oui').sum()
    
    # Analyser les symptômes mentionnés
    symptom_column = 'comment ca se manifeste'
    symptoms = []
    for _, row in df.iterrows():
        if pd.notna(row[symptom_column]):
            symptoms.append(str(row[symptom_column]).lower())
    
    # Identifier les symptômes courants
    common_symptoms = ['intoxication', 'yeux', 'plaie', 'rhumatisme', 'respiratoire']
    symptom_counts = {symptom: sum(1 for s in symptoms if symptom in s) for symptom in common_symptoms}
    
    results = {
        'pesticide_types': dict(pesticide_counts.most_common(10)),
        'exposure_levels': {
            'high': (df['Pesticide_exposure_score'] > 50).sum(),
            'medium': ((df['Pesticide_exposure_score'] > 20) & (df['Pesticide_exposure_score'] <= 50)).sum(),
            'low': (df['Pesticide_exposure_score'] <= 20).sum()
        },
        'protection_usage': {
            'adequate': (df['Protection_factor'] < 0.5).sum(),
            'minimal': ((df['Protection_factor'] >= 0.5) & (df['Protection_factor'] < 1.0)).sum(),
            'none': (df['Protection_factor'] == 1.0).sum()
        },
        'health_impacts': {
            'intoxication_cases': intoxication_cases,
            'disease_emergence': disease_cases,
            'symptom_distribution': symptom_counts
        },
        'training': {
            'trained': (df['avez vous suivi une formation sur l\'utilisation des produits agrochimiques'] == 'oui').sum(),
            'not_trained': (df['avez vous suivi une formation sur l\'utilisation des produits agrochimiques'] == 'non').sum()
        }
    }
    
    return results

def analyze_fertilizer_exposure(df):
    """Analyse l'exposition aux engrais chimiques"""
    
    # Quantité d'engrais utilisée
    fertilizer_column = 'quelle quantite d\'engrais chimique utiliser vous'
    
    # Nettoyer les données d'engrais
    df['fertilizer_quantity_clean'] = pd.to_numeric(df[fertilizer_column], errors='coerce')
    
    # Catégoriser l'utilisation
    def categorize_fertilizer_use(quantity):
        if pd.isna(quantity):
            return 'non_specifie'
        elif quantity <= 3:
            return 'faible'
        elif quantity <= 6:
            return 'moyen'
        else:
            return 'eleve'
    
    df['fertilizer_category'] = df['fertilizer_quantity_clean'].apply(categorize_fertilizer_use)
    
    # Analyser les méthodes de gestion des déchets
    waste_column = 'que faites vous des contenants vides de produits agrochimiques (sacs, bidons) après usage'
    waste_methods = []
    
    for _, row in df.iterrows():
        if pd.notna(row[waste_column]):
            methods = str(row[waste_column]).lower().split(',')
            waste_methods.extend([m.strip() for m in methods])
    
    from collections import Counter
    waste_counts = Counter(waste_methods)
    
    # Identifier les pratiques dangereuses
    dangerous_practices = ['brûlé', 'enfouissement', 'canal', 'jeté']
    dangerous_waste_handling = sum(
        1 for method in waste_methods 
        if any(practice in method for practice in dangerous_practices)
    )
    
    results = {
        'fertilizer_usage': df['fertilizer_category'].value_counts().to_dict(),
        'average_quantity': df['fertilizer_quantity_clean'].mean(),
        'waste_management': dict(waste_counts.most_common()),
        'dangerous_practices_count': dangerous_waste_handling,
        'has_collection_system': (df['avez vous un systeme de collecte ou de traitement des déchets agricoles (matières organique) et agrochimiques (contenant des pesticides)'] != 'neant').sum()
    }
    
    return results

def analyze_vulnerable_groups(df):
    """Analyse l'exposition des groupes vulnérables"""
    
    # Enfants travaillant dans les exploitations
    child_labor = (df['Des enfants abandonnent ils  l\'école pour venir travailler dans votre exploitation'] == 'oui').sum()
    
    # Emploi de femmes et jeunes
    women_employed = df['employez vous /des femmes '].sum()
    youth_employed = df['employez vous /des jeunes'].sum()
    disabled_employed = df['employez vous /des personnes en situation de handicap'].sum()
    
    # Protection par groupe
    protection_by_group = {
        'women': df[df['employez vous /des femmes '] == 1]['Protection_factor'].mean(),
        'youth': df[df['employez vous /des jeunes'] == 1]['Protection_factor'].mean()
    }
    
    results = {
        'child_labor_cases': child_labor,
        'employment': {
            'women': women_employed,
            'youth': youth_employed,
            'disabled': disabled_employed
        },
        'average_protection_score': protection_by_group,
        'percentage_employing_vulnerable': {
            'women': (women_employed / len(df)) * 100,
            'youth': (youth_employed / len(df)) * 100,
            'children': (child_labor / len(df)) * 100
        }
    }
    
    return results

def generate_health_report(df):
    """Génère un rapport complet sur l'exposition sanitaire"""
    
    print("Analyse de l'exposition aux pesticides et engrais...")
    
    # Analyser l'exposition aux pesticides
    pesticide_exposure = analyze_pesticide_exposure(df)
    
    # Analyser l'exposition aux engrais
    fertilizer_exposure = analyze_fertilizer_exposure(df)
    
    # Analyser les groupes vulnérables
    vulnerable_groups = analyze_vulnerable_groups(df)
    
    report = {
        'pesticide_exposure': pesticide_exposure,
        'fertilizer_exposure': fertilizer_exposure,
        'vulnerable_groups': vulnerable_groups,
        'summary': {
            'high_exposure_count': pesticide_exposure['exposure_levels']['high'],
            'no_protection_count': pesticide_exposure['protection_usage']['none'],
            'untrained_count': pesticide_exposure['training']['not_trained'],
            'child_labor_rate': vulnerable_groups['percentage_employing_vulnerable']['children']
        }
    }
    
    # Afficher le résumé
    print("\n=== RÉSUMÉ DE L'EXPOSITION SANITAIRE ===")
    
    print(f"\n1. Exposition aux pesticides:")
    print(f"   - Agriculteurs à exposition élevée: {pesticide_exposure['exposure_levels']['high']}")
    print(f"   - Sans protection: {pesticide_exposure['protection_usage']['none']}")
    print(f"   - Non formés: {pesticide_exposure['training']['not_trained']}")
    print(f"   - Cas d'intoxication reportés: {pesticide_exposure['health_impacts']['intoxication_cases']}")
    
    print(f"\n2. Utilisation d'engrais chimiques:")
    print(f"   - Quantité moyenne: {fertilizer_exposure['average_quantity']:.1f} unités/ha")
    print(f"   - Pratiques dangereuses de gestion des déchets: {fertilizer_exposure['dangerous_practices_count']} cas")
    
    print(f"\n3. Groupes vulnérables:")
    print(f"   - Travail des enfants: {vulnerable_groups['percentage_employing_vulnerable']['children']:.1f}% des exploitations")
    print(f"   - Femmes employées: {vulnerable_groups['percentage_employing_vulnerable']['women']:.1f}%")
    print(f"   - Jeunes employés: {vulnerable_groups['percentage_employing_vulnerable']['youth']:.1f}%")
    
    return report

if __name__ == "__main__":
    from data_loader import prepare_data
    df = prepare_data()
    
    if df is not None:
        report = generate_health_report(df)