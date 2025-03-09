
from random import choice
from copy import deepcopy

GOOD_BLOCKS = [".", " ", "="]
PACMAN = "P"


class Fire:
    def __init__(self, game_map, fire_positions):
        self.game_map = game_map # Game map only with the wall and road
        self.fire_positions = set(fire_positions)  # Store multiple fire positions
        self.seen = set(fire_positions)  # Track fire positions to prevent duplicates

    def __get_fire_expansion_possibilities(self, position):
        """ Get all possible expansion positions from a given fire position """
        possibilities = []
        row, col = position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            new_row, new_col = row+dx, col+dy
            if 0 <= new_row < len(self.game_map) and 0 <= new_col < len(self.game_map[0]):
                if (new_row, new_col) not in self.seen:
                    possibilities.append((new_row, new_col))

        return possibilities

    def move_fire(self, agent_agents):
        """ Expand fire in all four directions """
        # Update the fire positions
        new_fire_positions = set()
        for fire_position in self.fire_positions:
            possible_positions = self.__get_fire_expansion_possibilities(fire_position)
            for new_position in possible_positions:
                new_fire_positions.add(new_position)
                self.seen.add(new_position)

        self.fire_positions.update(new_fire_positions)  # Update fire positions list

        # Update the agent agents
        new_agent_agents = []
        for agent_agent in agent_agents:
            if agent_agent.agent_position not in self.fire_positions:
                new_agent_agents.append(agent_agent)

        # Update the dead number of agent agents
        dead_num = len(agent_agents) - len(new_agent_agents)

        return new_agent_agents, dead_num