from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
from src.rules.rules_engine import GameState, BasketballRules
from src.rules.metrics import BasketballMetrics, Position, Player

@dataclass
class Action:
    """Represents a possible action a player can take"""
    player_id: int
    action_type: str  # 'move', 'pass', 'shoot', 'defend'
    target_position: Optional[Position] = None
    target_player_id: Optional[int] = None
    priority: float = 0.0  # Higher priority means more important action

class DecisionMaker:
    def __init__(self, metrics: BasketballMetrics, rules: BasketballRules):
        self.metrics = metrics
        self.rules = rules
        self.action_weights = {
            'spacing_violation': 1.0,
            'defensive_hole': 0.9,
            'attack_position': 0.8,
            'defensive_position': 0.8,
            'ball_possession_time': 0.7,
            'defensive_help': 0.6,
            'zone_respect': 0.5
        }

    def analyze_game_state(self, state: GameState) -> Dict[str, bool]:
        """Analyze the current game state and return rule violations"""
        return self.rules.evaluate_game_state(state)

    def get_team_actions(self, state: GameState, team: int) -> List[Action]:
        """Get list of possible actions for a team based on game state"""
        actions = []
        team_players = [p for p in state.players if p.team == team]
        
        # If team has ball possession
        if state.ball_possession == team:
            actions.extend(self._get_offensive_actions(state, team_players))
        else:
            actions.extend(self._get_defensive_actions(state, team_players))
            
        return sorted(actions, key=lambda x: x.priority, reverse=True)

    def _get_offensive_actions(self, state: GameState, team_players: List[Player]) -> List[Action]:
        """Generate offensive actions based on game state"""
        actions = []
        evaluation = self.analyze_game_state(state)
        
        # Check spacing violations
        if not evaluation[f'team{state.ball_possession}_spacing']:
            for player in team_players:
                for other_player in team_players:
                    if player != other_player:
                        distance = self.metrics.distance_between_players(
                            player.position, other_player.position)
                        if distance < self.metrics.DMIN:
                            # Calculate new position to maintain spacing
                            new_pos = self._calculate_spacing_position(
                                player.position, other_player.position)
                            actions.append(Action(
                                player_id=player.id,
                                action_type='move',
                                target_position=new_pos,
                                priority=self.action_weights['spacing_violation']
                            ))

        # Check attack positions
        if not evaluation[f'team{state.ball_possession}_attack_positions']:
            for player in team_players:
                if not self.metrics.is_in_opponent_court(player, state.ball_possession):
                    # Calculate position in opponent's court
                    new_pos = self._calculate_attack_position(
                        player.position, state.ball_possession)
                    actions.append(Action(
                        player_id=player.id,
                        action_type='move',
                        target_position=new_pos,
                        priority=self.action_weights['attack_position']
                    ))

        # Check ball possession time
        if not evaluation['ball_possession_time']:
            # Find player closest to basket for shooting
            shooter = min(team_players, 
                        key=lambda p: self.metrics.distance_between_players(
                            p.position, state.basket_positions[1]))
            actions.append(Action(
                player_id=shooter.id,
                action_type='shoot',
                priority=self.action_weights['ball_possession_time']
            ))

        return actions

    def _get_defensive_actions(self, state: GameState, team_players: List[Player]) -> List[Action]:
        """Generate defensive actions based on game state"""
        actions = []
        evaluation = self.analyze_game_state(state)
        
        # Check defensive holes
        if not evaluation[f'team{state.ball_possession}_defensive_holes']:
            for i, player1 in enumerate(team_players):
                for player2 in team_players[i+1:]:
                    if self.metrics.is_defensive_hole(player1, player2):
                        # Calculate position to fill the hole
                        new_pos = self._calculate_defensive_position(
                            player1.position, player2.position)
                        actions.append(Action(
                            player_id=player1.id,
                            action_type='move',
                            target_position=new_pos,
                            priority=self.action_weights['defensive_hole']
                        ))

        # Check defensive help
        if not evaluation[f'team{state.ball_possession}_defensive_help']:
            attacking_players = [p for p in state.players if p.team != state.ball_possession]
            for attacker in attacking_players:
                if state.ball_possession == attacker.team:
                    for defender in team_players:
                        if self.metrics.distance_between_players(
                            defender.position, attacker.position) < self.metrics.DSEUIL:
                            # Find closest teammate for help defense
                            helper = min(team_players,
                                       key=lambda p: self.metrics.distance_between_players(
                                           p.position, attacker.position))
                            if helper != defender:
                                new_pos = self._calculate_help_defense_position(
                                    defender.position, attacker.position)
                                actions.append(Action(
                                    player_id=helper.id,
                                    action_type='move',
                                    target_position=new_pos,
                                    priority=self.action_weights['defensive_help']
                                ))

        return actions

    def _calculate_spacing_position(self, pos1: Position, pos2: Position) -> Position:
        """Calculate new position to maintain proper spacing"""
        dx = pos2.center_x - pos1.center_x
        dy = pos2.center_y - pos1.center_y
        distance = self.metrics.distance_between_players(pos1, pos2)
        
        if distance < self.metrics.DMIN:
            # Move away from other player
            scale = (self.metrics.DMIN - distance) / distance
            new_x = pos1.center_x - dx * scale
            new_y = pos1.center_y - dy * scale
            
            return Position(
                x1=new_x - 0.5,
                x2=new_x + 0.5,
                y1=new_y - 0.5,
                y2=new_y + 0.5
            )
        return pos1

    def _calculate_attack_position(self, current_pos: Position, team: int) -> Position:
        """Calculate position in opponent's court for attack"""
        if team == 1:
            target_x = self.metrics.mid_court_x + 2.0
        else:
            target_x = self.metrics.mid_court_x - 2.0
            
        return Position(
            x1=target_x - 0.5,
            x2=target_x + 0.5,
            y1=current_pos.center_y - 0.5,
            y2=current_pos.center_y + 0.5
        )

    def _calculate_defensive_position(self, pos1: Position, pos2: Position) -> Position:
        """Calculate position to fill defensive hole"""
        mid_x = (pos1.center_x + pos2.center_x) / 2
        mid_y = (pos1.center_y + pos2.center_y) / 2
        
        return Position(
            x1=mid_x - 0.5,
            x2=mid_x + 0.5,
            y1=mid_y - 0.5,
            y2=mid_y + 0.5
        )

    def _calculate_help_defense_position(self, defender_pos: Position, attacker_pos: Position) -> Position:
        """Calculate position for help defense"""
        # Position between defender and attacker
        mid_x = (defender_pos.center_x + attacker_pos.center_x) / 2
        mid_y = (defender_pos.center_y + attacker_pos.center_y) / 2
        
        return Position(
            x1=mid_x - 0.5,
            x2=mid_x + 0.5,
            y1=mid_y - 0.5,
            y2=mid_y + 0.5
        ) 