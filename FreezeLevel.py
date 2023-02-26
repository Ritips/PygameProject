from DeathHero import end_screen
from Player import Player
from Constructions import *
from LoadLevel import *
from DefinePlayerLevel import *
from SETTINGS import *
from FreezeImages import fireplace, bookcase_png, music_system, door, key_image, chest_image
from WinScreen import win_screen
from EscMenu import EscMenu
import pygame
import random


pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
inventory_group = pygame.sprite.Group()
other_interface_opened = pygame.sprite.Group()
open_content = pygame.sprite.Group()
item_group_position = pygame.sprite.Group()
furniture = pygame.sprite.Group()
freeze_bar_group = pygame.sprite.Group()
global_value_check_player = False
global_value_complete_task2 = False


# creating some objects especially for the level
class FreezeBar(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(FreezeBar, self).__init__(sprites, freeze_bar_group)
        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, tile_width * 2, tile_height // 4)
        self.image = pygame.Surface((tile_width * 2, tile_height // 4), pygame.SRCALPHA, 32)
        self.image.fill(black)
        self.freeze_counter = 0
        self.freeze_counter_maximum = 4000 * FPS // 60

    def update(self, heat=False, **kwargs):
        if heat and self.freeze_counter > 1:
            self.freeze_counter -= 2
        else:
            self.freeze_counter += 1
        self.image.fill(black)
        f_w = self.freeze_counter * self.rect.w // self.freeze_counter_maximum
        if abs(self.freeze_counter - self.freeze_counter_maximum) < 5:
            [sprite.kill() for sprite in group_player]
        pygame.draw.rect(self.image, blue, (0, 0, f_w, tile_height // 4))
        pygame.draw.rect(self.image, black, (0, 0, 2 * tile_width, tile_height // 4), 2 * width // 800)


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


class Chest(CommonObject):
    def __init__(self, pos):
        super(Chest, self).__init__(pos, groups=(sprites, furniture))
        self.image = chest_image
        self.key_contain = True

    def update(self, press_e=False, reset_key=False, **kwargs):
        if group_player.sprites() in sprites:
            self.target = group_player.sprites()[0]
        if press_e and self.key_contain and self.check_pos_player():
            self.key_contain = False
            inventory_group.update(item=KeyIcon((0, 0)), chest=self)
        if reset_key:
            self.key_contain = True


# for first task (each item should be in each corner)
class Item(CommonObject):
    def __init__(self, pos):
        super(Item, self).__init__(pos, groups=(sprites, item_group_position, furniture))
        self.image = music_system

    def update(self, press_c=False, remove_self=False, **kwargs):
        if group_player.sprites() in sprites:
            self.target = group_player.sprites()[0]
        if press_c and self.check_pos_player():
            inventory_group.update(item=ItemIcon((0, 0)), item_sprite=self)


# just market to switch rooms
class Door(CommonObject):
    def __init__(self, pos, task=None):
        super(Door, self).__init__(pos, groups=(sprites, furniture))
        self.image = door
        self.task = task

    def update(self, task1=False, task2=False, staff=None, **kwargs):
        global global_value_complete_task2
        if task1 == 1 and staff and (staff[0] == 1 and self.task == staff[0]) and self.check_pos_player():
            if staff[3]:
                staff[2].set_inventory(staff[1])
                staff[2].change_status()
            else:
                if staff[2].get_status():
                    res = staff[2].get_reset()
                    reset_main_level(res[0], res[1])
                    staff[2].change_status()
        if task2 and self.check_pos_player():
            global_value_complete_task2 = True


class BookCase(CommonObject):  # you can find here more books than usually
    image = bookcase_png

    def __init__(self, pos, file=None):
        super(BookCase, self).__init__(pos, groups=(sprites, furniture))
        self.image = BookCase.image
        self.interface = BookCaseInterface(file=file)

    def update(self, press_e=False, close=False, **kwargs):
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
        if close:
            self.interface.update(close=close)


class BookCaseInterface(pygame.sprite.Sprite):
    def __init__(self, file=None):
        super(BookCaseInterface, self).__init__()
        w, h = 600 * width // 800, 200 * height // 600
        w_cell, h_cell, w_line = 60 * width // 800, 50 * height // 600, 2 * width // 800
        self.const = w, h, w_cell, h_cell, w_line
        self.rect = pygame.Rect(100 * width // 800, 50 * height // 600, w, h)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.image.fill(dark_grey)
        self.items = [[CellItem((self.rect.x + w_cell * x,
                                 self.rect.y + h_cell * y)) for x in range(w // w_cell)] for y in range(h // h_cell)]
        if file:
            try:
                with open(file, 'r', encoding='utf-8') as inventory_file:
                    for el in map(str.strip, inventory_file.readlines()):
                        self.append_item(BookIcon((0, 0), el))
            except FileNotFoundError:
                pass

    def append_item(self, item):
        success = False
        for y in range(len(self.items)):
            for x in range(len(self.items[0])):
                if self.items[y][x].check_empty():
                    item.rect = item.rect.move(self.rect.x + x * self.const[-2], self.rect.y + y * self.const[3])
                    self.items[y][x] = item
                    success = True
                    self.redraw_items()
                    break
            if success:
                break
        if not success:
            self.redraw_items()
            inventory_group.update(item=item)

    def remove_item(self, pos):
        x, y = pos
        item = self.items[y][x]
        if not item.check_empty():
            self.items[y][x] = CellItem((self.rect.x + x * self.const[2], self.rect.y + y * self.const[3]))
            inventory_group.update(item=item)
            self.redraw_items()

    def redraw_items(self):
        w, h, w_cell, h_cell, w_line = self.const
        pygame.draw.rect(self.image, light_grey, (0, 0, w, h), 3 * width // 800)
        [self.image.blit(self.items[i][j].image, (j * w_cell, i * h_cell))
         for i in range(len(self.items)) for j in range(len(self.items[0]))]
        [pygame.draw.rect(self.image, light_grey, (x, y, w_cell, h_cell), w_line)
         for y in range(0, h, h_cell) for x in range(0, w, w_cell)]

    def update(self, click_pos=None, btn_click=None, close=False, item=None, **kwargs):
        if click_pos:
            res = self.get_click(click_pos)
            if res[0]:
                x, y = res[-1]
                if not btn_click:
                    if self.items[y][x].__class__ == ItemIcon:
                        pass
                    else:
                        self.items[y][x].get_content()
                else:  # put item in chest/bookcase/inventory
                    self.remove_item(res[-1])
        if close:
            self.remove(sprites)
        if item:
            self.append_item(item)

    def get_click(self, pos):
        if self.rect.y <= pos[-1] <= self.rect.y + self.rect.h:
            if self.rect.x <= pos[0] <= self.rect.x + self.rect.w:
                return True, ((pos[0] - self.rect.x) // self.const[-3], (pos[1] - self.rect.y) // self.const[-2])
        return False, False, False


class BookInterface(pygame.sprite.Sprite):
    def __init__(self, file=None):
        super(BookInterface, self).__init__()
        self.rect = pygame.Rect(200 * width // 800, 100 * height // 600, 400 * width // 800, 450 * height // 600)
        self.read = pygame.Rect(self.rect.x, 525 * height // 600, self.rect.w, 25 * height // 600)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.font_size = 25 * width // 800
        self.font = pygame.font.Font(None, self.font_size)
        self.image.fill(dark_grey)
        try:
            with open(file, 'r', encoding='utf-8') as f_book:
                self.content = list(map(str.strip, f_book.readlines()))
        except FileNotFoundError:
            self.content = []
        for i in range(len(self.content)):
            text = self.font.render(self.content[i], True, white)
            self.image.blit(text, (10 * width // 800, 5 * height // 600 + self.font_size * i))
        line = 3 * width // 800
        pygame.draw.rect(self.image, light_grey, (0, 425 * height // 600, self.rect.w, 25 * height // 600), line)
        pygame.draw.rect(self.image, light_grey, (0, 0, self.rect.w, self.rect.h), line)

    def update(self, click_pos=None, close=False, **kwargs):
        if close or (click_pos and self.confirm_reading(click_pos)):
            self.kill()

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
        self.image.fill(dark_grey)
        self.empty = True

    def check_empty(self):
        return self.empty

    def get_content(self):
        return


class BookIcon(CellItem):
    def __init__(self, pos, file):
        super(BookIcon, self).__init__(pos)
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        w_space, h_space = 15 * width // 800, 5 * height // 600
        w2, h2 = self.size[0] - 2 * w_space, self.size[-1] - 2 * h_space
        pygame.draw.rect(self.image, (r, g, b), (w_space, h_space, w2, h2))
        pygame.draw.rect(self.image, black, (w_space, h_space, w2, h2), 3 * width // 800)
        self.empty = False
        self.interface = BookInterface(file=file)

    def get_content(self):
        inventory_group.update(close_inventory=True), [sprite.kill() for sprite in other_interface_opened]
        self.interface.add(sprites), self.interface.add(open_content)


class ItemIcon(CellItem):
    def __init__(self, pos):
        super(ItemIcon, self).__init__(pos)
        self.empty = False
        self.image = pygame.transform.scale(music_system, (60 * width // 800, 50 * height // 600))

    def get_content(self):
        player = group_player.sprites()[0]
        x, y = player.rect.x // tile_width, player.rect.y // tile_height
        t = CommonObject((x, y), groups=(other_interface_opened, ))
        if pygame.sprite.spritecollideany(t, constructions) or pygame.sprite.spritecollideany(t, furniture):
            t.kill()
            inventory_group.update(item=ItemIcon((0, 0)))
            return
        t.kill()
        Item((x, y))
        inventory_group.update(close_inventory=True)


class KeyIcon(CellItem):
    def __init__(self, pos):
        super(KeyIcon, self).__init__(pos)
        self.empty = False
        self.image = pygame.transform.scale(key_image, (60 * width // 800, 50 * height // 600))

    def get_content(self):
        furniture.update(task2=2)


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
        pygame.draw.rect(self.image, light_grey, (0, 0, w, h), w_line)
        [pygame.draw.rect(self.image, light_grey, (i, 0, w_cell, h), w_line) for i in range(0, w, w_cell)]

    def redraw_items(self):
        w, h, w_line, w_cell = self.const
        for i in range(len(self.items)):
            if self.items[i]:
                self.image.blit(self.items[i].image, (i * w_cell, 0))
        pygame.draw.rect(self.image, light_grey, (0, 0, w, h), w_line)
        [pygame.draw.rect(self.image, light_grey, (i, 0, w_cell, h), w_line) for i in range(0, w, w_cell)]

    def update(self, press_b=False, close_inventory=False, click_pos=None,
               btn_click=None, item=None, item_sprite=None, chest=None, **kwargs):
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
                if not btn_click:
                    el = self.items[res[-1]]
                    if el.__class__ == ItemIcon:
                        self.remove_item(res[-1], other_interface=False)
                    el.get_content()
                else:
                    self.remove_item(res[-1])
        if item:
            if self.add_item(item):
                if item_sprite:
                    item_sprite.kill()
            else:
                if chest:
                    chest.update(reset_key=True)

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
                self.redraw_items()
                return True
        other_interface_opened.update(item=item)
        self.redraw_items()
        return False

    def remove_item(self, index, other_interface=True):
        item = self.items[index]
        if not item.check_empty():
            self.items[index] = CellItem((self.rect.x + self.const[-1] * index, self.rect.y))
            if other_interface:
                other_interface_opened.update(item=item)
            self.redraw_items()


# to be honest I don't know for what this class. Maybe it will be a loader and container for txt file
class Room:
    def __init__(self):
        self.pos = (3, 3)
        self.save_furniture = pygame.sprite.Group()
        self.level = 'freezelevel/room.txt'
        self.room_sprites = pygame.sprite.Group()
        self.status = False
        self.inventory = None
        self.player = None
        self.status_load_objects = True

    def change_status(self):
        self.status = not self.status
        if not self.status:
            for sprite in self.room_sprites:
                constructions.remove(sprite), sprites.remove(sprite), furniture.remove(sprite)
            self.player = self.inventory = None

    def set_inventory(self, inventory):
        self.inventory = inventory

    def get_status(self):
        return self.status

    def get_reset(self):
        return (self.player.rect.x, self.player.rect.y), self.save_furniture

    def load_level(self):
        if not self.status:
            return
        for sprite in furniture:
            self.save_furniture.add(sprite)
            furniture.remove(sprite), sprites.remove(sprite), constructions.remove(sprite)
            item_group_position.remove(sprite)
        [sprite.kill() for sprite in group_player]
        delete_sprites()
        with open(self.level, 'r', encoding='utf-8') as f_room:
            map_room = list(map(str.strip, f_room.readlines()))
        x, y = len(map_room[0]), len(map_room)
        [WallCastle((j, i)) if map_room[i][j] == 'W' else PathCastle((j, i)) for i in range(y) for j in range(x)]
        group = []
        if self.status_load_objects:
            self.status_load_objects = False
            for i in range(y):
                for j in range(x):
                    if map_room[i][j] == 'D':
                        self.pos = (j * tile_width, i * tile_height)
                        group.append(Door((j, i), task=1))
                    elif map_room[i][j] == 'F':
                        group.append(FirePlace((j, i)))
                    elif map_room[i][j] == 'C':
                        group.append(Chest((j, i)))
            [self.room_sprites.add(el) for el in group]
        else:
            for el in self.room_sprites:
                if el.__class__ == FirePlace:
                    constructions.add(el)
                furniture.add(el), sprites.add(el), group.append(el)
        self.player = Player(self.pos)
        self.inventory.add(inventory_group)
        [el.set_target(self.player) for el in group]
        return self.start_game()

    def start_game(self):
        global global_value_check_player
        change_image_time = 0
        esc_menu = None
        running = True
        FreezeBar((0, 0.6))
        player = self.player
        task1 = 1
        staff2 = (1, self.inventory, self, False)

        while running:
            if not self.status:
                return 0, None
            screen.fill(dark_grey)
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
                            return 1, None  # key for queen_level_game()
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
                        open_content.update(click_pos=event.pos)
                    else:
                        if other_interface_opened.sprites() not in sprites and inventory_group.sprites() not in sprites:
                            player.func_attack(True)
                        else:
                            inventory_group.update(click_pos=event.pos)
                            other_interface_opened.update(click_pos=event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if other_interface_opened.sprites() in sprites and inventory_group.sprites() in sprites:
                        other_interface_opened.update(click_pos=event.pos, btn_click=True)
                        inventory_group.update(click_pos=event.pos, btn_click=True)
                if event.type == pygame.KEYDOWN:  # key press
                    if event.key == 27:  # call EscMenu
                        esc_menu = EscMenu()
                    elif event.key == 101 and not open_content.sprites() in sprites:
                        furniture.update(press_e=True, task1=task1, staff=staff2)
                    elif event.key == 98 and not open_content.sprites() in sprites:
                        inventory_group.update(press_b=True)
                    elif event.key == 99:
                        furniture.update(press_c=True)
            if not change_image_time % 80:
                change_image_time = 0
            sprites.draw(screen)
            group_player.draw(screen)
            if inventory_group.sprites() in sprites:
                inventory_group.draw(screen)
            if other_interface_opened.sprites() in sprites:
                other_interface_opened.draw(screen)
            if open_content.sprites() in sprites:
                group_player.update(can_move=False, check=pygame.key.get_pressed(), flag_change_image=change_image_time)
                open_content.draw(screen)
            else:
                sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time)
            if player not in sprites and not global_value_check_player:
                return 2, None
            freeze_bar_group.update(), furniture.update()
            pygame.display.set_caption(str(clock.get_fps()))  # title of the screen
            pygame.display.flip()
            clock.tick(FPS)


# for my teammate. It was an argument why hi didn't want to do something.
# Actually He was sad because I forgot about his idea (Level that should have done by him)
class FirePlace(CommonObject):  # Central hitting
    images = fireplace

    def __init__(self, pos):
        super(FirePlace, self).__init__(pos, groups=(sprites, constructions, furniture))
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
        if self.check_pos_player(dx=self.dx * 4, dy=self.dy * 4) and self.status:
            freeze_bar_group.update(heat=True)
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
    pygame.mixer.music.load('data\\Matrix_3_cut.wav')
    pygame.mixer.music.play(-1, 0.0)
    if index == 3:
        y, x = len(level_draw), len(level_draw[0])
        [WallCastle((j, i)) if level_draw[i][j] == 'W' else PathCastle((j, i)) for i in range(y) for j in range(x)]
        some_objects = []
        tmp_x = tmp_y = 0
        bookcase_count = 1
        door_task_count = 1
        for i in range(y):
            for j in range(x):
                if level_draw[i][j] == 'F':
                    object_fireplace = FirePlace((j, i))
                    some_objects.append(object_fireplace)
                elif level_draw[i][j] == 'P':
                    tmp_x, tmp_y = j * tile_width, i * tile_height
                elif level_draw[i][j] == 'B':
                    object_bookcase = BookCase((j, i), file=f'freezelevel/Bookcase{bookcase_count}.txt')
                    if bookcase_count != 2:
                        object_bookcase.interface.append_item(ItemIcon((0, 0)))
                    bookcase_count += 1
                    some_objects.append(object_bookcase)
                elif level_draw[i][j] == 'D':
                    some_objects.append(Door((j, i), task=door_task_count))
                    door_task_count += 1
        player = Player((tmp_x, tmp_y))
        [el.set_target(player) for el in some_objects]
        return dark_grey, player


def reset_main_level(player_coord, some_sprites=None):
    global global_value_check_player
    with open('data/FreezeLevel.txt', 'r', encoding='utf-8') as f_reset:
        data = list(map(str.strip, f_reset.readlines()))
    y, x = len(data), len(data[0])
    for sprite in sprites:
        sprites.remove(sprite), constructions.remove(sprite), furniture.remove(sprite)
    [WallCastle((j, i)) if data[i][j] == 'W' else PathCastle((j, i)) for i in range(y) for j in range(x)]
    [sprite.kill() for sprite in group_player]
    player = Player((player_coord[0], player_coord[1]))
    if some_sprites:
        for sprite in some_sprites:
            if sprite.__class__ == FirePlace:
                constructions.add(sprite)
            sprites.add(sprite), furniture.add(sprite)
    [el.set_target(player) for el in furniture]
    FreezeBar((0, 0.6))
    global_value_check_player = True


def complete_task_order():
    left = right = bottom = False
    for sprite in item_group_position:
        if sprite.rect.x // tile_width == 1 and sprite.rect.y // tile_height == 4:
            left = True
        elif sprite.rect.x // tile_width == 14 and sprite.rect.y // tile_height == 1:
            right = True
        elif 8 < sprite.rect.x // tile_width < 15 and sprite.rect.y // tile_height == 10:
            bottom = True
    if left and right and bottom:
        return True
    return False


def start_freeze_level_game():
    global global_value_check_player, global_value_complete_task2
    delete_sprites()
    class_level = LEVELS.get_level()  # it doesn't work now (Level not defined in DefinePlayerLevel.py)
    level_to_draw, index = class_level.get_level()
    color, player = draw_level(level_draw=level_to_draw, index=index)
    change_image_time = 0
    esc_menu = None
    running = True
    task1 = task2 = 0
    inventory = Inventory()
    FreezeBar((0, 0.6))
    inventory_group.update(item=BookIcon((0, 0), 'freezelevel/conditions.txt'))
    inventory_group.update(item=BookIcon((0, 0), 'freezelevel/settings.txt'))
    inventory_group.update(click_pos=(160 * width // 800, 275 * height // 600))
    room1 = Room()
    staff1 = (1, inventory, room1, True)

    while running:
        screen.fill(color)
        if not task1 and complete_task_order():
            task1 = 1
        if room1.get_status():
            flag = room1.load_level()
            if flag[0] == 1:
                return 1
            if flag[0] == 2:
                return 2
        if player not in sprites and not global_value_check_player:
            pygame.mixer.music.load('data\\haha.mp3')
            pygame.mixer.music.play(1, 0.0)
            return 2
        if global_value_complete_task2:
            global_value_complete_task2 = False
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
                    open_content.update(click_pos=event.pos)
                else:
                    if other_interface_opened.sprites() not in sprites and inventory_group.sprites() not in sprites:
                        player.func_attack(True)
                    else:
                        inventory_group.update(click_pos=event.pos)
                        other_interface_opened.update(click_pos=event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if other_interface_opened.sprites() in sprites and inventory_group.sprites() in sprites:
                    other_interface_opened.update(click_pos=event.pos, btn_click=True)
                    inventory_group.update(click_pos=event.pos, btn_click=True)
            if event.type == pygame.KEYDOWN:  # key press
                if event.key == 27:  # call EscMenu
                    esc_menu = EscMenu()
                elif event.key == 101 and not open_content.sprites() in sprites:
                    furniture.update(press_e=True, task1=task1, task2=task2, staff=staff1)
                    if global_value_check_player:
                        player = group_player.sprites()[0]
                        global_value_check_player = False
                elif event.key == 98 and not open_content.sprites() in sprites:
                    inventory_group.update(press_b=True)
                elif event.key == 99:
                    furniture.update(press_c=True)
        if not change_image_time % 80:
            change_image_time = 0
        sprites.draw(screen)
        group_player.draw(screen)
        if inventory_group.sprites() in sprites:
            inventory_group.draw(screen)
        if other_interface_opened.sprites() in sprites:
            other_interface_opened.draw(screen)
        if open_content.sprites() in sprites:
            group_player.update(can_move=False, check=pygame.key.get_pressed(), flag_change_image=change_image_time)
            open_content.draw(screen)
        else:
            sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time)
        freeze_bar_group.update(), furniture.update()
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


def delete_sprites():
    [sprite.kill() for sprite in sprites], [construction.kill() for construction in constructions]
    [sprite.kill() for sprite in open_content], [sprite.kill() for sprite in other_interface_opened]
    [sprite.kill() for sprite in freeze_bar_group], [sprite.kill() for sprite in furniture]
    [sprite.kill() for sprite in item_group_position], [sprite.kill() for sprite in inventory_group]


def freeze_game(restart=False):
    delete_sprites()
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