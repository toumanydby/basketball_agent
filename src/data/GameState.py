from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import numpy as np

@dataclass
class GameState:
    """
    Represents a single moment in a basketball game with all relevant positions and context.
    
    Attributes:
        timestamp (float): Time in seconds from the start of the game
        team1_positions (Dict[str, Tuple[float, float]]): Dictionary mapping player IDs to their (x, y) positions for team 1
        team2_positions (Dict[str, Tuple[float, float]]): Dictionary mapping player IDs to their (x, y) positions for team 2
        ball_position (Tuple[float, float]): (x, y) position of the ball
        score (Tuple[int, int]): Current score (team1_score, team2_score)
        time_remaining (float): Time remaining in the period in seconds
        period (int): Current period number
    """
    
    timestamp: float
    team1_positions: Dict[str, Tuple[float, float]]
    team2_positions: Dict[str, Tuple[float, float]]
    ball_position: Tuple[float, float]
    score: Tuple[int, int]
    time_remaining: float
    period: int
    
    def __post_init__(self):
        """Validate the game state data after initialization."""
        self._validate_positions()
        self._validate_score()
        self._validate_time()
    
    def _validate_positions(self):
        """Validate that all positions are within court boundaries."""
        # TODO: Implement court boundary validation
        pass
    
    def _validate_score(self):
        """Validate that scores are non-negative."""
        if self.score[0] < 0 or self.score[1] < 0:
            raise ValueError("Scores cannot be negative")
    
    def _validate_time(self):
        """Validate that time values are reasonable."""
        if self.timestamp < 0:
            raise ValueError("Timestamp cannot be negative")
        if self.time_remaining < 0:
            raise ValueError("Time remaining cannot be negative")
    
    def get_player_position(self, team: int, player_id: str) -> Tuple[float, float]:
        """
        Get the position of a specific player.
        
        Args:
            team (int): Team number (1 or 2)
            player_id (str): Player identifier
            
        Returns:
            Tuple[float, float]: (x, y) position of the player
        """
        positions = self.team1_positions if team == 1 else self.team2_positions
        if player_id not in positions:
            raise ValueError(f"Player {player_id} not found in team {team}")
        return positions[player_id]
    
    def get_distance_to_ball(self, team: int, player_id: str) -> float:
        """
        Calculate the distance between a player and the ball.
        
        Args:
            team (int): Team number (1 or 2)
            player_id (str): Player identifier
            
        Returns:
            float: Distance between player and ball
        """
        player_pos = self.get_player_position(team, player_id)
        return np.sqrt((player_pos[0] - self.ball_position[0])**2 + 
                      (player_pos[1] - self.ball_position[1])**2)
    
    def get_player_distances(self, team: int, player_id: str) -> Dict[str, float]:
        """
        Calculate distances between a player and all other players on their team.
        
        Args:
            team (int): Team number (1 or 2)
            player_id (str): Player identifier
            
        Returns:
            Dict[str, float]: Dictionary mapping player IDs to their distances
        """
        positions = self.team1_positions if team == 1 else self.team2_positions
        player_pos = self.get_player_position(team, player_id)
        
        distances = {}
        for other_id, other_pos in positions.items():
            if other_id != player_id:
                distances[other_id] = np.sqrt((player_pos[0] - other_pos[0])**2 + 
                                            (player_pos[1] - other_pos[1])**2)
        return distances
