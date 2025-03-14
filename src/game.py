import time
from src.agent_base import AgentBase
from src.agent_mcts import AgentMCTS
from src.fire import Fire
import os
from copy import deepcopy

FIRE_TICKS = 2 # Determine how often the fire spreads


class Game:
    def __init__(self, game_map):
        self.game_map, agent_positions, fire_positions, self.safety_positions = self.__read_map(game_map)
        self.agents = [AgentBase(self.game_map, pos, self.safety_positions) for pos in agent_positions]  # Use based Agent
        # self.agents = [AgentMCTS(self.game_map, pos, self.safety_positions) for pos in agent_positions]  # Use MCTS-based Agent
        self.agent_num = len(self.agents) # Number of agents
        self.fire = Fire(self.game_map, fire_positions)
        self.ticks = 0
        self.safe = 0 # Number of safe agents
        self.dead = 0 # Number of dead agents

    def run(self):
        """ Run the game"""

        while True:
            # Check if the game is ended
            if self.__check_end():
                break

            time.sleep(0.5)
            
            # Update each agent position
            new_agents = []
            for i, agent in enumerate(self.agents):
                agent_status = self.agents[i].move_agent(self.fire.fire_positions)
                
                # Check the status of the agent and update the statics
                if agent_status == 0: # Dead
                    self.dead += 1
                elif agent_status == 1: # Alive
                    new_agents.append(agent)
                elif agent_status == 2: # Saved
                    self.safe += 1

            self.agents = new_agents

            # Fire moves after every few ticks
            if self.ticks % FIRE_TICKS == FIRE_TICKS - 1:
                self.agents, dead_num = self.fire.move_fire(self.agents)
                self.dead += dead_num

            # Clear the terminal
            os.system('cls' if os.name == 'nt' else 'clear')

            # Update the tick and print the map
            self.ticks += 1
            self.print_game()



    def __read_map(self, game_map):
        """ Read game map to get clean map with road and wall and get agent positions, fire positions, and safety positions """
        agent_positions = []
        fire_positions = []
        safety_positions = []

        for r in range(len(game_map)):
            for c in range(len(game_map[0])):
                if game_map[r][c] == 'P':
                    agent_positions.append((r,c))
                    game_map[r][c] = ' '
                elif game_map[r][c] == 'F':
                    fire_positions.append((r,c))
                    game_map[r][c] = ' ' 
                elif game_map[r][c] == 'S':
                    safety_positions.append((r,c))
                    game_map[r][c] = ' ' 

        return game_map, agent_positions, fire_positions, safety_positions
        

    def __get_output_map(self):
        """ Get the map array with its status """
        output_map = deepcopy(self.game_map)

        for agent in self.agents:
            agent_position = agent.agent_position
            output_map[agent_position[0]][agent_position[1]] = 'P'
        
        for fire_position in self.fire.fire_positions:
            output_map[fire_position[0]][fire_position[1]] = 'F'

        for safety_position in self.safety_positions:
            output_map[safety_position[0]][safety_position[1]] = 'S'

        return output_map

    def print_game(self):
        """ Console the map """
        output_map = self.__get_output_map()
        qnt_lines = len(output_map)
        qnt_columns = len(output_map[0])
        print(f"Ticks: {self.ticks}, Safe: {self.safe}, Dead: {self.dead}")
        for i in range(qnt_lines):
            for j in range(qnt_columns):
                print(output_map[i][j], end=" ")
            print()

    def __check_end(self):
        """ Check if the all the agent has already been dead or safe """
        if len(self.agents) == 0:
            print(f"Game ended")
            print(f"With {self.agent_num} Agents")
            return True