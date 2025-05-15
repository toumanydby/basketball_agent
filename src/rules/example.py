from src.rules.metrics import Position, Player, BasketballMetrics
from src.rules.rules_engine import GameState, BasketballRules

def create_example_game_state():
    # Create court metrics (standard basketball court dimensions in meters)
    metrics = BasketballMetrics(court_width=15, court_length=28)
    
    # Create basket positions (using bounding boxes)
    team1_basket = Position(x1=-0.5, x2=0.5, y1=7.0, y2=8.0)  # Left basket
    team2_basket = Position(x1=27.5, x2=28.5, y1=7.0, y2=8.0)  # Right basket
    
    # Create players with bounding boxes
    players = [
        # Team 1 players
        Player(id=1, position=Position(x1=4.5, x2=5.5, y1=2.5, y2=3.5), team=1, zone=(0, 0, 7, 7)),
        Player(id=2, position=Position(x1=6.5, x2=7.5, y1=4.5, y2=5.5), team=1, zone=(0, 7, 7, 14)),
        Player(id=3, position=Position(x1=5.5, x2=6.5, y1=7.5, y2=8.5), team=1, zone=(7, 0, 14, 7)),
        Player(id=4, position=Position(x1=3.5, x2=4.5, y1=9.5, y2=10.5), team=1, zone=(7, 7, 14, 14)),
        Player(id=5, position=Position(x1=7.5, x2=8.5, y1=11.5, y2=12.5), team=1, zone=(0, 14, 7, 21)),
        
        # Team 2 players
        Player(id=6, position=Position(x1=19.5, x2=20.5, y1=2.5, y2=3.5), team=2, zone=(21, 0, 28, 7)),
        Player(id=7, position=Position(x1=21.5, x2=22.5, y1=4.5, y2=5.5), team=2, zone=(21, 7, 28, 14)),
        Player(id=8, position=Position(x1=20.5, x2=21.5, y1=7.5, y2=8.5), team=2, zone=(14, 0, 21, 7)),
        Player(id=9, position=Position(x1=18.5, x2=19.5, y1=9.5, y2=10.5), team=2, zone=(14, 7, 21, 14)),
        Player(id=10, position=Position(x1=22.5, x2=23.5, y1=11.5, y2=12.5), team=2, zone=(21, 14, 28, 21)),
    ]
    
    # Create game state with ball position as bounding box
    return GameState(
        players=players,
        ball_position=Position(x1=5.5, x2=6.5, y1=4.5, y2=5.5),  # Ball with team 1
        ball_possession=1,  # Team 1 has the ball
        basket_positions=(team1_basket, team2_basket),
        timestamp=10.0,
        previous_state=None
    )

def main():
    # Create metrics and rules
    metrics = BasketballMetrics(court_width=15, court_length=28)
    rules = BasketballRules(metrics)
    
    # Create example game state
    game_state = create_example_game_state()
    
    # Evaluate the game state
    evaluation = rules.evaluate_game_state(game_state)
    
    # Print results
    print("Game State Evaluation:")
    for rule, result in evaluation.items():
        print(f"{rule}: {'✓' if result else '✗'}")

if __name__ == "__main__":
    main() 