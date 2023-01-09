from LoadImage import load_image
import pygame


front_stay = load_image('HeroFrontStay.png')
front_right_leg = load_image('HeroFrontRightLeg.png')
front_left_leg = load_image('HeroFrontLeftLeg.png')
side_left_leg = load_image('HeroSideLeftLeg.png')
side_right_leg = load_image('HeroSideRightLeg.png')
side_stay = load_image('HeroSideStay.png')
back_stay = load_image('HeroBackStay.png')
back_right_leg = load_image('HeroBackRightLeg.png')
back_left_leg = load_image('HeroBackLeftLeg.png')

side_stay_punch_left_1 = load_image('HeroStayPunchLeft1.png')
side_stay_punch_left_2 = load_image('HeroStayPunchLeft2.png')
side_stay_punch_left_3 = load_image('HeroStayPunchLeft3.png')
side_left_leg_punch_left_1 = load_image('HeroLeftLegPunchLeft1.png')
side_left_leg_punch_left_2 = load_image('HeroLeftLegPunchLeft2.png')
side_left_leg_punch_left_3 = load_image('HeroLeftLegPunchLeft3.png')
side_right_leg_punch_left_1 = load_image('HeroRightLegPunchLeft1.png')
side_right_leg_punch_left_2 = load_image('HeroRightLegPunchLeft2.png')
side_right_leg_punch_left_3 = load_image('HeroRightLegPunchLeft1.png')

side_stay_punch_right_1 = load_image('HeroStayPunchRight1.png')
side_stay_punch_right_2 = load_image('HeroStayPunchRight2.png')
side_stay_punch_right_3 = load_image('HeroStayPunchRight3.png')
side_left_leg_punch_right_1 = load_image('HeroLeftLegPunchRight1.png')
side_left_leg_punch_right_2 = load_image('HeroLeftLegPunchRight2.png')
side_left_leg_punch_right_3 = load_image('HeroLeftLegPunchRight3.png')
side_right_leg_punch_right_1 = load_image('HeroRightLegPunchRight1.png')
side_right_leg_punch_right_2 = load_image('HeroRightLegPunchRight2.png')
side_right_leg_punch_right_3 = load_image('HeroRightLegPunchRight3.png')

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
    'side_stay_punch_left_1': side_stay_punch_left_1,
    'side_stay_punch_left_2': side_stay_punch_left_2,
    'side_stay_punch_left_3': side_stay_punch_left_3,
    'side_left_leg_punch_left_1': side_left_leg_punch_left_1,
    'side_left_leg_punch_left_2': side_left_leg_punch_left_2,
    'side_left_leg_punch_left_3': side_left_leg_punch_left_3,
    'side_right_leg_punch_left_1': side_right_leg_punch_left_1,
    'side_right_leg_punch_left_2': side_right_leg_punch_left_2,
    'side_right_leg_punch_left_3': side_right_leg_punch_left_3,
    'side_stay_punch_right_1': side_stay_punch_right_1,
    'side_stay_punch_right_2': side_stay_punch_right_2,
    'side_stay_punch_right_3': side_stay_punch_right_3,
    'side_left_leg_punch_right_1': side_left_leg_punch_right_1,
    'side_left_leg_punch_right_2': side_left_leg_punch_right_2,
    'side_left_leg_punch_right_3': side_left_leg_punch_right_3,
    'side_right_leg_punch_right_1': side_right_leg_punch_right_1,
    'side_right_leg_punch_right_2': side_right_leg_punch_right_2,
    'side_right_leg_punch_right_3': side_right_leg_punch_right_3,
    'side_stay_punch_left_1_reverse': pygame.transform.flip(side_stay_punch_left_1, True, False),
    'side_stay_punch_left_2_reverse': pygame.transform.flip(side_stay_punch_left_2, True, False),
    'side_stay_punch_left_3_reverse': pygame.transform.flip(side_stay_punch_left_3, True, False),
    'side_left_leg_punch_left_1_reverse': pygame.transform.flip(side_left_leg_punch_left_1, True, False),
    'side_left_leg_punch_left_2_reverse': pygame.transform.flip(side_left_leg_punch_left_2, True, False),
    'side_left_leg_punch_left_3_reverse': pygame.transform.flip(side_left_leg_punch_left_3, True, False),
    'side_right_leg_punch_left_1_reverse': pygame.transform.flip(side_right_leg_punch_left_1, True, False),
    'side_right_leg_punch_left_2_reverse': pygame.transform.flip(side_right_leg_punch_left_2, True, False),
    'side_right_leg_punch_left_3_reverse': pygame.transform.flip(side_right_leg_punch_left_3, True, False),
    'side_stay_punch_right_1_reverse': pygame.transform.flip(side_stay_punch_right_1, True, False),
    'side_stay_punch_right_2_reverse': pygame.transform.flip(side_stay_punch_right_2, True, False),
    'side_stay_punch_right_3_reverse': pygame.transform.flip(side_stay_punch_right_3, True, False),
    'side_left_leg_punch_right_1_reverse': pygame.transform.flip(side_left_leg_punch_right_1, True, False),
    'side_left_leg_punch_right_2_reverse': pygame.transform.flip(side_left_leg_punch_right_2, True, False),
    'side_left_leg_punch_right_3_reverse': pygame.transform.flip(side_left_leg_punch_right_3, True, False),
    'side_right_leg_punch_right_1_reverse': pygame.transform.flip(side_right_leg_punch_right_1, True, False),
    'side_right_leg_punch_right_2_reverse': pygame.transform.flip(side_right_leg_punch_right_2, True, False),
    'side_right_leg_punch_right_3_reverse': pygame.transform.flip(side_right_leg_punch_right_3, True, False)
}
