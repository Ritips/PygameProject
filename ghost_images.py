from LoadImage import load_image
import pygame

move1 = load_image('ghost1.png')
move2 = load_image('ghost2.png')
move3 = load_image('ghost3.png')
attack1 = load_image('ghost_attack1.png')
attack2 = load_image('ghost_attack2.png')

ghost_images = {
    'move1': move1,
    'move2': move2,
    'move3': move3,
    'attack1': attack1,
    'attack2': attack2,

    'move1_reverse': pygame.transform.flip(move1, True, False),
    'move2_reverse': pygame.transform.flip(move2, True, False),
    'move3_reverse': pygame.transform.flip(move3, True, False),
    'attack1_reverse': pygame.transform.flip(attack1, True, False),
    'attack2_reverse': pygame.transform.flip(attack2, True, False),
}