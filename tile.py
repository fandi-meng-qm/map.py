from position import Position
from enum import Enum


class TileType(Enum):
    WALL = 'W'
    DOOR = 'D'
    ROOM = 'R'
    CORRIDOR = 'C'

    @staticmethod
    def get_type(code):
        if code == 'W':
            return TileType.WALL
        elif code == 'D':
            return TileType.DOOR
        elif code == 'R':
            return TileType.ROOM
        elif code == 'C':
            return TileType.CORRIDOR

    def get_code(self):
        return self.value


class Tile:
    __position = None
    __type = None

    def __init__(self, x, y, tile_type):
        self.__position = Position(x, y)
        self.__type = tile_type

    def get_position(self):
        return self.__position

    def get_coordinate(self):
        return self.__position.get_coordinate()

    def get_type(self):
        return self.__type

    def __str__(self):
        x, y = self.get_coordinate()
        return 'Tile x=%d y=%d %s' % (x, y, self.__type)
