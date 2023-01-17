from LoadImage import load_image
import pygame

slime_movement_images = ['slime1.png', 'slime2.png', 'slime3.png', 'slime4.png', 'slime1.png']
slime_attack_images = ['slime_attack1', 'slime_attack2', 'slime_attack3', 'slime_attack1']
move1 = load_image('slime1.png')
move2 = load_image('slime2.png')
move3 = load_image('slime3.png')
move4 = load_image('slime4.png')
attack1 = load_image('slime_attack1.png')
attack2 = load_image('slime_attack2.png')
attack3 = load_image('slime_attack3.png')

slime_images = {
    'move1': move1,
    'move2': move1,
    'move3': move1,
    'move4': move1,
    'attack1': attack1,
    'attack2': attack2,
    'attack3': attack3,

    'move1_reverse': pygame.transform.flip(move1, True, False),
    'move2_reverse': pygame.transform.flip(move2, True, False),
    'move3_reverse': pygame.transform.flip(move3, True, False),
    'move4_reverse': pygame.transform.flip(move4, True, False),
    'attack1_reverse': pygame.transform.flip(attack1, True, False),
    'attack2_reverse': pygame.transform.flip(attack2, True, False),
    'attack3_reversed': pygame.transform.flip(attack3, True, False),
}