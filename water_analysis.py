"""
Analyse de la consommation d'eau dans la riziculture
"""
import pandas as pd
import numpy as np

def analyze_water_consumption(df):
    """Analyse la consommation d'eau par hectare"""
    
    # Statistiques de base
    water_stats = {
        'mean': df['Water_consumption_m3'].mean(),
        'median': df['Water_consumption_m3'].median(),
        'std': df['Water_consumption_m3'].std(),
        'min': df['Water_consumption_m3'].min(),
        'max': df['Water_consumption_m3'].max()
    }
    
    # Distribution par catégorie
    consumption_categories = {
        'Très faible (<10000 m³/ha)': (df['Water_consumption_m3'] < 10000).sum(),
        'Faible (10000-13000 m³/ha)': ((df['Water_consumption_m3'] >= 10000) & (df['Water_consumption_m3'] <= 13000)).sum(),
        'Moyenne (13001-16250 m³/ha)': ((df['Water_consumption_m3'] > 13000) & (df['Water_consumption_m3'] <= 16250)).sum(),
        'Élevée (>16250 m³/ha)': (df['Water_consumption_m3'] > 16250).sum()
    }
    
    # Calcul du volume total estimé
    total_surface = df['Superficie cultivée en 2025'].sum()
    total_water_volume = (df['Water_consumption_m3'] * df['Superficie cultivée en 2025']).sum()
    
    results = {
        'statistics': water_stats,
        'distribution': consumption_categories,
        'total_estimation': {
            'total_surface_ha': total_surface,
            'total_water_volume_m3': total_water_volume,
            'average_per_farm': total_water_volume / len(df) if len(df) > 0 else 0
        }
    }
    
    return results

def analyze_irrigation_methods(df):
    """Analyse les méthodes d'irrigation utilisées"""
    
    irrigation_columns = [
        'les types d\'irrigation utilisée /gravitaire',
        'les types d\'irrigation utilisée /pompage',
        'les types d\'irrigation utilisée /pluvial unique',
        'les types d\'irrigation utilisée /à la raie',
        'les types d\'irrigation utilisée /autres'
    ]
    
    irrigation_methods = {}
    for col in irrigation_columns:
        if col in df.columns:
            method = col.split('/')[-1].strip()
            irrigation_methods[method] = df[col].sum()
    
    # Sources d'eau
    water_sources_columns = [
        'origine de l\'eau /fleuve senegal',
        'origine de l\'eau /lac de guier',
        'origine de l\'eau /Forage',
        'origine de l\'eau /chenal',
        'origine de l\'eau /pluie',
        'origine de l\'eau /autre '
    ]
    
    water_sources = {}
    for col in water_sources_columns:
        if col in df.columns:
            source = col.split('/')[-1].strip()
            water_sources[source] = df[col].sum()
    
    # Types d'énergie pour l'irrigation
    energy_columns = [
        'Types d\'energie pour l\'irrigation pour /Gasoil',
        'Types d\'energie pour l\'irrigation pour /solaire',
        'Types d\'energie pour l\'irrigation pour /electricite',
        'Types d\'energie pour l\'irrigation pour /autre'
    ]
    
    energy_types = {}
    for col in energy_columns:
        if col in df.columns:
            energy = col.split('/')[-1].strip()
            energy_types[energy] = df[col].sum()
    
    results = {
        'irrigation_methods': irrigation_methods,
        'water_sources': water_sources,
        'energy_types': energy_types,
        'efficiency_indicators': {
            'pompage_percentage': (irrigation_methods.get('pompage', 0) / len(df)) * 100 if len(df) > 0 else 0,
            'solar_energy_percentage': (energy_types.get('solaire', 0) / len(df)) * 100 if len(df) > 0 else 0,
            'river_dependency': (water_sources.get('fleuve senegal', 0) / len(df)) * 100 if len(df) > 0 else 0
        }
    }
    
    return results

