"""
Application avancée d'analyse de poker avec configuration
Supporte la configuration via config.json et le scan automatique de répertoires
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from poker_analyzer import WinamaxParser, HandAnalyzer
from pdf_generator import PokerPDFGenerator

# Configuration de l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class Config:
    """Gestion de la configuration de l'application"""
    
    DEFAULT_CONFIG = {
        "default_input_directory": "",
        "default_output_directory": "",
        "default_hero_name": "Roll_Back",
        "auto_open_pdf": True,
        "language": "fr"
    }
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Charge la configuration depuis le fichier JSON"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Fusionner avec les valeurs par défaut
                    return {**self.DEFAULT_CONFIG, **config}
            except Exception as e:
                print(f"⚠️  Erreur lors du chargement de la config: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Créer le fichier de config par défaut
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Dict = None):
        """Sauvegarde la configuration dans le fichier JSON"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"✅ Configuration sauvegardée dans {self.config_file}")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde de la config: {e}")
    
    def get(self, key: str, default=None):
        """Récupère une valeur de configuration"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Définit une valeur de configuration"""
        self.config[key] = value
        self.save_config()


def clear_screen():
    """Efface l'écran du terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Affiche l'en-tête de l'application"""
    clear_screen()
    print("=" * 70)
    print("🎯 ANALYSEUR DE POKER PROFESSIONNEL v2.0 🎯".center(70))
    print("=" * 70)
    print()


def scan_directory(directory: str, pattern: str = "*.txt") -> List[str]:
    """Scanne un répertoire pour trouver les fichiers d'historique"""
    if not os.path.exists(directory):
        return []
    
    files = []
    path = Path(directory)
    
    # Chercher les fichiers .txt
    for file in path.glob(pattern):
        if file.is_file():
            files.append(str(file))
    
    return sorted(files, key=lambda x: os.path.getmtime(x), reverse=True)


