"""
Module de visualisation des données
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from config import GRAPH_CONFIG, GRAPHS_DIR
import warnings
warnings.filterwarnings('ignore')

# Configuration de style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.size'] = GRAPH_CONFIG['font_size']
plt.rcParams['figure.figsize'] = GRAPH_CONFIG['figure_size']
plt.rcParams['figure.dpi'] = GRAPH_CONFIG['dpi']

def create_harmful_practices_chart(report_data):
    """Crée un graphique des pratiques agricoles nuisibles"""
    
    practices = report_data['harmful_practices']
    
    # Filtrer les pratiques significatives
    significant_practices = {k: v for k, v in practices.items() if v['percentage'] > 20}
    
    # Préparer les données
    labels = [v['description'] for v in significant_practices.values()]
    percentages = [v['percentage'] for v in significant_practices.values()]
    
    # Créer le graphique
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(labels, percentages, color=GRAPH_CONFIG['colors'][:len(labels)])
    
    # Ajouter les valeurs
    for bar, pct in zip(bars, percentages):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                f'{pct:.1f}%', va='center', fontsize=10)
    
    ax.set_xlabel('Pourcentage d\'agriculteurs (%)', fontsize=GRAPH_CONFIG['label_size'])
    ax.set_title('Pratiques Agricoles Nuisibles Identifiées', fontsize=GRAPH_CONFIG['title_size'], fontweight='bold')
    ax.set_xlim(0, 100)
    
    plt.tight_layout()
    plt.savefig(GRAPHS_DIR / 'pratiques_nuisibles.png', dpi=GRAPH_CONFIG['dpi'], bbox_inches='tight')
    plt.close()

def create_deforestation_evolution_chart(report_data):
    """Crée un graphique de l'évolution de la déforestation"""
    
    deforestation = report_data['deforestation']
    
    # Évolution des surfaces
    years = list(deforestation['surface_evolution'].keys())
    surfaces = list(deforestation['surface_evolution'].values())
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Graphique 1: Évolution des surfaces
    ax1.plot(years, surfaces, marker='o', linewidth=2, markersize=8, color=GRAPH_CONFIG['colors'][0])
    ax1.fill_between(years, surfaces, alpha=0.3, color=GRAPH_CONFIG['colors'][0])
    ax1.set_xlabel('Année', fontsize=GRAPH_CONFIG['label_size'])
    ax1.set_ylabel('Surface totale cultivée (ha)', fontsize=GRAPH_CONFIG['label_size'])
    ax1.set_title('Évolution des Surfaces Cultivées', fontsize=GRAPH_CONFIG['title_size'])
    ax1.grid(True, alpha=0.3)
    
    # Graphique 2: Mentions de déforestation
    keywords = dict(deforestation['keywords_frequency'])
    if keywords:
        ax2.bar(keywords.keys(), keywords.values(), color=GRAPH_CONFIG['colors'][1])
        ax2.set_xlabel('Mots-clés', fontsize=GRAPH_CONFIG['label_size'])
        ax2.set_ylabel('Fréquence', fontsize=GRAPH_CONFIG['label_size'])
        ax2.set_title('Mentions de Déforestation', fontsize=GRAPH_CONFIG['title_size'])
        ax2.tick_params(axis='x', rotation=45)
    
    plt.suptitle(f'Impact sur la Déforestation ({deforestation["percentage"]:.1f}% des agriculteurs concernés)', 
                 fontsize=GRAPH_CONFIG['title_size']+2, fontweight='bold')
    plt.tight_layout()
    plt.savefig(GRAPHS_DIR / 'deforestation_evolution.png', dpi=GRAPH_CONFIG['dpi'], bbox_inches='tight')
    plt.close()