def analyze_water_management_practices(df):
    """Analyse les pratiques de gestion de l'eau"""
    
    # Connaissances du système SRI (System of Rice Intensification)
    sri_column = 'Avez vous connaissance du système de riziculture intensive qui consiste à produire avec moins d\'eau et d\'intrant agricole '
    sri_knowledge = {
        'knows_and_applies': 0,
        'knows_but_not_applied': 0,
        'does_not_know': 0
    }
    
    if sri_column in df.columns:
        sri_knowledge = {
            'knows_and_applies': (df[sri_column].str.contains('oui', case=False, na=False) & 
                                 ~df[sri_column].str.contains('pas appliqué', case=False, na=False)).sum(),
            'knows_but_not_applied': df[sri_column].str.contains('pas appliqué|pas utilisé', case=False, na=False).sum(),
            'does_not_know': (df[sri_column] == 'non').sum()
        }
    
    # État du système d'irrigation
    irrigation_system_issues = []
    system_column = 'comment jugez vous votre système d\'irrigation et de drainage'
    
    if system_column in df.columns:
        for _, row in df.iterrows():
            if pd.notna(row[system_column]):
                comment = str(row[system_column]).lower()
                issues = {
                    'ancien': 'ancien' in comment,
                    'manque_entretien': 'entretien' in comment,
                    'deficitaire': 'déficitaire' in comment or 'deficitaire' in comment,
                    'archaique': 'archaique' in comment or 'archaïque' in comment,
                    'pas_drainage': 'pas de drainage' in comment
                }
                irrigation_system_issues.append(issues)
    
    df_issues = pd.DataFrame(irrigation_system_issues) if irrigation_system_issues else pd.DataFrame()
    
    # Pratiques de conservation
    conservation_practices = {
        'zones_tampons': 0,
        'strategies_contamination': 0
    }
    
    zones_col = 'utilisez vous des pratiques pour limiter l\'impact de la riziculture sur l\'environnement en adoptant ces mesures/zones tamponspour proteger les cours d\'eau'
    strategies_col = 'utilisez vous des pratiques pour limiter l\'impact de la riziculture sur l\'environnement en adoptant ces mesures/strategies developpees pour eviter la contamination des eaux (digues, cordons, etc)'
    
    if zones_col in df.columns:
        conservation_practices['zones_tampons'] = df[zones_col].sum()
    if strategies_col in df.columns:
        conservation_practices['strategies_contamination'] = df[strategies_col].sum()
    
    # Gestion de la pollution de l'eau - CORRECTION ICI
    water_pollution_perception = {
        'eau_trouble': 0,
        'pesticide_residues': 0
    }
    
    # Vérifier la colonne eau trouble
    eau_trouble_col = 'comment decrivez vous la pollution de l\'eau(eau trouble, mauvaise odeur, etc)'
    if eau_trouble_col in df.columns:
        water_pollution_perception['eau_trouble'] = df[eau_trouble_col].str.contains('trouble', case=False, na=False).sum()
    
    # Vérifier les colonnes possibles pour les résidus de pesticides
    pesticide_residue_columns = [
        'votre zone est elle confrontée à la presence de residus de pesticides dans les canaux, expliquez_1',
        'votre zone est elle confrontée à la presence de residus de pesticides dans les canaux',
        'presence residus pesticides canaux',
        'residus pesticides'
    ]
    
    for col in pesticide_residue_columns:
        if col in df.columns:
            water_pollution_perception['pesticide_residues'] = (df[col] == 'oui').sum()
            break
    
    results = {
        'sri_adoption': sri_knowledge,
        'system_problems': {
            'ancien': df_issues['ancien'].sum() if len(df_issues) > 0 else 0,
            'manque_entretien': df_issues['manque_entretien'].sum() if len(df_issues) > 0 else 0,
            'deficitaire': df_issues['deficitaire'].sum() if len(df_issues) > 0 else 0,
            'archaique': df_issues['archaique'].sum() if len(df_issues) > 0 else 0,
            'pas_drainage': df_issues['pas_drainage'].sum() if len(df_issues) > 0 else 0
        },
        'conservation_practices': conservation_practices,
        'water_pollution_perception': water_pollution_perception
    }
    
    return results

def analyze_water_efficiency(df):
    """Analyse l'efficacité de l'utilisation de l'eau"""
    
    # Relation entre consommation d'eau et rendement
    # Approximation basée sur la rentabilité déclarée
    rentability_map = {
        'tres rentable': 3,
        'moyennement rentable': 2,
        'peu rentable': 1,
        'pas rentable': 0
    }
    
    rentability_column = 'comment notez vous la rentabilité de votre production'
    if rentability_column in df.columns:
        df['rentability_score'] = df[rentability_column].map(rentability_map).fillna(1)
    else:
        df['rentability_score'] = 1
    
    # Efficacité = rentabilité / consommation d'eau (normalisée)
    df['water_efficiency'] = df['rentability_score'] / (df['Water_consumption_m3'] / 10000)
    df['water_efficiency'] = df['water_efficiency'].replace([np.inf, -np.inf], 0).fillna(0)
    
    # Grouper par niveau de consommation
    efficiency_by_consumption = {
        'low_consumption': df[df['Water_consumption_m3'] < 13000]['water_efficiency'].mean(),
        'medium_consumption': df[(df['Water_consumption_m3'] >= 13000) & (df['Water_consumption_m3'] <= 16250)]['water_efficiency'].mean(),
        'high_consumption': df[df['Water_consumption_m3'] > 16250]['water_efficiency'].mean()
    }
    
    # Nombre de campagnes par an et consommation
    campaigns_col = 'Nombre de campagne par an'
    campaigns_water = {}
    if campaigns_col in df.columns:
        campaigns_water = df.groupby(campaigns_col)['Water_consumption_m3'].agg(['mean', 'count']).to_dict('index')
    
    results = {
        'average_efficiency': df['water_efficiency'].mean(),
        'efficiency_by_consumption': efficiency_by_consumption,
        'campaigns_impact': campaigns_water,
        'recommendations': {
            'need_efficiency_improvement': (df['water_efficiency'] < 1).sum(),
            'overconsumption_cases': (df['Water_consumption_m3'] > 16250).sum()
        }
    }
    
    return results

