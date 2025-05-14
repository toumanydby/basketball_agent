from dataclasses import dataclass
from typing import List, Optional, Tuple
from src.rules.metrics import Position, Player, BasketballMetrics

@dataclass
class GameState:
    players: List[Player]
    ball_position: Position
    ball_possession: Optional[int]  # team number (1 or 2) or None if ball is in air
    basket_positions: Tuple[Position, Position]  # (team1_basket, team2_basket)
    timestamp: float
    previous_state: Optional['GameState'] = None

    def __init__(self, players: List[Player], ball_position: Position, ball_possession: Optional[int], basket_positions: Tuple[Position, Position], timestamp: float, previous_state: Optional['GameState']):
        self.players = players
        self.ball_position = ball_position
        self.ball_possession = ball_possession
        self.basket_positions = basket_positions
        self.timestamp = timestamp
        self.previous_state = previous_state

class BasketballRules:
    def __init__(self, metrics: BasketballMetrics):
        self.metrics = metrics
        self.max_ball_possession_time = 3.0  # seconds

    def check_attack_positions(self, state: GameState, team: int) -> bool:
        """Check if all players are in correct positions during attack"""
        if not state.ball_possession == team:
            return True
        
        for player in state.players:
            if player.team == team:
                if not self.metrics.is_in_opponent_court(player, team):
                    return False
        return True

    def check_defensive_positions(self, state: GameState, team: int) -> bool:
        """Check if all players are in correct positions during defense"""
        if state.ball_possession == team:
            return True
        
        for player in state.players:
            if player.team == team:
                if self.metrics.is_in_opponent_court(player, team):
                    return False
        return True

    def check_team_spacing(self, state: GameState, team: int) -> bool:
        """Check if players are properly spaced during attack"""
        if not state.ball_possession == team:
            return True

        team_players = [p for p in state.players if p.team == team]
        for i, player1 in enumerate(team_players):
            for player2 in team_players[i+1:]:
                if self.metrics.distance_between_players(player1.position, player2.position) < self.metrics.DMIN:
                    return False
        return True

    def check_ball_possession_time(self, state: GameState) -> bool:
        """Check if ball possession time is within limits"""
        if not state.previous_state or not state.ball_possession:
            return True
        
        if state.ball_possession == state.previous_state.ball_possession:
            possession_time = state.timestamp - state.previous_state.timestamp
            return possession_time <= self.max_ball_possession_time
        return True

    def check_defensive_holes(self, state: GameState, team: int) -> bool:
        """Check for defensive holes in team formation"""
        if state.ball_possession == team:
            return True

        team_players = [p for p in state.players if p.team == team]
        for i, player1 in enumerate(team_players):
            for player2 in team_players[i+1:]:
                if self.metrics.is_defensive_hole(player1, player2):
                    return False
        return True

    def check_defensive_help(self, state: GameState, team: int) -> bool:
        """Check if defensive help is needed and provided"""
        if state.ball_possession == team:
            return True

        attacking_players = [p for p in state.players if p.team != team]
        defending_players = [p for p in state.players if p.team == team]

        for attacker in attacking_players:
            if state.ball_possession == attacker.team:
                for defender in defending_players:
                    if self.metrics.distance_between_players(defender.position, attacker.position) < self.metrics.DSEUIL:
                        # Check if another defender is helping
                        for helper in defending_players:
                            if helper != defender:
                                if self.metrics.distance_between_players(helper.position, attacker.position) < self.metrics.DSEUIL:
                                    return True
                        return False
        return True

    def check_zone_respect(self, state: GameState) -> bool:
        """Check if all players are in their assigned zones"""
        return all(self.metrics.is_in_assigned_zone(player) for player in state.players)

    def check_defensive_positioning(self, state: GameState, team: int) -> bool:
        """Check if defenders are correctly positioned between attackers and basket"""
        if state.ball_possession == team:
            return True

        basket_pos = state.basket_positions[team-1]
        attacking_players = [p for p in state.players if p.team != team]
        defending_players = [p for p in state.players if p.team == team]

        for attacker in attacking_players:
            if state.ball_possession == attacker.team:
                for defender in defending_players:
                    if not self.metrics.is_in_defensive_position(defender, attacker, basket_pos):
                        return False
        return True

    def evaluate_game_state(self, state: GameState) -> dict:
        """Evaluate the current game state against all rules"""
        return {
            'team1_attack_positions': self.check_attack_positions(state, 1),
            'team2_attack_positions': self.check_attack_positions(state, 2),
            'team1_defensive_positions': self.check_defensive_positions(state, 1),
            'team2_defensive_positions': self.check_defensive_positions(state, 2),
            'team1_spacing': self.check_team_spacing(state, 1),
            'team2_spacing': self.check_team_spacing(state, 2),
            'ball_possession_time': self.check_ball_possession_time(state),
            'team1_defensive_holes': self.check_defensive_holes(state, 1),
            'team2_defensive_holes': self.check_defensive_holes(state, 2),
            'team1_defensive_help': self.check_defensive_help(state, 1),
            'team2_defensive_help': self.check_defensive_help(state, 2),
            'zone_respect': self.check_zone_respect(state),
            'team1_defensive_positioning': self.check_defensive_positioning(state, 1),
            'team2_defensive_positioning': self.check_defensive_positioning(state, 2)
        } 
