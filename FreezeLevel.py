from DeathHero import end_screen
from Player import Player
from Constructions import *
from LoadLevel import *
from DefinePlayerLevel import *
from SETTINGS import *
from FreezeImages import fireplace, bookcase_png
from WinScreen import win_screen
from EscMenu import EscMenu
import pygame


pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
inventory_group = pygame.sprite.Group()
other_interface_opened = pygame.sprite.Group()
open_content = pygame.sprite.Group()


# creating some objects especially for the level
class Button(pygame.sprite.Sprite):  # Button that can carry out click function
    def __init__(self, pos, w, h):
        super(Button, self).__init__(sprites)
        self.pos_x, self.pos_y = pos
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, dark_grey, (0, 0, w, h))
        pygame.draw.rect(self.image, light_grey, (0, 0, w, h), 3)
        self.font = pygame.font.Font(None, font_size)
        self.space_y = int(8 * height / 600)

    def is_clicked(self, pos):
        if pos[0] in range(self.rect.x, self.rect.x + self.rect.w + 1):
            if pos[1] in range(self.rect.y, self.rect.y + self.rect.h + 1):
                return True
        return False


class CommonObject(pygame.sprite.Sprite):
    def __init__(self, pos, groups=None):
        super(CommonObject, self).__init__()
        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, tile_width, tile_height)
        self.image = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA, 32)
        self.image.fill((0, 0, 0, 200))
        self.target = None
        [self.add(group) for group in groups if group.__class__ == pygame.sprite.Group] if groups else self.add(sprites)
        self.dx = self.dy = 0

    def set_target(self, target):
        self.target = target if target else None

    def check_pos_player(self, dx=0, dy=0):
        if not self.target:
            return False

        x, x1 = self.target.rect.x, self.target.rect.x + self.target.rect.w
        y, y1 = self.target.rect.y, self.target.rect.y + self.target.rect.h
        x_start, x_end = self.rect.x - dx, self.rect.x + self.rect.w + dx
        y_start, y_end = self.rect.y - dy, self.rect.y + self.rect.h + dy
        if x in range(x_start, x_end) or x1 in range(x_start, x_end):
            if y in range(y_start, y_end) or y1 in range(y_start, y_end):
                return True
        return False


# for first task (each item should be in each corner)
class Item(CommonObject):
    def __init__(self, pos):
        super(Item, self).__init__(pos)


# just market to switch rooms
class Door(CommonObject):
    def __init__(self, pos):
        super(Door, self).__init__(pos)


class BookCase(CommonObject):  # you can find here more books than usually
    image = bookcase_png

    def __init__(self, pos):
        super(BookCase, self).__init__(pos)
        self.image = BookCase.image
        self.interface = BookCaseInterface()

    def update(self, press_e=False, **kwargs):
        if self.interface in sprites and not self.check_pos_player(dx=0, dy=0):
            self.interface.remove(sprites), inventory_group.update(close_inventory=True)
            self.interface.remove(other_interface_opened)
        if press_e and self.check_pos_player(dx=0, dy=0):
            if self.interface not in sprites:
                self.interface.add(other_interface_opened)
                self.interface.add(sprites), inventory_group.update(press_b=True)
            else:
                self.interface.remove(sprites), inventory_group.update(close_inventory=True)
                self.interface.remove(other_interface_opened)


