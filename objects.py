from position import Position
from record import *
import pygame


class GameObject:
    _position = None
    _display = True

    def __init__(self, x, y):
        self._position = Position(x, y)

    def get_position(self):
        return self._position

    def get_coordinate(self):
        return self._position.get_coordinate()

    def set_position(self, x, y):
        self._position = Position(x, y)


class Action(Enum):
    MOVE_UP = 'U'
    MOVE_DOWN = 'D'
    MOVE_LEFT = 'L'
    MOVE_RIGHT = 'R'
    PICK = 'P'
    KILL = 'K'
    WAIT = 'W'


class Role(GameObject):
    __type = None
    __good_at = None
    __weapon = None
    __alive = True
    __movable = True
    __auto = True
    __ai = None

    def __init__(self, x, y, role_type, good_at):
        super().__init__(x, y)
        self.__type = role_type
        self.__good_at = good_at
        if role_type == RoleType.VICTIM:
            self.__movable = False

    def get_type(self):
        return self.__type

    def is_good_at(self):
        return self.__good_at

    def get_weapon(self):
        return self.__weapon

    def pick_weapon(self, weapon):
        self.__weapon = weapon

    def is_alive(self):
        return self.__alive

    def killed(self):
        self.__alive = False

    def is_movable(self):
        return self.__movable

    def set_movable(self, movable):
        self.__movable = movable

    def set_human_play(self):
        self.__auto = False
        self.__ai = None

    def set_ai(self, ai):
        self.__ai = ai

    # take random action for AI player
    def move(self, actions, buttons, funcs):
        if self.__auto:
            return self.__ai.next(self._position, actions)
        else:
            mark = True
            action = None
            while mark:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        buttons[0].handle_event(funcs[0])
                    if event.type == pygame.QUIT:
                        quit(0)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and Action.PICK in actions:
                            mark = False
                            action = Action.PICK
                        elif event.key == pygame.K_SPACE and Action.KILL in actions:
                            mark = False
                            action = Action.KILL
                        elif event.key == pygame.K_w and Action.MOVE_UP in actions:
                            mark = False
                            action = Action.MOVE_UP
                        elif event.key == pygame.K_s and Action.MOVE_DOWN in actions:
                            mark = False
                            action = Action.MOVE_DOWN
                        elif event.key == pygame.K_a and Action.MOVE_LEFT in actions:
                            mark = False
                            action = Action.MOVE_LEFT
                        elif event.key == pygame.K_d and Action.MOVE_RIGHT in actions:
                            mark = False
                            action = Action.MOVE_RIGHT
            return action

    def __str__(self):
        x, y = self.get_coordinate()
        return '%s x=%d y=%d' % (self.get_type(), x, y)


class WeaponType(Enum):
    KNIFE = 'Knife'
    ROPE = 'Rope'
    POISON = 'Poison'
    GUN = 'Gun'
    BLADE = 'Blade'

    def __str__(self):
        return self.value

    def get_code(self):
        if self == WeaponType.KNIFE:
            return 0
        elif self == WeaponType.ROPE:
            return 1
        elif self == WeaponType.POISON:
            return 2
        elif self == WeaponType.GUN:
            return 4
        elif self == WeaponType.BLADE:
            return 5


class Weapon(GameObject):
    __type = None
    __owner = None
    __collectable = True

    def __init__(self, x, y, weapon_type):
        super().__init__(x, y)
        self.__type = weapon_type

    def picked(self, owner):
        self._display = False
        self.__collectable = False
        self.__owner = owner

    def is_collectable(self):
        return self.__collectable

    def get_coordinate(self):
        if self.__owner is not None:
            return self.__owner.get_coordinate()
        return super().get_coordinate()

    def get_type(self):
        return self.__type

    def __str__(self):
        x, y = self.get_coordinate()
        return 'Weapon: %s x=%d y=%d' % (self.get_type(), x, y)

