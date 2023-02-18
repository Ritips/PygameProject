from LoadImage import load_image
from SETTINGS import width, height
import pygame


def freeze_transform_image(image, dx=0, dy=0):
    x, y = image.get_size()
    x, y = int((x - dx) * width / 800), int((y - dy) * height / 600)
    return pygame.transform.scale(image, (x, y))


def freeze_transform_images(dictionary):
    for key in dictionary:
        dictionary[key] = freeze_transform_image(dictionary[key])


fire_place0 = load_image('FirePlace0.png')
fire_place1 = load_image('FirePlace1.png')
fire_place2 = load_image('FirePlace2.png')
fire_place3 = load_image('FirePlace3.png')

fireplace = {0: fire_place0, 1: fire_place1, 2: fire_place2, 3: fire_place3}
freeze_transform_images(fireplace)

bookcase_png = freeze_transform_image(load_image('BookCase.png'), dx=2, dy=2)
