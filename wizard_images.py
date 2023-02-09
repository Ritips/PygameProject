from LoadImage import load_image
import pygame
from SETTINGS import wizard_ball_height, wizard_ball_width
import pygame


def transform_image(image_to_transform):
    return pygame.transform.scale(image_to_transform, (wizard_ball_width, wizard_ball_height))


ball1 = load_image('wizard_weapon1.png')
ball2 = load_image('wizard_weapon2.png')

wizard_ball_images = [ball1, ball2]
wizard_ball_images = list(map(lambda x: transform_image(x), wizard_ball_images))

move1 = load_image('wizard1.png')
move2 = load_image('wizard2.png')
move3 = load_image('wizard3.png')
move_side1 = load_image('wizard_left_side1.png')
move_side2 = load_image('wizard_left_side2.png')
move_side3 = load_image('wizard_left_side3.png')
attack1 = load_image('wizard_attack1.png')
attack2 = load_image('wizard_attack2.png')


wizard_images = {
    'move1': pygame.transform.scale(move1, (10 * 3, 15 * 3)),
    'move2': pygame.transform.scale(move2, (10 * 3, 15 * 3)),
    'move3': pygame.transform.scale(move3, (10 * 3, 15 * 3)),
    'attack1': pygame.transform.scale(attack1, (10 * 3, 15 * 3)),
    'attack2': pygame.transform.scale(attack2, (10 * 3, 15 * 3)),

    'move_side1': pygame.transform.scale(move_side1, (10 * 3, 15 * 3)),
    'move_side2': pygame.transform.scale(move_side2, (10 * 3, 15 * 3)),
    'move_side3': pygame.transform.scale(move_side3, (10 * 3, 15 * 3)),
    'move_side1_reverse': pygame.transform.flip(pygame.transform.scale(move_side1, (10 * 3, 15 * 3)), True, False),
    'move_side2_reverse': pygame.transform.flip(pygame.transform.scale(move_side2, (10 * 3, 15 * 3)), True, False),
    'move_side3_reverse': pygame.transform.flip(pygame.transform.scale(move_side3, (10 * 3, 15 * 3)), True, False),
}