class BookCaseInterface(pygame.sprite.Sprite):
    def __init__(self):
        super(BookCaseInterface, self).__init__()
        w, h = 600 * width // 800, 200 * height // 600
        w_cell, h_cell, w_line = 60 * width // 800, 50 * height // 600, 2 * width // 800
        self.const = w, h, w_cell, h_cell, w_line
        self.rect = pygame.Rect(100 * width // 800, 50 * height // 600, w, h)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.image.fill(dark_grey)
        self.items = [[CellItem((self.rect.x + w_cell * x,
                                 self.rect.y + h_cell * y)) for x in range(w // w_cell)] for y in range(h // h_cell)]

    def redraw_items(self):
        w, h, w_cell, h_cell, w_line = self.const
        pygame.draw.rect(self.image, light_grey, (0, 0, w, h), 3 * width // 800)
        for y in range(0, h, h_cell):
            for x in range(0, w, w_cell):
                pygame.draw.rect(self.image, light_grey, (x, y, w_cell, h_cell), w_line)

    def update(self, click_pos=None, close=False, **kwargs):
        if click_pos:
            res = self.get_click(click_pos)
            if res[0]:
                x, y = res[-1]
                self.items[y][x].get_content()
        if close:
            self.remove(sprites)
        self.redraw_items()

    def get_click(self, pos):
        if self.rect.y <= pos[-1] <= self.rect.y + self.rect.h:
            if self.rect.x <= pos[0] <= self.rect.x + self.rect.w:
                return True, ((pos[0] - self.rect.x) // self.const[-3], (pos[1] - self.rect.y) // self.const[-2])
        return False, False, False


class BookInterface(pygame.sprite.Sprite):
    def __init__(self, file=None):
        super(BookInterface, self).__init__(open_content)
        self.rect = pygame.Rect(200 * width // 800, 100 * height // 600, 400 * width // 800, 450 * height // 600)
        self.read = pygame.Rect(self.rect.x, 525 * height // 600, self.rect.w, 25 * height // 600)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.image.fill(dark_grey)
        line = 3 * width // 800
        pygame.draw.rect(self.image, light_grey, (0, 425 * height // 600, self.rect.w, 25 * height // 600), line)
        pygame.draw.rect(self.image, light_grey, (0, 0, self.rect.w, self.rect.h), line)

    def update(self, click_pos=None, close=False, **kwargs):
        if close or (click_pos and self.confirm_reading(click_pos)):
            self.remove(sprites)

    def confirm_reading(self, pos):
        x, y, w, h = self.read
        if (x <= pos[0] <= x + w) and (y <= pos[1] <= y + h):
            return True


# Simple object, that contain png (For Inventory)
class CellItem(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(CellItem, self).__init__()
        self.size = w_cell, h_cell = 60 * width // 800, 50 * height // 600
        self.rect = pygame.Rect(pos[0], pos[1], self.size[0], self.size[1])
        self.image = pygame.Surface((self.size[0], self.size[-1]), pygame.SRCALPHA, 32)
        self.empty = True

    def check_empty(self):
        return self.empty

    def get_content(self):
        return


class BookIcon(CellItem):
    def __init__(self, pos):
        super(BookIcon, self).__init__(pos)
        colors = [purple]
        w_space, h_space = 15 * width // 800, 5 * height // 600
        w2, h2 = self.size[0] - 2 * w_space, self.size[-1] - 2 * h_space
        pygame.draw.rect(self.image, random.choice(colors), (w_space, h_space, w2, h2))
        self.empty = False
        self.interface = BookInterface()

    def get_content(self):
        self.interface.add(sprites)
        inventory_group.update(close_inventory=True), other_interface_opened.update(close=True)


# to see some items. For instance, book
class Inventory(pygame.sprite.Sprite):
    def __init__(self):
        super(Inventory, self).__init__(inventory_group)
        w, h, w_line, w_cell = 600 * width // 800, 50 * height // 600, 3 * width // 800, 60 * width // 800
        self.const = w, h, w_line, w_cell
        self.rect = pygame.Rect(100 * width // 800, 275 * height // 600, w, h)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.image.fill(dark_grey)
        self.items = [CellItem((self.rect.x + w_cell * i, self.rect.y)) for i in range(10)]
        book = BookIcon((0, 0))
        self.add_item(book)
        pygame.draw.rect(self.image, light_grey, (0, 0, w, h), w_line)
        [pygame.draw.rect(self.image, light_grey, (i, 0, w_cell, h), w_line) for i in range(0, w, w_cell)]

    def redraw_items(self):
        w, h, w_line, w_cell = self.const
        for i in range(len(self.items)):
            if self.items[i]:
                self.image.blit(self.items[i].image, (i * w_cell, 0))
        pygame.draw.rect(self.image, light_grey, (0, 0, w, h), w_line)
        [pygame.draw.rect(self.image, light_grey, (i, 0, w_cell, h), w_line) for i in range(0, w, w_cell)]

    def update(self, press_b=False, close_inventory=False, click_pos=None, **kwargs):
        if press_b:
            if other_interface_opened:
                self.add(sprites)
            else:
                self.add(sprites) if self not in sprites else self.remove(sprites)
        if close_inventory:
            self.remove(sprites)
        if click_pos:
            res = self.click_cell(click_pos)
            if res[0]:
                self.items[res[-1]].get_content()
        self.redraw_items()

    def click_cell(self, pos):
        if self.rect.y <= pos[-1] <= self.rect.y + self.rect.h:
            if self.rect.x <= pos[0] <= self.rect.x + self.rect.w:
                return True, (pos[0] - self.rect.x) // self.const[-1]
        return False, False

    def add_item(self, item):
        for i in range(len(self.items)):
            if self.items[i].check_empty():
                item.rect = item.rect.move(self.rect.x + i * self.const[-1], self.rect.y)
                self.items[i] = item
                break


# To open the second door
class Key(pygame.sprite.Sprite):
    pass


# to be honest I don't know for what this class. Maybe it will be a loader and container for txt file
class Room:
    pass


# for my teammate. It was an argument why hi didn't want to do something.
# Actually He was sad because I forgot about his idea (Level that should have done by him)
class FirePlace(CommonObject):  # Central hitting
    images = fireplace

    def __init__(self, pos):
        super(FirePlace, self).__init__(pos, groups=(sprites, constructions))
        self.status = False  # turned on/off
        self.key = 0
        self.image = FirePlace.images[self.key]
        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, tile_width, tile_height)
        self.target = None
        self.dx = tile_width // 4
        self.dy = tile_height // 4

    def change_status(self):
        if not self.check_pos_player(dx=self.dx, dy=self.dy):
            return
        self.status = 1 if not self.status else 0

    def update(self, flag_change_image=0, press_e=False, **kwargs):
        if press_e:
            self.change_status()
        if self.status and flag_change_image % 8 == 0:
            self.key = (self.key + 1) % 4
            self.key = self.key if self.key else 1
        if not self.status:
            self.key = 0
        self.image = FirePlace.images[self.key]


class InterfaceTaskOrder(pygame.sprite.Sprite):  # Task 2
    pass


def draw_level(level_draw=None, index=0):  # draws sprites (player, enemies, walls) Main FreezeLevel
    if index == 3:
        y, x = len(level_draw), len(level_draw[0])
        [WallCastle((j, i)) if level_draw[i][j] == 'W' else PathCastle((j, i)) for i in range(y) for j in range(x)]
        some_objects = []
        tmp_x = tmp_y = 0
        for i in range(y):
            for j in range(x):
                if level_draw[i][j] == 'F':
                    object_fireplace = FirePlace((j, i))
                    some_objects.append(object_fireplace)
                elif level_draw[i][j] == 'P':
                    tmp_x, tmp_y = j * tile_width, i * tile_height
                elif level_draw[i][j] == 'B':
                    object_bookcase = BookCase((j, i))
                    some_objects.append(object_bookcase)
        player = Player((tmp_x, tmp_y))
        [el.set_target(player) for el in some_objects]
        return dark_grey, player


def start_freeze_level_game():
    [sprite.kill() for sprite in sprites], [construction.kill() for construction in constructions]
    class_level = LEVELS.get_level()  # it doesn't work now (Level not defined in DefinePlayerLevel.py)
    level_to_draw, index = class_level.get_level()
    color, player = draw_level(level_draw=level_to_draw, index=index)
    change_image_time = 0
    esc_menu = None
    running = True
    pass_level = False
    Inventory()

    while running:
        screen.fill(color)
        if player not in sprites:
            return 2
        if pass_level:
            return 3

        if esc_menu:  # is EscMenu opened
            pygame.mouse.set_visible(True)  # make cursor visible
            sprites.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if esc_menu.close(event.pos):
                        exit()
                    elif esc_menu.continue_game(event.pos):
                        esc_menu.kill()
                        esc_menu = None
                    elif esc_menu.return_start_menu(event.pos):
                        sprites.empty()
                        enemies.empty()
                        group_player.empty()
                        return 1  # key for queen_level_game()
                if event.type == pygame.KEYDOWN and event.key == 27:
                    esc_menu.kill()
                    esc_menu = None
            pygame.display.flip()
            continue  # to freeze another processes such as movement hero, enemies or another objects

        if not inventory_group.sprites() in sprites and not open_content.sprites() in sprites:
            pygame.mouse.set_visible(False)  # make cursor invisible for beauty
        else:
            pygame.mouse.set_visible(True)
        change_image_time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not player.check_kd():  # attack
                if open_content.sprites() in sprites:
                    inventory_group.update(), other_interface_opened.update()
                    open_content.update(click_pos=event.pos)
                else:
                    if not other_interface_opened.sprites() and inventory_group.sprites() not in sprites:
                        player.func_attack(True)
                    else:
                        inventory_group.update(click_pos=event.pos)
                        other_interface_opened.update(click_pos=event.pos)
            if event.type == pygame.KEYDOWN:  # key press
                if event.key == 27:  # call EscMenu
                    esc_menu = EscMenu()
                elif event.key == 101 and not open_content.sprites() in sprites:
                    sprites.update(press_e=True)
                elif event.key == 98 and not open_content.sprites() in sprites:
                    inventory_group.update(press_b=True)
        if not change_image_time % 80:
            change_image_time = 0
        sprites.draw(screen)
        if open_content.sprites() in sprites:
            sprites.update(can_move=False, check=pygame.key.get_pressed(), flag_change_image=change_image_time)
        else:
            sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time)
        pygame.display.set_caption(str(clock.get_fps()))  # title of the screen
        pygame.display.flip()
        clock.tick(FPS)
    return 0


def restart_func():
    result = end_screen(more_sprites=sprites)
    if result == 11:
        return 110101
    elif result == 22:
        return freeze_game(restart=True)


def win_func():
    result = win_screen(more_sprites=sprites)
    if result == 123:
        return 110105
    return 110101


def freeze_game(restart=False):
    [sprite.kill() for sprite in sprites], [construction.kill() for construction in constructions]
    if not restart:
        return 110101
    flag = start_freeze_level_game()
    if flag == 1:
        return 110101
    if flag == 2:
        return restart_func()
    if flag == 3:
        return win_func()


def freeze_level():
    return freeze_game(restart=True)
