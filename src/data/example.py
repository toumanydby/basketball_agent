from src.data.data_processor import DataProcessor
from src.rules.metrics import BasketballMetrics
from src.rules.rules_engine import BasketballRules

def example_json_processing():
    # Example JSON data with multiple frames showing different game situations
    json_data = {
        "frames": [
            # Frame 1: Team 1 in attack with good spacing
            {
                "timestamp": 10.0,
                "players": [
                    # Team 1 players
                    {"id": 1, "team": 1, "x1": 4.5, "x2": 5.5, "y1": 2.5, "y2": 3.5, "height": 2.0},  # Point guard
                    {"id": 2, "team": 1, "x1": 7.5, "x2": 8.5, "y1": 4.5, "y2": 5.5, "height": 1.95},  # Shooting guard
                    {"id": 3, "team": 1, "x1": 6.5, "x2": 7.5, "y1": 7.5, "y2": 8.5, "height": 2.05},  # Small forward
                    {"id": 4, "team": 1, "x1": 4.5, "x2": 5.5, "y1": 10.5, "y2": 11.5, "height": 1.90},  # Power forward
                    {"id": 5, "team": 1, "x1": 8.5, "x2": 9.5, "y1": 12.5, "y2": 13.5, "height": 2.10},  # Center
                    # Team 2 players
                    {"id": 6, "team": 2, "x1": 19.5, "x2": 20.5, "y1": 2.5, "y2": 3.5, "height": 2.0},
                    {"id": 7, "team": 2, "x1": 22.5, "x2": 23.5, "y1": 4.5, "y2": 5.5, "height": 1.95},
                    {"id": 8, "team": 2, "x1": 21.5, "x2": 22.5, "y1": 7.5, "y2": 8.5, "height": 2.05},
                    {"id": 9, "team": 2, "x1": 19.5, "x2": 20.5, "y1": 10.5, "y2": 11.5, "height": 1.90},
                    {"id": 10, "team": 2, "x1": 23.5, "x2": 24.5, "y1": 12.5, "y2": 13.5, "height": 2.10}
                ],
                "ball": {"x1": 5.5, "x2": 6.5, "y1": 4.5, "y2": 5.5},
                "ball_possession": 1,
                "score": {"1": 10, "2": 8},
                "time_remaining": 600.0
            },
            # Frame 2: Team 1 with poor spacing (violation)
            {
                "timestamp": 11.0,
                "players": [
                    # Team 1 players (too close together)
                    {"id": 1, "team": 1, "x1": 4.5, "x2": 5.5, "y1": 2.5, "y2": 3.5, "height": 2.0},
                    {"id": 2, "team": 1, "x1": 5.0, "x2": 6.0, "y1": 3.0, "y2": 4.0, "height": 1.95},  # Too close to player 1
                    {"id": 3, "team": 1, "x1": 6.5, "x2": 7.5, "y1": 7.5, "y2": 8.5, "height": 2.05},
                    {"id": 4, "team": 1, "x1": 4.5, "x2": 5.5, "y1": 10.5, "y2": 11.5, "height": 1.90},
                    {"id": 5, "team": 1, "x1": 8.5, "x2": 9.5, "y1": 12.5, "y2": 13.5, "height": 2.10},
                    # Team 2 players
                    {"id": 6, "team": 2, "x1": 19.5, "x2": 20.5, "y1": 2.5, "y2": 3.5, "height": 2.0},
                    {"id": 7, "team": 2, "x1": 22.5, "x2": 23.5, "y1": 4.5, "y2": 5.5, "height": 1.95},
                    {"id": 8, "team": 2, "x1": 21.5, "x2": 22.5, "y1": 7.5, "y2": 8.5, "height": 2.05},
                    {"id": 9, "team": 2, "x1": 19.5, "x2": 20.5, "y1": 10.5, "y2": 11.5, "height": 1.90},
                    {"id": 10, "team": 2, "x1": 23.5, "x2": 24.5, "y1": 12.5, "y2": 13.5, "height": 2.10}
                ],
                "ball": {"x1": 5.0, "x2": 6.0, "y1": 3.0, "y2": 4.0},
                "ball_possession": 1,
                "score": {"1": 10, "2": 8},
                "time_remaining": 599.0
            },
            # Frame 3: Team 2 in attack with defensive hole
            {
                "timestamp": 12.0,
                "players": [
                    # Team 1 players (defense with hole)
                    {"id": 1, "team": 1, "x1": 4.5, "x2": 5.5, "y1": 2.5, "y2": 3.5, "height": 2.0},
                    {"id": 2, "team": 1, "x1": 7.5, "x2": 8.5, "y1": 4.5, "y2": 5.5, "height": 1.95},
                    {"id": 3, "team": 1, "x1": 6.5, "x2": 7.5, "y1": 7.5, "y2": 8.5, "height": 2.05},
                    {"id": 4, "team": 1, "x1": 4.5, "x2": 5.5, "y1": 10.5, "y2": 11.5, "height": 1.90},
                    {"id": 5, "team": 1, "x1": 8.5, "x2": 9.5, "y1": 12.5, "y2": 13.5, "height": 2.10},
                    # Team 2 players (attack)
                    {"id": 6, "team": 2, "x1": 19.5, "x2": 20.5, "y1": 2.5, "y2": 3.5, "height": 2.0},
                    {"id": 7, "team": 2, "x1": 22.5, "x2": 23.5, "y1": 4.5, "y2": 5.5, "height": 1.95},
                    {"id": 8, "team": 2, "x1": 21.5, "x2": 22.5, "y1": 7.5, "y2": 8.5, "height": 2.05},
                    {"id": 9, "team": 2, "x1": 19.5, "x2": 20.5, "y1": 10.5, "y2": 11.5, "height": 1.90},
                    {"id": 10, "team": 2, "x1": 23.5, "x2": 24.5, "y1": 12.5, "y2": 13.5, "height": 2.10}
                ],
                "ball": {"x1": 20.5, "x2": 21.5, "y1": 3.5, "y2": 4.5},
                "ball_possession": 2,
                "score": {"1": 10, "2": 8},
                "time_remaining": 598.0
            }
        ]
    }

    # Process the data
    processor = DataProcessor()
    frames = processor.process_json(json_data)
    states = processor.create_game_states(frames)

    # Evaluate using rules engine
    metrics = BasketballMetrics(court_width=15, court_length=28)
    rules = BasketballRules(metrics)
    
    # Evaluate each state
    for i, state in enumerate(states, 1):
        print(f"\nFrame {i} Evaluation:")
        evaluation = rules.evaluate_game_state(state)
        for rule, result in evaluation.items():
            print(f"{rule}: {'✓' if result else '✗'}")

