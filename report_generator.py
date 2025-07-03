"""
Générateur de rapport PDF complet
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
import os
from config import REPORTS_DIR, GRAPHS_DIR

class ReportGenerator:
    def __init__(self, filename="rapport_analyse_environnementale.pdf"):
        self.filename = REPORTS_DIR / filename
        self.doc = SimpleDocTemplate(str(self.filename), pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Styles personnalisés
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2E86AB'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2E86AB'),
            spaceAfter=12
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        )
    
    def add_title_page(self, report_data):
        """Ajoute la page de titre"""
        self.story.append(Spacer(1, 2*inch))
        
        title = Paragraph("ANALYSE ENVIRONNEMENTALE ET SANITAIRE<br/>DES PRATIQUES RIZICOLES", self.title_style)
        self.story.append(title)
        
        self.story.append(Spacer(1, 0.5*inch))
        
        subtitle = Paragraph("Projet TAAT2 - Évaluation d'Impact", self.heading_style)
        self.story.append(subtitle)
        
        self.story.append(Spacer(1, 2*inch))
        
        # Informations de base
        info_text = f"""
        <b>Date du rapport:</b> {datetime.now().strftime('%d/%m/%Y')}<br/>
        <b>Nombre d'agriculteurs enquêtés:</b> {report_data['impact']['summary']['total_farmers']}<br/>
        <b>Zones couvertes:</b> Vallée du fleuve Sénégal<br/>
        <b>Période d'enquête:</b> Juin-Juillet 2025
        """
        info = Paragraph(info_text, self.normal_style)
        self.story.append(info)
        
        self.story.append(PageBreak())
    
    def add_executive_summary(self, all_reports):
        """Ajoute le résumé exécutif"""
        self.story.append(Paragraph("RÉSUMÉ EXÉCUTIF", self.heading_style))
        
        summary_text = f"""
        Cette étude analyse les impacts environnementaux et sanitaires des pratiques rizicoles dans la vallée du fleuve Sénégal. 
        L'enquête a porté sur {all_reports['impact']['summary']['total_farmers']} agriculteurs et révèle des enjeux majeurs :
        
        <b>Principaux constats :</b><br/>
        • <b>Pratiques nuisibles:</b> {all_reports['impact']['summary']['main_harmful_practice']} est la pratique la plus répandue<br/>
        • <b>Déforestation:</b> {all_reports['impact']['summary']['deforestation_rate']:.1f}% des agriculteurs mentionnent des impacts<br/>
        • <b>Biodiversité:</b> {all_reports['impact']['summary']['biodiversity_impact_rate']:.1f}% reportent des impacts négatifs<br/>
        • <b>Eau:</b> Consommation moyenne de {all_reports['water']['summary']['average_consumption_m3']:,.0f} m³/ha<br/>
        • <b>Pesticides:</b> {all_reports['health']['summary']['untrained_count']} agriculteurs non formés à leur utilisation<br/>
        • <b>Protection:</b> {all_reports['health']['summary']['no_protection_count']} agriculteurs sans équipement de protection<br/>
        
        <b>Recommandations prioritaires :</b><br/>
        1. Formation urgente sur l'utilisation sécurisée des pesticides<br/>
        2. Promotion du Système de Riziculture Intensive (SRI)<br/>
        3. Mise en place de systèmes de collecte des déchets chimiques<br/>
        4. Protection renforcée des groupes vulnérables (femmes, jeunes)<br/>
        5. Programme de reboisement et conservation de la biodiversité
        """
        
        summary = Paragraph(summary_text, self.normal_style)
        self.story.append(summary)
        self.story.append(PageBreak())
    
    def add_methodology(self):
        """Ajoute la section méthodologie"""
        self.story.append(Paragraph("MÉTHODOLOGIE", self.heading_style))
        
        methodology_text = """
        <b>Collecte des données :</b><br/>
        Les données ont été collectées via des enquêtes terrain auprès des riziculteurs de la vallée du fleuve Sénégal 
        entre juin et juillet 2025. Un questionnaire structuré a permis de recueillir des informations sur :
        
        • Les pratiques agricoles et l'utilisation d'intrants<br/>
        • La consommation d'eau et les méthodes d'irrigation<br/>
        • L'exposition aux pesticides et les mesures de protection<br/>
        • Les impacts environnementaux observés<br/>
        • Les caractéristiques socio-démographiques<br/>
        
        <b>Analyse des données :</b><br/>
        L'analyse a porté sur l'identification des pratiques nuisibles, l'évaluation des impacts environnementaux, 
        l'analyse de l'exposition sanitaire et l'étude des corrélations socio-démographiques.
        """
        
        methodology = Paragraph(methodology_text, self.normal_style)
        self.story.append(methodology)
        self.story.append(Spacer(1, 0.5*inch))
    
    def add_section_with_image(self, title, content, image_name=None):
        """Ajoute une section avec texte et image optionnelle"""
        self.story.append(Paragraph(title, self.heading_style))
        self.story.append(Paragraph(content, self.normal_style))
        
        if image_name and os.path.exists(GRAPHS_DIR / image_name):
            self.story.append(Spacer(1, 0.2*inch))
            img = Image(str(GRAPHS_DIR / image_name), width=6*inch, height=4*inch)
            self.story.append(img)
            self.story.append(Spacer(1, 0.3*inch))
    
    def add_harmful_practices_section(self, report_data):
        """Ajoute la section sur les pratiques nuisibles"""
        practices = report_data['harmful_practices']
        
        content = "<b>Pratiques agricoles nuisibles identifiées :</b><br/><br/>"
        
        for practice, data in practices.items():
            if data['percentage'] > 20:  # Seuil significatif
                content += f"• <b>{data['description']}:</b> {data['percentage']:.1f}% des agriculteurs<br/>"
                content += f"  Impact: {data['impact']}<br/><br/>"
        
        self.add_section_with_image(
            "PRATIQUES AGRICOLES NUISIBLES",
            content,
            "pratiques_nuisibles.png"
        )
    
    def add_environmental_impact_section(self, report_data):
        """Ajoute la section sur les impacts environnementaux"""
        deforestation = report_data['deforestation']
        biodiversity = report_data['biodiversity']
        
        content = f"""
        <b>Déforestation :</b><br/>
        {deforestation['percentage']:.1f}% des agriculteurs mentionnent des activités de déforestation. 
        L'évolution des surfaces cultivées montre une augmentation de {deforestation['surface_evolution']['2023']} ha 
        en 2023 à {deforestation['surface_evolution']['2025']} ha en 2025.<br/><br/>
        
        <b>Impact sur la biodiversité :</b><br/>
        {biodiversity['percentage_negative_impact']:.1f}% des agriculteurs reportent un impact négatif sur la biodiversité. 
        Les agriculteurs utilisant des pesticides montrent un taux d'impact de {biodiversity['correlation_with_pesticides']['with_pesticides']:.1f}% 
        contre {biodiversity['correlation_with_pesticides']['without_pesticides']:.1f}% pour ceux n'en utilisant pas.
        """
        
        self.add_section_with_image(
            "IMPACTS ENVIRONNEMENTAUX",
            content,
            "deforestation_evolution.png"
        )
        
        self.add_section_with_image(
            "",
            "",
            "biodiversite_impact.png"
        )
    
    def add_health_exposure_section(self, report_data):
        """Ajoute la section sur l'exposition sanitaire"""
        pesticide = report_data['pesticide_exposure']
        fertilizer = report_data['fertilizer_exposure']
        vulnerable = report_data['vulnerable_groups']
        
        content = f"""
        <b>Exposition aux pesticides :</b><br/>
        • Agriculteurs à exposition élevée : {pesticide['exposure_levels']['high']}<br/>
        • Sans protection adéquate : {pesticide['protection_usage']['none']}<br/>
        • Non formés : {pesticide['training']['not_trained']}<br/>
        • Cas d'intoxication reportés : {pesticide['health_impacts']['intoxication_cases']}<br/><br/>
        
        <b>Utilisation d'engrais chimiques :</b><br/>
        Quantité moyenne utilisée : {fertilizer['average_quantity']:.1f} unités/ha<br/>
        Gestion dangereuse des déchets : {fertilizer['dangerous_practices_count']} cas<br/><br/>
        
        <b>Groupes vulnérables :</b><br/>
        • Travail des enfants : {vulnerable['percentage_employing_vulnerable']['children']:.1f}% des exploitations<br/>
        • Femmes employées : {vulnerable['percentage_employing_vulnerable']['women']:.1f}%<br/>
        • Jeunes employés : {vulnerable['percentage_employing_vulnerable']['youth']:.1f}%
        """
        
        self.add_section_with_image(
            "EXPOSITION SANITAIRE",
            content,
            "exposition_pesticides.png"
        )
    
    def add_water_usage_section(self, report_data):
        """Ajoute la section sur l'utilisation de l'eau"""
        consumption = report_data['consumption']
        irrigation = report_data['irrigation']
        management = report_data['management']
        
        content = f"""
        <b>Consommation d'eau :</b><br/>
        • Moyenne : {consumption['statistics']['mean']:,.0f} m³/ha<br/>
        • Volume total estimé : {consumption['total_estimation']['total_water_volume_m3']:,.0f} m³<br/>
        • Surconsommation (>16250 m³/ha) : {report_data['summary']['high_consumption_percentage']:.1f}% des agriculteurs<br/><br/>
        
        <b>Méthodes d'irrigation :</b><br/>
        • Pompage : {irrigation['efficiency_indicators']['pompage_percentage']:.1f}%<br/>
        • Énergie solaire : {irrigation['efficiency_indicators']['solar_energy_percentage']:.1f}%<br/>
        • Dépendance au fleuve Sénégal : {irrigation['efficiency_indicators']['river_dependency']:.1f}%<br/><br/>
        
        <b>Système de Riziculture Intensive (SRI) :</b><br/>
        • Connaissent et appliquent : {management['sri_adoption']['knows_and_applies']} agriculteurs<br/>
        • Connaissent mais n'appliquent pas : {management['sri_adoption']['knows_but_not_applied']} agriculteurs<br/>
        • Taux d'adoption : {report_data['summary']['sri_adoption_rate']:.1f}%
        """
        
        self.add_section_with_image(
            "UTILISATION DE L'EAU",
            content,
            "consommation_eau.png"
        )
    
    def add_correlation_section(self, report_data):
        """Ajoute la section sur les corrélations"""
        education = report_data['education']
        age = report_data['age']
        combined = report_data['combined_analysis']
        
        content = f"""
        <b>Corrélations identifiées :</b><br/>
        
        • <b>Niveau d'éducation :</b> {('Corrélation significative' if education['correlation_stats']['significant'] else 'Pas de corrélation significative')} 
        avec l'exposition aux pesticides (tendance {education['trend']})<br/><br/>
        
        • <b>Âge :</b> Coefficient de corrélation = {age['correlation_stats']['pearson_r']:.3f} 
        {('(significatif)' if age['correlation_stats']['significant'] else '(non significatif)')}<br/><br/>
        
        • <b>Profils à risque :</b> {combined['high_risk_profile']['count']} agriculteurs identifiés comme à haut risque<br/>
        Âge moyen : {combined['high_risk_profile']['avg_age']:.1f} ans<br/><br/>
        
        <b>Recommandations ciblées :</b><br/>
        """
        
        for key, rec in combined['targeted_recommendations'].items():
            if rec['target']:
                content += f"• {rec['message']}<br/>"
        
        self.add_section_with_image(
            "ANALYSE SOCIO-DÉMOGRAPHIQUE",
            content,
            "analyse_sociodemographique.png"
        )
    
    def add_recommendations(self):
        """Ajoute les recommandations finales"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("RECOMMANDATIONS", self.heading_style))
        
        recommendations = """
        <b>1. Formation et sensibilisation :</b><br/>
        • Mettre en place des programmes de formation obligatoires sur l'utilisation sécurisée des pesticides<br/>
        • Développer des supports pédagogiques adaptés aux agriculteurs peu scolarisés<br/>
        • Organiser des démonstrations pratiques sur le terrain<br/><br/>
        
        <b>2. Amélioration des pratiques agricoles :</b><br/>
        • Promouvoir activement le Système de Riziculture Intensive (SRI)<br/>
        • Encourager la rotation des cultures et l'utilisation de fertilisants organiques<br/>
        • Subventionner l'acquisition d'équipements de protection individuelle<br/><br/>
        
        <b>3. Gestion environnementale :</b><br/>
        • Établir un système de collecte et traitement des déchets agrochimiques<br/>
        • Créer des zones tampons autour des cours d'eau<br/>
        • Lancer un programme de reboisement des berges<br/><br/>
        
        <b>4. Gestion de l'eau :</b><br/>
        • Moderniser les systèmes d'irrigation pour réduire la consommation<br/>
        • Promouvoir l'utilisation de l'énergie solaire pour le pompage<br/>
        • Former les agriculteurs aux techniques d'irrigation économes<br/><br/>
        
        <b>5. Protection des groupes vulnérables :</b><br/>
        • Interdire strictement le travail des enfants dans les rizières<br/>
        • Fournir des équipements de protection adaptés aux femmes<br/>
        • Créer des programmes spécifiques pour les jeunes agriculteurs<br/><br/>
        
        <b>6. Suivi et évaluation :</b><br/>
        • Mettre en place un système de monitoring environnemental<br/>
        • Effectuer des contrôles réguliers de la qualité de l'eau<br/>
        • Créer une base de données pour suivre l'évolution des pratiques
        """
        
        self.story.append(Paragraph(recommendations, self.normal_style))
    
    def generate_report(self, all_reports):
        """Génère le rapport complet"""
        print("Génération du rapport PDF...")
        
        # Page de titre
        self.add_title_page(all_reports['impact'])
        
        # Résumé exécutif
        self.add_executive_summary(all_reports)
        
        # Méthodologie
        self.add_methodology()
        
        # Sections principales
        self.add_harmful_practices_section(all_reports['impact'])
        self.story.append(PageBreak())
        
        self.add_environmental_impact_section(all_reports['impact'])
        self.story.append(PageBreak())
        
        self.add_health_exposure_section(all_reports['health'])
        self.story.append(PageBreak())
        
        self.add_water_usage_section(all_reports['water'])
        self.story.append(PageBreak())
        
        self.add_correlation_section(all_reports['correlation'])
        
        # Recommandations
        self.add_recommendations()
        
        # Générer le PDF
        self.doc.build(self.story)
        print(f"✓ Rapport généré : {self.filename}")

def create_summary_table(all_reports):
    """Crée un tableau récapitulatif en format texte"""
    
    summary_file = REPORTS_DIR / "resume_executif.txt"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("RÉSUMÉ EXÉCUTIF - ANALYSE ENVIRONNEMENTALE ET SANITAIRE\n")
        f.write("="*60 + "\n\n")
        
        f.write("INDICATEURS CLÉS\n")
        f.write("-"*30 + "\n")
        f.write(f"Agriculteurs enquêtés: {all_reports['impact']['summary']['total_farmers']}\n")
        f.write(f"Taux de déforestation: {all_reports['impact']['summary']['deforestation_rate']:.1f}%\n")
        f.write(f"Impact sur biodiversité: {all_reports['impact']['summary']['biodiversity_impact_rate']:.1f}%\n")
        f.write(f"Consommation eau moyenne: {all_reports['water']['summary']['average_consumption_m3']:,.0f} m³/ha\n")
        f.write(f"Sans protection pesticides: {all_reports['health']['summary']['no_protection_count']} agriculteurs\n")
        f.write(f"Travail des enfants: {all_reports['health']['summary']['child_labor_rate']:.1f}%\n")
        f.write("\n")
        
        f.write("PRATIQUES NUISIBLES PRINCIPALES\n")
        f.write("-"*30 + "\n")
        for practice, data in all_reports['impact']['harmful_practices'].items():
            if data['percentage'] > 30:
                f.write(f"- {data['description']}: {data['percentage']:.1f}%\n")
        f.write("\n")
        
        f.write("RECOMMANDATIONS PRIORITAIRES\n")
        f.write("-"*30 + "\n")
        f.write("1. Formation urgente sur utilisation sécurisée des pesticides\n")
        f.write("2. Promotion du Système de Riziculture Intensive (SRI)\n")
        f.write("3. Mise en place de systèmes de collecte des déchets chimiques\n")
        f.write("4. Protection renforcée des groupes vulnérables\n")
        f.write("5. Programme de reboisement et conservation biodiversité\n")
    
    print(f"✓ Résumé exécutif créé : {summary_file}")

if __name__ == "__main__":
    print("Module de génération de rapport prêt")
    print("Utilisez ReportGenerator().generate_report(all_reports) pour créer le rapport PDF")