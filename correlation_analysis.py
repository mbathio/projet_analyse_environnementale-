"""
Analyse des corrélations entre facteurs socio-démographiques et exposition aux pesticides
"""
import pandas as pd
import numpy as np
from scipy import stats

def analyze_education_correlation(df):
    """Analyse la corrélation entre niveau d'éducation et exposition aux pesticides"""
    
    # Grouper par niveau d'éducation
    education_exposure = df.groupby('niveau d\'instruction ').agg({
        'Pesticide_exposure_score': ['mean', 'std', 'count'],
        'Protection_factor': 'mean',
        'avez vous suivi une formation sur l\'utilisation des produits agrochimiques': lambda x: (x == 'oui').sum()
    })
    
    # Test statistique (ANOVA)
    education_groups = []
    for level in df['niveau d\'instruction '].unique():
        if pd.notna(level):
            group_scores = df[df['niveau d\'instruction '] == level]['Pesticide_exposure_score'].dropna()
            if len(group_scores) > 0:
                education_groups.append(group_scores)
    
    if len(education_groups) > 1:
        f_stat, p_value = stats.f_oneway(*education_groups)
    else:
        f_stat, p_value = np.nan, np.nan
    
    # Analyser les pratiques par niveau d'éducation
    education_practices = {}
    for level in df['niveau d\'instruction '].unique():
        if pd.notna(level):
            subset = df[df['niveau d\'instruction '] == level]
            education_practices[level] = {
                'sample_size': len(subset),
                'avg_exposure': subset['Pesticide_exposure_score'].mean(),
                'protection_usage': (subset['Protection_factor'] < 1.0).mean() * 100,
                'training_rate': (subset['avez vous suivi une formation sur l\'utilisation des produits agrochimiques'] == 'oui').mean() * 100,
                'safe_disposal': subset['que faites vous des contenants vides de produits agrochimiques (sacs, bidons) après usage'].str.contains('recyclage|collecte', case=False, na=False).mean() * 100
            }
    
    results = {
        'correlation_stats': {
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': p_value < 0.05 if not np.isnan(p_value) else False
        },
        'by_education_level': education_practices,
        'trend': 'negative' if df['Education_level'].corr(df['Pesticide_exposure_score']) < 0 else 'positive'
    }
    
    return results

def analyze_age_correlation(df):
    """Analyse la corrélation entre âge et exposition aux pesticides"""
    
    # Grouper par groupe d'âge
    age_exposure = df.groupby('Age_group').agg({
        'Pesticide_exposure_score': ['mean', 'std', 'count'],
        'Protection_factor': 'mean',
        'Uses_pesticides': 'mean'
    })
    
    # Corrélation linéaire avec l'âge
    age_mask = df['Age_clean'].notna() & df['Pesticide_exposure_score'].notna()
    if age_mask.sum() > 2:
        correlation, p_value = stats.pearsonr(
            df[age_mask]['Age_clean'], 
            df[age_mask]['Pesticide_exposure_score']
        )
    else:
        correlation, p_value = np.nan, np.nan
    
    # Analyser les pratiques par groupe d'âge
    age_practices = {}
    for group in df['Age_group'].unique():
        subset = df[df['Age_group'] == group]
        age_practices[group] = {
            'sample_size': len(subset),
            'avg_exposure': subset['Pesticide_exposure_score'].mean(),
            'pesticide_usage': subset['Uses_pesticides'].mean() * 100,
            'avg_age': subset['Age_clean'].mean() if group != 'Non spécifié' else np.nan,
            'protection_usage': (subset['Protection_factor'] < 1.0).mean() * 100
        }
    
    # Analyser l'expérience et l'exposition
    experience_exposure = df.groupby('Expérience en riziculture ')['Pesticide_exposure_score'].agg(['mean', 'count'])
    
    results = {
        'correlation_stats': {
            'pearson_r': correlation,
            'p_value': p_value,
            'significant': p_value < 0.05 if not np.isnan(p_value) else False
        },
        'by_age_group': age_practices,
        'by_experience': experience_exposure.to_dict('index')
    }
    
    return results

def analyze_marital_status_correlation(df):
    """Analyse la corrélation entre situation matrimoniale et exposition aux pesticides"""
    
    # Grouper par situation matrimoniale
    marital_exposure = df.groupby('Situation matrimoniale').agg({
        'Pesticide_exposure_score': ['mean', 'std', 'count'],
        'Protection_factor': 'mean',
        'employez vous /des femmes ': 'sum',
        'employez vous /des jeunes': 'sum'
    })
    
    # Test statistique (t-test entre mariés et non-mariés)
    married = df[df['Situation matrimoniale'] == 'marié.e']['Pesticide_exposure_score'].dropna()
    not_married = df[df['Situation matrimoniale'] != 'marié.e']['Pesticide_exposure_score'].dropna()
    
    if len(married) > 0 and len(not_married) > 0:
        t_stat, p_value = stats.ttest_ind(married, not_married)
    else:
        t_stat, p_value = np.nan, np.nan
    
    # Analyser les responsabilités familiales
    marital_practices = {}
    for status in df['Situation matrimoniale'].unique():
        if pd.notna(status):
            subset = df[df['Situation matrimoniale'] == status]
            marital_practices[status] = {
                'sample_size': len(subset),
                'avg_exposure': subset['Pesticide_exposure_score'].mean(),
                'employs_women': subset['employez vous /des femmes '].mean() * 100,
                'employs_youth': subset['employez vous /des jeunes'].mean() * 100,
                'child_labor': (subset['Des enfants abandonnent ils  l\'école pour venir travailler dans votre exploitation'] == 'oui').mean() * 100,
                'protection_usage': (subset['Protection_factor'] < 1.0).mean() * 100
            }
    
    results = {
        'correlation_stats': {
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05 if not np.isnan(p_value) else False
        },
        'by_marital_status': marital_practices
    }
    
    return results

