from LoadImage import load_image
from SETTINGS import tile_width, tile_height
import pygame


def transform_image(image_to_transform):
    return pygame.transform.scale(image_to_transform, (tile_width - 1, tile_height - 1))


queen_wall_image = transform_image(load_image('Wall1.png'))
queen_path_image = transform_image(load_image('Path1.png'))
start_wall_image = transform_image(load_image('WallCastle.png'))
start_path_image = transform_image(load_image('PathCastle.png'))
second_level_path = [transform_image((load_image('path_level_2_1.png'))),
                     transform_image((load_image('path_level_2_2.png'))),
                     transform_image((load_image('path_level_2_3.png')))]
second_level_wall = [transform_image((load_image('wall_level_2_1.png'))),
                     transform_image((load_image('wall_level_2_2.png')))]
