from src.rules.metrics import BasketballMetrics
from src.rules.rules_engine import BasketballRules
from src.decision.decision_maker import DecisionMaker
from src.rules.example import create_example_game_state

def demonstrate_decision_making():
    # Create metrics and rules
    metrics = BasketballMetrics(court_width=15, court_length=28)
    rules = BasketballRules(metrics)
    
    # Create decision maker
    decision_maker = DecisionMaker(metrics, rules)
    
    # Create example game state
    game_state = create_example_game_state()
    
    # Get actions for both teams
    team1_actions = decision_maker.get_team_actions(game_state, 1)
    team2_actions = decision_maker.get_team_actions(game_state, 2)
    
    # Print actions for Team 1
    print("\nTeam 1 Actions (in order of priority):")
    for action in team1_actions:
        print(f"Player {action.player_id}: {action.action_type}")
        if action.target_position:
            print(f"  Target Position: ({action.target_position.center_x:.1f}, {action.target_position.center_y:.1f})")
        if action.target_player_id:
            print(f"  Target Player: {action.target_player_id}")
        print(f"  Priority: {action.priority:.2f}")
    
    # Print actions for Team 2
    print("\nTeam 2 Actions (in order of priority):")
    for action in team2_actions:
        print(f"Player {action.player_id}: {action.action_type}")
        if action.target_position:
            print(f"  Target Position: ({action.target_position.center_x:.1f}, {action.target_position.center_y:.1f})")
        if action.target_player_id:
            print(f"  Target Player: {action.target_player_id}")
        print(f"  Priority: {action.priority:.2f}")

if __name__ == "__main__":
    demonstrate_decision_making() 