def analyze_combined_factors(df):
    """Analyse l'interaction entre plusieurs facteurs"""
    
    # Créer un modèle simple d'exposition basé sur plusieurs facteurs
    factors_impact = {
        'education_weight': abs(df['Education_level'].corr(df['Pesticide_exposure_score'])),
        'age_weight': abs(df['Age_clean'].corr(df['Pesticide_exposure_score'])) if df['Age_clean'].notna().sum() > 2 else 0,
        'training_impact': df.groupby('avez vous suivi une formation sur l\'utilisation des produits agrochimiques')['Pesticide_exposure_score'].mean().to_dict()
    }
    
    # Identifier les profils à risque
    high_risk_profile = df[
        (df['Pesticide_exposure_score'] > 50) & 
        (df['Protection_factor'] >= 0.7)
    ]
    
    risk_profile_stats = {
        'count': len(high_risk_profile),
        'avg_age': high_risk_profile['Age_clean'].mean(),
        'education_distribution': high_risk_profile['niveau d\'instruction '].value_counts().to_dict(),
        'marital_distribution': high_risk_profile['Situation matrimoniale'].value_counts().to_dict()
    }
    
    # Recommandations par profil
    recommendations = {
        'young_farmers': {
            'target': df[df['Age_group'] == 'Jeune (18-35)']['Protection_factor'].mean() > 0.7,
            'message': "Formation intensive sur les risques des pesticides pour les jeunes agriculteurs"
        },
        'low_education': {
            'target': df[df['Education_level'] <= 1]['Pesticide_exposure_score'].mean() > 30,
            'message': "Programmes de sensibilisation adaptés pour les agriculteurs peu scolarisés"
        },
        'family_heads': {
            'target': df[df['Situation matrimoniale'] == 'marié.e']['employez vous /des femmes '].mean() > 0.5,
            'message': "Protection renforcée pour les exploitations familiales"
        }
    }
    
    results = {
        'factors_impact': factors_impact,
        'high_risk_profile': risk_profile_stats,
        'targeted_recommendations': recommendations
    }
    
    return results

def generate_correlation_report(df):
    """Génère un rapport complet sur les corrélations"""
    
    print("Analyse des corrélations socio-démographiques...")
    
    # Analyser chaque facteur
    education_corr = analyze_education_correlation(df)
    age_corr = analyze_age_correlation(df)
    marital_corr = analyze_marital_status_correlation(df)
    combined = analyze_combined_factors(df)
    
    report = {
        'education': education_corr,
        'age': age_corr,
        'marital_status': marital_corr,
        'combined_analysis': combined,
        'summary': {
            'significant_correlations': [],
            'high_risk_count': combined['high_risk_profile']['count'],
            'main_risk_factors': []
        }
    }
    
    # Identifier les corrélations significatives
    if education_corr['correlation_stats']['significant']:
        report['summary']['significant_correlations'].append('education')
    if age_corr['correlation_stats']['significant']:
        report['summary']['significant_correlations'].append('age')
    if marital_corr['correlation_stats']['significant']:
        report['summary']['significant_correlations'].append('marital_status')
    
    # Afficher le résumé
    print("\n=== RÉSUMÉ DES CORRÉLATIONS ===")
    
    print(f"\n1. Corrélation avec le niveau d'éducation:")
    print(f"   - Significative: {'Oui' if education_corr['correlation_stats']['significant'] else 'Non'}")
    print(f"   - Tendance: {'Moins d\\'exposition avec plus d\\'éducation' if education_corr['trend'] == 'negative' else 'Plus d\\'exposition avec plus d\\'éducation'}")
    
    print(f"\n2. Corrélation avec l'âge:")
    print(f"   - Coefficient de corrélation: {age_corr['correlation_stats']['pearson_r']:.3f}")
    print(f"   - Significative: {'Oui' if age_corr['correlation_stats']['significant'] else 'Non'}")
    
    print(f"\n3. Corrélation avec la situation matrimoniale:")
    print(f"   - Significative: {'Oui' if marital_corr['correlation_stats']['significant'] else 'Non'}")
    
    print(f"\n4. Profils à risque:")
    print(f"   - Nombre d'agriculteurs à haut risque: {combined['high_risk_profile']['count']}")
    print(f"   - Âge moyen: {combined['high_risk_profile']['avg_age']:.1f} ans")
    
    print(f"\n5. Recommandations prioritaires:")
    for key, rec in combined['targeted_recommendations'].items():
        if rec['target']:
            print(f"   - {rec['message']}")
    
    return report

if __name__ == "__main__":
    from data_loader import prepare_data
    df = prepare_data()
    
    if df is not None:
        report = generate_correlation_report(df)