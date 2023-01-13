import pygame


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        read = list(map(str.strip, mapFile.readlines()))
    max_width = max(map(len, read))
    return list(map(lambda x: x.ljust(max_width, '.'), read))


sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
group_player = pygame.sprite.Group()
