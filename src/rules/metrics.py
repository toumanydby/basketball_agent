import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Optional

@dataclass
class Position:
    x1: float
    x2: float
    y1: float
    y2: float

    def __init__(self, x1: float, x2: float, y1: float, y2: float):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
		

    @property
    def center_x(self) -> float:
        """Get the center x coordinate of the bounding box"""
        return (self.x1 + self.x2) / 2

    @property
    def center_y(self) -> float:
        """Get the center y coordinate of the bounding box"""
        return (self.y1 + self.y2) / 2

    @property
    def center(self) -> Tuple[float, float]:
        """Get the center point of the bounding box"""
        return (self.center_x, self.center_y)

    @property
    def width(self) -> float:
        """Get the width of the bounding box"""
        return abs(self.x2 - self.x1)

    @property
    def height(self) -> float:
        """Get the height of the bounding box"""
        return abs(self.y2 - self.y1)

@dataclass
class Player:
    id: int
    position: Position
    team: int  # 1 or 2
    height: float
    zone: Optional[Tuple[float, float, float, float]] = None  # (x1, y1, x2, y2)

    def __init__(self, id: int, position: Position, team: int, zone : Optional[Tuple[float, float, float, float]]):
        self.id = id
        self.position = position
        self.team = team
        self.height = position.height
        self.zone = zone

class BasketballMetrics:
    def __init__(self, court_width: float, court_length: float):
        self.court_width = court_width
        self.court_length = court_length
        self.mid_court_x = court_length / 2
        self.STROU = 4.0  # meters
        self.DMIN = 4.0   # meters
        self.DREBOND = 3.0  # meters
        self.DSEUIL = 2.0  # meters for defensive help

    def distance_between_players(self, pos1: Position, pos2: Position) -> float:
        """Calculate distance between two players using their center points"""
        return np.sqrt((pos2.center_x - pos1.center_x)**2 + (pos2.center_y - pos1.center_y)**2)

    def player_space_occupation(self, position: Position) -> float:
        """Calculate space occupation of a player using their bounding box"""
        return position.width * position.height

    def is_in_opponent_court(self, player: Player, team: int) -> bool:
        """Check if player is in opponent's court using their center point"""
        if team == 1:
            return player.position.center_x > self.mid_court_x
        return player.position.center_x < self.mid_court_x

    def is_in_team(self, player: Player, team: int) -> bool:
        """Check if player belongs to specified team"""
        return player.team == team

    def is_in_attack(self, player: Player, ball_possession: int) -> bool:
        """Check if player's team is in attack"""
        return (player.team == ball_possession and 
                self.is_in_opponent_court(player, player.team))

    def is_defensive_hole(self, player1: Player, player2: Player) -> bool:
        """Check if there's a defensive hole between two players"""
        return self.distance_between_players(player1.position, player2.position) > self.STROU

    def is_in_defensive_position(self, defender: Player, attacker: Player, basket_pos: Position) -> bool:
        """Check if defender is in correct position between attacker and basket"""
        defender_to_basket = self.distance_between_players(defender.position, basket_pos)
        attacker_to_basket = self.distance_between_players(attacker.position, basket_pos)
        return defender_to_basket < attacker_to_basket

    def is_in_assigned_zone(self, player: Player) -> bool:
        """Check if player is in their assigned zone"""
        if not player.zone:
            return True
        x1, y1, x2, y2 = player.zone
        return (x1 <= player.position.center_x <= x2 and 
                y1 <= player.position.center_y <= y2)

    def is_rebound_opportunity(self, player: Player, basket_pos: Position) -> bool:
        """Check if player is in position for a rebound"""
        return self.distance_between_players(player.position, basket_pos) < self.DREBOND 