def create_biodiversity_impact_chart(report_data):
    """Crée un graphique de l'impact sur la biodiversité"""
    
    biodiversity = report_data['biodiversity']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Graphique 1: Distribution des impacts
    impacts = biodiversity['impact_distribution']
    if impacts:
        labels = list(impacts.keys())
        values = list(impacts.values())
        colors = ['#E63946' if label in ['disparition', 'diminution', 'proliferation_negative'] 
                 else '#06D6A0' for label in labels]
        
        ax1.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribution des Impacts sur la Biodiversité', fontsize=GRAPH_CONFIG['title_size'])
    
    # Graphique 2: Corrélation avec pesticides
    correlation = biodiversity['correlation_with_pesticides']
    categories = ['Avec pesticides', 'Sans pesticides']
    values = [correlation['with_pesticides'], correlation['without_pesticides']]
    
    ax2.bar(categories, values, color=[GRAPH_CONFIG['colors'][2], GRAPH_CONFIG['colors'][3]])
    ax2.set_ylabel('Impact négatif (%)', fontsize=GRAPH_CONFIG['label_size'])
    ax2.set_title('Impact selon l\'Utilisation de Pesticides', fontsize=GRAPH_CONFIG['title_size'])
    ax2.set_ylim(0, 100)
    
    for i, v in enumerate(values):
        ax2.text(i, v + 2, f'{v:.1f}%', ha='center', fontsize=10)
    
    plt.suptitle('Impact sur la Biodiversité', fontsize=GRAPH_CONFIG['title_size']+2, fontweight='bold')
    plt.tight_layout()
    plt.savefig(GRAPHS_DIR / 'biodiversite_impact.png', dpi=GRAPH_CONFIG['dpi'], bbox_inches='tight')
    plt.close()

def create_pesticide_exposure_chart(report_data):
    """Crée un graphique de l'exposition aux pesticides"""
    
    pesticide = report_data['pesticide_exposure']
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Graphique 1: Niveaux d'exposition
    exposure_levels = pesticide['exposure_levels']
    labels = list(exposure_levels.keys())
    values = list(exposure_levels.values())
    colors = ['#E63946', '#F77F00', '#06D6A0']
    
    ax1.pie(values, labels=labels, colors=colors, autopct='%1.0f', startangle=90)
    ax1.set_title('Niveaux d\'Exposition aux Pesticides', fontsize=GRAPH_CONFIG['title_size'])
    
    # Graphique 2: Protection utilisée
    protection = pesticide['protection_usage']
    ax2.bar(protection.keys(), protection.values(), color=GRAPH_CONFIG['colors'][:3])
    ax2.set_ylabel('Nombre d\'agriculteurs', fontsize=GRAPH_CONFIG['label_size'])
    ax2.set_title('Utilisation d\'Équipements de Protection', fontsize=GRAPH_CONFIG['title_size'])
    
    # Graphique 3: Formation
    training = pesticide['training']
    ax3.pie(training.values(), labels=training.keys(), autopct='%1.0f', colors=['#06D6A0', '#E63946'])
    ax3.set_title('Formation sur l\'Utilisation des Pesticides', fontsize=GRAPH_CONFIG['title_size'])
    
    # Graphique 4: Symptômes reportés
    symptoms = pesticide['health_impacts']['symptom_distribution']
    if symptoms:
        ax4.barh(list(symptoms.keys()), list(symptoms.values()), color=GRAPH_CONFIG['colors'][1])
        ax4.set_xlabel('Nombre de cas', fontsize=GRAPH_CONFIG['label_size'])
        ax4.set_title('Symptômes d\'Exposition Reportés', fontsize=GRAPH_CONFIG['title_size'])
    
    plt.suptitle('Analyse de l\'Exposition aux Pesticides', fontsize=GRAPH_CONFIG['title_size']+2, fontweight='bold')
    plt.tight_layout()
    plt.savefig(GRAPHS_DIR / 'exposition_pesticides.png', dpi=GRAPH_CONFIG['dpi'], bbox_inches='tight')
    plt.close()

def create_water_consumption_chart(report_data):
    """Crée un graphique de la consommation d'eau"""
    
    water = report_data['consumption']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Graphique 1: Distribution de la consommation
    distribution = water['distribution']
    labels = list(distribution.keys())
    values = list(distribution.values())
    
    ax1.bar(range(len(labels)), values, color=GRAPH_CONFIG['colors'][:len(labels)])
    ax1.set_xticks(range(len(labels)))
    ax1.set_xticklabels(labels, rotation=45, ha='right')
    ax1.set_ylabel('Nombre d\'agriculteurs', fontsize=GRAPH_CONFIG['label_size'])
    ax1.set_title('Distribution de la Consommation d\'Eau', fontsize=GRAPH_CONFIG['title_size'])
    
    # Ajouter une ligne pour la moyenne
    mean_consumption = water['statistics']['mean']
    ax1.axhline(y=len(values)/4, color='red', linestyle='--', label=f'Moyenne: {mean_consumption:.0f} m³/ha')
    ax1.legend()
    
    # Graphique 2: Sources d'eau et méthodes d'irrigation
    irrigation = report_data['irrigation']
    sources = irrigation['water_sources']
    
    # Top 3 sources
    top_sources = dict(sorted(sources.items(), key=lambda x: x[1], reverse=True)[:3])
    
    ax2.pie(top_sources.values(), labels=top_sources.keys(), autopct='%1.1f%%', 
            colors=GRAPH_CONFIG['colors'][2:5])
    ax2.set_title('Principales Sources d\'Eau', fontsize=GRAPH_CONFIG['title_size'])
    
    plt.suptitle('Analyse de la Consommation d\'Eau dans la Riziculture', 
                 fontsize=GRAPH_CONFIG['title_size']+2, fontweight='bold')
    plt.tight_layout()
    plt.savefig(GRAPHS_DIR / 'consommation_eau.png', dpi=GRAPH_CONFIG['dpi'], bbox_inches='tight')
    plt.close()

