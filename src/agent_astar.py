import heapq
from src.agent_base import AgentBase, WALL

class AgentAStar(AgentBase):
    def __init__(self, game_map, agent_position, safety_positions):
        super().__init__(game_map, agent_position, safety_positions)

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, position, blocked_positions):
        row, col = position
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < len(self.game_map) and 0 <= nc < len(self.game_map[0]):
                if (nr, nc) not in blocked_positions:
                    neighbors.append((nr, nc))
        return neighbors

    def a_star_search(self, start, goal, blocked_positions):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current_f, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            for neighbor in self.get_neighbors(current, blocked_positions):
                tentative_g = g_score.get(current, float('inf')) + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))
                    f_score[neighbor] = f

        return None

    def move_agent(self, fire_positions):
        fire_adjacent = set()
        for (r, c) in fire_positions:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(self.game_map) and 0 <= nc < len(self.game_map[0]):
                    fire_adjacent.add((nr, nc))

        blocked = set()
        for r in range(len(self.game_map)):
            for c in range(len(self.game_map[0])):
                if self.game_map[r][c] == WALL:
                    blocked.add((r, c))
        blocked.update(fire_positions)
        blocked.update(fire_adjacent)

        sorted_safety = sorted(
            self.safety_positions,
            key=lambda pos: self.heuristic(pos, self.agent_position)
        )

        path = None
        for safety_pos in sorted_safety:
            path = self.a_star_search(self.agent_position, safety_pos, blocked)
            if path:
                break

        new_position = self.agent_position
        if path and len(path) >= 2:
            new_position = path[1]

        self.agent_position = new_position
        self.distance_traveled += 1

        if new_position in fire_positions:
            return 0
        elif new_position in self.safety_positions:
            return 2
        else:
            return 1