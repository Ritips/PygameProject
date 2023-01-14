from LoadLevel import constructions, horizontal_borders, vertical_borders, sprites
from SETTINGS import tile_width, tile_height
from walls_images import queen_wall_image, queen_path_image
import pygame


class WallQueen(pygame.sprite.Sprite):
    image = queen_wall_image

    def __init__(self, pos):
        super(WallQueen, self).__init__(constructions, sprites)
        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, tile_width, tile_height)
        self.image = WallQueen.image


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super(Border, self).__init__(constructions)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class PathQueen(pygame.sprite.Sprite):
    image = queen_path_image

    def __init__(self, pos):
        super(PathQueen, self).__init__(sprites)
        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, tile_width, tile_height)
        self.image = PathQueen.image

