import numpy as np
import random
import math
from collections import defaultdict
from src.agent_base import WALL, ACTIONS, DIRECTION_MAP
from src.fire import Fire
import copy


class AgentQLearning:
    def __init__(self, game_map, agent_position, safety_positions, learning_rate=0.1, discount_factor=0.9, epsilon=0.2):
        self.game_map = game_map
        self.agent_position = agent_position
        self.safety_positions = set(safety_positions)
        self.fire_positions = set()
        
        # Q-table: State (position) x Action
        self.q_table = defaultdict(lambda: np.zeros(len(ACTIONS)))

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.distance_traveled = 0

    def get_valid_actions(self, position):
        """Returns list of valid action indices from current position."""
        row, col = position
        valid_actions = []

        for action_idx, action in ACTIONS.items():
            dx, dy = DIRECTION_MAP[action]
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < len(self.game_map) and 0 <= new_col < len(self.game_map[0]):
                if self.game_map[new_row][new_col] != WALL:
                    valid_actions.append(action_idx)
        return valid_actions

    def get_distance(self, pos1, pos2):
        """Compute Manhattan distance"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def compute_reward(self, position, safety_positions, fire_positions):
        """Reward based on proximity to safety/fire"""
        if position in self.safety_positions:
            return 100  # High reward for reaching safety
        if position in self.fire_positions:
            return -100  # Heavy penalty for fire

        safety_distances = [self.get_distance(position, safe) for safe in safety_positions]
        fire_distances = [self.get_distance(position, fire) for fire in fire_positions]

        nearest_safety_distance = min(safety_distances) if safety_distances else float('inf')
        nearest_fire_distance = min(fire_distances) if fire_distances else float('inf')

        return 10 - nearest_safety_distance + (nearest_fire_distance - 5)

    def choose_action(self, state, train=True):
        """Epsilon-greedy action selection."""
        valid_actions = self.get_valid_actions(state)
        if not valid_actions:
            return None  # No valid moves

        if train and random.random() < self.epsilon:
            return random.choice(valid_actions)  # Explore
        else:
            q_values = self.q_table[state]
            return max(valid_actions, key=lambda a: q_values[a])  # Exploit best action

    def learn(self, fire, agent_id, fire_ticks, episodes=200, max_steps_per_episode=100):
        """Train agent via Q-learning."""
        print(f'Agent {agent_id} start learning! Learn {episodes} episodes')
        for episode in range(episodes):
            state = tuple(self.agent_position)  # Start at initial position
            fire_cpy = copy.deepcopy(fire)
            for i in range(max_steps_per_episode):
                action = self.choose_action(state)
                if action is None:
                    break  # No valid actions, terminate episode

                dx, dy = DIRECTION_MAP[ACTIONS[action]]
                next_state = (state[0] + dx, state[1] + dy)

                reward = self.compute_reward(next_state, self.safety_positions, fire_cpy.fire_positions)
                valid_actions = self.get_valid_actions(next_state)
                if not valid_actions:
                    max_future_q = 0
                else:
                    max_future_q = max(self.q_table[next_state][a] for a in valid_actions) 

                # Temporal Difference update (Q-learning update)
                self.q_table[state][action] += self.learning_rate * (
                    reward + self.discount_factor * max_future_q - self.q_table[state][action]
                )

                state = next_state
                if i % fire_ticks == 0:
                    fire.expand()

                if state in self.fire_positions or state in self.safety_positions:
                    break  # Stop episode if agent reaches fire or safety
        
        print(f'Agent {agent_id} Done Learning!')
    def move_agent(self, fire_positions):
        """Move agent using the trained Q-table."""
        self.fire_positions = set(fire_positions)
        current_state = tuple(self.agent_position)

        action = self.choose_action(current_state, train=False)
        if action is None:
            return 0  # Stuck/dead

        dx, dy = DIRECTION_MAP[ACTIONS[action]]
        new_position = (self.agent_position[0] + dx, self.agent_position[1] + dy)
        self.agent_position = new_position
        self.distance_traveled += 1

        if new_position in self.fire_positions:
            return 0  # Dead
        elif new_position in self.safety_positions:
            return 2  # Safe
        return 1  # Alive
