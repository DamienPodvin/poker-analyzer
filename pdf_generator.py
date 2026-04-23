"""
Générateur de rapports PDF pour l'analyse de poker
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from typing import List, Dict
from poker_analyzer import Hand, HandAnalyzer


class PokerPDFGenerator:
    """Génère un rapport PDF professionnel d'analyse de poker"""
    
    def __init__(self, output_filename: str = "poker_analysis.pdf"):
        self.output_filename = output_filename
        self.doc = SimpleDocTemplate(
            output_filename,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Styles personnalisés
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        self.subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=8,
            alignment=TA_JUSTIFY
        )
        
        self.error_style = ParagraphStyle(
            'ErrorStyle',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.red,
            spaceAfter=8
        )
        
        self.success_style = ParagraphStyle(
            'SuccessStyle',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.green,
            spaceAfter=8
        )
    
    def generate_report(self, hands: List[Hand], analyzer: HandAnalyzer, hero_name: str, critical_hands_filter: str = 'all'):
        """Génère le rapport complet
        
        Args:
            hands: Liste des mains à analyser
            analyzer: Analyseur de mains
            hero_name: Nom du joueur
            critical_hands_filter: Filtre pour les mains critiques ('all', 'won', 'lost')
        """
        
        # Calculer la répartition des types de jeu
        game_types = {}
        for hand in hands:
            game_type = hand.game_type
            game_types[game_type] = game_types.get(game_type, 0) + 1
        
        # Page de titre
        self._add_title_page(hero_name, len(hands), game_types)
        
        # Résumé exécutif
        self._add_executive_summary(analyzer.statistics)
        
        # Analyse des mains critiques (avec filtre)
        self._add_critical_hands_analysis(analyzer.get_critical_hands(), critical_hands_filter)
        
        # Statistiques détaillées
        self._add_detailed_statistics(hands, analyzer.statistics)
        
        # Recommandations
        self._add_recommendations(analyzer.statistics, hands)
        
        # Construire le PDF
        self.doc.build(self.story)
        print(f"✅ Rapport PDF généré: {self.output_filename}")
    
    def _add_title_page(self, hero_name: str, num_hands: int, game_types: Dict[str, int] = None):
        """Ajoute la page de titre"""
        self.story.append(Spacer(1, 2*inch))
        
        title = Paragraph("🎯 ANALYSE DE SESSION POKER", self.title_style)
        self.story.append(title)
        self.story.append(Spacer(1, 0.3*inch))
        
        subtitle = Paragraph(f"Joueur: <b>{hero_name}</b>", self.heading_style)
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Informations sur les types de jeu
        game_type_info = ""
        if game_types:
            game_type_info = "<br/>Types de jeu: " + ", ".join([f"<b>{k}</b> ({v})" for k, v in game_types.items()])
        
        info = Paragraph(
            f"Nombre de mains analysées: <b>{num_hands}</b><br/>"
            f"Date du rapport: <b>{datetime.now().strftime('%d/%m/%Y %H:%M')}</b>"
            f"{game_type_info}",
            self.body_style
        )
        self.story.append(info)
        self.story.append(PageBreak())
    
    def _add_executive_summary(self, stats: Dict):
        """Ajoute le résumé exécutif"""
        self.story.append(Paragraph("📊 RÉSUMÉ EXÉCUTIF", self.heading_style))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Tableau des statistiques principales
        win_rate = (stats['hands_won'] / stats['total_hands'] * 100) if stats['total_hands'] > 0 else 0
        
        data = [
            ['Métrique', 'Valeur'],
            ['Total de mains jouées', str(stats['total_hands'])],
            ['Mains gagnées', f"{stats['hands_won']} ({win_rate:.1f}%)"],
            ['Mains perdues', str(stats['hands_lost'])],
            ['Mains foldées', str(stats['hands_folded'])],
            ['Situations all-in', str(stats['all_in_hands'])],
            ['Gros pots (>30BB)', str(stats['big_pots'])],
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_critical_hands_analysis(self, critical_hands: List[Dict], result_filter: str = 'all'):
        """Ajoute l'analyse des mains critiques avec filtre par résultat
        
        Args:
            critical_hands: Liste des mains critiques
            result_filter: 'all', 'won', 'lost'
        """
        self.story.append(PageBreak())
        
        # Titre avec indication du filtre
        title = "🎯 ANALYSE DES MAINS CRITIQUES"
        if result_filter == 'won':
            title += " - MAINS GAGNÉES ✅"
        elif result_filter == 'lost':
            title += " - MAINS PERDUES ❌"
        
        self.story.append(Paragraph(title, self.heading_style))
        self.story.append(Spacer(1, 0.2*inch))
        
        if not critical_hands:
            self.story.append(Paragraph("Aucune main critique identifiée.", self.body_style))
            return
        
        # Filtrer les mains selon le résultat
        filtered_hands = critical_hands
        if result_filter == 'won':
            filtered_hands = [item for item in critical_hands if item['hand'].hero_result == 'won']
        elif result_filter == 'lost':
            filtered_hands = [item for item in critical_hands if item['hand'].hero_result == 'lost']
        
        if not filtered_hands:
            filter_text = "gagnées" if result_filter == 'won' else "perdues"
            self.story.append(Paragraph(f"Aucune main critique {filter_text} identifiée.", self.body_style))
            return
        
        # Info sur le filtrage
        if result_filter != 'all':
            info_text = f"<i>{len(filtered_hands)} main(s) sur {len(critical_hands)} total</i>"
            self.story.append(Paragraph(info_text, self.body_style))
            self.story.append(Spacer(1, 0.1*inch))
        
        # Afficher les mains filtrées
        for idx, item in enumerate(filtered_hands, 1):
            hand = item['hand']
            analysis = item['analysis']
            
            # Titre de la main
            title = f"Main #{idx} - {analysis['type']}"
            if analysis['severity'] == 'error':
                title += " ❌"
            elif analysis['severity'] == 'good':
                title += " ✅"
            
            self.story.append(Paragraph(title, self.subheading_style))
            
            # Informations de base
            blinds_parts = hand.blinds.split('/')
            bb = int(blinds_parts[2]) if len(blinds_parts) > 2 else 200
            stack_bb = hand.hero_stack / bb if bb > 0 else 0
            
            info_text = f"""
            <b>Contexte:</b><br/>
            • Level {hand.level} - Blinds: {hand.blinds}<br/>
            • Position: {hand.hero_position}<br/>
            • Stack: {hand.hero_stack} ({stack_bb:.1f} BB)<br/>
            • Cartes: <b>{hand.hero_cards}</b><br/>
            • Pot: {hand.pot_size} chips<br/>
            """
            self.story.append(Paragraph(info_text, self.body_style))
            
            # Actions préflop (limité pour performance)
            if hand.preflop_actions:
                self.story.append(Paragraph("<b>Préflop:</b>", self.body_style))
                for action in hand.preflop_actions[:3]:  # Limite à 3 actions clés
                    self.story.append(Paragraph(f"• {action}", self.body_style))
                if len(hand.preflop_actions) > 3:
                    self.story.append(Paragraph(f"<i>... et {len(hand.preflop_actions) - 3} autre(s) action(s)</i>", self.body_style))
            
            # Flop
            if hand.flop:
                self.story.append(Paragraph(f"<b>Flop: {hand.flop}</b>", self.body_style))
                for action in hand.flop_actions[:3]:
                    self.story.append(Paragraph(f"• {action}", self.body_style))
                if len(hand.flop_actions) > 3:
                    self.story.append(Paragraph(f"<i>... et {len(hand.flop_actions) - 3} autre(s) action(s)</i>", self.body_style))
            
            # Turn
            if hand.turn:
                self.story.append(Paragraph(f"<b>Turn: {hand.turn}</b>", self.body_style))
                for action in hand.turn_actions[:3]:
                    self.story.append(Paragraph(f"• {action}", self.body_style))
                if len(hand.turn_actions) > 3:
                    self.story.append(Paragraph(f"<i>... et {len(hand.turn_actions) - 3} autre(s) action(s)</i>", self.body_style))
            
            # River
            if hand.river:
                self.story.append(Paragraph(f"<b>River: {hand.river}</b>", self.body_style))
                for action in hand.river_actions[:3]:
                    self.story.append(Paragraph(f"• {action}", self.body_style))
                if len(hand.river_actions) > 3:
                    self.story.append(Paragraph(f"<i>... et {len(hand.river_actions) - 3} autre(s) action(s)</i>", self.body_style))
            
            # Résultat
            result_style = self.success_style if hand.hero_result == 'won' else self.error_style
            result_text = f"<b>Résultat: {hand.hero_result.upper()}</b>"
            if hand.amount_won > 0:
                result_text += f" (+{hand.amount_won} chips)"
            self.story.append(Paragraph(result_text, result_style))
            
            # Analyse stratégique détaillée
            if analysis['description']:
                self.story.append(Paragraph(f"<b>Résumé:</b> {analysis['description']}", self.body_style))
            
            # Analyse préflop
            if analysis.get('preflop_analysis'):
                self.story.append(Paragraph(f"<b>🎯 Analyse Préflop:</b>", self.subheading_style))
                self.story.append(Paragraph(analysis['preflop_analysis'], self.body_style))
            
            # Analyse flop
            if analysis.get('flop_analysis'):
                self.story.append(Paragraph(f"<b>🎯 Analyse Flop:</b>", self.subheading_style))
                self.story.append(Paragraph(analysis['flop_analysis'], self.body_style))
            
            # Analyse turn
            if analysis.get('turn_analysis'):
                self.story.append(Paragraph(f"<b>🎯 Analyse Turn:</b>", self.subheading_style))
                self.story.append(Paragraph(analysis['turn_analysis'], self.body_style))
            
            # Analyse river
            if analysis.get('river_analysis'):
                self.story.append(Paragraph(f"<b>🎯 Analyse River:</b>", self.subheading_style))
                self.story.append(Paragraph(analysis['river_analysis'], self.body_style))
            
            # Notes stratégiques
            if analysis.get('strategic_notes'):
                self.story.append(Paragraph(f"<b>📝 Notes stratégiques:</b>", self.subheading_style))
                for note in analysis['strategic_notes']:
                    self.story.append(Paragraph(f"• {note}", self.error_style if '⚠️' in note else self.body_style))
            
            # Recommandations
            if analysis.get('recommendation'):
                self.story.append(Paragraph(f"<b>💡 Recommandations:</b>", self.subheading_style))
                self.story.append(Paragraph(analysis['recommendation'], self.success_style if '✅' in analysis['recommendation'] else self.body_style))
            
            self.story.append(Spacer(1, 0.3*inch))
            
            # Page break tous les 3 mains pour la lisibilité
            if idx % 3 == 0 and idx < len(critical_hands):
                self.story.append(PageBreak())
    
    def _add_detailed_statistics(self, hands: List[Hand], stats: Dict):
        """Ajoute les statistiques détaillées"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("📈 STATISTIQUES DÉTAILLÉES", self.heading_style))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Analyse par position
        position_stats = {}
        for hand in hands:
            pos = hand.hero_position
            if pos not in position_stats:
                position_stats[pos] = {'total': 0, 'won': 0, 'lost': 0, 'folded': 0}
            
            position_stats[pos]['total'] += 1
            if hand.hero_result == 'won':
                position_stats[pos]['won'] += 1
            elif hand.hero_result == 'lost':
                position_stats[pos]['lost'] += 1
            else:
                position_stats[pos]['folded'] += 1
        
        self.story.append(Paragraph("<b>Performance par position:</b>", self.subheading_style))
        
        pos_data = [['Position', 'Mains', 'Gagnées', 'Perdues', 'Foldées', 'Win Rate']]
        for pos, data in sorted(position_stats.items()):
            win_rate = (data['won'] / data['total'] * 100) if data['total'] > 0 else 0
            pos_data.append([
                pos,
                str(data['total']),
                str(data['won']),
                str(data['lost']),
                str(data['folded']),
                f"{win_rate:.1f}%"
            ])
        
        pos_table = Table(pos_data, colWidths=[1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1*inch])
        pos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        self.story.append(pos_table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_recommendations(self, stats: Dict, hands: List[Hand]):
        """Ajoute les recommandations"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("💡 RECOMMANDATIONS", self.heading_style))
        self.story.append(Spacer(1, 0.2*inch))
        
        recommendations = []
        
        # Analyse du taux de victoire
        win_rate = (stats['hands_won'] / stats['total_hands'] * 100) if stats['total_hands'] > 0 else 0
        
        if win_rate < 30:
            recommendations.append(
                "⚠️ <b>Taux de victoire faible:</b> Votre win rate est inférieur à 30%. "
                "Concentrez-vous sur la sélection de mains préflop et évitez les spots marginaux."
            )
        elif win_rate > 50:
            recommendations.append(
                "✅ <b>Excellent taux de victoire:</b> Continuez sur cette lancée ! "
                "Votre sélection de mains et vos décisions sont solides."
            )
        
        # Analyse des all-in
        all_in_rate = (stats['all_in_hands'] / stats['total_hands'] * 100) if stats['total_hands'] > 0 else 0
        
        if all_in_rate > 20:
            recommendations.append(
                "⚠️ <b>Trop de situations all-in:</b> Vous vous retrouvez all-in dans plus de 20% des mains. "
                "Travaillez votre gestion de stack et évitez les spots à variance élevée."
            )
        
        # Recommandations générales
        recommendations.extend([
            "📚 <b>Étude recommandée:</b> Analysez vos ranges préflop selon votre position et le format (MTT/Cash).",
            "🎯 <b>Focus:</b> Travaillez la lecture des boards et l'identification des spots de value vs bluff.",
            "💪 <b>Discipline:</b> Maintenez une bankroll management stricte et évitez le tilt.",
            "📊 <b>Tracking:</b> Continuez à analyser vos sessions régulièrement pour identifier les leaks."
        ])
        
        for rec in recommendations:
            self.story.append(Paragraph(rec, self.body_style))
            self.story.append(Spacer(1, 0.15*inch))
        
        # Conclusion
        self.story.append(Spacer(1, 0.3*inch))
        self.story.append(Paragraph(
            "<b>Conclusion:</b> Ce rapport vous donne un aperçu de votre jeu. "
            "Utilisez ces informations pour identifier vos points forts et vos axes d'amélioration. "
            "Le poker est un jeu d'apprentissage continu - bonne chance aux tables ! 🎰",
            self.body_style
        ))


if __name__ == "__main__":
    print("Module de génération PDF chargé ✅")

# Made with Bob
