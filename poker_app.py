"""
Application principale d'analyse de poker
Interface utilisateur pour analyser des fichiers d'historique et générer des rapports PDF
"""

import os
import sys
from pathlib import Path
from poker_analyzer import WinamaxParser, HandAnalyzer
from pdf_generator import PokerPDFGenerator

# Configuration de l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def clear_screen():
    """Efface l'écran du terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Affiche l'en-tête de l'application"""
    clear_screen()
    print("=" * 70)
    print("🎯 ANALYSEUR DE POKER PROFESSIONNEL 🎯".center(70))
    print("=" * 70)
    print()


def get_hero_name() -> str:
    """Demande le nom du joueur à analyser"""
    print("📝 Configuration")
    print("-" * 70)
    hero_name = input("Entrez votre pseudo Winamax (par défaut: Roll_Back): ").strip()
    if not hero_name:
        hero_name = "Roll_Back"
    return hero_name


def get_input_files() -> list:
    """Demande les fichiers à analyser"""
    print("\n📂 Sélection des fichiers")
    print("-" * 70)
    print("Vous pouvez analyser un ou plusieurs fichiers d'historique.")
    print("Entrez les chemins des fichiers (un par ligne).")
    print("Appuyez sur Entrée deux fois pour terminer.")
    print()
    
    files = []
    while True:
        file_path = input(f"Fichier #{len(files) + 1} (ou Entrée pour terminer): ").strip()
        
        if not file_path:
            if files:
                break
            else:
                print("⚠️  Vous devez entrer au moins un fichier !")
                continue
        
        # Enlever les guillemets si présents
        file_path = file_path.strip('"').strip("'")
        
        if os.path.exists(file_path):
            files.append(file_path)
            print(f"   ✅ Fichier ajouté: {Path(file_path).name}")
        else:
            print(f"   ❌ Fichier introuvable: {file_path}")
    
    return files


def get_output_filename() -> str:
    """Demande le nom du fichier PDF de sortie"""
    print("\n💾 Nom du rapport PDF")
    print("-" * 70)
    default_name = f"poker_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output_name = input(f"Nom du fichier PDF (par défaut: {default_name}): ").strip()
    
    if not output_name:
        output_name = default_name
    
    if not output_name.endswith('.pdf'):
        output_name += '.pdf'
    
    return output_name


def analyze_files(files: list, hero_name: str, output_filename: str):
    """Analyse les fichiers et génère le rapport"""
    print("\n⚙️  Analyse en cours...")
    print("-" * 70)
    
    # Parser tous les fichiers
    parser = WinamaxParser(hero_name)
    all_hands = []
    
    for idx, file_path in enumerate(files, 1):
        print(f"📖 Lecture du fichier {idx}/{len(files)}: {Path(file_path).name}")
        try:
            hands = parser.parse_file(file_path)
            all_hands.extend(hands)
            print(f"   ✅ {len(hands)} mains extraites")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    if not all_hands:
        print("\n❌ Aucune main trouvée dans les fichiers !")
        return False
    
    print(f"\n📊 Total: {len(all_hands)} mains à analyser")
    
    # Analyser les mains
    print("\n🔍 Analyse des mains...")
    analyzer = HandAnalyzer()
    stats = analyzer.analyze_hands(all_hands)
    
    print(f"   ✅ Analyse terminée")
    print(f"   • Mains gagnées: {stats['hands_won']}")
    print(f"   • Mains perdues: {stats['hands_lost']}")
    print(f"   • All-in: {stats['all_in_hands']}")
    print(f"   • Gros pots: {stats['big_pots']}")
    
    # Générer le PDF
    print(f"\n📄 Génération du rapport PDF: {output_filename}")
    try:
        pdf_gen = PokerPDFGenerator(output_filename)
        pdf_gen.generate_report(all_hands, analyzer, hero_name)
        print(f"   ✅ Rapport généré avec succès !")
        print(f"   📍 Emplacement: {os.path.abspath(output_filename)}")
        return True
    except Exception as e:
        print(f"   ❌ Erreur lors de la génération du PDF: {e}")
        return False