def generate_water_report(df):
    """Génère un rapport complet sur l'utilisation de l'eau"""
    
    print("Analyse de l'utilisation de l'eau dans la riziculture...")
    
    try:
        # Analyser la consommation
        consumption = analyze_water_consumption(df)
        
        # Analyser les méthodes d'irrigation
        irrigation = analyze_irrigation_methods(df)
        
        # Analyser les pratiques de gestion
        management = analyze_water_management_practices(df)
        
        # Analyser l'efficacité
        efficiency = analyze_water_efficiency(df)
        
        report = {
            'consumption': consumption,
            'irrigation': irrigation,
            'management': management,
            'efficiency': efficiency,
            'summary': {
                'average_consumption_m3': consumption['statistics']['mean'],
                'total_water_used_m3': consumption['total_estimation']['total_water_volume_m3'],
                'high_consumption_percentage': (consumption['distribution']['Élevée (>16250 m³/ha)'] / len(df)) * 100 if len(df) > 0 else 0,
                'sri_adoption_rate': (management['sri_adoption']['knows_and_applies'] / len(df)) * 100 if len(df) > 0 else 0,
                'irrigation_problems': sum(management['system_problems'].values())
            }
        }
        
        # Afficher le résumé
        print("\n=== RÉSUMÉ DE L'UTILISATION DE L'EAU ===")
        
        print(f"\n1. Consommation d'eau:")
        print(f"   - Consommation moyenne: {consumption['statistics']['mean']:,.0f} m³/ha")
        print(f"   - Volume total estimé: {consumption['total_estimation']['total_water_volume_m3']:,.0f} m³")
        print(f"   - Surconsommation (>16250 m³/ha): {report['summary']['high_consumption_percentage']:.1f}% des agriculteurs")
        
        print(f"\n2. Méthodes d'irrigation:")
        print(f"   - Pompage: {irrigation['efficiency_indicators']['pompage_percentage']:.1f}%")
        print(f"   - Énergie solaire: {irrigation['efficiency_indicators']['solar_energy_percentage']:.1f}%")
        print(f"   - Dépendance au fleuve Sénégal: {irrigation['efficiency_indicators']['river_dependency']:.1f}%")
        
        print(f"\n3. Gestion de l'eau:")
        print(f"   - Connaissance du SRI: {management['sri_adoption']['knows_and_applies'] + management['sri_adoption']['knows_but_not_applied']} agriculteurs")
        print(f"   - Application du SRI: {report['summary']['sri_adoption_rate']:.1f}%")
        print(f"   - Problèmes d'irrigation signalés: {report['summary']['irrigation_problems']} cas")
        
        print(f"\n4. Efficacité:")
        print(f"   - Score moyen d'efficacité: {efficiency['average_efficiency']:.2f}")
        print(f"   - Cas nécessitant amélioration: {efficiency['recommendations']['need_efficiency_improvement']}")
        
        return report
        
    except Exception as e:
        print(f"Erreur lors de l'analyse de l'eau: {str(e)}")
        # Retourner un rapport par défaut en cas d'erreur
        return {
            'consumption': {'statistics': {'mean': 0}, 'distribution': {}, 'total_estimation': {'total_water_volume_m3': 0}},
            'irrigation': {'irrigation_methods': {}, 'water_sources': {}, 'energy_types': {}, 'efficiency_indicators': {'pompage_percentage': 0, 'solar_energy_percentage': 0, 'river_dependency': 0}},
            'management': {'sri_adoption': {'knows_and_applies': 0, 'knows_but_not_applied': 0, 'does_not_know': 0}, 'system_problems': {}, 'conservation_practices': {}, 'water_pollution_perception': {}},
            'efficiency': {'average_efficiency': 0, 'efficiency_by_consumption': {}, 'campaigns_impact': {}, 'recommendations': {'need_efficiency_improvement': 0, 'overconsumption_cases': 0}},
            'summary': {'average_consumption_m3': 0, 'total_water_used_m3': 0, 'high_consumption_percentage': 0, 'sri_adoption_rate': 0, 'irrigation_problems': 0}
        }

if __name__ == "__main__":
    from data_loader import prepare_data
    df = prepare_data()
    
    if df is not None:
        report = generate_water_report(df)