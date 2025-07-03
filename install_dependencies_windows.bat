@echo off
REM Script d'installation des dépendances pour Windows

echo =====================================
echo Installation des dependances Python
echo =====================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.8 ou superieur depuis python.org
    pause
    exit /b 1
)

echo [OK] Python detecte
python --version
echo.

REM Créer l'environnement virtuel si nécessaire
if not exist "env_analyse" (
    echo Creation de l'environnement virtuel...
    python -m venv env_analyse
    echo [OK] Environnement virtuel cree
    echo.
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call env_analyse\Scripts\activate.bat
echo [OK] Environnement virtuel active
echo.

REM Mettre à jour pip
echo Mise a jour de pip...
python -m pip install --upgrade pip
echo.

REM Installer les dépendances
echo Installation des packages necessaires...
echo -------------------------------------

REM Si requirements.txt existe, l'utiliser
if exist "requirements.txt" (
    echo Installation depuis requirements.txt...
    pip install -r requirements.txt
) else (
    REM Sinon, installer manuellement
    echo Installation manuelle des packages...
    
    pip install pandas
    pip install numpy
    pip install scipy
    pip install matplotlib
    pip install seaborn
    pip install openpyxl
    pip install reportlab
)

echo.
echo =====================================
echo Installation terminee!
echo =====================================
echo.
echo Pour activer l'environnement virtuel : env_analyse\Scripts\activate.bat
echo Pour lancer le projet : python main.py
echo.
pause