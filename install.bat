@echo off
echo ========================================
echo  INSTALLATION - ANALYSEUR DE POKER
echo ========================================
echo.

echo Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo.
    echo Telechargez Python depuis : https://www.python.org/downloads/
    echo IMPORTANT : Cochez "Add Python to PATH" pendant l'installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python est installe
echo.

echo Installation des dependances...
python -m pip install --upgrade pip
python -m pip install reportlab

if errorlevel 1 (
    echo.
    echo [ERREUR] L'installation a echoue
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  INSTALLATION TERMINEE AVEC SUCCES !
echo ========================================
echo.
echo Pour lancer l'application :
echo   1. Double-cliquez sur "lancer.bat"
echo   2. Ou tapez : python poker_app_advanced.py
echo.
echo N'oubliez pas de configurer vos repertoires dans config.json
echo.
pause

@REM Made with Bob
