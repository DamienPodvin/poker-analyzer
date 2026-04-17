# 📖 Guide de Configuration - Analyseur de Poker

## 🎯 Configuration Rapide

### Étape 1 : Éditer le fichier `config.json`

Ouvre le fichier `config.json` avec un éditeur de texte et modifie les chemins :

```json
{
  "default_input_directory": "C:\\Ton\\Chemin\\Vers\\HistoriquesPoker",
  "default_output_directory": "C:\\Ton\\Chemin\\Vers\\RapportsPDF",
  "default_hero_name": "TonPseudo",
  "auto_open_pdf": true,
  "language": "fr"
}
```

### Étape 2 : Paramètres Expliqués

#### `default_input_directory`
- **Rôle** : Répertoire où se trouvent tes fichiers d'historique Winamax
- **Exemple** : `"C:\\Users\\TonNom\\Documents\\Winamax\\Historiques"`
- **Astuce** : Utilise des doubles backslash `\\` sous Windows

#### `default_output_directory`
- **Rôle** : Répertoire où seront sauvegardés les rapports PDF
- **Exemple** : `"C:\\Users\\TonNom\\Documents\\Poker\\Analyses"`
- **Note** : Le répertoire sera créé automatiquement s'il n'existe pas

#### `default_hero_name`
- **Rôle** : Ton pseudo Winamax par défaut
- **Exemple** : `"MonPseudo123"`
- **Important** : Doit correspondre exactement à ton pseudo sur Winamax

#### `auto_open_pdf`
- **Rôle** : Ouvrir automatiquement le PDF après génération
- **Valeurs** : `true` ou `false`
- **Recommandé** : `true` pour un accès immédiat

#### `language`
- **Rôle** : Langue de l'interface (futur)
- **Valeurs** : `"fr"` ou `"en"`

---

## 🚀 Utilisation Après Configuration

### Option 1 : Application Avancée (Recommandé)

```bash
python poker_app_advanced.py
```

**Avantages :**
- Menu interactif
- Scan automatique du répertoire configuré
- Sélection multiple de fichiers
- Configuration modifiable depuis l'application

**Workflow :**
1. Lance l'application
2. Choisis "1. Analyser des fichiers"
3. Sélectionne les fichiers à analyser (ex: `1,2,3` ou `last` ou `all`)
4. Le PDF est généré dans le répertoire configuré
5. Le PDF s'ouvre automatiquement

### Option 2 : Ligne de Commande Rapide

```bash
python poker_app.py "chemin/vers/fichier.txt" "TonPseudo"
```

**Avantages :**
- Ultra rapide
- Utilise automatiquement la config pour le répertoire de sortie
- Parfait pour scripter

---

## 📂 Organisation Recommandée

```
Documents/
├── Poker/
│   ├── Historiques/          ← default_input_directory
│   │   ├── session1.txt
│   │   ├── session2.txt
│   │   └── session3.txt
│   │
│   └── Analyses/             ← default_output_directory
│       ├── poker_analysis_20240117_190000.pdf
│       ├── poker_analysis_20240118_210000.pdf
│       └── poker_analysis_20240119_220000.pdf
```

---

## 🔧 Exemples de Configuration

### Configuration Windows (Box)
```json
{
  "default_input_directory": "C:\\Users\\DamienPodvin\\Box\\BoxPodvinDamien\\UtilisationIA\\AnalyseMainPoker",
  "default_output_directory": "C:\\Users\\DamienPodvin\\Box\\BoxPodvinDamien\\UtilisationIA\\AnalyseMainPoker\\RapportsPDF",
  "default_hero_name": "Roll_Back",
  "auto_open_pdf": true,
  "language": "fr"
}
```

### Configuration Windows (Documents)
```json
{
  "default_input_directory": "C:\\Users\\MonNom\\Documents\\Winamax\\Historiques",
  "default_output_directory": "C:\\Users\\MonNom\\Documents\\Poker\\Rapports",
  "default_hero_name": "MonPseudo",
  "auto_open_pdf": true,
  "language": "fr"
}
```

### Configuration Mac/Linux
```json
{
  "default_input_directory": "/Users/MonNom/Documents/Winamax/Historiques",
  "default_output_directory": "/Users/MonNom/Documents/Poker/Rapports",
  "default_hero_name": "MonPseudo",
  "auto_open_pdf": true,
  "language": "fr"
}
```

---

## ⚙️ Modifier la Configuration depuis l'Application

1. Lance `python poker_app_advanced.py`
2. Choisis option "3. Configuration"
3. Sélectionne le paramètre à modifier
4. Entre la nouvelle valeur
5. La configuration est sauvegardée automatiquement

---

## 🎯 Workflow Complet Recommandé

### 1. Configuration Initiale (Une seule fois)
```bash
# Édite config.json avec tes chemins
notepad config.json  # Windows
nano config.json     # Mac/Linux
```

### 2. Utilisation Quotidienne

**Après chaque session de poker :**

```bash
# Lance l'application
python poker_app_advanced.py

# Choisis option 1
# Sélectionne "last" pour analyser la dernière session
# Le PDF s'ouvre automatiquement
```

**Ou en ligne de commande :**

```bash
python poker_app.py "chemin/vers/derniere_session.txt" "TonPseudo"
```

### 3. Analyse Multi-Sessions

```bash
# Lance l'application avancée
python poker_app_advanced.py

# Choisis option 1
# Sélectionne "all" ou "1,2,3,4,5"
# Obtiens un rapport consolidé
```

---

## 🐛 Résolution de Problèmes

### Le répertoire de sortie n'existe pas
✅ **Solution** : L'application le crée automatiquement

### Les chemins ne fonctionnent pas
✅ **Solution** : Utilise des doubles backslash `\\` sous Windows
```json
"default_input_directory": "C:\\Users\\Nom\\Documents"
```

### Le PDF ne s'ouvre pas automatiquement
✅ **Solution** : Vérifie que `auto_open_pdf` est à `true` dans config.json

### Pseudo non trouvé dans les fichiers
✅ **Solution** : Vérifie que `default_hero_name` correspond exactement à ton pseudo Winamax

---

## 💡 Astuces Pro

### 1. Créer un raccourci
Crée un fichier `analyser.bat` (Windows) :
```batch
@echo off
cd C:\Chemin\Vers\Application
python poker_app_advanced.py
pause
```

### 2. Analyse automatique
Crée un script qui analyse automatiquement les nouveaux fichiers :
```python
import os
from poker_app import quick_analysis

input_dir = "C:\\Chemin\\Historiques"
for file in os.listdir(input_dir):
    if file.endswith('.txt'):
        quick_analysis(os.path.join(input_dir, file))
```

### 3. Organiser par date
Configure le répertoire de sortie avec des sous-dossiers par mois :
```json
"default_output_directory": "C:\\Poker\\Analyses\\2024\\Janvier"
```

---

**Tu es maintenant prêt à analyser tes sessions de poker comme un pro ! 🎰**