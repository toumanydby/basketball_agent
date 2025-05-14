import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Tuple
from src.rules.rules_engine import GameState, BasketballRules
from src.rules.metrics import Position, Player, BasketballMetrics
import matplotlib.pyplot as plt

Metrics = BasketballMetrics(15,28)
Rules = BasketballRules(Metrics)

def chain_evaluation(lStates: List[GameState]) -> dict:
    Ret = {
            'team1_attack_positions':[] ,
            'team2_attack_positions': [],
            'team1_defensive_positions': [],
            'team2_defensive_positions': [],
            'team1_spacing': [],
            'team2_spacing': [],
            'ball_possession_time': [],
            'team1_defensive_holes': [],
            'team2_defensive_holes': [],
            'team1_defensive_help': [],
            'team2_defensive_help': [],
            'zone_respect': [],
            'team1_defensive_positioning': [],
            'team2_defensive_positioning': []
        }  
    for i in range(len(lStates)):
        eval = BasketballRules.evaluate_game_state(Rules,lStates[i])
        Ret['team1_attack_positions'] += [eval['team1_attack_positions']] 
        Ret['team2_attack_positions'] += [eval['team2_attack_positions']] 
        Ret['team1_defensive_positions'] += [eval['team1_defensive_positions']] 
        Ret['team2_defensive_positions'] += [eval['team2_defensive_positions']] 
        Ret['team1_spacing'] += [eval['team1_spacing']] 
        Ret['team2_spacing'] += [eval['team2_spacing']] 
        Ret['ball_possession_time'] += [eval['ball_possession_time']] 
        Ret['team1_defensive_holes'] += [eval['team1_defensive_holes']] 
        Ret['team2_defensive_holes'] += [eval['team2_defensive_holes']] 
        Ret['team1_defensive_help'] += [eval['team1_defensive_help']] 
        Ret['team2_defensive_help'] += [eval['team2_defensive_help']] 
        Ret['zone_respect'] += [eval['zone_respect']] 
        Ret['team1_defensive_positioning'] += [eval['team1_defensive_positioning']] 
        Ret['team2_defensive_positioning'] += [eval['team2_defensive_positioning']] 
    return Ret

def recup_timestamp(lStates: List[GameState]) -> List[float]:
    Ret = []
    for i in range(len(lStates)):
       Ret = Ret + [lStates[i].timestamp]
    return Ret

def display_graphique(lStates: List[GameState]):
    evals = chain_evaluation(lStates)
    timestamps = recup_timestamp(lStates)

    plt.figure("Rule: attack positions, team 1")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['team1_attack_positions'])

    plt.figure("Rule: attack positions, team 2")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['team2_attack_positions'])

    plt.figure("Rule: defensive positions, team 1")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['team1_defensive_positions'])

    plt.figure("Rule: defensive positions, team 2")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['team2_defensive_positions'])

    plt.figure("Rule: spacing, team 1")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['team1_spacing'])

    plt.figure("Rule: spacing, team 2")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['team2_spacing'])

    plt.figure("Rule: ball possession time")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['ball_possession_time'])

    plt.figure("Rule: defensive holes, team 1")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['team1_defensive_holes'])

    plt.figure("Rule: defensive holes, team 2")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['team2_defensive_holes'])

    plt.figure("Rule: defensive assistance, team 1")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['team1_defensive_help'])

    plt.figure("Rule: defensive assistance, team 2")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['team2_defensive_help'])

    plt.figure("Rule: zone affiliation")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['zone_respect'])

    plt.figure("Rule: basket protection, team 1")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['team1_defensive_positioning'])

    plt.figure("Rule: basket protection, team 2")
    plt.ylabel("Respect of the rule")
    plt.xlabel("timestamp")
    plt.plot(timestamps, evals['team2_defensive_positioning'])



    plt.show()
    


Players1 = [Player(1, Position(15,16,5,7), 1, None), Player(2, Position(16,7,15,7), 1, None), Player(3, Position(10,11,2,4), 2, None), Player(4, Position(10,11,6,8), 2, None)] 
Players2 = [Player(1, Position(17,18,7,9), 1, None), Player(2, Position(18,19,7,9), 1, None), Player(3, Position(8,9,0,2), 2, None), Player(4, Position(8,9,4,6), 2, None)] 
state1 = GameState(Players1, Position(15,15.2, 16, 16.2), 1, (Position(0,0.3,8,8.3),Position(0,0.3,28,28.3)), 1, None)
state2 = GameState(Players1, Position(15,15.2, 16, 16.2), 1, (Position(0,0.3,8,8.3),Position(0,0.3,28,28.3)), 2, state1)

lGameState =[state1, state2]

display_graphique(lGameState)

