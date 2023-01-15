from map import Map
from algorithm import *
from detective import *
import constant
import random
import os, pickle


class DeadlyHotel:
    _map = None
    _destinations = []
    _roles = []
    _weapons = []
    _role_origins = []
    _weapon_origins = []
    _turns = 0
    _records = []

    def __init__(self, config):
        self._turns = config['turn_num']
        self.config = config

    def display(self):
        print('Map:')
        print(self._map)
        for role in self._roles:
            print(role)
        print()
        for weapon in self._weapons:
            print(weapon)

    def init(self):
        self._map = Map(self.config)
        self._init_destinations()
        self._init_roles()
        self._init_weapons()

    def _init_destinations(self):
        # self._destinations.append(Position(1, 1))  # A
        # self._destinations.append(Position(1, 4))  # B
        # self._destinations.append(Position(1, 7))  # C
        # self._destinations.append(Position(1, 10))  # D
        # self._destinations.append(Position(1, 13))  # E
        # self._destinations.append(Position(1, 16))  # F
        # self._destinations.append(Position(6, 2))  # G
        # self._destinations.append(Position(6, 9))  # H
        # self._destinations.append(Position(6, 16))  #
        for room in self._map.rooms:
            self._destinations.append(Position(room[0], room[1]))
        for store in self._map.stores:
            self._destinations.append(Position(store[0], store[1]))

    def _init_roles(self):
        victims = self.config['victim_num']
        npcs = self.config['npc_num']
        roles = victims + npcs
        possible_types = [RoleType.CLEANER, RoleType.WRITER, RoleType.WAITRESS, RoleType.RANGER, RoleType.KNIGHT]
        possible_weapons = [WeaponType.KNIFE, WeaponType.ROPE, WeaponType.POISON, WeaponType.GUN, WeaponType.BLADE]
        types = []
        self.__weapons = []
        for i in range(npcs):
            types.append(possible_types[i])
            self.__weapons.append(possible_weapons[i])
        for i in range(victims):
            types.append(RoleType.VICTIM)
            self.__weapons.append(None)
        self._init_role_origins()
        for i in range(0, roles):
            index = random.randint(0, len(self._role_origins) - 1)
            x, y = self._role_origins.pop(index).get_coordinate()
            role = Role(x, y, types[i], self.__weapons[i])
            self._roles.append(role)
        for i in range(0, roles - victims):
            ai = GoodGuyBFS(self._map, self._destinations)
            self._roles[i].set_ai(ai)

    # generate available init positions for roles
    def _init_role_origins(self):
        # self._role_origins.append(Position(1, 1))  # A
        # self._role_origins.append(Position(1, 4))  # B
        # self._role_origins.append(Position(1, 7))  # C
        # self._role_origins.append(Position(1, 10))  # D
        # self._role_origins.append(Position(1, 13))  # E
        # self._role_origins.append(Position(1, 16))  # F
        for room in self._map.rooms:
            self._role_origins.append(Position(room[0], room[1]))

    def _init_weapons(self):
        weapons = self.config['npc_num']
        weapon_type = self.__weapons
        self._init_weapon_origins()
        for i in range(0, weapons):
            index = random.randint(0, len(self._weapon_origins) - 1)
            x, y = self._weapon_origins.pop(index).get_coordinate()
            weapon = Weapon(x, y, weapon_type[i])
            self._weapons.append(weapon)

    # generate available init positions for weapons
    def _init_weapon_origins(self):
        # self._weapon_origins.append(Position(6, 2))  # G
        # self._weapon_origins.append(Position(6, 9))  # H
        # self._weapon_origins.append(Position(6, 16))  # I
        for store in self._map.stores:
            self._weapon_origins.append(Position(store[0], store[1]))

    # generate legal actions for a role
    def _get_legal_actions(self, role):
        actions = []
        if role == RoleType.VICTIM:
            actions.append(Action.WAIT)
        else:
            x, y = role.get_coordinate()
            # check weapon
            relation = {
                WeaponType.KNIFE: RoleType.CLEANER,
                WeaponType.ROPE: RoleType.WRITER,
                WeaponType.POISON: RoleType.WAITRESS,
                WeaponType.GUN: RoleType.RANGER,
                WeaponType.BLADE: RoleType.KNIGHT
            }
            if role.get_weapon() is None:
                for weapon in self._weapons:
                    weapon_x, weapon_y = weapon.get_coordinate()
                    if weapon.is_collectable():
                        if x == weapon_x and y == weapon_y:
                            if relation[weapon.get_type()] == role.get_type():
                                actions.append(Action.PICK)
                                break
            # check victim
            for i in range(0, self.config['victim_num']):
                victim = self._roles[-(i+1)]
                victim_x, victim_y = victim.get_coordinate()
                if victim.is_alive():
                    if x == victim_x and y == victim_y:
                        if role.get_weapon() is not None:
                            actions.append(Action.KILL)
            # check four directions
            # left
            if y - 1 > 0:
                if self._map.get_tile_type(x, y - 1) is not TileType.WALL:
                    actions.append(Action.MOVE_LEFT)
            # right
            if y + 1 < self._map.get_cols():
                if self._map.get_tile_type(x, y + 1) is not TileType.WALL:
                    actions.append(Action.MOVE_RIGHT)
            # up
            if x - 1 > 0:
                if self._map.get_tile_type(x - 1, y) is not TileType.WALL:
                    actions.append(Action.MOVE_UP)
            # down
            if x + 1 < self._map.get_rows():
                if self._map.get_tile_type(x + 1, y) is not TileType.WALL:
                    actions.append(Action.MOVE_DOWN)
        return actions

    def _update_state(self, role, action, turn):
        if role.get_type == RoleType.VICTIM:
            return
        else:
            x, y = role.get_coordinate()
            if action == Action.WAIT:
                return
            elif action == Action.PICK:
                for weapon in self._weapons:
                    weapon_x, weapon_y = weapon.get_coordinate()
                    if x == weapon_x and y == weapon_y:
                        weapon.picked(role)
                        role.pick_weapon(weapon)
                        break
            elif action == Action.KILL:
                for i in range(self.config['npc_num'], self.config['npc_num']+self.config['victim_num']):
                    x, y = self._roles[i].get_coordinate()
                    rx, ry = role.get_position().get_coordinate()
                    if rx == x and ry == y:
                        self._roles[i].killed()
                record = DeathRecord(role.get_position(), turn, role.get_weapon().get_type())
                self._records.append(record)
            elif action == Action.MOVE_UP:
                role.set_position(x - 1, y)
                self.record_meeting(role, turn)
            elif action == Action.MOVE_DOWN:
                role.set_position(x + 1, y)
                self.record_meeting(role, turn)
            elif action == Action.MOVE_LEFT:
                role.set_position(x, y - 1)
                self.record_meeting(role, turn)
            elif action == Action.MOVE_RIGHT:
                role.set_position(x, y + 1)
                self.record_meeting(role, turn)

    def record_meeting(self, role, turn):
        x, y = role.get_coordinate()
        # victim = self._roles[3]
        for other_role in self._roles:
            if other_role != role and other_role.get_type() != RoleType.VICTIM:
                other_x, other_y = other_role.get_coordinate()
                if (x == other_x - 1 and y == other_y) or (x == other_x + 1 and y == other_y) \
                        or (x == other_x and y == other_y + 1) or (x == other_x and y == other_y - 1):
                    record = MeetRecord(role.get_position(), turn, role.get_type(), other_role.get_type())
                    self._records.append(record)

    def loop(self):
        wait_role = []
        turn = 1
        while turn < self._turns + 1:
            for role in self._roles:
                if role != self._roles[3] and role in wait_role:
                    wait_role.remove(role)
                    continue
                actions = self._get_legal_actions(role)
                action = role.move(actions)
                if action == Action.KILL and role.get_weapon().get_type() != role.is_good_at():
                    wait_role.append(role)
                self._update_state(role, action, turn)
            turn += 1

    def finish(self):
        records = []
        for record in self._records:
            print(record)
            records.append(record.get_numerical())
        filenum = len(os.listdir('records'))+1
        with open('records/'+str(filenum)+'.dat', 'wb') as f:
            pickle.dump(records, f)
        # ai = GoodGuyBFS(self._map, self._destinations)
        # detective = Detective(self._records, ai)
        # detective.detect()
