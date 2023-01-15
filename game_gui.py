import pygame.draw
import constant
import os
from algorithm import *
from game import DeadlyHotel


def back_action():
    os.startfile(os.path.join(os.path.abspath('./'), 'main.py'))
    quit(0)


class Color:
    # 自定义颜色
    ACHIEVEMENT = (220, 160, 87)
    VERSION = (220, 160, 87)

    # 固定颜色
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GREY = (128, 128, 128)  # 中性灰
    TRANSPARENT = (255, 255, 255, 0)  # 白色的完全透明


class Text:
    def __init__(self, text: str, text_color):
        """
        text: 文本内容，如'大学生模拟器'，注意是字符串形式
        text_color: 字体颜色，如Color.WHITE、COLOR.BLACK
        font_type: 字体文件(.ttc)，如'msyh.ttc'，注意是字符串形式
        font_size: 字体大小，如20、10
        """
        self.text = text
        self.text_color = text_color

        font = pygame.freetype.SysFont('cambria', 28)
        self.text_image, self.text_rect = font.render(self.text, self.text_color)

        self.text_width = self.text_image.get_width()
        self.text_height = self.text_image.get_height()

    def draw(self, surface: pygame.Surface, upper_left_x, upper_left_y):
        rect = self.text_rect
        rect.center = upper_left_x + self.text_width / 2, upper_left_y + self.text_height / 2
        rect = rect.inflate(10, 10)
        pygame.draw.rect(surface, self.text_color, rect, 1)
        surface.blit(self.text_image, (upper_left_x, upper_left_y))


class ButtonText(Text):
    def __init__(self, text: str, text_color):
        super().__init__(text, text_color)
        self.rect = self.text_image.get_rect()

    def draw(self, surface: pygame.Surface, upper_left_x, upper_left_y):
        super().draw(surface, upper_left_x, upper_left_y)
        self.rect.center = upper_left_x+self.text_width/2, upper_left_y+self.text_height/2

    def handle_event(self, command):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if hovered:
            command()


