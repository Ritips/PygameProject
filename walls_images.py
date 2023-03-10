from LoadImage import load_image
from SETTINGS import tile_width, tile_height
import pygame


def transform_image(image_to_transform):
    return pygame.transform.scale(image_to_transform, (tile_width - 1, tile_height - 1))


start_wall_image = transform_image(load_image('WallCastle.png'))
start_path_image = transform_image(load_image('PathCastle.png'))
escape_path = transform_image(load_image('EscapePath.png'))
