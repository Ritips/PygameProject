import pygame
from SETTINGS import *
from StartScreen import start_screen
from Player import Player


pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
sprites = pygame.sprite.Group()

player = Player((100, 100))
sprites.add(player)


def start_game():
    global_const_check_punch = False
    change_image_time = 0
    while True:
        screen.fill(black)
        change_image_time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        if not change_image_time % 80:
            change_image_time = 0
        sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time,
                       check_punch=global_const_check_punch)
        sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
start_game()
