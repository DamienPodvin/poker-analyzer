@echo off
echo ========================================
echo  PUSH VERS GITHUB - POKER ANALYZER
echo ========================================
echo.

REM Configuration Git
echo Configuration de Git...
git config --global user.email "podvin.damien59@gmail.com"
git config --global user.name "Damien Podvin"

REM Ajout des fichiers
echo.
echo Ajout des fichiers au repository...
git add poker_analyzer.py
git add pdf_generator.py
git add poker_app.py
git add poker_app_advanced.py
git add config.json
git add requirements_poker.txt
git add install.bat
git add lancer.bat
git add install.sh
git add lancer.sh
git add README_POKER.md
git add GUIDE_CONFIGURATION.md
git add INSTALLATION.md
git add DEPLOIEMENT.md
git add .gitignore

REM Commit
echo.
echo Creation du commit...
git commit -m "Initial commit: Poker Analyzer v2.0 - Application complete d'analyse de poker avec rapports PDF"

REM Affichage des instructions pour GitHub
echo.
echo ========================================
echo  PROCHAINES ETAPES
echo ========================================
echo.
echo 1. Va sur https://github.com/new
echo 2. Nom du repository: poker-analyzer
echo 3. Description: Application d'analyse de mains de poker avec generation de rapports PDF
echo 4. Choisis: Public
echo 5. NE coche PAS "Initialize with README"
echo 6. Clique sur "Create repository"
echo.
echo 7. GitHub va te donner des commandes, utilise celles-ci:
echo.
echo    git remote add origin https://github.com/TON_USERNAME/poker-analyzer.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 8. Entre ton username GitHub et ton mot de passe quand demande
echo.
pause

@REM Made with Bob
