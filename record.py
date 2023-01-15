from enum import Enum


class EventType(Enum):
    MEET = 0
    DEATH = 1


class RoleType(Enum):
    CLEANER = 'cleaner'
    WRITER = 'writer'
    WAITRESS = 'waitress'
    VICTIM = 'victim'
    RANGER = 'ranger'
    KNIGHT = 'knight'

    def __str__(self):
        return self.value

    def get_code(self):
        if self == RoleType.CLEANER:
            return 0
        elif self == RoleType.WRITER:
            return 1
        elif self == RoleType.WAITRESS:
            return 2
        elif self == RoleType.VICTIM:
            return 3
        elif self == RoleType.RANGER:
            return 4
        elif self == RoleType.KNIGHT:
            return 5

    @staticmethod
    def from_int(i):
        return [RoleType.CLEANER, RoleType.WRITER, RoleType.WAITRESS, RoleType.VICTIM, RoleType.RANGER, RoleType.KNIGHT][i]


class Record:
    _event = None
    _position = None
    _turn = None

    def __init__(self, position, turn):
        self._position = position
        self._turn = turn

    def get_type(self):
        return self._event

    def get_position(self):
        return self._position

    def get_turn(self):
        return self._turn


class DeathRecord(Record):
    __weapon = None

    def __init__(self, position, turn, weapon):
        super().__init__(position, turn)
        self._event = EventType.DEATH
        self.__weapon = weapon

    def get_weapon(self):
        return self.__weapon

    def __str__(self):
        return 'victim was killed by ' + str(self.__weapon) \
               + ' at ' + str(self._position) + ' in turn ' + str(self._turn)

    def get_numerical(self):
        x, y = self._position.get_coordinate()
        return [
            0, # killed
            6, # victim
            self.__weapon.get_code(),
            x,
            y,
            self._turn
        ]


class MeetRecord(Record):
    __role_a = None
    __role_b = None

    def __init__(self, position, turn, role_a, role_b):
        super().__init__(position, turn)
        self._event = EventType.MEET
        self.__role_a = role_a
        self.__role_b = role_b

    def __str__(self):
        return str(self.__role_a) + " meet " + str(self.__role_b) \
               + " at " + str(self._position) + ' in turn ' + str(self._turn)

    def get_role_a(self):
        return self.__role_a

    def get_role_b(self):
        return self.__role_b

    def get_numerical(self):
        x, y = self._position.get_coordinate()
        return [
            1, # meet
            self.__role_a.get_code(),
            self.__role_b.get_code(),
            x,
            y,
            self._turn
        ]

