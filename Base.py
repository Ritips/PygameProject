from LoadLevel import *
import pygame
from SETTINGS import *
from StartScreen import start_screen
from Player import Player
from Queen import Queen
from Slime import Slime


pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

player = Player((100, 100))
slime = Slime((100, 100))
queen = Queen()
queen.set_target(player)


def get_rect(x, y):
    return tile_width * x + 1, tile_height * y + 1, tile_width - 2, tile_height - 2


def start_game():
    level_to_draw = load_level(level_first)
    change_image_time = 0
    while True:
        screen.fill('grey')
        change_image_time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not player.check_kd():
                player.func_attack(True)
        if not change_image_time % 80:
            change_image_time = 0
        for i in range(len(level_to_draw)):
            for j in range(len(level_to_draw[i])):
                if level_to_draw[i][j] == 'W':
                    pygame.draw.rect(screen, 'darkorange', get_rect(j, i))
        sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time)
        sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
start_game()
