from DeathHero import end_screen
from Player import Player
from Constructions import *
from LoadLevel import *
from DefinePlayerLevel import *
from SETTINGS import *
from WinScreen import win_screen
from EscMenu import EscMenu
from trytomakeriddle import *
from walls_images import escape_path
import pygame


pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


class EscapePath(pygame.sprite.Sprite):
    image = escape_path

    def __init__(self, pos):
        super(EscapePath, self).__init__(sprites)
        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, tile_width, tile_height)
        self.image = EscapePath.image


def draw_level(level_draw=None, index=0):
    pygame.mixer.music.load('data\\Matrix_3_cut.wav')
    pygame.mixer.music.play(-1, 0.0)
    if index == 4:
        for i in range(len(level_draw)):
            for j in range(len(level_draw[i])):
                if level_draw[i][j] == 'W':
                    WallCastle((j, i))
                else:
                    PathCastle((j, i))
                if level_draw[i][j] == 'E':
                    EscapePath((j, i))
        player = Player((7 * tile_width, tile_height))
        return black, player


def ghost_level_function_game():
    # deleting all previous sprites before drawing new sprites
    [sprite.kill() for sprite in sprites], [construction.kill() for construction in constructions]
    class_level = LEVELS.get_level()  # get level (It is class which is determined in DefinePlayer.py)
    level_to_draw, index = class_level.get_level()  # get list of the symbols and index
    color, player = draw_level(index=index, level_draw=level_to_draw)  # get color(background) and player
    change_image_time = 0  # counter (kd) to switch image
    esc_menu = None
    running = True
    while running:
        screen.fill(color)
        if player not in sprites:
            return 2  # key for ghost_level_game()
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
                        return 1  # key for ghost_level_game()
                if event.type == pygame.KEYDOWN and event.key == 27:
                    esc_menu.kill()
                    esc_menu = None
            pygame.display.flip()
            continue  # to freeze another processes such as movement hero, enemies or another objects
        pygame.mouse.set_visible(False)  # make cursor invisible for beauty
        change_image_time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == 101:
                x, y, h, w = player.rect
                if 40 * width // 800 < x < 90 * width // 800 and 40 * height // 600 < y < 90 * height // 600:
                    pygame.mouse.set_visible(True)
                    pygame.mixer.music.load('data\\riddlemusic.mp3')
                    pygame.mixer.music.play(-1, 0.0)
                    running = start_riddle()
                    pygame.mixer.music.load('data\\Matrix_3_cut.wav')
                    pygame.mixer.music.play(-1, 0.0)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not player.check_kd():  # attack
                player.func_attack(True)
            if event.type == pygame.KEYDOWN and event.key == 27:  # call EscMenu
                esc_menu = EscMenu()
        if not change_image_time % 80:
            change_image_time = 0
        sprites.draw(screen)
        sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time)
        pygame.display.set_caption(str(clock.get_fps()))  # title of the screen
        pygame.display.flip()
        clock.tick(FPS)
    LEVELS.finish_level()
    return 3


def restart():
    result = end_screen(more_sprites=sprites)  # call EndScreen. Sprites ara given for the background
    if result == 11:
        return 110101  # this key is used to return to the lobby (start screen)
    elif result == 22:
        return ghost_level_game(restart_func=True)  # restart


def show_win_menu():
    result = win_screen(more_sprites=sprites)  # call WinScreen. Sprites are given for the background
    if result == 123:
        return 110105  # this key is used to select next level
    return 110101  # this key is used to return to the lobby (start screen)


def ghost_level_game(restart_func=False):
    [sprite.kill() for sprite in sprites]  # delete all sprites to minimise resources
    if not restart_func:  # start menu
        return 110101
    flag = ghost_level_function_game()
    if flag == 1:  # start menu
        return 110101
    elif flag == 2:  # restart
        return restart()
    elif flag == 3:  # win menu
        return show_win_menu()


def ghost_level():  # start function
    return ghost_level_game(restart_func=True)
