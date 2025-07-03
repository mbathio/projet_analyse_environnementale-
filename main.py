"""
Script principal pour l'analyse environnementale et sanitaire des pratiques rizicoles
"""
import sys
import warnings
warnings.filterwarnings('ignore')

from data_loader import prepare_data
from impact_analysis import generate_impact_report
from health_analysis import generate_health_report
from water_analysis import generate_water_report
from correlation_analysis import generate_correlation_report
from visualization import generate_all_visualizations
from report_generator import ReportGenerator, create_summary_table

def print_header():
    """Affiche l'en-tête du programme"""
    print("="*70)
    print("ANALYSE ENVIRONNEMENTALE ET SANITAIRE DES PRATIQUES RIZICOLES")
    print("Projet TAAT2 - Évaluation d'Impact")
    print("="*70)
    print()

def main():
    """Fonction principale"""
    print_header()
    
    # Étape 1: Chargement et nettoyage des données
    print("ÉTAPE 1: CHARGEMENT DES DONNÉES")
    print("-"*40)
    df = prepare_data()
    
    if df is None:
        print("✗ Erreur: Impossible de charger les données")
        sys.exit(1)
    
    print("\n" + "="*70 + "\n")
    
    # Étape 2: Analyses thématiques
    print("ÉTAPE 2: ANALYSES THÉMATIQUES")
    print("-"*40)
    
    # Analyse des impacts environnementaux
    print("\n>>> Analyse des impacts environnementaux...")
    impact_report = generate_impact_report(df)
    
    # Analyse de l'exposition sanitaire
    print("\n>>> Analyse de l'exposition sanitaire...")
    health_report = generate_health_report(df)
    
    # Analyse de l'utilisation de l'eau
    print("\n>>> Analyse de l'utilisation de l'eau...")
    water_report = generate_water_report(df)
    
    # Analyse des corrélations socio-démographiques
    print("\n>>> Analyse des corrélations socio-démographiques...")
    correlation_report = generate_correlation_report(df)
    
    print("\n" + "="*70 + "\n")
    
    # Compilation de tous les rapports
    all_reports = {
        'impact': impact_report,
        'health': health_report,
        'water': water_report,
        'correlation': correlation_report
    }
    
    # Étape 3: Génération des visualisations
    print("ÉTAPE 3: GÉNÉRATION DES VISUALISATIONS")
    print("-"*40)
    generate_all_visualizations(df, all_reports)
    
    print("\n" + "="*70 + "\n")
    
    # Étape 4: Génération du rapport final
    print("ÉTAPE 4: GÉNÉRATION DU RAPPORT FINAL")
    print("-"*40)
    
    # Générer le rapport PDF
    report_gen = ReportGenerator()
    report_gen.generate_report(all_reports)
    
    # Créer le résumé exécutif
    create_summary_table(all_reports)
    
    print("\n" + "="*70 + "\n")
    
    # Résumé final
    print("ANALYSE TERMINÉE AVEC SUCCÈS!")
    print("-"*40)
    print("\nFichiers générés:")
    print("✓ Données nettoyées: data/cleaned_data.csv")
    print("✓ Graphiques: resultats/graphiques/")
    print("✓ Rapport PDF: resultats/rapports/rapport_analyse_environnementale.pdf")
    print("✓ Résumé exécutif: resultats/rapports/resume_executif.txt")
    
    print("\n" + "="*70)
    print("\nRECOMMANDATIONS PRINCIPALES:")
    print("-"*40)
    print("1. Formation urgente sur l'utilisation sécurisée des pesticides")
    print(f"   → {health_report['summary']['untrained_count']} agriculteurs non formés")
    print("\n2. Réduction de la consommation d'eau")
    print(f"   → {water_report['summary']['high_consumption_percentage']:.1f}% en surconsommation")
    print("\n3. Protection de la biodiversité")
    print(f"   → {impact_report['summary']['biodiversity_impact_rate']:.1f}% d'impacts négatifs reportés")
    print("\n4. Élimination du travail des enfants")
    print(f"   → {health_report['summary']['child_labor_rate']:.1f}% des exploitations concernées")
    print("\n5. Gestion des déchets chimiques")
    print(f"   → Pratiques dangereuses dans la majorité des exploitations")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Analyse interrompue par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n✗ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)