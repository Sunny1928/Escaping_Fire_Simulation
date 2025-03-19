# **Fire Evacuation Simulation**

A Python-based terminal simulation where agents attempt to escape a spreading fire using different strategies.

## **Overview**

This project simulates a fire evacuation scenario where multiple agents attempt to escape from a fire using different decision-making methods. The implemented methods include random movement, Monte Carlo Tree Search (MCTS), and Q-learning.

## **Methods**

- **Random**: Agents move arbitrarily without strategic planning.
- **MCTS (Monte Carlo Tree Search)**: Agents use a search-based approach to determine optimal moves.
- **Q-learning**: Agents learn optimal escape strategies through reinforcement learning.

## Run the simulation

To run the simulation, use the following command:

```
python main.py --method <METHOD> --rollout <EPOCHS> --end_ticks <TICKS> --iter <ITERATIONS>
```

### Arguments:

- `--method`: Choose from `MCTS`, `Random`, or `Qlearning`. (Required)
- `--rollout`: Number of epochs for training MCTS and Q-learning. (Default: 100)
- `--end_ticks`: End tick for MCTS. (Default: 7)
- `--iter`: Number of iterations to average performance. (Default: 10)

### Example usage:

Run the simulation using Q-learning with 200 training epochs and averaging over 5 runs:

```
python main.py --method Qlearning --rollout 200 --iter 5
```

Run the simulation using MCTS with an end tick of 10:

```
python main.py --method MCTS --end_ticks 10
```

## Variable

- Define game constants In **main**.py

```
SAFE_ZONE = "S"
FIRE = "F"
WALL = "="
PACMAN = "P"
```

- In /src/game.py

```
FIRE_TICKS = 2 # Determine how often the fire spreads
```

## Usage

Update /src/agent_base.py
