import pygame
import os

pygame.init()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if color_key:
            image = image.convert()
            if color_key == -1:
                color_key = image.get_at((0, 0))
            elif color_key == -2:  # handmade
                color_key = (254, 253, 251, 255)
                image = pygame.transform.rotate(image, -90)
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()
        return image
    except FileNotFoundError:
        raise ValueError(f'File {fullname} not found')


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        read = list(map(str.strip, mapFile.readlines()))
    max_width = max(map(len, read))
    return list(map(lambda x: x.ljust(max_width, '.'), read))
