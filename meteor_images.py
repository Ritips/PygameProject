from LoadImage import load_image
import pygame
from SETTINGS import meteor_width, meteor_height


def transform_image(image_to_transform):
    return pygame.transform.scale(image_to_transform, (meteor_width, meteor_height))


meteor1 = load_image('Meteor1.png')
meteor2 = load_image('Meteor2.png')
meteor3 = load_image('Meteor3.png')
meteor4 = load_image('Meteor4.png')
meteor5 = load_image('Meteor5.png')

meteor_images = [meteor1, meteor2, meteor3, meteor4, meteor5]
meteor_images = list(map(lambda x: transform_image(x), meteor_images))
