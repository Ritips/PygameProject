from Player import Player
from Constructions import *
from LoadLevel import *
from DefinePlayerLevel import *
from SETTINGS import *
from EscMenu import EscMenu
from Wizard import Wizard
from DeathHero import end_screen
from WinScreen import win_screen
import pygame


pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def draw_level(level_draw=None, index=0):
    pygame.mixer.music.load('data\\Matrix_3_cut.wav')
    pygame.mixer.music.play(-1, 0.0)
    if index == 1:
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

        return black, player


def start_second_level():
    [sprite.kill() for sprite in sprites]
    [construction.kill() for construction in constructions]
    class_level = LEVELS.get_level()
    level_to_draw, index = class_level.get_level()
    color, player = draw_level(index=index, level_draw=level_to_draw)
    change_image_time = 0
    esc_menu = None
    running = True
    while running:
        screen.fill(color)
        if player not in sprites:
            return 2
        if not enemies.sprites():
            LEVELS.finish_level()
            return 3
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
                        return 1
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
        sprites.draw(screen)
        sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time)
        pygame.display.set_caption(str(clock.get_fps()))
        pygame.display.flip()
        clock.tick(FPS)
    return 0


def restart_second_level():
    result = end_screen(more_sprites=sprites)
    if result == 11:
        return 110101
    elif result == 22:
        return second_level_game(restart_func=True)


def show_win_menu_second():
    result = win_screen(more_sprites=sprites)
    if result == 123:
        return 110105
    return 110101


def second_level_game(restart_func=False):
    [sprite.kill() for sprite in sprites]
    [construction.kill() for construction in constructions]
    if not restart_func:
        return 110101
    flag = start_second_level()
    if flag == 1:
        return 110101
    elif flag == 2:
        return restart_second_level()
    elif flag == 3:
        return show_win_menu_second()


def second_level():
    return second_level_game(restart_func=True)
