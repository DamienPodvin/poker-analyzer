# 📦 Guide de Déploiement sur un Autre Ordinateur

## 🎯 Fichiers à Copier

### Fichiers Essentiels (OBLIGATOIRES)
```
✅ poker_analyzer.py          # Moteur d'analyse
✅ pdf_generator.py           # Générateur de PDF
✅ poker_app.py              # Application simple
✅ poker_app_advanced.py     # Application avancée
✅ config.json               # Configuration
✅ requirements_poker.txt    # Dépendances Python
```

### Scripts d'Installation (RECOMMANDÉS)
```
✅ install.bat               # Installation Windows
✅ lancer.bat               # Lanceur Windows
✅ install.sh               # Installation Mac/Linux
✅ lancer.sh                # Lanceur Mac/Linux
```

### Documentation (OPTIONNELLE mais recommandée)
```
✅ LISEZMOI.txt             # Instructions rapides
✅ INSTALLATION.md          # Guide d'installation complet
✅ README_POKER.md          # Documentation complète
✅ GUIDE_CONFIGURATION.md   # Guide de configuration
✅ DEPLOIEMENT.md           # Ce fichier
```

---

## 🚀 Méthodes de Déploiement

### Méthode 1 : Package ZIP (Recommandé)

#### Étape 1 : Créer le package
1. Crée un dossier `PokerAnalyzer`
2. Copie tous les fichiers listés ci-dessus
3. Compresse en ZIP : `PokerAnalyzer.zip`

#### Étape 2 : Partager
- Email
- Clé USB
- Cloud (Box, Dropbox, Google Drive)
- Réseau local

#### Étape 3 : Installation sur le nouvel ordinateur
1. Décompresse le ZIP
2. **Windows** : Double-clic sur `install.bat`
3. **Mac/Linux** : Terminal → `chmod +x install.sh && ./install.sh`
4. Édite `config.json` avec les bons chemins
5. Lance l'application

---

### Méthode 2 : Clé USB Portable

#### Créer une clé USB prête à l'emploi

**Structure de la clé :**
```
USB_PokerAnalyzer/
├── 📄 LISEZMOI.txt          ← À lire en premier !
├── 📁 Application/
│   ├── poker_analyzer.py
│   ├── pdf_generator.py
│   ├── poker_app.py
│   ├── poker_app_advanced.py
│   ├── config.json
│   └── requirements_poker.txt
├── 📁 Scripts/
│   ├── install.bat
│   ├── lancer.bat
│   ├── install.sh
│   └── lancer.sh
└── 📁 Documentation/
    ├── INSTALLATION.md
    ├── README_POKER.md
    └── GUIDE_CONFIGURATION.md
```

**Instructions pour l'utilisateur :**
1. Copie le dossier `Application` sur ton ordinateur
2. Copie les scripts d'installation dans le même dossier
3. Lance `install.bat` (Windows) ou `install.sh` (Mac/Linux)
4. Configure `config.json`
5. Lance l'application

---

### Méthode 3 : Cloud (Box, Dropbox, etc.)

#### Étape 1 : Upload
1. Crée un dossier partagé dans ton cloud
2. Upload tous les fichiers
3. Partage le lien

#### Étape 2 : Instructions pour l'utilisateur
```
1. Télécharge tous les fichiers depuis le lien
2. Place-les dans un dossier (ex: C:\PokerAnalyzer)
3. Double-clic sur install.bat (Windows) ou lance install.sh (Mac/Linux)
4. Édite config.json avec tes chemins
5. Lance lancer.bat ou lancer.sh
```

---

## ⚙️ Configuration Initiale sur le Nouvel Ordinateur

### 1. Éditer config.json

**Avant (exemple de ton ordinateur) :**
```json
{
  "default_input_directory": "C:\\Users\\DamienPodvin\\Box\\...\\AnalyseMainPoker",
  "default_output_directory": "C:\\Users\\DamienPodvin\\Box\\...\\RapportsPDF",
  "default_hero_name": "Roll_Back",
  "auto_open_pdf": true,
  "language": "fr"
}
```

**Après (sur le nouvel ordinateur) :**
```json
{
  "default_input_directory": "C:\\Users\\NouvelUtilisateur\\Documents\\Poker\\Historiques",
  "default_output_directory": "C:\\Users\\NouvelUtilisateur\\Documents\\Poker\\Rapports",
  "default_hero_name": "NouveauPseudo",
  "auto_open_pdf": true,
  "language": "fr"
}
```

### 2. Créer les Répertoires

**Windows :**
```batch
mkdir "C:\Users\NouvelUtilisateur\Documents\Poker\Historiques"
mkdir "C:\Users\NouvelUtilisateur\Documents\Poker\Rapports"
```

**Mac/Linux :**
```bash
mkdir -p ~/Documents/Poker/Historiques
mkdir -p ~/Documents/Poker/Rapports
```

---

## 🧪 Test de l'Installation

