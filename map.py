from tile import Tile, TileType
from random import random, randint
from flood import generate

# 空地数量
X = 3


class Map:
    __map = []
    __rows = 0
    __cols = 0

    def __init__(self, config):
        if config['map'] == 'random':
            if not self.__load_map(config):
                print('Wrong map file.')
                quit(1)
        else:
            if not self.__load_map1(config):
                print('Wrong map file.')
                quit(1)

    def __load_map(self, config):
        self.__cols = max([
            (config['room_size'][0] + 1) * config['room_num'] + X,
            (config['store_size'][0] + 1) * config['store_num'] + X
        ])
        # print(config)
        self.__rows = config['room_size'][1] + config['store_size'][1] + 4 + X
        for i in range(0, self.__rows):
            self.__map.append([])
            for j in range(0, self.__cols):
                self.__map[i].append('C')

        for i in range(0, self.__rows):
            self.__map[i][0] = 'W'
            self.__map[i][self.__cols - 1] = 'W'
        for j in range(0, self.__cols):
            self.__map[0][j] = 'W'
            self.__map[self.__rows - 1][j] = 'W'

        x = config['room_size'][0]
        y = config['room_size'][1]
        room_position = [[1, 1], [1, self.__cols - 1 - x]]
        for r in range(1, config['room_num'] - 1):
            roomx = randint(room_position[r - 1][1] + x + 1, self.__cols - (x + 1) * (config['room_num'] - r) - 1)
            room_position.insert(r, [1, roomx])
        self.rooms = []
        for room in room_position:
            self.rooms.append([room[0] + int(y / x), room[1] + int(x / 2)])
        for room in room_position:
            for i in range(room[0], room[0] + y):
                for j in range(room[1], room[1] + x):
                    self.__map[i][j] = 'R'
            for i in range(room[0] - 1, room[0] + y + 1):
                self.__map[i][room[1] - 1] = 'W'
                self.__map[i][room[1] + x] = 'W'
            for j in range(room[1] - 1, room[1] + x + 1):
                self.__map[room[0] - 1][j] = 'W'
                self.__map[room[0] + y][j] = 'W'
            self.__map[room[0] + y][room[1]] = 'D'

        store_start = self.__rows - config['store_size'][1] - 1
        x = config['store_size'][0]
        y = config['store_size'][1]
        store_position = [[store_start, 1], [store_start, self.__cols - 1 - x]]
        for r in range(1, config['store_num'] - 1):
            storex = randint(store_position[r - 1][1] + x + 1, self.__cols - (x + 1) * (config['store_num'] - r) - 1)
            store_position.insert(r, [store_start, storex])
        self.stores = []
        for store in store_position:
            self.stores.append([store[0] + int(y / x), store[1] + int(x / 2)])
        for store in store_position:
            for i in range(store[0], store[0] + y):
                for j in range(store[1], store[1] + x):
                    self.__map[i][j] = 'R'
            for i in range(store[0] - 1, store[0] + y + 1):
                self.__map[i][store[1] - 1] = 'W'
                self.__map[i][store[1] + x] = 'W'
            for j in range(store[1] - 1, store[1] + x + 1):
                self.__map[store[0] - 1][j] = 'W'
                self.__map[store[0] + y][j] = 'W'
            self.__map[store[0] - 1][store[1]] = 'D'

        for i in range(0, self.__rows):
            for j in range(0, self.__cols):
                if self.__map[i][j] == 'W':
                    try:
                        neighbours = [
                            self.__map[i - 1][j],
                            self.__map[i + 1][j],
                            self.__map[i][j - 1],
                            self.__map[i][j + 1]
                        ]
                        if neighbours.count('C') == 1 and neighbours.count('R') > 0 and neighbours.count('D') == 0:
                            if random() < 0.5:
                                self.__map[i][j] = 'D'
                    except:
                        pass

        with open('test.txt', 'w', encoding='utf-8') as f:
            for i in range(self.__rows):
                f.write(''.join([str(_) for _ in self.__map[i]]) + '\n')

        for i in range(0, self.__rows):
            for j in range(0, self.__cols):
                self.__map[i][j] = Tile(i, j, TileType.get_type(self.__map[i][j]))
        return True

    def __load_map1(self, config):
        map_data, rooms, stores, rows, cols = generate(config)
        self.__rows = rows
        self.__cols = cols
        self.rooms = rooms
        self.stores = stores
        for i in range(0, self.__rows):
            self.__map.append([])
            for j in range(0, self.__cols):
                self.__map[i].append('C')
        for i in range(0, self.__rows):
            for j in range(0, self.__cols):
                self.__map[i][j] = Tile(i, j, TileType.get_type(map_data[i][j]))
        return True
        # with open('map/1.txt', 'r') as file:
        #     try:
        #         line = file.readline()
        #         self.__rows = int(line)
        #         line = file.readline()
        #         self.__cols = int(line)
        #     except ValueError:
        #         return False
        #     try:
        #         for i in range(0, self.__rows):
        #             self.__map.append([])
        #             line = file.readline()
        #             if len(line) < self.__cols:
        #                 return
        #             for j in range(0, self.__cols):
        #                 code = line[j:j + 1]
        #                 self.__map[i].append(Tile(i, j, TileType.get_type(code)))
        #     except ValueError:
        #         return False
        # return True

    def get_rows(self):
        return self.__rows

    def get_cols(self):
        return self.__cols

    def get_tile_type(self, x, y):
        return self.__map[x][y].get_type()

    def __str__(self):
        value = ''
        for i in range(0, self.__rows):
            for j in range(0, self.__cols):
                value += self.__map[i][j].get_type().get_code()
            value += '\n'
        return value
