# Simulate the time required for everyone to escape the fire

A simple Python-based terminal simulation of agents escaping fire using different methods.

## Method
- Based (Randomly move)
- MCTS

## Running

To start application, type:

```
python .
```
## Variable
- Define game constants In __main__.py
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