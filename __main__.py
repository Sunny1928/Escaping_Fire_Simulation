from src.game import Game
from copy import deepcopy
import argparse

# Define game constants
SAFE_ZONE = "S"
FIRE = "F"
WALL = "="
PACMAN = "P"

game_map = [
    ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '='],
    ['=', 'S', ' ', ' ', ' ', '=', 'P', ' ', ' ', ' ', 'P', ' ', '=', ' ', ' ', ' ', ' ', 'S', '='],
    ['=', ' ', ' ', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '=', ' ', ' ', ' ', '=', ' ', '='],
    ['=', ' ', ' ', ' ', ' ', '=', ' ', ' ', ' ', ' ', ' ', ' ', '=', 'P', 'P', ' ', ' ', ' ', '='],
    ['=', ' ', ' ', ' ', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '=', ' ', ' ', 'P', 'P', ' ', '='],
    ['=', ' ', ' ', ' ', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '=', '=', ' ', 'P', 'P', ' ', '='],
    ['=', ' ', ' ', ' ', 'P', ' ', ' ', 'P', ' ', ' ', ' ', ' ', '=', '=', '=', ' ', ' ', ' ', '='],
    ['=', 'P', '=', '=', '=', '=', ' ', ' ', '=', ' ', ' ', ' ', '=', '=', ' ', ' ', ' ', 'P', '='],
    ['=', ' ', '=', ' ', ' ', '=', ' ', '=', '=', ' ', ' ', ' ', '=', ' ', ' ', ' ', ' ', ' ', '='],
    ['=', ' ', '=', ' ', ' ', '=', ' ', '=', '=', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '='],
    ['=', ' ', '=', '=', ' ', '=', ' ', ' ', '=', '=', 'F', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '='],
    ['=', ' ', '=', '=', ' ', '=', ' ', ' ', '=', '=', 'P', ' ', ' ', ' ', ' ', ' ', ' ', '=', '='],
    ['=', 'P', '=', ' ', ' ', '=', ' ', '=', '=', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '=', '='],
    ['=', ' ', '=', ' ', ' ', '=', ' ', '=', '=', ' ', ' ', ' ', ' ', '=', ' ', 'P', '=', 'P', '='],
    ['=', ' ', ' ', ' ', 'P', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '=', ' ', '=', ' ', ' ', '='],
    ['=', ' ', ' ', ' ', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '=', '=', '=', ' ', ' ', ' ', '='],
    ['=', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '=', '=', ' ', ' ', ' ', '='],
    ['=', ' ', ' ', ' ', ' ', '=', '=', ' ', 'P', ' ', ' ', ' ', ' ', '=', ' ', ' ', ' ', ' ', '='],
    ['=', ' ', 'P', ' ', ' ', '=', '=', ' ', 'P', ' ', ' ', ' ', ' ', '=', ' ', ' ', ' ', ' ', '='],
    ['=', ' ', 'P', ' ', ' ', ' ', ' ', ' ', '=', '=', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '='],
    ['=', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '=', '=', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '='],
    ['=', 'S', ' ', ' ', ' ', 'P', ' ', ' ', '=', '=', 'P', ' ', ' ', ' ', ' ', ' ', ' ', 'S', '='],
    ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=']]

def parse_args():
    parser = argparse.ArgumentParser(description="Evacuation Strategy Experiment")

    parser.add_argument(
        "--method", 
        type=str, 
        choices=["MCTS", "Random", "Qlearning", "AStar"], 
        required=True, 
        help="Choose the method: MCTS, Random, Astar, or Qlearning"
    )
    parser.add_argument(
        "--rollout", 
        type=int, 
        default=100, 
        help="Number of epochs used for training MCTS and Q-learning"
    )
    parser.add_argument(
        "--end_ticks", 
        type=int, 
        default=7, 
        help="End tick for MCTS"
    )
    parser.add_argument(
        "--iter", 
        type=int, 
        default=10, 
        help="Number of times to run the experiment for averaging performance"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    res_tick = []
    res_safe = []
    objective = []
    for _ in range(args.iter):
        tick, safe, num_agents, obj = Game(deepcopy(game_map), args.method, rollout=args.rollout, end_ticks=args.end_ticks).run()
        res_tick.append(tick)
        res_safe.append(safe)
        objective.append(obj)

    print(f"Method: {args.method}")
    print(f"Average Saved Agent: {round(sum(res_safe)/(num_agents*args.iter), 2)}")
    print(f"Average Time: {round(sum(res_tick)/args.iter, 2)}")
    print(f"Objective function: {round(sum(objective) / len(objective))}")
    print(f"Average objective: {round(sum(objective) / (num_agents*len(objective)))}")

