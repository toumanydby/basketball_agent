import json
import pandas as pd
from typing import List, Dict, Union, Optional
from dataclasses import dataclass
from src.rules.metrics import Position, Player
from src.rules.rules_engine import GameState

@dataclass
class GameFrame:
    """Represents a single frame of game data"""
    timestamp: float
    players: List[Player]
    ball_position: Position
    ball_possession: Optional[int]
    score: Dict[int, int]  # team_id -> score
    time_remaining: float

class DataProcessor:
    def __init__(self, court_width: float = 15.0, court_length: float = 28.0):
        self.court_width = court_width
        self.court_length = court_length

    def _create_position(self, x1: float, x2: float, y1: float, y2: float) -> Position:
        """Create a Position object from bounding box coordinates"""
        return Position(x1=x1, x2=x2, y1=y1, y2=y2)

    def _create_player(self, player_data: Dict) -> Player:
        """Create a Player object from player data"""
        return Player(
            id=player_data['id'],
            position=self._create_position(
                player_data['x1'], player_data['x2'],
                player_data['y1'], player_data['y2']
            ),
            team=player_data['team'],
            height=player_data.get('height', 2.0),  # Default height if not provided
            zone=player_data.get('zone')  # Optional zone assignment
        )

    def process_json(self, json_data: Union[str, Dict]) -> List[GameFrame]:
        """Process game data from JSON format"""
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data

        frames = []
        for frame_data in data['frames']:
            players = [self._create_player(p) for p in frame_data['players']]
            
            ball_pos = self._create_position(
                frame_data['ball']['x1'],
                frame_data['ball']['x2'],
                frame_data['ball']['y1'],
                frame_data['ball']['y2']
            )

            frame = GameFrame(
                timestamp=frame_data['timestamp'],
                players=players,
                ball_position=ball_pos,
                ball_possession=frame_data.get('ball_possession'),
                score=frame_data.get('score', {1: 0, 2: 0}),
                time_remaining=frame_data.get('time_remaining', 0.0)
            )
            frames.append(frame)
        
        return frames

    def process_csv(self, csv_path: str) -> List[GameFrame]:
        """Process game data from CSV format"""
        df = pd.read_csv(csv_path)
        
        # Group by timestamp to create frames
        frames = []
        for timestamp, frame_data in df.groupby('timestamp'):
            players = []
            
            # Process player data
            for _, row in frame_data[frame_data['type'] == 'player'].iterrows():
                player = self._create_player({
                    'id': row['id'],
                    'team': row['team'],
                    'x1': row['x1'],
                    'x2': row['x2'],
                    'y1': row['y1'],
                    'y2': row['y2'],
                    'height': row.get('height', 2.0)
                })
                players.append(player)
            
            # Get ball data
            ball_data = frame_data[frame_data['type'] == 'ball'].iloc[0]
            ball_pos = self._create_position(
                ball_data['x1'],
                ball_data['x2'],
                ball_data['y1'],
                ball_data['y2']
            )
            
            frame = GameFrame(
                timestamp=timestamp,
                players=players,
                ball_position=ball_pos,
                ball_possession=frame_data['ball_possession'].iloc[0] if 'ball_possession' in frame_data else None,
                score={
                    1: frame_data['score_team1'].iloc[0] if 'score_team1' in frame_data else 0,
                    2: frame_data['score_team2'].iloc[0] if 'score_team2' in frame_data else 0
                },
                time_remaining=frame_data['time_remaining'].iloc[0] if 'time_remaining' in frame_data else 0.0
            )
            frames.append(frame)
        
        return frames

    def create_game_states(self, frames: List[GameFrame]) -> List[GameState]:
        """Convert GameFrames to GameStates for the rules engine"""
        states = []
        previous_state = None
        
        for frame in frames:
            # Create basket positions (assuming standard court dimensions)
            team1_basket = Position(x1=-0.5, x2=0.5, y1=7.0, y2=8.0)
            team2_basket = Position(x1=self.court_length-0.5, x2=self.court_length+0.5, y1=7.0, y2=8.0)
            
            state = GameState(
                players=frame.players,
                ball_position=frame.ball_position,
                ball_possession=frame.ball_possession,
                basket_positions=(team1_basket, team2_basket),
                timestamp=frame.timestamp,
                previous_state=previous_state
            )
            states.append(state)
            previous_state = state
        
        return states 