def create_correlation_matrix(df):
    """Crée une matrice de corrélation"""
    
    # Sélectionner les variables pertinentes
    correlation_vars = [
        'Age_clean',
        'Education_level',
        'Pesticide_exposure_score',
        'Water_consumption_m3',
        'Protection_factor',
        'Soil_erosion_score'
    ]
    
    # Créer la matrice de corrélation
    corr_data = df[correlation_vars].corr()
    
    # Créer le graphique
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Heatmap
    mask = np.triu(np.ones_like(corr_data, dtype=bool))
    sns.heatmap(corr_data, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=1, cbar_kws={"shrink": .8})
    
    # Labels personnalisés
    labels = ['Âge', 'Éducation', 'Exposition\nPesticides', 'Consommation\nEau', 
              'Protection', 'Érosion\nSols']
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_yticklabels(labels, rotation=0)
    
    plt.title('Matrice de Corrélation des Facteurs Socio-Environnementaux', 
              fontsize=GRAPH_CONFIG['title_size'], fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(GRAPHS_DIR / 'correlation_matrix.png', dpi=GRAPH_CONFIG['dpi'], bbox_inches='tight')
    plt.close()

def create_sociodemographic_analysis(report_data):
    """Crée des graphiques d'analyse socio-démographique"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Graphique 1: Exposition par niveau d'éducation
    education = report_data['education']['by_education_level']
    ed_levels = list(education.keys())
    ed_exposure = [v['avg_exposure'] for v in education.values()]
    
    ax1.bar(ed_levels, ed_exposure, color=GRAPH_CONFIG['colors'][0])
    ax1.set_xlabel('Niveau d\'éducation', fontsize=GRAPH_CONFIG['label_size'])
    ax1.set_ylabel('Score moyen d\'exposition', fontsize=GRAPH_CONFIG['label_size'])
    ax1.set_title('Exposition aux Pesticides par Niveau d\'Éducation', fontsize=GRAPH_CONFIG['title_size'])
    ax1.tick_params(axis='x', rotation=45)
    
    # Graphique 2: Exposition par groupe d'âge
    age = report_data['age']['by_age_group']
    age_groups = list(age.keys())
    age_exposure = [v['avg_exposure'] for v in age.values()]
    
    ax2.bar(age_groups, age_exposure, color=GRAPH_CONFIG['colors'][1])
    ax2.set_xlabel('Groupe d\'âge', fontsize=GRAPH_CONFIG['label_size'])
    ax2.set_ylabel('Score moyen d\'exposition', fontsize=GRAPH_CONFIG['label_size'])
    ax2.set_title('Exposition aux Pesticides par Groupe d\'Âge', fontsize=GRAPH_CONFIG['title_size'])
    
    # Graphique 3: Protection par situation matrimoniale
    marital = report_data['marital_status']['by_marital_status']
    mar_status = list(marital.keys())
    mar_protection = [v['protection_usage'] for v in marital.values()]
    
    ax3.bar(mar_status, mar_protection, color=GRAPH_CONFIG['colors'][2])
    ax3.set_xlabel('Situation matrimoniale', fontsize=GRAPH_CONFIG['label_size'])
    ax3.set_ylabel('Utilisation de protection (%)', fontsize=GRAPH_CONFIG['label_size'])
    ax3.set_title('Protection par Situation Matrimoniale', fontsize=GRAPH_CONFIG['title_size'])
    ax3.tick_params(axis='x', rotation=45)
    
    # Graphique 4: Profil à risque
    risk_profile = report_data['combined_analysis']['high_risk_profile']
    ax4.text(0.1, 0.9, f'Profils à Haut Risque', fontsize=14, fontweight='bold', transform=ax4.transAxes)
    ax4.text(0.1, 0.7, f'Nombre total: {risk_profile["count"]}', fontsize=12, transform=ax4.transAxes)
    ax4.text(0.1, 0.5, f'Âge moyen: {risk_profile["avg_age"]:.1f} ans', fontsize=12, transform=ax4.transAxes)
    ax4.text(0.1, 0.3, 'Recommandations prioritaires:', fontsize=12, fontweight='bold', transform=ax4.transAxes)
    
    y_pos = 0.2
    for rec in report_data['combined_analysis']['targeted_recommendations'].values():
        if rec['target']:
            ax4.text(0.1, y_pos, f'• {rec["message"][:50]}...', fontsize=10, transform=ax4.transAxes)
            y_pos -= 0.08
    
    ax4.axis('off')
    
    plt.suptitle('Analyse Socio-Démographique et Exposition aux Risques', 
                 fontsize=GRAPH_CONFIG['title_size']+2, fontweight='bold')
    plt.tight_layout()
    plt.savefig(GRAPHS_DIR / 'analyse_sociodemographique.png', dpi=GRAPH_CONFIG['dpi'], bbox_inches='tight')
    plt.close()

def create_summary_dashboard(all_reports):
    """Crée un tableau de bord résumé"""
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Titre principal
    fig.suptitle('Tableau de Bord - Impacts Environnementaux et Sanitaires de la Riziculture', 
                 fontsize=16, fontweight='bold')
    
    # Indicateurs clés
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axis('off')
    
    # Calculer les indicateurs
    total_farmers = all_reports['impact']['summary']['total_farmers']
    deforestation_rate = all_reports['impact']['summary']['deforestation_rate']
    biodiversity_impact = all_reports['impact']['summary']['biodiversity_impact_rate']
    high_water_consumption = all_reports['water']['summary']['high_consumption_percentage']
    no_protection = (all_reports['health']['summary']['no_protection_count'] / total_farmers) * 100
    
    indicators = [
        ('Agriculteurs enquêtés', f'{total_farmers}'),
        ('Impact déforestation', f'{deforestation_rate:.1f}%'),
        ('Impact biodiversité', f'{biodiversity_impact:.1f}%'),
        ('Surconsommation eau', f'{high_water_consumption:.1f}%'),
        ('Sans protection', f'{no_protection:.1f}%')
    ]
    
    for i, (label, value) in enumerate(indicators):
        x = 0.1 + (i * 0.18)
        ax1.text(x, 0.7, value, fontsize=20, fontweight='bold', ha='center')
        ax1.text(x, 0.3, label, fontsize=12, ha='center')
    
    # Graphiques synthétiques
    # ... (ajouter d'autres visualisations selon les besoins)
    
    plt.savefig(GRAPHS_DIR / 'tableau_de_bord.png', dpi=GRAPH_CONFIG['dpi'], bbox_inches='tight')
    plt.close()

def generate_all_visualizations(df, all_reports):
    """Génère toutes les visualisations"""
    
    print("Génération des graphiques...")
    
    # Graphiques individuels
    create_harmful_practices_chart(all_reports['impact'])
    print("✓ Graphique des pratiques nuisibles créé")
    
    create_deforestation_evolution_chart(all_reports['impact'])
    print("✓ Graphique de déforestation créé")
    
    create_biodiversity_impact_chart(all_reports['impact'])
    print("✓ Graphique de biodiversité créé")
    
    create_pesticide_exposure_chart(all_reports['health'])
    print("✓ Graphique d'exposition aux pesticides créé")
    
    create_water_consumption_chart(all_reports['water'])
    print("✓ Graphique de consommation d'eau créé")
    
    create_correlation_matrix(df)
    print("✓ Matrice de corrélation créée")
    
    create_sociodemographic_analysis(all_reports['correlation'])
    print("✓ Analyse socio-démographique créée")
    
    create_summary_dashboard(all_reports)
    print("✓ Tableau de bord créé")
    
    print(f"\nTous les graphiques ont été sauvegardés dans : {GRAPHS_DIR}")

if __name__ == "__main__":
    print("Module de visualisation prêt à l'emploi")
    print("Utilisez generate_all_visualizations(df, all_reports) pour créer tous les graphiques")