def main():
    """Fonction principale"""
    from datetime import datetime
    
    print_header()
    
    print("Bienvenue dans l'analyseur de poker professionnel !")
    print("Cette application analyse vos historiques de mains Winamax")
    print("et génère un rapport PDF détaillé avec recommandations.")
    print()
    
    try:
        # Configuration
        hero_name = get_hero_name()
        files = get_input_files()
        output_filename = get_output_filename()
        
        # Confirmation
        print("\n✅ Configuration terminée")
        print("-" * 70)
        print(f"Joueur: {hero_name}")
        print(f"Fichiers à analyser: {len(files)}")
        for f in files:
            print(f"  • {Path(f).name}")
        print(f"Rapport PDF: {output_filename}")
        print()
        
        confirm = input("Lancer l'analyse ? (O/n): ").strip().lower()
        if confirm and confirm != 'o' and confirm != 'oui':
            print("\n❌ Analyse annulée.")
            return
        
        # Analyse
        success = analyze_files(files, hero_name, output_filename)
        
        if success:
            print("\n" + "=" * 70)
            print("✅ ANALYSE TERMINÉE AVEC SUCCÈS !".center(70))
            print("=" * 70)
            print(f"\nVotre rapport est disponible: {output_filename}")
            print("Bonne analyse et bonne chance aux tables ! 🎰")
        else:
            print("\n❌ L'analyse a échoué. Vérifiez les erreurs ci-dessus.")
    
    except KeyboardInterrupt:
        print("\n\n❌ Analyse interrompue par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()


def quick_analysis(file_path: str, hero_name: str = "Roll_Back", output_name: str = None, output_dir: str = None):
    """
    Fonction rapide pour analyser un fichier sans interface interactive
    
    Args:
        file_path: Chemin vers le fichier d'historique
        hero_name: Nom du joueur (défaut: Roll_Back)
        output_name: Nom du fichier PDF de sortie (optionnel)
        output_dir: Répertoire de sortie (optionnel, utilise config.json si disponible)
    """
    from datetime import datetime
    import json
    
    # Charger la config si disponible
    if output_dir is None and os.path.exists('config.json'):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                output_dir = config.get('default_output_directory', '')
        except:
            pass
    
    # Générer le nom du fichier si non fourni
    if not output_name:
        output_name = f"poker_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Construire le chemin complet
    if output_dir and os.path.exists(output_dir):
        output_path = os.path.join(output_dir, output_name)
    else:
        output_path = output_name
    
    print(f"🎯 Analyse rapide de {Path(file_path).name}")
    print(f"   Joueur: {hero_name}")
    print(f"   Sortie: {output_path}")
    print()
    
    try:
        # Parser
        parser = WinamaxParser(hero_name)
        hands = parser.parse_file(file_path)
        print(f"✅ {len(hands)} mains extraites")
        
        # Analyser
        analyzer = HandAnalyzer()
        stats = analyzer.analyze_hands(hands)
        print(f"✅ Analyse terminée")
        
        # Générer PDF
        pdf_gen = PokerPDFGenerator(output_path)
        pdf_gen.generate_report(hands, analyzer, hero_name)
        print(f"✅ Rapport PDF généré: {os.path.abspath(output_path)}")
        
        # Ouvrir le PDF automatiquement si configuré
        if os.path.exists('config.json'):
            try:
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if config.get('auto_open_pdf', False):
                        os.startfile(output_path)
                        print(f"📖 Ouverture du PDF...")
            except:
                pass
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Si des arguments sont passés en ligne de commande, utiliser le mode rapide
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        hero_name = sys.argv[2] if len(sys.argv) > 2 else "Roll_Back"
        output_name = sys.argv[3] if len(sys.argv) > 3 else None
        
        quick_analysis(file_path, hero_name, output_name)
    else:
        # Sinon, lancer l'interface interactive
        main()

# Made with Bob
