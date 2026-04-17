# 🚀 Guide d'Installation - Analyseur de Poker

## 📋 Prérequis

### 1. Python
L'application nécessite **Python 3.8 ou supérieur**.

#### Vérifier si Python est installé :
```bash
python --version
```

#### Si Python n'est pas installé :

**Windows :**
1. Télécharge Python depuis [python.org](https://www.python.org/downloads/)
2. ⚠️ **IMPORTANT** : Coche "Add Python to PATH" pendant l'installation
3. Installe Python

**Mac :**
```bash
brew install python3
```

**Linux (Ubuntu/Debian) :**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## 📦 Installation sur un Nouvel Ordinateur

### Méthode 1 : Installation Automatique (Recommandé)

#### Windows
1. Copie tous les fichiers de l'application dans un dossier
2. Double-clique sur `install.bat`
3. Attends que l'installation se termine
4. C'est prêt !

#### Mac/Linux
1. Copie tous les fichiers de l'application dans un dossier
2. Ouvre un terminal dans ce dossier
3. Exécute :
```bash
chmod +x install.sh
./install.sh
```

### Méthode 2 : Installation Manuelle

#### Étape 1 : Copier les fichiers
Copie ces fichiers sur le nouvel ordinateur :
```
📁 PokerAnalyzer/
├── poker_analyzer.py
├── pdf_generator.py
├── poker_app.py
├── poker_app_advanced.py
├── config.json
├── requirements_poker.txt
├── README_POKER.md
├── GUIDE_CONFIGURATION.md
└── INSTALLATION.md (ce fichier)
```

#### Étape 2 : Installer les dépendances
Ouvre un terminal/invite de commandes dans le dossier et exécute :

```bash
pip install -r requirements_poker.txt
```

Ou manuellement :
```bash
pip install reportlab
```

#### Étape 3 : Configurer l'application
Édite `config.json` avec les chemins de ton nouvel ordinateur :

```json
{
  "default_input_directory": "C:\\Chemin\\Vers\\Historiques",
  "default_output_directory": "C:\\Chemin\\Vers\\Rapports",
  "default_hero_name": "TonPseudo",
  "auto_open_pdf": true,
  "language": "fr"
}
```

#### Étape 4 : Tester l'installation
```bash
python poker_app_advanced.py
```

---

## 🔧 Résolution de Problèmes

### Erreur : "python n'est pas reconnu"

**Windows :**
1. Réinstalle Python en cochant "Add Python to PATH"
2. Ou ajoute Python au PATH manuellement :
   - Cherche "Variables d'environnement" dans Windows
   - Ajoute le chemin de Python (ex: `C:\Python39\`)

**Mac/Linux :**
Utilise `python3` au lieu de `python` :
```bash
python3 poker_app_advanced.py
```

### Erreur : "pip n'est pas reconnu"

```bash
python -m pip install -r requirements_poker.txt
```

### Erreur : "Module reportlab not found"

```bash
python -m pip install reportlab
```

### Erreur : "Permission denied"

**Mac/Linux :**
```bash
sudo pip install -r requirements_poker.txt
```

---

## 📱 Installation sur Différents Systèmes

### Windows 10/11

1. **Télécharge Python** : [python.org](https://www.python.org/downloads/)
2. **Installe Python** (coche "Add to PATH")
3. **Copie les fichiers** de l'application
4. **Ouvre PowerShell** dans le dossier (Shift + Clic droit → "Ouvrir PowerShell ici")
5. **Installe les dépendances** :
   ```powershell
   pip install reportlab
   ```
6. **Lance l'application** :
   ```powershell
   python poker_app_advanced.py
   ```

### macOS

1. **Installe Homebrew** (si pas déjà fait) :
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. **Installe Python** :
   ```bash
   brew install python3
   ```
3. **Copie les fichiers** de l'application
4. **Ouvre Terminal** dans le dossier
5. **Installe les dépendances** :
   ```bash
   pip3 install reportlab
   ```
6. **Lance l'application** :
   ```bash
   python3 poker_app_advanced.py
   ```

### Linux (Ubuntu/Debian)

1. **Installe Python** :
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
2. **Copie les fichiers** de l'application
3. **Ouvre Terminal** dans le dossier
4. **Installe les dépendances** :
   ```bash
   pip3 install reportlab
   ```
5. **Lance l'application** :
   ```bash
   python3 poker_app_advanced.py
   ```

---

## 🎯 Vérification de l'Installation

### Test Rapide

```bash
# Vérifie Python
python --version

# Vérifie pip
pip --version

# Vérifie reportlab
python -c "import reportlab; print('ReportLab OK')"

# Lance l'application
python poker_app_advanced.py
```

Si tout fonctionne, tu verras le menu principal !

---

## 📦 Créer un Package Portable

### Pour Windows

Crée un dossier `PokerAnalyzer_Portable` avec :
```
PokerAnalyzer_Portable/
├── app/
│   ├── poker_analyzer.py
│   ├── pdf_generator.py
│   ├── poker_app.py
│   ├── poker_app_advanced.py
│   ├── config.json
│   └── requirements_poker.txt
│
├── docs/
│   ├── README_POKER.md
│   ├── GUIDE_CONFIGURATION.md
│   └── INSTALLATION.md
│
├── install.bat
└── lancer.bat
```

**install.bat** :
```batch
@echo off
echo Installation de l'Analyseur de Poker...
cd app
python -m pip install -r requirements_poker.txt
echo.
echo Installation terminee !
pause
```

**lancer.bat** :
```batch
@echo off
cd app
python poker_app_advanced.py
pause
```

### Pour Mac/Linux

Crée un fichier `lancer.sh` :
```bash
#!/bin/bash
cd app
python3 poker_app_advanced.py
```

Rends-le exécutable :
```bash
chmod +x lancer.sh
```

---

## 🌐 Partager l'Application

### Option 1 : Fichier ZIP
1. Compresse tous les fichiers dans un ZIP
2. Partage le ZIP
3. L'utilisateur décompresse et suit INSTALLATION.md

### Option 2 : Clé USB
1. Copie tous les fichiers sur une clé USB
2. Inclus un fichier `LISEZMOI.txt` avec les instructions

### Option 3 : Cloud (Box, Dropbox, etc.)
1. Upload tous les fichiers dans un dossier cloud
2. Partage le lien
3. L'utilisateur télécharge et installe

---

## 🔐 Checklist d'Installation

- [ ] Python 3.8+ installé
- [ ] pip fonctionnel
- [ ] reportlab installé
- [ ] Tous les fichiers .py copiés
- [ ] config.json configuré avec les bons chemins
- [ ] Application testée et fonctionnelle

---

## 💡 Conseils

### Pour une Installation Propre

1. **Crée un environnement virtuel** (optionnel mais recommandé) :
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   
   # Puis installe les dépendances
   pip install -r requirements_poker.txt
   ```

2. **Utilise toujours le même dossier** pour faciliter les mises à jour

3. **Sauvegarde ton config.json** avant toute mise à jour

---

## 🆘 Support

Si tu rencontres des problèmes :

1. Vérifie que Python est bien installé : `python --version`
2. Vérifie que reportlab est installé : `pip list | grep reportlab`
3. Vérifie les chemins dans config.json
4. Consulte la section "Résolution de Problèmes" ci-dessus

---

**L'installation est maintenant terminée ! 🎉**

Lance `python poker_app_advanced.py` pour commencer à analyser tes sessions !