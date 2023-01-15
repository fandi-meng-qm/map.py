from objects import *


class Detective:
    __records = None
    __suspicion = {}
    __weapon_room = []
    __room = {}
    __ai = None
    __death_record = None

    def __init__(self, records, ai):
        self.__records = records
        self.__ai = ai
        self.__suspicion[RoleType.CLEANER] = 0
        self.__suspicion[RoleType.WRITER] = 0
        self.__suspicion[RoleType.WAITRESS] = 0
        self.__init_room()
        self.__init_weapon_room()
        for record in self.__records:
            if record.get_type() == EventType.DEATH:
                self.__death_record = record

    def __init_room(self):
        room = [Position(1, 1), Position(1, 2), Position(1, 1)]
        self.__room[0] = room
        room = [Position(1, 4), Position(1, 5), Position(2, 4)]
        self.__room[1] = room
        room = [Position(1, 7), Position(1, 8), Position(2, 7)]
        self.__room[2] = room
        room = [Position(1, 10), Position(1, 11), Position(2, 10)]
        self.__room[3] = room
        room = [Position(1, 13), Position(1, 14), Position(2, 13)]
        self.__room[4] = room
        room = [Position(1, 16), Position(1, 17), Position(2, 16)]
        self.__room[5] = room

    def __init_weapon_room(self):
        # G
        self.__weapon_room.append(Position(5, 2))
        self.__weapon_room.append(Position(6, 1))
        self.__weapon_room.append(Position(6, 2))
        self.__weapon_room.append(Position(6, 3))
        self.__weapon_room.append(Position(6, 4))
        self.__weapon_room.append(Position(7, 1))
        self.__weapon_room.append(Position(7, 2))
        self.__weapon_room.append(Position(7, 3))
        # H
        self.__weapon_room.append(Position(5, 9))
        self.__weapon_room.append(Position(6, 7))
        self.__weapon_room.append(Position(6, 8))
        self.__weapon_room.append(Position(6, 9))
        self.__weapon_room.append(Position(6, 10))
        self.__weapon_room.append(Position(6, 11))
        self.__weapon_room.append(Position(7, 8))
        self.__weapon_room.append(Position(7, 9))
        self.__weapon_room.append(Position(7, 10))
        # I
        self.__weapon_room.append(Position(5, 16))
        self.__weapon_room.append(Position(6, 14))
        self.__weapon_room.append(Position(6, 15))
        self.__weapon_room.append(Position(6, 16))
        self.__weapon_room.append(Position(6, 17))
        self.__weapon_room.append(Position(7, 15))
        self.__weapon_room.append(Position(7, 16))
        self.__weapon_room.append(Position(7, 17))

    def __have_murder_time(self):
        for record in self.__records:
            if record.get_type() == EventType.MEET:
                difference = abs(self.__death_record.get_turn() - record.get_turn())
                path = self.__ai.find_path(record.get_position(), self.__ai.bfs(self.__death_record.get_position()))
                if difference < len(path):
                    if record.get_turn() < self.__death_record.get_turn():
                        self.__suspicion[record.get_role_a()] += 30
                        self.__suspicion[record.get_role_b()] += 30
                    else:
                        self.__suspicion[record.get_role_a()] += 15
                        self.__suspicion[record.get_role_b()] += 15
                else:
                    if record.get_turn() < self.__death_record.get_turn():
                        self.__suspicion[RoleType.from_int(3 - record.get_role_a().get_code() -
                                                           record.get_role_b().get_code())] += 100

    def __pass_same_room(self):
        times = []
        for role in self.__suspicion:
            times.append([0, 0, 0, 0, 0, 0])
        for record in self.__records:
            if record.get_type() == EventType.MEET:
                position = record.get_position()
                for key in self.__room.keys():
                    if position in self.__room[key]:
                        times[record.get_role_a().get_code()][key] += 1
                        times[record.get_role_b().get_code()][key] += 1
                        break
        for role in self.__suspicion.keys():
            for key in self.__room.keys():
                if times[role.get_code()][key] >= 2:
                    self.__suspicion[role] += times[role.get_code()][key]

    def __pass_weapon_room(self):
        for record in self.__records:
            if record.get_type() == EventType.MEET and record.get_turn() < self.__death_record.get_turn():
                if record.get_position() in self.__weapon_room:
                    self.__suspicion[record.get_role_a()] += 8
                    self.__suspicion[record.get_role_b()] += 8

    def __no_records(self):
        meet = {}
        for key in self.__suspicion.keys():
            meet[key] = 0
        for record in self.__records:
            if record.get_type() == EventType.MEET:
                meet[record.get_role_a()] += 1
                meet[record.get_role_b()] += 1
        for key in meet.keys():
            if meet[key] == 0:
                self.__suspicion[key] += 5

    def detect(self):
        if self.__death_record is None:
            print('Nothing to detect.')
            return
        self.__have_murder_time()
        self.__pass_same_room()
        self.__pass_weapon_room()
        self.__no_records()
        print('suspicion point:')
        for role in self.__suspicion.keys():
            print('%s: %d' % (role, self.__suspicion[role]))