class DeadlyHotelGUI(DeadlyHotel):
    __window = None
    __window_width = 0
    __window_height = 0
    __tile_img = []
    __role_img = []
    __role_armed_img = []
    __role_dead_img = []
    __role_display = []
    __weapon_img = []
    __role = None
    __ai = False

    def __init__(self, config):
        super().__init__(config)
        self.__ai = config['mode']
        # self.__ai = False

    def init(self):
        pygame.init()
        super().init()
        index = random.randint(0, self.config['npc_num'] - 1)
        self.__role = self._roles[index]
        if not self.__ai:
            self.__role.set_human_play()
        else:
            ai = RandomAction(self._map, self._destinations)
            self.__role.set_ai(ai)
        self.__init_window()
        self.__init_images()
        self.__draw_map()
        self.__draw_roles()
        self.__draw_weapons()
        self.__draw_info()
        self.__draw_buttons()
        pygame.display.update()

    def __init_window(self):
        self.__window_width = self._map.get_cols() * constant.tile_width
        if self.__window_width < 1000:
            self.__window_width = 1000
        self.__window_height = self._map.get_rows() * constant.tile_height + 200
        self.__window = pygame.display.set_mode((self.__window_width, self.__window_height))
        pygame.display.set_caption("Deadly Hotel")
        self.__window.fill(constant.white)

    def __init_images(self):
        for i in range(4):
            self.__tile_img.append(pygame.image.load('img/tile_' + str(i) + '.png').convert_alpha())
        for i in range(0, 6):
            self.__role_img.append(pygame.image.load('img/role_' + str(i) + '.png').convert_alpha())
            self.__role_armed_img.append(pygame.image.load('img/armed_' + str(i) + '.png').convert_alpha())
            self.__role_dead_img.append(pygame.image.load('img/armed_' + str(i) + '.png').convert_alpha())
        for i in range(0, 5):
            self.__weapon_img.append(pygame.image.load('img/weapon_' + str(i) + '.png').convert_alpha())
            self.__weapon_img[i].set_colorkey(constant.white)

    def __draw_map(self):
        for i in range(0, self._map.get_rows()):
            for j in range(0, self._map.get_cols()):
                tile = self._map.get_tile_type(i, j)
                index = 0
                if tile == TileType.WALL:
                    index = 0
                elif tile == TileType.DOOR:
                    index = 1
                elif tile == TileType.ROOM:
                    index = 2
                elif tile == TileType.CORRIDOR:
                    index = 3
                self.__window.blit(self.__tile_img[index], (constant.tile_width * j, constant.tile_height * i))

    def __draw_roles(self):
        self.__role_display = []
        roles = [RoleType.CLEANER, RoleType.WRITER, RoleType.WAITRESS, RoleType.VICTIM, RoleType.RANGER, RoleType.KNIGHT]
        for i in range(0, len(self._roles)):
            role = self._roles[i]
            idx = roles.index(role.get_type())
            x, y = role.get_coordinate()
            if not role.is_alive():
                self.__role_display.append(self.__role_dead_img[idx])
            else:
                if role.get_weapon() is not None:
                    self.__role_display.append(self.__role_armed_img[idx])
                else:
                    self.__role_display.append(self.__role_img[idx])
            self.__role_display[i].set_colorkey(constant.white)
            self.__window.blit(self.__role_display[i], (constant.tile_width * y, constant.tile_height * x))

    def __draw_weapons(self):
        weapons = [WeaponType.KNIFE, WeaponType.ROPE, WeaponType.POISON, WeaponType.GUN, WeaponType.BLADE]
        for i in range(0, len(self._weapons)):
            weapon = self._weapons[i]
            idx = weapons.index(weapon.get_type())
            if weapon.is_collectable():
                x, y = weapon.get_coordinate()
                self.__window.blit(self.__weapon_img[idx], (constant.tile_width * y, constant.tile_height * x))

    def __draw_buttons(self):
        button_begin_height = self._map.get_rows() * constant.tile_height + 10
        button_begin_width = self.__window_width / 2 + 50
        self.button_back = ButtonText('Back to Config', Color.BLACK)
        self.button_back.draw(self.__window, button_begin_width, button_begin_height)

    def __draw_info(self):
        text_begin_height = self._map.get_rows() * constant.tile_height + 10
        font = pygame.freetype.SysFont('cambria', 20)
        surface, rect = font.render('Triangle stands for cleaner, who is good at using knife.', constant.black)
        self.__window.blit(surface, (10, text_begin_height + 0 * constant.font_height))
        surface, rect = font.render('Square stands for writer, who is good at using rope.', constant.black)
        self.__window.blit(surface, (10, text_begin_height + 1 * constant.font_height))
        surface, rect = font.render('Circle stands for waitress, who is good at using poison.', constant.black)
        self.__window.blit(surface, (10, text_begin_height + 2 * constant.font_height))
        surface, rect = font.render('Star stands for victim, who can not move.', constant.black)
        self.__window.blit(surface, (10, text_begin_height + 5 * constant.font_height))
        surface, rect = font.render('Diamond stands for ranger, who is good at using gun.', constant.black)
        self.__window.blit(surface, (10, text_begin_height + 3 * constant.font_height))
        surface, rect = font.render('Heart stands for knight, who is good at using blade.', constant.black)
        self.__window.blit(surface, (10, text_begin_height + 4 * constant.font_height))
        if not self.__ai:
            surface, rect = font.render('You are ' + self.__role.get_type().value, constant.red)
            self.__window.blit(surface, (10, text_begin_height + 6 * constant.font_height))
        else:
            surface, rect = font.render('AI is ' + self.__role.get_type().value, constant.red)
            self.__window.blit(surface, (10, text_begin_height + 6 * constant.font_height))
        surface, rect = font.render('WASD for moving, SPACE for pick up weapon or kill.', constant.blue)
        self.__window.blit(surface, (10, text_begin_height + 7 * constant.font_height))

    def update_gui(self):
        self.__draw_map()
        self.__draw_roles()
        self.__draw_weapons()
        self.__draw_info()
        pygame.display.update()

    def loop(self):
        wait_role = []
        turn = 1
        while turn < self._turns + 1:
            for i in range(0, self.config['npc_num']):
                role = self._roles[i]
                if role in wait_role:
                    wait_role.remove(role)
                    continue
                actions = self._get_legal_actions(role)
                action = role.move(actions, [self.button_back], [back_action])
                '''
                if role is not self.__role:
                    print('%s is at %s want to %s in turn %d' % (role.get_type(), str(role.get_position()), action, turn))
                '''
                if action == Action.KILL and role.get_weapon().get_type() != role.is_good_at():
                    wait_role.append(role)
                self._update_state(role, action, turn)
            turn += 1
            if self.__ai:
                pygame.time.delay(500)
            self.update_gui()

    def finish_gui(self):
        # TODO
        return

    def finish(self):
        super().finish()
        if not self.__ai:
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        break


