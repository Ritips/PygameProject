import pygame
from SETTINGS import *
from LoadLevel import enemies, sprites
from FindPath import *
from valkyrie_images import valkyrie_images


class Valkyrie(pygame.sprite.Sprite):
    images = valkyrie_images

    def __init__(self, pos):
        super(Valkyrie, self).__init__(sprites, enemies)

        self.health = 3000
        self.max_health = 3000
        self.kd_bar_show = 100
        self.bar_status_show = False
        self.speed = 2
        self.cell_to_move = []

        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, player_width, player_height)
        self.key = 'front1'
        self.image = Valkyrie.images[self.key]

    def update(self, **kwargs):
        pass
