# 🎯 Filtrage par Type de Jeu

## Vue d'ensemble

L'analyseur de poker détecte automatiquement le type de jeu de chaque main et permet de filtrer les analyses par type spécifique.

## Types de jeu détectés

L'application reconnaît automatiquement les types suivants :

- **MTT** (Multi-Table Tournament) - Tournois classiques
- **Cash Game** - Parties d'argent
- **Expresso** - Tournois turbo Winamax
- **Sit & Go** - Tournois à table unique

## Configuration du filtre

### Via le menu Configuration

1. Lancez l'application : `python poker_app_advanced.py`
2. Sélectionnez **"3. Configuration"**
3. Choisissez **"5. Filtre type de jeu"**
4. Sélectionnez le type souhaité :
   - **1. Tous (all)** - Analyse toutes les mains (par défaut)
   - **2. MTT uniquement** - Uniquement les tournois MTT
   - **3. Cash Game uniquement** - Uniquement les parties cash
   - **4. Expresso uniquement** - Uniquement les Expressos
   - **5. Sit & Go uniquement** - Uniquement les Sit & Go

### Via le fichier config.json

Modifiez directement le paramètre `game_type_filter` :

```json
{
  "default_input_directory": "C:\\...",
  "default_output_directory": "C:\\...",
  "default_hero_name": "Roll_Back",
  "auto_open_pdf": true,
  "language": "fr",
  "game_type_filter": "MTT"
}
```

Valeurs possibles : `"all"`, `"MTT"`, `"Cash Game"`, `"Expresso"`, `"Sit & Go"`

## Fonctionnement

### Détection automatique

Le type de jeu est détecté à partir du nom du tournoi dans l'historique Winamax :

- **Expresso** : Contient "expresso" dans le nom
- **Cash Game** : Contient "cash" ou "cash game"
- **Sit & Go** : Contient "sit" et "go"
- **MTT** : Par défaut pour tous les autres tournois

### Application du filtre

Lors de l'analyse :

1. Toutes les mains sont d'abord extraites des fichiers
2. Le filtre est appliqué selon la configuration
3. Seules les mains du type sélectionné sont analysées
4. Le rapport PDF indique le nombre de mains par type

### Exemple de sortie

```
📖 [1/1] 20241215_AfterWork80K(202202155)_real_holdem_no-limit.txt
   ✅ 202 mains extraites

🔍 Filtre appliqué: MTT
   Mains avant filtre: 202
   Mains après filtre: 202

📊 Total: 202 mains à analyser
```

## Cas d'usage

### Analyser uniquement vos MTT

Idéal pour :
- Étudier votre jeu en tournoi
- Comparer vos performances MTT vs Cash
- Identifier les leaks spécifiques aux tournois

**Configuration** : `"game_type_filter": "MTT"`

### Analyser uniquement vos Expressos

Parfait pour :
- Optimiser votre stratégie Expresso
- Analyser les spots push/fold
- Suivre votre ROI en Expresso

**Configuration** : `"game_type_filter": "Expresso"`

### Analyser uniquement vos Cash Games

Utile pour :
- Améliorer votre jeu en cash
- Analyser les spots de value bet
- Étudier votre gestion de bankroll

**Configuration** : `"game_type_filter": "Cash Game"`

## Rapport PDF

Le rapport PDF généré inclut maintenant :

### Page de titre enrichie

```
🎯 ANALYSE DE SESSION POKER

Joueur: Roll_Back
Nombre de mains analysées: 202
Date du rapport: 17/04/2026 16:00
Types de jeu: MTT (202)
```

### Statistiques par type

Si vous analysez tous les types (`"all"`), le rapport affiche la répartition :

```
Types de jeu: MTT (150), Cash Game (30), Expresso (22)
```

## Avantages

✅ **Analyse ciblée** - Concentrez-vous sur un format spécifique
✅ **Comparaison** - Comparez vos performances entre formats
✅ **Optimisation** - Identifiez vos points forts par format
✅ **Flexibilité** - Changez de filtre à tout moment
✅ **Automatique** - Détection sans intervention manuelle

## Conseils

💡 **Astuce 1** : Analysez d'abord avec `"all"` pour voir la répartition de vos sessions

💡 **Astuce 2** : Créez des rapports séparés par type pour une analyse approfondie

💡 **Astuce 3** : Utilisez le filtre MTT pour préparer un tournoi important

💡 **Astuce 4** : Le filtre Cash Game est idéal pour analyser vos sessions régulières

## Dépannage

### Le filtre ne trouve aucune main

**Problème** : Message "Aucune main de type 'XXX' trouvée !"

**Solutions** :
1. Vérifiez que vos fichiers contiennent bien ce type de jeu
2. Utilisez `"all"` pour voir tous les types disponibles
3. Vérifiez l'orthographe dans config.json (sensible à la casse)

### Type de jeu mal détecté

**Problème** : Une main est classée dans le mauvais type

**Solution** : Le nom du tournoi dans l'historique Winamax détermine le type. Si nécessaire, contactez le support pour améliorer la détection.

## Mise à jour

Cette fonctionnalité a été ajoutée dans la version 2.1 de l'analyseur.

Pour mettre à jour depuis GitHub :
```bash
git pull origin master
```

---

**Besoin d'aide ?** Consultez le README_POKER.md ou ouvrez une issue sur GitHub.