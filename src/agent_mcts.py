import numpy as np
import random
import math
from collections import defaultdict

# Define game constants
WALL = "="

# Actions Mapping
ACTIONS = {
    0: "up",
    1: "down",
    2: "left",
    3: "right"
}

DIRECTION_MAP = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1)
}

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state  # Agent's current position
        self.parent = parent  # Parent node in the tree
        self.children = {}  # Store child nodes (action -> MCTSNode)
        self.visits = 0  # Number of times this node has been visited
        self.value = 0  # Cumulative reward

    def best_child(self, exploration_weight=1.0):
        """ Select the best child based on Upper Confidence Bound """
        return max(
            self.children.items(),
            key=lambda child: child[1].value / (child[1].visits + 1e-6) + exploration_weight * math.sqrt(math.log(self.visits + 1) / (child[1].visits + 1e-6))
        )[1]

    def is_fully_expanded(self, valid_moves):
        """ Check if all possible moves have been expanded """
        return set(self.children.keys()) == {action for action, _ in valid_moves}

    def get_unexpanded_moves(self, valid_moves):
        """ Return a list of moves that haven't been expanded yet """
        return [action for action, _ in valid_moves if action not in self.children]

class AgentMCTS:
    def __init__(self, game_map, agent_position, safety_positions, simulations=100, end_ticks=10):
        self.game_map = game_map
        self.agent_position = agent_position
        self.safety_positions = safety_positions
        self.fire_positions = None
        self.simulations = simulations
        self.end_ticks = end_ticks

    def get_valid_moves(self, position):
        """ Get all possible moves from the current position """
        row, col = position
        moves = []

        for action, (dx, dy) in DIRECTION_MAP.items():
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < len(self.game_map) and 0 <= new_col < len(self.game_map[0]):
                if self.game_map[new_row][new_col] not in [WALL]:  
                    moves.append((list(ACTIONS.keys())[list(ACTIONS.values()).index(action)], (new_row, new_col)))

        return moves

    def get_distance(self, pos1, pos2):
        """ Compute Manhattan distance between two positions """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def compute_reward(self, position):
        """ Compute reward based on proximity to safety and fire """
        # Distance to nearest safety spot
        safety_distances = [self.get_distance(position, safe) for safe in self.safety_positions]
        nearest_safety_distance = min(safety_distances) if safety_distances else float('inf')

        # Distance to nearest fire
        fire_distances = [self.get_distance(position, fire) for fire in self.fire_positions]
        nearest_fire_distance = min(fire_distances) if fire_distances else float('inf')

        # Reward formula
        reward = 10 - nearest_safety_distance  # Closer to safety = more reward
        reward += nearest_fire_distance - 5  # Closer to fire = penalty

        # Special cases
        if position in self.safety_positions:
            reward += 100  # Reached safety
        elif position in self.fire_positions:
            reward -= 100 # Got burned

        return reward

    def simulate(self, position, depth):
        """ Perform a random rollout (simulation) from the given position """
        total_reward = 0
        for _ in range(depth):  # Simulate up to 10 steps ahead
            valid_moves = self.get_valid_moves(position)
            if not valid_moves:
                return -10  # Negative reward for being stuck

            _, position = random.choice(valid_moves)  # Take a random action

            reward = self.compute_reward(position)
            if reward >= 100 or reward <= -100:
                return reward * depth  # End simulation if safety or fire is reached
            
            total_reward += reward * depth

        return total_reward  # Small penalty for each move to encourage efficiency


    def backpropagate(self, node, reward):
        """ Backpropagate the result of a simulation up the tree. """
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent  # Move up the tree

    def select_action(self):
        """ Perform MCTS to choose the best move for Agent. """
        root = MCTSNode(tuple(self.agent_position))

        for _ in range(self.simulations):  # Run multiple simulations
            node = root
            state = tuple(self.agent_position)

            # Selection: Traverse the tree using UCT until reaching an expandable node
            while node.is_fully_expanded(self.get_valid_moves(state)) and node.children:
                node = node.best_child()
                state = node.state

            # Expansion: Add a new child node for an unvisited action
            valid_moves = self.get_valid_moves(state)
            unexpanded_moves = node.get_unexpanded_moves(valid_moves)

            if unexpanded_moves:
                action = random.choice(unexpanded_moves)
                next_position = dict(valid_moves)[action]
                new_node = MCTSNode(next_position, parent=node)
                node.children[action] = new_node
                node = new_node
                state = next_position

            # Simulation: Perform a rollout from the new state
            reward = self.simulate(state, self.end_ticks)

            # Backpropagation: Update values in the tree
            self.backpropagate(node, reward)

        # Choose the best move from the root
        best_action = max(root.children.items(), key=lambda child: child[1].visits)[0]
        return best_action

    def move_agent(self, fire_positions):
        """ Use MCTS to move Agent intelligently. """
        self.fire_positions = fire_positions
        action = self.select_action()
        new_position = (self.agent_position[0] + DIRECTION_MAP[ACTIONS[action]][0], self.agent_position[1] + DIRECTION_MAP[ACTIONS[action]][1])
        self.agent_position = new_position
       
        status = 1 # Alive
        if self.agent_position in self.fire_positions:
            status = 0 # Dead
        elif self.agent_position in self.safety_positions:
            status = 2 # Safe


        return status