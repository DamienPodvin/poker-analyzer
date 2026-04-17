"""
Analyseur de mains de poker Winamax
Génère un rapport PDF détaillé avec analyse des mains
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class Hand:
    """Représente une main de poker"""
    hand_id: str
    tournament: str
    game_type: str  # 'MTT', 'Cash Game', 'Expresso', 'Sit & Go'
    level: str
    blinds: str
    timestamp: str
    table: str
    button_seat: int
    hero_name: str
    hero_position: str
    hero_cards: Optional[str]
    hero_stack: int
    players: Dict[str, int]
    preflop_actions: List[str]
    flop: Optional[str]
    flop_actions: List[str]
    turn: Optional[str]
    turn_actions: List[str]
    river: Optional[str]
    river_actions: List[str]
    showdown: List[str]
    pot_size: int
    hero_result: str  # 'won', 'lost', 'folded'
    amount_won: int


class WinamaxParser:
    """Parse les fichiers d'historique Winamax"""
    
    def __init__(self, hero_name: str = "Roll_Back"):
        self.hero_name = hero_name
        self.hands: List[Hand] = []
    
    def parse_file(self, filepath: str) -> List[Hand]:
        """Parse un fichier d'historique complet"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Séparer les mains individuelles
        hand_texts = content.split('\n\n\n')
        
        for hand_text in hand_texts:
            if hand_text.strip():
                hand = self._parse_hand(hand_text)
                if hand and hand.hero_cards:  # Ne garde que les mains où Hero a joué
                    self.hands.append(hand)
        
        return self.hands
    
    def _parse_hand(self, text: str) -> Optional[Hand]:
        """Parse une main individuelle"""
        lines = text.strip().split('\n')
        if not lines:
            return None
        
        try:
            # Parse la première ligne (header)
            header = lines[0]
            hand_id_match = re.search(r'HandId: #([\w-]+)', header)
            tournament_match = re.search(r'Tournament "([^"]+)"', header)
            level_match = re.search(r'level: (\d+)', header)
            blinds_match = re.search(r'\((\d+/\d+/\d+)\)', header)
            timestamp_match = re.search(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})', header)
            
            if not all([hand_id_match, tournament_match, level_match, blinds_match]):
                return None
            
            hand_id = hand_id_match.group(1)
            tournament = tournament_match.group(1)
            level = level_match.group(1)
            blinds = blinds_match.group(1)
            timestamp = timestamp_match.group(1) if timestamp_match else ""
            
            # Détection du type de jeu
            game_type = self._detect_game_type(tournament, header)
            
            # Parse la table et le bouton
            table_line = lines[1]
            table_match = re.search(r"Table: '([^']+)'", table_line)
            button_match = re.search(r'Seat #(\d+)', table_line)
            table = table_match.group(1) if table_match else ""
            button_seat = int(button_match.group(1)) if button_match else 0
            
            # Parse les joueurs et leurs stacks
            players = {}
            hero_position = ""
            hero_stack = 0
            hero_seat = 0
            
            i = 2
            while i < len(lines) and lines[i].startswith('Seat'):
                seat_match = re.match(r'Seat (\d+): ([^\s]+) \((\d+)', lines[i])
                if seat_match:
                    seat_num = int(seat_match.group(1))
                    player_name = seat_match.group(2)
                    stack = int(seat_match.group(3))
                    players[player_name] = stack
                    
                    if player_name == self.hero_name:
                        hero_stack = stack
                        hero_seat = seat_num
                i += 1
            
            # Déterminer la position du héros
            hero_position = self._get_position(hero_seat, button_seat, len(players))
            
            # Parse les cartes du héros
            hero_cards = None
            for line in lines:
                if f"Dealt to {self.hero_name}" in line:
                    cards_match = re.search(r'\[([^\]]+)\]', line)
                    if cards_match:
                        hero_cards = cards_match.group(1)
                    break
            
            # Parse les actions par street
            preflop_actions = []
            flop = None
            flop_actions = []
            turn = None
            turn_actions = []
            river = None
            river_actions = []
            showdown = []
            
            current_street = "preflop"
            for line in lines:
                if "*** PRE-FLOP ***" in line:
                    current_street = "preflop"
                elif "*** FLOP ***" in line:
                    current_street = "flop"
                    flop_match = re.search(r'\[([^\]]+)\]', line)
                    if flop_match:
                        flop = flop_match.group(1)
                elif "*** TURN ***" in line:
                    current_street = "turn"
                    turn_match = re.search(r'\]\[([^\]]+)\]', line)
                    if turn_match:
                        turn = turn_match.group(1)
                elif "*** RIVER ***" in line:
                    current_street = "river"
                    river_match = re.search(r'\]\[([^\]]+)\]$', line)
                    if river_match:
                        river = river_match.group(1)
                elif "*** SHOW DOWN ***" in line:
                    current_street = "showdown"
                elif current_street == "preflop" and any(action in line for action in ['folds', 'calls', 'raises', 'bets', 'checks', 'all-in']):
                    preflop_actions.append(line.strip())
                elif current_street == "flop" and any(action in line for action in ['folds', 'calls', 'raises', 'bets', 'checks', 'all-in']):
                    flop_actions.append(line.strip())
                elif current_street == "turn" and any(action in line for action in ['folds', 'calls', 'raises', 'bets', 'checks', 'all-in']):
                    turn_actions.append(line.strip())
                elif current_street == "river" and any(action in line for action in ['folds', 'calls', 'raises', 'bets', 'checks', 'all-in']):
                    river_actions.append(line.strip())
                elif current_street == "showdown" and "shows" in line:
                    showdown.append(line.strip())
            
            # Parse le résultat
            pot_size = 0
            hero_result = "folded"
            amount_won = 0
            
            for line in lines:
                if "Total pot" in line:
                    pot_match = re.search(r'Total pot (\d+)', line)
                    if pot_match:
                        pot_size = int(pot_match.group(1))
                
                if f"{self.hero_name} collected" in line:
                    hero_result = "won"
                    amount_match = re.search(r'collected (\d+)', line)
                    if amount_match:
                        amount_won = int(amount_match.group(1))
                elif f"{self.hero_name} shows" in line and hero_result != "won":
                    hero_result = "lost"
            
            return Hand(
                hand_id=hand_id,
                tournament=tournament,
                game_type=game_type,
                level=level,
                blinds=blinds,
                timestamp=timestamp,
                table=table,
                button_seat=button_seat,
                hero_name=self.hero_name,
                hero_position=hero_position,
                hero_cards=hero_cards,
                hero_stack=hero_stack,
                players=players,
                preflop_actions=preflop_actions,
                flop=flop,
                flop_actions=flop_actions,
                turn=turn,
                turn_actions=turn_actions,
                river=river,
                river_actions=river_actions,
                showdown=showdown,
                pot_size=pot_size,
                hero_result=hero_result,
                amount_won=amount_won
            )
        
        except Exception as e:
            print(f"Erreur lors du parsing d'une main: {e}")
            return None
    
    def _detect_game_type(self, tournament: str, header: str) -> str:
        """Détecte le type de jeu à partir du nom du tournoi et du header"""
        tournament_lower = tournament.lower()
        header_lower = header.lower()
        
        # Détection Expresso
        if 'expresso' in tournament_lower or 'expresso' in header_lower:
            return 'Expresso'
        
        # Détection Cash Game
        if 'cash' in tournament_lower or 'cash game' in header_lower:
            return 'Cash Game'
        
        # Détection Sit & Go
        if 'sit' in tournament_lower and 'go' in tournament_lower:
            return 'Sit & Go'
        
        # Par défaut, considérer comme MTT si c'est un tournoi
        if 'tournament' in header_lower or 'mtt' in tournament_lower:
            return 'MTT'
        
        # Si aucune détection, retourner "Inconnu"
        return 'MTT'  # Par défaut MTT car la plupart des fichiers Winamax sont des tournois
    
    def _get_position(self, hero_seat: int, button_seat: int, num_players: int) -> str:
        """Détermine la position du joueur"""
        if num_players == 6:  # 6-max
            positions = {
                0: "BTN",
                1: "SB",
                2: "BB",
                3: "UTG",
                4: "MP",
                5: "CO"
            }
        else:  # Full ring (9 joueurs)
            positions = {
                0: "BTN",
                1: "SB",
                2: "BB",
                3: "UTG",
                4: "UTG+1",
                5: "MP",
                6: "MP+1",
                7: "HJ",
                8: "CO"
            }
        
        relative_pos = (hero_seat - button_seat) % num_players
        return positions.get(relative_pos, "Unknown")


class HandAnalyzer:
    """Analyse les mains de poker et identifie les erreurs/bons coups"""
    
    def __init__(self):
        self.critical_hands = []
        self.statistics = {
            'total_hands': 0,
            'hands_won': 0,
            'hands_lost': 0,
            'hands_folded': 0,
            'all_in_hands': 0,
            'big_pots': 0,
            'errors': 0,
            'good_plays': 0
        }
    
    def analyze_hands(self, hands: List[Hand]) -> Dict:
        """Analyse toutes les mains et génère des statistiques"""
        self.statistics['total_hands'] = len(hands)
        
        for hand in hands:
            # Statistiques de base
            if hand.hero_result == 'won':
                self.statistics['hands_won'] += 1
            elif hand.hero_result == 'lost':
                self.statistics['hands_lost'] += 1
            else:
                self.statistics['hands_folded'] += 1
            
            # Identifier les mains all-in
            all_actions = hand.preflop_actions + hand.flop_actions + hand.turn_actions + hand.river_actions
            if any('all-in' in action and hand.hero_name in action for action in all_actions):
                self.statistics['all_in_hands'] += 1
            
            # Identifier les gros pots (>30BB)
            blinds_parts = hand.blinds.split('/')
            bb = int(blinds_parts[2]) if len(blinds_parts) > 2 else 200
            if hand.pot_size > bb * 30:
                self.statistics['big_pots'] += 1
            
            # Analyser les décisions critiques
            analysis = self._analyze_hand(hand)
            if analysis['is_critical']:
                self.critical_hands.append({
                    'hand': hand,
                    'analysis': analysis
                })
        
        return self.statistics
    
    def _analyze_hand(self, hand: Hand) -> Dict:
        """Analyse stratégique détaillée d'une main"""
        analysis = {
            'is_critical': False,
            'type': '',
            'severity': '',  # 'error', 'good', 'neutral'
            'description': '',
            'recommendation': '',
            'preflop_analysis': '',
            'flop_analysis': '',
            'turn_analysis': '',
            'river_analysis': '',
            'strategic_notes': []
        }
        
        # Calculer les infos de base
        blinds_parts = hand.blinds.split('/')
        bb = int(blinds_parts[2]) if len(blinds_parts) > 2 else 200
        stack_bb = hand.hero_stack / bb if bb > 0 else 0
        
        # Vérifier si c'est une main all-in
        all_actions = hand.preflop_actions + hand.flop_actions + hand.turn_actions + hand.river_actions
        hero_all_in = any('all-in' in action and hand.hero_name in action for action in all_actions)
        
        # Identifier les mains critiques
        if hero_all_in or hand.pot_size > bb * 30:
            analysis['is_critical'] = True
            
            # Analyse préflop
            analysis['preflop_analysis'] = self._analyze_preflop(hand, stack_bb)
            
            # Analyse postflop
            if hand.flop:
                analysis['flop_analysis'] = self._analyze_flop(hand, stack_bb)
            
            if hand.turn:
                analysis['turn_analysis'] = self._analyze_turn(hand, stack_bb)
            
            if hand.river:
                analysis['river_analysis'] = self._analyze_river(hand, stack_bb)
            
            # Déterminer le type et la sévérité
            if hero_all_in:
                analysis['type'] = 'All-in'
                if hand.hero_result == 'won':
                    analysis['severity'] = 'good'
                    analysis['description'] = f"✅ All-in gagné avec {hand.hero_cards}"
                elif hand.hero_result == 'lost':
                    analysis['severity'] = 'error'
                    analysis['description'] = f"❌ All-in perdu avec {hand.hero_cards}"
                    # Analyser si c'était une erreur stratégique
                    if self._is_bad_allin(hand, stack_bb):
                        analysis['strategic_notes'].append("⚠️ All-in questionnable stratégiquement")
            else:
                analysis['type'] = 'Gros pot'
                analysis['severity'] = 'neutral'
            
            # Recommandations stratégiques
            analysis['recommendation'] = self._generate_recommendation(hand, stack_bb, analysis)
        
        return analysis
    
    def _analyze_preflop(self, hand: Hand, stack_bb: float) -> str:
        """Analyse les décisions préflop"""
        analysis = []
        
        # Identifier l'action du héros
        hero_actions = [a for a in hand.preflop_actions if hand.hero_name in a]
        
        if not hero_actions:
            return "Pas d'action préflop"
        
        # Analyser selon la position et le stack
        if stack_bb < 15:
            analysis.append(f"📊 Short stack ({stack_bb:.1f}BB) - Mode push/fold recommandé")
        elif stack_bb < 30:
            analysis.append(f"📊 Stack moyen ({stack_bb:.1f}BB) - Jouer tight-aggressive")
        else:
            analysis.append(f"📊 Stack confortable ({stack_bb:.1f}BB) - Possibilité de jouer postflop")
        
        # Analyser l'action
        for action in hero_actions:
            if 'raises' in action or 'all-in' in action:
                analysis.append(f"✅ Action agressive en {hand.hero_position}")
            elif 'calls' in action:
                analysis.append(f"⚠️ Call en {hand.hero_position} - Évaluer la range adverse")
            elif 'folds' in action:
                analysis.append(f"✅ Fold discipliné")
        
        return " | ".join(analysis)
    
    def _analyze_flop(self, hand: Hand, stack_bb: float) -> str:
        """Analyse les décisions au flop"""
        if not hand.flop:
            return ""
        
        analysis = []
        analysis.append(f"Board: {hand.flop}")
        
        # Analyser la texture du board
        cards = hand.flop.split()
        if len(cards) >= 3:
            # Board coordonné ou sec
            suits = [c[-1] for c in cards if len(c) >= 2]
            if len(set(suits)) == 1:
                analysis.append("⚠️ Board monotone - Attention aux tirages couleur")
            
            # Connectivité
            ranks = [c[:-1] for c in cards]
            if any(r in ['J', 'Q', 'K', 'A'] for r in ranks):
                analysis.append("📊 Board high - Favorise les ranges d'ouverture")
        
        # Actions du héros
        hero_actions = [a for a in hand.flop_actions if hand.hero_name in a]
        for action in hero_actions:
            if 'bets' in action or 'raises' in action:
                analysis.append("✅ Agression au flop")
            elif 'all-in' in action:
                analysis.append("⚠️ All-in au flop - Spot à variance élevée")
            elif 'checks' in action:
                analysis.append("📊 Check - Pot control ou piège?")
        
        return " | ".join(analysis)
    
    def _analyze_turn(self, hand: Hand, stack_bb: float) -> str:
        """Analyse les décisions à la turn"""
        if not hand.turn:
            return ""
        
        analysis = [f"Turn: {hand.turn}"]
        
        hero_actions = [a for a in hand.turn_actions if hand.hero_name in a]
        for action in hero_actions:
            if 'all-in' in action:
                analysis.append("⚠️ All-in à la turn - Décision critique")
            elif 'calls' in action and 'all-in' in action:
                analysis.append("⚠️ Call all-in - Pot odds et équité à évaluer")
        
        return " | ".join(analysis)
    
    def _analyze_river(self, hand: Hand, stack_bb: float) -> str:
        """Analyse les décisions à la river"""
        if not hand.river:
            return ""
        
        analysis = [f"River: {hand.river}"]
        
        hero_actions = [a for a in hand.river_actions if hand.hero_name in a]
        for action in hero_actions:
            if 'bets' in action:
                analysis.append("✅ Value bet ou bluff river")
            elif 'calls' in action:
                analysis.append("📊 Call river - Hero call ou pot odds?")
            elif 'folds' in action:
                analysis.append("✅ Fold river - Discipline")
        
        return " | ".join(analysis)
    
    def _is_bad_allin(self, hand: Hand, stack_bb: float) -> bool:
        """Détermine si un all-in était stratégiquement mauvais"""
        # All-in préflop avec gros stack
        if stack_bb > 40 and not hand.flop:
            # Vérifier si c'était avec une main marginale
            if hand.hero_cards:
                cards = hand.hero_cards.split()
                if len(cards) == 2:
                    # Petites paires ou mains moyennes avec gros stack = questionnable
                    if any(c[0] in ['2', '3', '4', '5', '6', '7'] for c in cards):
                        return True
        
        # All-in sur tirage au flop avec peu d'équité
        if hand.flop and any('all-in' in a and hand.hero_name in a for a in hand.flop_actions):
            if hand.hero_result == 'lost':
                return True
        
        return False
    
    def _generate_recommendation(self, hand: Hand, stack_bb: float, analysis: Dict) -> str:
        """Génère des recommandations stratégiques"""
        recommendations = []
        
        # Recommandations selon le résultat
        if hand.hero_result == 'lost':
            if stack_bb > 40:
                recommendations.append("💡 Avec un gros stack, privilégie le jeu postflop plutôt que les all-in préflop")
            
            if hand.flop and any('all-in' in a for a in hand.flop_actions):
                recommendations.append("💡 Sur tirage, évalue ton équité avant de t'engager all-in")
            
            recommendations.append("💡 Analyse les ranges adverses et les pot odds avant les décisions critiques")
        
        elif hand.hero_result == 'won':
            if any('all-in' in a and hand.hero_name in a for a in hand.preflop_actions):
                recommendations.append("✅ Bon timing pour le push - Continue à identifier ces spots")
            
            if hand.river and any('calls' in a and hand.hero_name in a for a in hand.river_actions):
                recommendations.append("✅ Excellent hero call - Ta lecture était correcte")
        
        # Recommandations selon la position
        if hand.hero_position in ['SB', 'BB']:
            recommendations.append("📚 En blinds, défends avec une range appropriée selon l'agresseur")
        elif hand.hero_position == 'BTN':
            recommendations.append("📚 Au bouton, exploite ta position avec une range élargie")
        
        return " | ".join(recommendations) if recommendations else "Continue à jouer solide"
    
    def get_critical_hands(self) -> List[Dict]:
        """Retourne les mains critiques triées par importance"""
        return sorted(self.critical_hands, 
                     key=lambda x: x['hand'].pot_size, 
                     reverse=True)[:10]  # Top 10 mains


if __name__ == "__main__":
    # Test du parser
    parser = WinamaxParser("Roll_Back")
    hands = parser.parse_file(r"C:\Users\DamienPodvin\Box\BoxPodvinDamien\UtilisationIA\AnalyseMainPoker\20241117_AFTER WORK FUNDAY 80K(862496170)_real_holdem_no-limit.txt")
    
    print(f"✅ {len(hands)} mains parsées avec succès")
    
    # Test de l'analyseur
    analyzer = HandAnalyzer()
    stats = analyzer.analyze_hands(hands)
    
    print(f"\n📊 Statistiques:")
    print(f"  - Total mains: {stats['total_hands']}")
    print(f"  - Mains gagnées: {stats['hands_won']}")
    print(f"  - Mains perdues: {stats['hands_lost']}")
    print(f"  - Mains foldées: {stats['hands_folded']}")
    print(f"  - All-in: {stats['all_in_hands']}")
    print(f"  - Gros pots: {stats['big_pots']}")
    
    critical = analyzer.get_critical_hands()
    print(f"\n🎯 {len(critical)} mains critiques identifiées")

# Made with Bob
