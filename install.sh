#!/bin/bash

echo "========================================"
echo " INSTALLATION - ANALYSEUR DE POKER"
echo "========================================"
echo ""

# Vérifier Python
echo "Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python 3 n'est pas installé"
    echo ""
    echo "Installation de Python :"
    echo "  Mac: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo ""
    exit 1
fi

echo "[OK] Python est installé"
echo ""

# Vérifier pip
if ! command -v pip3 &> /dev/null; then
    echo "[ERREUR] pip3 n'est pas installé"
    echo "Installation: sudo apt install python3-pip"
    exit 1
fi

echo "Installation des dépendances..."
pip3 install --upgrade pip
pip3 install reportlab

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERREUR] L'installation a échoué"
    echo "Essayez: sudo pip3 install reportlab"
    echo ""
    exit 1
fi

echo ""
echo "========================================"
echo " INSTALLATION TERMINÉE AVEC SUCCÈS !"
echo "========================================"
echo ""
echo "Pour lancer l'application :"
echo "  ./lancer.sh"
echo "  ou: python3 poker_app_advanced.py"
echo ""
echo "N'oubliez pas de configurer vos répertoires dans config.json"
echo ""

# Made with Bob
