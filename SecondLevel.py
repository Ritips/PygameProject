from Player import Player
from Constructions import *
from LoadLevel import *
from DefinePlayerLevel import *
from SETTINGS import *
from EscMenu import EscMenu
from wizard import Wizard
import pygame


pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
text_group_sprites = pygame.sprite.Group()
exit_level = 0


class Text(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Text, self).__init__(text_group_sprites, sprites)
        self.font_size = 15 * width // 800
        self.font = pygame.font.Font(None, self.font_size)
        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, tile_width * 2, tile_height)
        self.image = pygame.Surface((tile_width * 2, tile_height), 32)
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.content = []

    def draw_text(self):
        space_height = 'tile_height - (i + 1) * (self.font_size - 4 * height // 600)'
        for i in range(len(self.content)):
            text = self.font.render(self.content[-(i + 1)], True, white)
            self.image.blit(text, (2, eval(space_height)))


class ExitLevel(Text):
    def __init__(self, pos):
        super(ExitLevel, self).__init__(pos)
        self.content = ['Come here']
        self.draw_text()
        self.status = 1

    def change_follow_status(self):
        self.status = 1

    def get_status(self):
        return self.status


def draw_level(level_draw=None, index=0):
    for sprite in sprites:
        sprite.kill()

    if index == 2:
        for i in range(len(level_draw)):
            for j in range(len(level_draw[i])):
                if level_draw[i][j] == 'W':
                    LevelSecondWall((j, i))
                else:
                    LevelSecondPath((j, i))

        player = Player((7 * tile_width, tile_height))
        for i in range(len(level_draw)):
            for j in range(len(level_draw[i])):
                if level_draw[i][j] == 'w':
                    Wizard((j, i), player)
                    print(j, i)

        return black, player


def second_level():
    global exit_level
    for sprite in sprites:
        sprite.kill()
    for construction in constructions:
        construction.kill()
    class_level = LEVELS.get_level()
    level_to_draw, index = class_level.get_level()
    color, player = draw_level(index=index, level_draw=level_to_draw)
    change_image_time = 0
    esc_menu = None
    running = True
    dialog = None
    notice_exit = ExitLevel((1, 0))
    notice_exit.change_follow_status()
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
        if not change_image_time % 80:
            change_image_time = 0
        if exit_level:
            exit_level = 0
            for sprite in sprites:
                sprite.kill()
            return 110103
        sprites.draw(screen)
        sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time)
        text_group_sprites.update(check_position_player=(player.rect.x, player.rect.y))
        pygame.display.set_caption(str(clock.get_fps()))
        pygame.display.flip()
        clock.tick(FPS)
    return 0