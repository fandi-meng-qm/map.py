import random
from objects import *
from tile import *


class AI:
    _map = None
    _destinations = []
    _current_destination = None

    def __init__(self, new_map, destinations):
        self._map = new_map
        self._destinations = destinations.copy()

    def _next_destination(self):
        index = random.randint(0, len(self._destinations) - 1)
        self._current_destination = self._destinations[index]

    def next(self, position, actions):
        index = random.randint(0, len(actions) - 1)
        return actions[index]

    def neighbors(self, position):
        neighbors = []
        x, y = position.get_coordinate()
        if x - 1 >= 0:
            if self._map.get_tile_type(x - 1, y) is not TileType.WALL:
                neighbors.append(Position(x - 1, y))
        if x + 1 < self._map.get_rows():
            if self._map.get_tile_type(x + 1, y) is not TileType.WALL:
                neighbors.append(Position(x + 1, y))
        if y - 1 >= 0:
            if self._map.get_tile_type(x, y - 1) is not TileType.WALL:
                neighbors.append(Position(x, y - 1))
        if y + 1 < self._map.get_cols():
            if self._map.get_tile_type(x, y + 1) is not TileType.WALL:
                neighbors.append(Position(x, y + 1))
        return neighbors


class RandomAction(AI):
    def __init__(self, new_map, destinations):
        super().__init__(new_map, destinations)


class GoodGuyBFS(AI):
    def __init__(self, new_map, destinations):
        super().__init__(new_map, destinations)
        self._next_destination()

    def next(self, position, actions):
        # if all rooms are searched, change to random mode
        if len(self._destinations) == 0:
            return super().next(position, actions)
        # if a room is searched, find a new destination
        x, y = position.get_coordinate()
        destination_x, destination_y = self._current_destination.get_coordinate()
        if x == destination_x and y == destination_y:
            self._destinations.remove(self._current_destination)
            if len(self._destinations) > 0:
                self._next_destination()
            else:
                return super().next(position, actions)
        parent = self.bfs(position)
        path = self.find_path(self._current_destination, parent)
        next_x, next_y = path[-3].get_coordinate()
        action = None
        if next_x == x - 1 and next_y == y:
            action = Action.MOVE_UP
        if next_x == x + 1 and next_y == y:
            action = Action.MOVE_DOWN
        if next_x == x and next_y == y - 1:
            action = Action.MOVE_LEFT
        if next_x == x and next_y == y + 1:
            action = Action.MOVE_RIGHT
        return action

    def bfs(self, position):
        queue = []
        seen = set()
        queue.append(position)
        seen.add(position)
        parent = {position: None}
        while len(queue) > 0:
            vertex = queue.pop(0)
            neighbors = self.neighbors(vertex)
            for node in neighbors:
                if node not in seen:
                    queue.append(node)
                    seen.add(node)
                    parent[node] = vertex
        return parent

    @staticmethod
    def find_path(destination, parent):
        temp_destination = destination
        path = [temp_destination]
        while temp_destination is not None:
            path.append(parent[temp_destination])
            temp_destination = parent[temp_destination]
        return path