def configure_app(config: Config):
    """Menu de configuration de l'application"""
    print_header()
    print("⚙️  CONFIGURATION DE L'APPLICATION")
    print("-" * 70)
    print()
    
    filters = config.get('filters', {})
    
    print("Configuration actuelle:")
    print(f"  1. Répertoire d'entrée: {config.get('default_input_directory') or 'Non défini'}")
    print(f"  2. Répertoire de sortie: {config.get('default_output_directory') or 'Non défini'}")
    print(f"  3. Pseudo par défaut: {config.get('default_hero_name')}")
    print(f"  4. Ouvrir le PDF automatiquement: {config.get('auto_open_pdf')}")
    print(f"  5. Filtre type de jeu: {filters.get('game_type', 'all')}")
    print(f"  6. Filtre position: {filters.get('position', 'all')}")
    print(f"  7. Filtre type de pot: {filters.get('pot_type', 'all')}")
    print(f"  8. Filtre phase tournoi: {filters.get('tournament_phase', 'all')}")
    print()
    
    choice = input("Modifier un paramètre (1-8) ou Entrée pour continuer: ").strip()
    
    if choice == '1':
        new_dir = input("Nouveau répertoire d'entrée: ").strip().strip('"').strip("'")
        if os.path.exists(new_dir):
            config.set('default_input_directory', new_dir)
            print("✅ Répertoire d'entrée mis à jour")
        else:
            print("❌ Répertoire introuvable")
    
    elif choice == '2':
        new_dir = input("Nouveau répertoire de sortie: ").strip().strip('"').strip("'")
        # Créer le répertoire s'il n'existe pas
        os.makedirs(new_dir, exist_ok=True)
        config.set('default_output_directory', new_dir)
        print("✅ Répertoire de sortie mis à jour")
    
    elif choice == '3':
        new_name = input("Nouveau pseudo par défaut: ").strip()
        if new_name:
            config.set('default_hero_name', new_name)
            print("✅ Pseudo mis à jour")
    
    elif choice == '4':
        auto_open = input("Ouvrir le PDF automatiquement ? (O/n): ").strip().lower()
        config.set('auto_open_pdf', auto_open != 'n')
        print("✅ Paramètre mis à jour")
    
    elif choice == '5':
        print("\nTypes de jeu disponibles:")
        print("  1. Tous (all)")
        print("  2. MTT uniquement")
        print("  3. Cash Game uniquement")
        print("  4. Expresso uniquement")
        print("  5. Sit & Go uniquement")
        filter_choice = input("\nVotre choix (1-5): ").strip()
        
        filter_map = {
            '1': 'all',
            '2': 'MTT',
            '3': 'Cash Game',
            '4': 'Expresso',
            '5': 'Sit & Go'
        }
        
        if filter_choice in filter_map:
            filters = config.get('filters', {})
            filters['game_type'] = filter_map[filter_choice]
            config.set('filters', filters)
            print(f"✅ Filtre type de jeu mis à jour: {filter_map[filter_choice]}")
        else:
            print("❌ Choix invalide")
    
    elif choice == '6':
        print("\nPositions disponibles:")
        print("  1. Toutes (all)")
        print("  2. BTN (Bouton)")
        print("  3. CO (Cut-Off)")
        print("  4. MP (Middle Position)")
        print("  5. UTG (Under The Gun)")
        print("  6. SB (Small Blind)")
        print("  7. BB (Big Blind)")
        filter_choice = input("\nVotre choix (1-7): ").strip()
        
        position_map = {
            '1': 'all',
            '2': 'BTN',
            '3': 'CO',
            '4': 'MP',
            '5': 'UTG',
            '6': 'SB',
            '7': 'BB'
        }
        
        if filter_choice in position_map:
            filters = config.get('filters', {})
            filters['position'] = position_map[filter_choice]
            config.set('filters', filters)
            print(f"✅ Filtre position mis à jour: {position_map[filter_choice]}")
        else:
            print("❌ Choix invalide")
    
    elif choice == '7':
        print("\nTypes de pot disponibles:")
        print("  1. Tous (all)")
        print("  2. Ouverture (open) - Hero ouvre le pot")
        print("  3. 3bet - Pot 3-betté")
        print("  4. All-in préflop")
        print("  5. Gros pot (>30BB)")
        filter_choice = input("\nVotre choix (1-5): ").strip()
        
        pot_type_map = {
            '1': 'all',
            '2': 'open',
            '3': '3bet',
            '4': 'all_in_preflop',
            '5': 'big_pot'
        }
        
        if filter_choice in pot_type_map:
            filters = config.get('filters', {})
            filters['pot_type'] = pot_type_map[filter_choice]
            config.set('filters', filters)
            print(f"✅ Filtre type de pot mis à jour: {pot_type_map[filter_choice]}")
        else:
            print("❌ Choix invalide")
    
    elif choice == '8':
        print("\nPhases de tournoi disponibles:")
        print("  1. Toutes (all)")
        print("  2. Early (début - levels 1-5)")
        print("  3. Middle (milieu - levels 6-10)")
        print("  4. Late (fin - levels 11-15)")
        print("  5. Bubble (bulle - levels 16-20)")
        print("  6. ITM (In The Money - level 21+)")
        filter_choice = input("\nVotre choix (1-6): ").strip()
        
        phase_map = {
            '1': 'all',
            '2': 'early',
            '3': 'middle',
            '4': 'late',
            '5': 'bubble',
            '6': 'itm'
        }
        
        if filter_choice in phase_map:
            filters = config.get('filters', {})
            filters['tournament_phase'] = phase_map[filter_choice]
            config.set('filters', filters)
            print(f"✅ Filtre phase tournoi mis à jour: {phase_map[filter_choice]}")
        else:
            print("❌ Choix invalide")
    
    if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
        input("\nAppuyez sur Entrée pour continuer...")


def select_files_from_directory(config: Config) -> List[str]:
    """Permet de sélectionner des fichiers depuis le répertoire configuré"""
    input_dir = config.get('default_input_directory')
    
    if not input_dir or not os.path.exists(input_dir):
        print("⚠️  Répertoire d'entrée non configuré ou introuvable.")
        print("   Utilisez l'option 'Configuration' pour le définir.")
        return []
    
    print(f"\n📂 Scan du répertoire: {input_dir}")
    files = scan_directory(input_dir)
    
    if not files:
        print("❌ Aucun fichier .txt trouvé dans ce répertoire.")
        return []
    
    print(f"\n✅ {len(files)} fichier(s) trouvé(s):\n")
    
    for idx, file in enumerate(files[:20], 1):  # Limite à 20 fichiers
        file_name = Path(file).name
        file_size = os.path.getsize(file) / 1024  # Ko
        file_date = datetime.fromtimestamp(os.path.getmtime(file)).strftime('%d/%m/%Y %H:%M')
        print(f"  {idx:2d}. {file_name[:50]:<50} ({file_size:.1f} Ko) - {file_date}")
    
    if len(files) > 20:
        print(f"\n  ... et {len(files) - 20} autre(s) fichier(s)")
    
    print("\nOptions:")
    print("  - Entrez les numéros des fichiers à analyser (ex: 1,2,3)")
    print("  - Tapez 'all' pour analyser tous les fichiers")
    print("  - Tapez 'last' pour analyser le dernier fichier")
    print("  - Appuyez sur Entrée pour annuler")
    
    choice = input("\nVotre choix: ").strip().lower()
    
    if not choice:
        return []
    
    if choice == 'all':
        return files
    
    if choice == 'last':
        return [files[0]]
    
    # Parse les numéros
    try:
        indices = [int(x.strip()) - 1 for x in choice.split(',')]
        selected = [files[i] for i in indices if 0 <= i < len(files)]
        return selected
    except:
        print("❌ Format invalide")
        return []


