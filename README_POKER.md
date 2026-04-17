# 🎯 Analyseur de Poker Professionnel

Application Python pour analyser vos historiques de mains Winamax et générer des rapports PDF détaillés avec recommandations.

## 📋 Fonctionnalités

- ✅ **Parse automatique** des fichiers d'historique Winamax
- 📊 **Statistiques détaillées** : win rate, performance par position, etc.
- 🎯 **Identification des mains critiques** : all-in, gros pots, décisions importantes
- 📄 **Rapport PDF professionnel** avec analyses et recommandations
- 🔄 **Support multi-fichiers** : analysez plusieurs sessions en une fois
- 🎮 **Filtrage par type de jeu** : MTT, Cash Game, Expresso, Sit & Go (NOUVEAU !)

## 🚀 Installation

### 1. Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### 2. Installation des dépendances

```bash
pip install -r requirements_poker.txt
```

Ou manuellement :
```bash
pip install reportlab
```

## 💻 Utilisation

### Mode interactif (recommandé)

Lancez l'application en mode interactif :

```bash
python poker_app.py
```

L'application vous guidera à travers les étapes :
1. Entrez votre pseudo Winamax
2. Sélectionnez les fichiers d'historique à analyser
3. Choisissez le nom du rapport PDF
4. Confirmez et lancez l'analyse

### Mode rapide (ligne de commande)

Pour une analyse rapide d'un seul fichier :

```bash
python poker_app.py "chemin/vers/fichier.txt" "VotrePseudo" "rapport.pdf"
```

Exemple :
```bash
python poker_app.py "C:\Users\...\historique.txt" "Roll_Back" "analyse_session.pdf"
```

### Utilisation en tant que module Python

```python
from poker_app import quick_analysis

# Analyse rapide
quick_analysis(
    file_path="chemin/vers/fichier.txt",
    hero_name="VotrePseudo",
    output_name="rapport.pdf"
)
```

## 📂 Format des fichiers

L'application supporte les fichiers d'historique Winamax au format texte (.txt).

**Où trouver vos historiques ?**
- Sur Winamax, allez dans : `Historique des mains` → `Exporter`
- Les fichiers sont généralement nommés : `YYYYMMDD_TOURNAMENT_NAME.txt`

## 📊 Contenu du rapport PDF

Le rapport généré contient :

### 1. Résumé exécutif
- Nombre total de mains
- Win rate global
- Statistiques de base (mains gagnées/perdues/foldées)
- Nombre de situations all-in
- Nombre de gros pots

### 2. Analyse des mains critiques
Pour chaque main importante :
- Contexte (level, blinds, position, stack)
- Cartes du héros
- Actions détaillées par street (préflop, flop, turn, river)
- Résultat
- Analyse et recommandations

### 3. Statistiques détaillées
- Performance par position (BTN, SB, BB, UTG, etc.)
- Win rate par position
- Distribution des résultats

### 4. Recommandations personnalisées
- Points forts identifiés
- Axes d'amélioration
- Conseils stratégiques
- Plan d'action

## 🎓 Exemples d'analyses

### Exemple 1 : Session MTT

```bash
python poker_app.py
```

**Entrées :**
- Pseudo : `Roll_Back`
- Fichier : `20241117_AFTER_WORK_FUNDAY_80K.txt`
- Sortie : `mtt_analysis_20241117.pdf`

**Résultat :** Rapport PDF de 10-15 pages avec analyse complète de la session.

### Exemple 2 : Analyse multi-sessions

Analysez plusieurs fichiers en une fois pour avoir une vue d'ensemble :

```bash
python poker_app.py
```

Ajoutez plusieurs fichiers quand demandé :
- `session1.txt`
- `session2.txt`
- `session3.txt`

## 🔧 Structure du projet

```
poker-analyzer/
│
├── poker_analyzer.py      # Parser et analyseur de mains
├── pdf_generator.py       # Générateur de rapports PDF
├── poker_app.py          # Application principale
├── requirements_poker.txt # Dépendances
└── README_POKER.md       # Ce fichier
```

## 📝 Modules

### `poker_analyzer.py`
- **WinamaxParser** : Parse les fichiers d'historique Winamax
- **HandAnalyzer** : Analyse les mains et identifie les patterns
- **Hand** : Dataclass représentant une main de poker

### `pdf_generator.py`
- **PokerPDFGenerator** : Génère des rapports PDF professionnels
- Styles personnalisés pour une présentation claire
- Tableaux et graphiques pour les statistiques

### `poker_app.py`
- Interface utilisateur interactive
- Mode ligne de commande
- Gestion des erreurs et validation

## 🎯 Conseils d'utilisation

1. **Exportez régulièrement** vos historiques depuis Winamax
2. **Analysez après chaque session** pour identifier rapidement les erreurs
3. **Comparez vos rapports** dans le temps pour suivre votre progression
4. **Concentrez-vous sur les mains critiques** identifiées par l'analyseur
5. **Appliquez les recommandations** pour améliorer votre jeu

## ⚠️ Limitations

- Supporte uniquement les fichiers Winamax (format texte)
- Analyse basée sur les actions visibles (pas d'accès aux cartes adverses non montrées)
- Recommandations générales (pas d'analyse GTO avancée)

## 🔮 Améliorations futures

- [ ] Support d'autres sites de poker (PokerStars, PartyPoker, etc.)
- [ ] Analyse GTO avec calculs d'équité
- [ ] Graphiques et visualisations avancées
- [ ] Base de données pour tracking long terme
- [ ] Interface graphique (GUI)
- [ ] Export en format Excel/CSV
- [ ] Comparaison avec des joueurs similaires

## 🐛 Résolution de problèmes

### Erreur : "Module reportlab not found"
```bash
pip install reportlab
```

### Erreur : "File not found"
Vérifiez que le chemin du fichier est correct. Utilisez des guillemets si le chemin contient des espaces :
```bash
python poker_app.py "C:\Users\Mon Dossier\fichier.txt"
```

### Le PDF ne s'ouvre pas
Assurez-vous d'avoir un lecteur PDF installé (Adobe Reader, Foxit, etc.)

### Aucune main trouvée
Vérifiez que :
- Le fichier est au bon format (export Winamax)
- Le pseudo entré correspond exactement à celui dans le fichier
- Le fichier n'est pas vide ou corrompu

## 📧 Support

Pour toute question ou suggestion d'amélioration, n'hésitez pas à me contacter.

## 📜 Licence

Ce projet est fourni "tel quel" à des fins éducatives et d'amélioration personnelle.

---

**Bonne analyse et bonne chance aux tables ! 🎰♠️♥️♣️♦️**