### Checklist de Vérification

```bash
# 1. Vérifier Python
python --version
# Doit afficher : Python 3.8.x ou supérieur

# 2. Vérifier pip
pip --version
# Doit afficher la version de pip

# 3. Vérifier reportlab
python -c "import reportlab; print('OK')"
# Doit afficher : OK

# 4. Tester l'application
python poker_app_advanced.py
# Doit afficher le menu principal
```

---

## 📋 Instructions pour l'Utilisateur Final

### Version Courte (LISEZMOI.txt)

```
INSTALLATION RAPIDE
===================

WINDOWS :
1. Double-cliquez sur "install.bat"
2. Éditez "config.json" avec vos chemins
3. Double-cliquez sur "lancer.bat"

MAC/LINUX :
1. Terminal : chmod +x install.sh && ./install.sh
2. Éditez "config.json" avec vos chemins
3. Terminal : ./lancer.sh
```

### Version Détaillée (INSTALLATION.md)

Renvoie vers le fichier INSTALLATION.md pour :
- Résolution de problèmes
- Installation manuelle
- Configuration avancée
- Support multi-plateformes

---

## 🔄 Mise à Jour de l'Application

### Pour mettre à jour sur un ordinateur existant :

1. **Sauvegarde config.json** (important !)
2. Remplace tous les fichiers .py
3. Restaure ton config.json
4. Relance l'application

**Fichiers à remplacer lors d'une mise à jour :**
- poker_analyzer.py
- pdf_generator.py
- poker_app.py
- poker_app_advanced.py

**Fichiers à NE PAS remplacer :**
- config.json (contient ta configuration personnelle)

---

## 🌐 Déploiement Multi-Utilisateurs

### Scénario : Plusieurs personnes utilisent l'application

#### Option 1 : Installation Individuelle
Chaque utilisateur :
1. Installe l'application dans son dossier personnel
2. Configure son propre config.json
3. Utilise ses propres répertoires

#### Option 2 : Installation Partagée
1. Installe l'application dans un dossier partagé
2. Chaque utilisateur crée son propre config.json :
   - `config_user1.json`
   - `config_user2.json`
3. Lance avec : `python poker_app.py --config config_user1.json`

---

## 💾 Sauvegarde et Portabilité

### Sauvegarder ta Configuration

**Fichiers à sauvegarder :**
```
✅ config.json              # Ta configuration personnelle
✅ Rapports PDF générés     # Tes analyses
```

**Fichiers à ne pas sauvegarder :**
```
❌ Fichiers .py             # Code source (peut être re-téléchargé)
❌ __pycache__/            # Cache Python
```

### Créer une Sauvegarde Complète

```bash
# Windows
xcopy /E /I PokerAnalyzer PokerAnalyzer_Backup

# Mac/Linux
cp -r PokerAnalyzer PokerAnalyzer_Backup
```

---

## 🆘 Résolution de Problèmes Courants

### "Python n'est pas reconnu"
**Solution :** Réinstalle Python en cochant "Add to PATH"

### "Module reportlab not found"
**Solution :** `pip install reportlab`

### "Permission denied" (Mac/Linux)
**Solution :** `chmod +x install.sh lancer.sh`

### Les chemins ne fonctionnent pas
**Solution :** Utilise des doubles backslash sous Windows : `C:\\Users\\...`

### Le PDF ne s'ouvre pas
**Solution :** Vérifie `auto_open_pdf` dans config.json

---

## 📞 Support

### Avant de Déployer

✅ Teste l'application sur ton ordinateur
✅ Vérifie que tous les fichiers sont présents
✅ Crée un LISEZMOI.txt clair
✅ Inclus les scripts d'installation

### Après le Déploiement

✅ Demande à l'utilisateur de tester l'installation
✅ Vérifie que config.json est bien configuré
✅ Assure-toi que les répertoires existent
✅ Teste avec un fichier d'exemple

---

## ✅ Checklist de Déploiement

### Avant de Partager

- [ ] Tous les fichiers .py sont présents
- [ ] config.json est inclus (avec des chemins d'exemple)
- [ ] requirements_poker.txt est présent
- [ ] Scripts d'installation (install.bat/sh) sont inclus
- [ ] Scripts de lancement (lancer.bat/sh) sont inclus
- [ ] LISEZMOI.txt est clair et complet
- [ ] Documentation est incluse
- [ ] Application testée sur ton ordinateur

### Après Installation sur le Nouvel Ordinateur

- [ ] Python est installé
- [ ] reportlab est installé
- [ ] config.json est configuré avec les bons chemins
- [ ] Les répertoires d'entrée/sortie existent
- [ ] L'application se lance sans erreur
- [ ] Un test d'analyse fonctionne
- [ ] Le PDF est généré correctement

---

**Ton application est maintenant prête à être déployée ! 🚀**

Pour toute question, consulte INSTALLATION.md ou README_POKER.md