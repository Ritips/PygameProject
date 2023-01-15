from StartScreen import start_screen
from Player import Player
from Queen import Queen
from Slime import Slime
from Constructions import *
from LoadLevel import *
from DefinePlayerLevel import *
from SETTINGS import *
import pygame


pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def draw_level(level_draw, index):
    if index == 1:
        for i in range(len(level_draw)):
            for j in range(len(level_draw[i])):
                if level_draw[i][j] == 'W':
                    WallQueen((j, i))
                else:
                    PathQueen((j, i))
        player = Player((2 * tile_width, tile_height))
        queen = Queen()
        queen.set_target(player)
        return purple, player
    return black


def start_game():
    class_level = LEVELS.get_level()
    index, level_to_draw = class_level.get_level()
    color, player = draw_level(index, level_to_draw)

    change_image_time = 0
    while True:
        screen.fill(color)
        change_image_time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not player.check_kd():
                player.func_attack(True)
        if not change_image_time % 80:
            change_image_time = 0

        sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time)
        sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
start_game()

