from LoadLevel import constructions, sprites
from SETTINGS import tile_width, tile_height
from walls_images import start_wall_image, start_path_image
import pygame


class PathCastle(pygame.sprite.Sprite):
    image = start_path_image

    def __init__(self, pos):
        super(PathCastle, self).__init__(sprites)
        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, tile_width, tile_height)
        self.image = PathCastle.image


class WallCastle(pygame.sprite.Sprite):
    image = start_wall_image

    def __init__(self, pos):
        super(WallCastle, self).__init__(constructions, sprites)
        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, tile_width, tile_height)
        self.image = WallCastle.image