def analyze_with_config(config: Config, files: List[str] = None):
    """Analyse les fichiers avec la configuration et filtres"""
    hero_name = config.get('default_hero_name')
    output_dir = config.get('default_output_directory')
    filters = config.get('filters', {})
    
    if not files:
        files = select_files_from_directory(config)
    
    if not files:
        print("\n❌ Aucun fichier sélectionné.")
        return False
    
    # Générer le nom du fichier de sortie
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"poker_analysis_{timestamp}.pdf"
    
    if output_dir and os.path.exists(output_dir):
        output_path = os.path.join(output_dir, output_filename)
    else:
        output_path = output_filename
    
    print(f"\n⚙️  Analyse en cours...")
    print("-" * 70)
    print(f"Joueur: {hero_name}")
    print(f"Fichiers: {len(files)}")
    print(f"Sortie: {output_path}")
    
    # Afficher les filtres actifs
    active_filters = []
    if filters.get('game_type', 'all') != 'all':
        active_filters.append(f"Type: {filters['game_type']}")
    if filters.get('position', 'all') != 'all':
        active_filters.append(f"Position: {filters['position']}")
    if filters.get('pot_type', 'all') != 'all':
        active_filters.append(f"Pot: {filters['pot_type']}")
    if filters.get('tournament_phase', 'all') != 'all':
        active_filters.append(f"Phase: {filters['tournament_phase']}")
    
    if active_filters:
        print(f"🔍 Filtres actifs: {', '.join(active_filters)}")
    print()
    
    # Parser tous les fichiers AVEC filtrage optimisé
    parser = WinamaxParser(hero_name, filters)
    all_hands = []
    
    for idx, file_path in enumerate(files, 1):
        print(f"📖 [{idx}/{len(files)}] {Path(file_path).name}")
        try:
            # Le parser applique déjà les filtres pendant le parsing
            hands = parser.parse_file(file_path)
            all_hands.extend(hands)
            print(f"   ✅ {len(hands)} mains extraites (après filtrage)")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    if not all_hands:
        print("\n❌ Aucune main trouvée correspondant aux filtres !")
        if active_filters:
            print("💡 Conseil: Essayez de désactiver certains filtres dans la configuration")
        return False
    
    print(f"\n📊 Total: {len(all_hands)} mains à analyser")
    
    # Analyser
    print("\n🔍 Analyse des mains...")
    analyzer = HandAnalyzer()
    stats = analyzer.analyze_hands(all_hands)
    
    print(f"   ✅ Analyse terminée")
    print(f"   • Mains gagnées: {stats['hands_won']}")
    print(f"   • Mains perdues: {stats['hands_lost']}")
    print(f"   • All-in: {stats['all_in_hands']}")
    
    # Générer le PDF
    print(f"\n📄 Génération du rapport PDF...")
    try:
        pdf_gen = PokerPDFGenerator(output_path)
        pdf_gen.generate_report(all_hands, analyzer, hero_name)
        print(f"   ✅ Rapport généré avec succès !")
        print(f"   📍 {os.path.abspath(output_path)}")
        
        # Ouvrir le PDF automatiquement si configuré
        if config.get('auto_open_pdf'):
            try:
                os.startfile(output_path)
                print(f"   📖 Ouverture du PDF...")
            except:
                pass
        
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def main_menu():
    """Menu principal de l'application"""
    config = Config()
    
    while True:
        print_header()
        print("MENU PRINCIPAL")
        print("-" * 70)
        print()
        print("1. Analyser des fichiers (sélection depuis le répertoire configuré)")
        print("2. Analyser un fichier spécifique (chemin manuel)")
        print("3. Configuration")
        print("4. Quitter")
        print()
        
        choice = input("Votre choix (1-4): ").strip()
        
        if choice == '1':
            analyze_with_config(config)
            input("\nAppuyez sur Entrée pour continuer...")
        
        elif choice == '2':
            file_path = input("\nChemin du fichier: ").strip().strip('"').strip("'")
            if os.path.exists(file_path):
                analyze_with_config(config, [file_path])
            else:
                print("❌ Fichier introuvable")
            input("\nAppuyez sur Entrée pour continuer...")
        
        elif choice == '3':
            configure_app(config)
        
        elif choice == '4':
            print("\n👋 Au revoir et bonne chance aux tables !")
            break
        
        else:
            print("❌ Choix invalide")
            input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n❌ Application interrompue.")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()

# Made with Bob
