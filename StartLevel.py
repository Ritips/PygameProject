from Player import Player
from Constructions import *
from LoadLevel import *
from DefinePlayerLevel import *
from SETTINGS import *
from EscMenu import EscMenu
from Valkyrie import Valkyrie
import pygame


pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
text_group_sprites = pygame.sprite.Group()


class Text(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Text, self).__init__(text_group_sprites, sprites)
        self.font_size = 15 * width // 800
        self.font = pygame.font.Font(None, self.font_size)
        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, tile_width * 2, tile_height)
        self.image = pygame.Surface((tile_width * 2, tile_height), 32)
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.near()
        self.content = []

    def update(self, check_position_player=None, **kwargs):
        self.near(check_position_player)

    def near(self, pos=None):
        if not pos:
            return
        x, y, w, h = self.rect
        x2, y2 = pos
        if abs(x - x2) <= w and abs(y - y2) <= h:
            sprites.add(self)
            return True
        else:
            self.remove(sprites)
            return False

    def draw_text(self):
        space_height = 'tile_height - (i + 1) * (self.font_size - 4 * height // 600)'
        for i in range(len(self.content)):
            text = self.font.render(self.content[-(i + 1)], True, white)
            self.image.blit(text, (2, eval(space_height)))


class TextControlHero(Text):
    def __init__(self, pos):
        super(TextControlHero, self).__init__(pos)
        self.content = ['To control', 'hero use', 'WASD']
        self.draw_text()


class TextTalk(Text):
    def __init__(self, pos):
        super(TextTalk, self).__init__(pos)
        self.content = ['Press E', 'to talk']
        self.draw_text()


class Dialog(pygame.sprite.Sprite):
    def __init__(self):
        super(Dialog, self).__init__(sprites)
        self.pos = 2 * tile_width, tile_height
        self.width, self.height = 12 * tile_width, 10 * tile_height
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        r, g, b = light_grey
        self.image.fill((r, g, b, 255))
        pygame.draw.rect(self.image, black, (0, 0, self.width, self.height), 5 * width // 800)


def draw_level(level_draw=None, index=0):
    if index == 0:
        for i in range(len(level_draw)):
            for j in range(len(level_draw[i])):
                if level_draw[i][j] == 'W':
                    WallCastle((j, i))
                else:
                    PathCastle((j, i))
                    if level_draw[i][j] == 'V':
                        Valkyrie((j, i))

        player = Player((7 * tile_width, tile_height))
        return dark_grey, player


def start_level_game():
    class_level = LEVELS.get_level()
    level_to_draw, index = class_level.get_level()
    color, player = draw_level(index=index, level_draw=level_to_draw)
    change_image_time = 0
    esc_menu = None
    running = True
    dialog = None
    control_notice = TextControlHero((8, 1))
    start_talk_notice = TextTalk((12, 2))
    while running:
        screen.fill(color)
        if player not in sprites:
            return 110101
        if dialog:
            pygame.mouse.set_visible(True)
            sprites.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == 101:
                    start_talk_notice = TextTalk((12, 2))
                    dialog.kill()
                    dialog = None
            continue
        if esc_menu:
            pygame.mouse.set_visible(True)
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
                        return 110101
                if event.type == pygame.KEYDOWN and event.key == 27:
                    esc_menu.kill()
                    esc_menu = None
            pygame.display.flip()
            continue
        pygame.mouse.set_visible(False)
        change_image_time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not player.check_kd():
                player.func_attack(True)
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    esc_menu = EscMenu()
                elif event.key == 101 and start_talk_notice.near((player.rect.x, player.rect.y)):
                    start_talk_notice.kill()
                    dialog = Dialog()
        if not change_image_time % 80:
            change_image_time = 0
        sprites.draw(screen)
        sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time)
        text_group_sprites.update(check_position_player=(player.rect.x, player.rect.y))
        pygame.display.set_caption(str(clock.get_fps()))
        pygame.display.flip()
        clock.tick(FPS)
    return 0
