"""
Script d'installation automatique des dépendances
"""
import subprocess
import sys
import os

def install_packages():
    """Installe tous les packages nécessaires"""
    
    print("="*60)
    print("INSTALLATION DES DÉPENDANCES DU PROJET")
    print("="*60)
    print()
    
    # Liste des packages à installer
    packages = [
        'pandas',
        'numpy', 
        'openpyxl',
        'matplotlib',
        'seaborn',
        'scipy',
        'reportlab'
    ]
    
    # Vérifier si nous sommes dans un environnement virtuel
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("⚠️  ATTENTION: Vous n'êtes pas dans un environnement virtuel!")
        print("Il est recommandé d'utiliser un environnement virtuel.")
        response = input("\nVoulez-vous continuer quand même? (o/n): ")
        if response.lower() != 'o':
            print("Installation annulée.")
            return
    
    print(f"\nPython utilisé: {sys.executable}")
    print(f"Version Python: {sys.version}")
    print()
    
    # Mettre à jour pip
    print("Mise à jour de pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✓ pip mis à jour")
    except subprocess.CalledProcessError:
        print("✗ Erreur lors de la mise à jour de pip")
    
    print("\nInstallation des packages...")
    print("-"*40)
    
    failed_packages = []
    
    for package in packages:
        print(f"\nInstallation de {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installé avec succès")
        except subprocess.CalledProcessError:
            print(f"✗ Erreur lors de l'installation de {package}")
            failed_packages.append(package)
    
    print("\n" + "="*60)
    
    if failed_packages:
        print("RÉSUMÉ: Installation partiellement réussie")
        print(f"Packages non installés: {', '.join(failed_packages)}")
        print("\nEssayez d'installer manuellement avec:")
        for pkg in failed_packages:
            print(f"  pip install {pkg}")
    else:
        print("RÉSUMÉ: Tous les packages ont été installés avec succès!")
        print("\nVous pouvez maintenant exécuter le projet avec:")
        print("  python main.py")
    
    print("="*60)

def check_installed_packages():
    """Vérifie quels packages sont déjà installés"""
    print("\nVérification des packages installés...")
    print("-"*40)
    
    packages_to_check = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'openpyxl': 'openpyxl',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'scipy': 'scipy',
        'reportlab': 'reportlab'
    }
    
    installed = []
    missing = []
    
    for display_name, import_name in packages_to_check.items():
        try:
            __import__(import_name)
            installed.append(display_name)
            print(f"✓ {display_name} est installé")
        except ImportError:
            missing.append(display_name)
            print(f"✗ {display_name} n'est pas installé")
    
    return installed, missing

if __name__ == "__main__":
    # Vérifier d'abord ce qui est installé
    installed, missing = check_installed_packages()
    
    if missing:
        print(f"\n{len(missing)} package(s) manquant(s): {', '.join(missing)}")
        response = input("\nVoulez-vous les installer maintenant? (o/n): ")
        if response.lower() == 'o':
            install_packages()
    else:
        print("\n✓ Tous les packages nécessaires sont déjà installés!")
        print("Vous pouvez exécuter le projet avec: python main.py")