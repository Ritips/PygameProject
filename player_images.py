from LoadImage import load_image
from SETTINGS import width, height
import pygame


def transform_player_image(image):
    x, y = image.get_size()
    x, y = int(width * x / 800), int(height * y / 600)
    return pygame.transform.scale(image, (x, y))


def transform_images(dictionary):
    for key in dictionary:
        dictionary[key] = transform_player_image(dictionary[key])


front_stay = load_image('HeroFrontStay.png')
front_right_leg = load_image('HeroFrontRightLeg.png')
front_left_leg = load_image('HeroFrontLeftLeg.png')
side_left_leg = load_image('HeroSideLeftLeg.png')
side_right_leg = load_image('HeroSideRightLeg.png')
side_stay = load_image('HeroSideStay.png')
back_stay = load_image('HeroBackStay.png')
back_right_leg = load_image('HeroBackRightLeg.png')
back_left_leg = load_image('HeroBackLeftLeg.png')

side_stay_push1 = load_image('HeroSideStayPush1.png')
side_stay_push2 = load_image('HeroSideStayPush2.png')

side_left_leg_push1 = load_image('HeroSideLeftLegPush1.png')
side_left_leg_push2 = load_image('HeroSideLeftLegPush2.png')

side_right_leg_push1 = load_image('HeroSideRightLegPush1.png')
side_right_leg_push2 = load_image('HeroSideRightLegPush2.png')


player_images = {
    'front_stay': front_stay,
    'front_right_leg': front_right_leg,
    'front_left_leg': front_left_leg,
    'side_left_leg': side_left_leg,
    'side_right_leg': side_right_leg,
    'side_stay': side_stay,
    'back_stay': back_stay,
    'back_right_leg': back_right_leg,
    'back_left_leg': back_left_leg,
    'side_left_leg_reverse': pygame.transform.flip(side_left_leg, True, False),
    'side_right_leg_reverse': pygame.transform.flip(side_right_leg, True, False),
    'side_stay_reverse': pygame.transform.flip(side_stay, True, False),

    'side_stay_push1': side_stay_push1,
    'side_stay_push2': side_stay_push2,
    'side_stay_push1_reverse': pygame.transform.flip(side_stay_push1, True, False),
    'side_stay_push2_reverse': pygame.transform.flip(side_stay_push2, True, False),

    'side_left_leg_push1': side_left_leg_push1,
    'side_left_leg_push2': side_left_leg_push2,
    'side_left_leg_push1_reverse': pygame.transform.flip(side_left_leg_push1, True, False),
    'side_left_leg_push2_reverse': pygame.transform.flip(side_left_leg_push2, True, False),

    'side_right_leg_push1': side_right_leg_push1,
    'side_right_leg_push2': side_right_leg_push2,
    'side_right_leg_push1_reverse': pygame.transform.flip(side_right_leg_push1, True, False),
    'side_right_leg_push2_reverse': pygame.transform.flip(side_right_leg_push2, True, False)
}

transform_images(player_images)