def example_csv_processing():
    # Example CSV data with multiple frames
    import pandas as pd
    import io

    csv_data = """timestamp,type,id,team,x1,x2,y1,y2,height,ball_possession,score_team1,score_team2,time_remaining
10.0,player,1,1,4.5,5.5,2.5,3.5,2.0,1,10,8,600.0
10.0,player,2,1,7.5,8.5,4.5,5.5,1.95,1,10,8,600.0
10.0,player,3,1,6.5,7.5,7.5,8.5,2.05,1,10,8,600.0
10.0,player,4,1,4.5,5.5,10.5,11.5,1.90,1,10,8,600.0
10.0,player,5,1,8.5,9.5,12.5,13.5,2.10,1,10,8,600.0
10.0,player,6,2,19.5,20.5,2.5,3.5,2.0,1,10,8,600.0
10.0,player,7,2,22.5,23.5,4.5,5.5,1.95,1,10,8,600.0
10.0,player,8,2,21.5,22.5,7.5,8.5,2.05,1,10,8,600.0
10.0,player,9,2,19.5,20.5,10.5,11.5,1.90,1,10,8,600.0
10.0,player,10,2,23.5,24.5,12.5,13.5,2.10,1,10,8,600.0
10.0,ball,0,0,5.5,6.5,4.5,5.5,0.0,1,10,8,600.0
11.0,player,1,1,4.5,5.5,2.5,3.5,2.0,1,10,8,599.0
11.0,player,2,1,5.0,6.0,3.0,4.0,1.95,1,10,8,599.0
11.0,player,3,1,6.5,7.5,7.5,8.5,2.05,1,10,8,599.0
11.0,player,4,1,4.5,5.5,10.5,11.5,1.90,1,10,8,599.0
11.0,player,5,1,8.5,9.5,12.5,13.5,2.10,1,10,8,599.0
11.0,player,6,2,19.5,20.5,2.5,3.5,2.0,1,10,8,599.0
11.0,player,7,2,22.5,23.5,4.5,5.5,1.95,1,10,8,599.0
11.0,player,8,2,21.5,22.5,7.5,8.5,2.05,1,10,8,599.0
11.0,player,9,2,19.5,20.5,10.5,11.5,1.90,1,10,8,599.0
11.0,player,10,2,23.5,24.5,12.5,13.5,2.10,1,10,8,599.0
11.0,ball,0,0,5.0,6.0,3.0,4.0,0.0,1,10,8,599.0
12.0,player,1,1,4.5,5.5,2.5,3.5,2.0,2,10,8,598.0
12.0,player,2,1,7.5,8.5,4.5,5.5,1.95,2,10,8,598.0
12.0,player,3,1,6.5,7.5,7.5,8.5,2.05,2,10,8,598.0
12.0,player,4,1,4.5,5.5,10.5,11.5,1.90,2,10,8,598.0
12.0,player,5,1,8.5,9.5,12.5,13.5,2.10,2,10,8,598.0
12.0,player,6,2,19.5,20.5,2.5,3.5,2.0,2,10,8,598.0
12.0,player,7,2,22.5,23.5,4.5,5.5,1.95,2,10,8,598.0
12.0,player,8,2,21.5,22.5,7.5,8.5,2.05,2,10,8,598.0
12.0,player,9,2,19.5,20.5,10.5,11.5,1.90,2,10,8,598.0
12.0,player,10,2,23.5,24.5,12.5,13.5,2.10,2,10,8,598.0
12.0,ball,0,0,20.5,21.5,3.5,4.5,0.0,2,10,8,598.0"""

    # Create a CSV file in memory
    csv_file = io.StringIO(csv_data)
    
    # Process the data
    processor = DataProcessor()
    frames = processor.process_csv(csv_file)
    states = processor.create_game_states(frames)

    # Evaluate using rules engine
    metrics = BasketballMetrics(court_width=15, court_length=28)
    rules = BasketballRules(metrics)
    
    # Evaluate each state
    for i, state in enumerate(states, 1):
        print(f"\nFrame {i} Evaluation:")
        evaluation = rules.evaluate_game_state(state)
        for rule, result in evaluation.items():
            print(f"{rule}: {'✓' if result else '✗'}")

if __name__ == "__main__":
    print("Processing JSON example:")
    example_json_processing()
    
    print("\nProcessing CSV example:")
    example_csv_processing() 