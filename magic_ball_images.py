from LoadImage import load_image
from SETTINGS import magic_ball_height, magic_ball_width
import pygame


def transform_image(image_to_transform):
    return pygame.transform.scale(image_to_transform, (magic_ball_width, magic_ball_height))


magic_ball1 = load_image('MagicBall1.png')
magic_ball2 = load_image('MagicBall2.png')
magic_ball3 = load_image('MagicBall3.png')
magic_ball4 = load_image('MagicBall4.png')

magic_ball_images = [magic_ball1, magic_ball2, magic_ball3, magic_ball4]
magic_ball_images = list(map(lambda x: transform_image(x), magic_ball_images))
