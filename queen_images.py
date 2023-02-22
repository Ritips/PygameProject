from LoadImage import load_image
import pygame
from SETTINGS import width, height


def transform_player_image(image):
    x, y = image.get_size()
    if width == 800 and height == 600:
        x, y = int(width * (x + 11) / 800), int(height * (y + 11) / 600)
    else:
        x, y = int(width * (x + 10) / 800), int(height * (y + 10) / 600)
    return pygame.transform.scale(image, (x, y))


def transform_images(dictionary):
    for key in dictionary:
        dictionary[key] = transform_player_image(dictionary[key])


queen_side_stay = load_image('QueenSideStay.png')
queen_side_step = load_image('QueenSideStep.png')
queen_side_attack = load_image('QueenSideAttack1.png')

queen_front_stay = load_image('QueenFrontStay.png')
queen_front_step = load_image('QueenFrontStep.png')

queen_back_stay = load_image('QueenBackStay.png')
queen_back_step = load_image('QueenBackStep.png')

queen_attack_particle1 = load_image('QueenParticle1.png')
queen_attack_particle2 = load_image('QueenParticle2.png')


queen_images = {
    'side_stay': queen_side_stay,
    'side_step': queen_side_step,
    'side_stay_reverse': pygame.transform.flip(queen_side_stay, True, False),
    'side_step_reverse': pygame.transform.flip(queen_side_step, True, False),
    'front_stay': queen_front_stay,
    'front_step': queen_front_step,
    'front_stay_reverse': pygame.transform.flip(queen_front_stay, True, False),
    'front_step_reverse': pygame.transform.flip(queen_front_step, True, False),
    'back_stay': queen_back_stay,
    'back_step': queen_back_step,
    'back_stay_reverse': pygame.transform.flip(queen_back_stay, True, False),
    'back_step_reverse': pygame.transform.flip(queen_back_step, True, False),
    'particle1': queen_attack_particle1,
    'particle2': queen_attack_particle2,
}

transform_images(queen_images)
