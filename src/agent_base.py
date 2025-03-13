from random import choice

# Define game constants
WALL = "="

"""
Status
0: dead
1: alive
2: in safe zone
"""

move_dict = {
    'up': (-1, 0),
    'left': (0, -1),
    'down': (1, 0),
    'right': (0, 1),
}


class AgentBase:
    def __init__(self, game_map, agent_position, safety_positions):
        self.game_map = game_map
        self.agent_position = agent_position
        self.safety_positions = safety_positions
        self.move = None

    @property
    def next_agent_position_location(self):
        """ Get the next position of current agent """
        positions = {
            "up": (self.agent_position[0] - 1, self.agent_position[1]),
            "down": (self.agent_position[0] + 1, self.agent_position[1]),
            "left": (self.agent_position[0], self.agent_position[1] - 1),
            "right": (self.agent_position[0], self.agent_position[1] + 1)
        }

        return positions.get(self.move)
    
    def __get_move_possibilities(self):
        """ Retrieve all possible movement options (only wall is impossible) """
        possibilities = []
        agent_column = [l[self.agent_position[1]] for l in self.game_map]
        agent_line = self.game_map[self.agent_position[0]]

        factory_status = {
            "up": agent_column[self.agent_position[0] - 1],
            "down": agent_column[self.agent_position[0] + 1],
            "left": agent_line[self.agent_position[1] - 1],
            "right": agent_line[self.agent_position[1] + 1]
        }

        for possibility, possibility_value in zip(factory_status.keys(), factory_status.values()):
            if possibility_value not in [WALL]:
                possibilities.append(possibility)

        return possibilities
    
    def get_move(self):
        """ Randomly move in the move_possibilities """
        move = choice(self.__get_move_possibilities())

        return move
        

    def move_agent(self, fire_positions):
        """ Move Agent and return agent status (0: Dead, 1: Alive, 2: Safe)"""
        # get the move of the agent 
        self.move = self.get_move()
        # print(self.move)
        new_position = (self.agent_position[0] + move_dict[self.move][0], self.agent_position[1] + move_dict[self.move][1])
        self.agent_position = new_position

        # Update the status of agent
        status = 1 # Alive
        if self.next_agent_position_location in fire_positions:
            status = 0 # Dead
        elif self.next_agent_position_location in self.safety_positions:
            status = 2 # Safe

        return status
