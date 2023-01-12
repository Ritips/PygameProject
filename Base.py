import pygame
from SETTINGS import *
from StartScreen import start_screen, sprites, enemies
from Player import Player
from Queen import Queen
from Slime import Slime


pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

player = Player((100, 100))
slime = Slime((100, 100))
queen = Queen((200, 200))
sprites.add(player)
enemies.add(queen)
enemies.add(slime)
sprites.add(enemies)

player.set_self_sprite(enemies)
damage_sprite = player.get_damage_box()  # visible check damage sprite
sprites.add(damage_sprite)


def start_game():
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
        sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time)
        sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
start_game()
