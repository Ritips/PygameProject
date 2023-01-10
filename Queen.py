import pygame
from SETTINGS import *
from queen_images import queen_images


class Queen(pygame.sprite.Sprite):
    images = queen_images

    def __init__(self, pos):
        super(Queen, self).__init__()
        self.rect = pygame.Rect(pos[0], pos[1], player_width, player_height)
        self.key = 'front_stay'

        self.health = 500
        self.damage = 100
        self.kd = 0
        self.kd_reset = 120
        self.attack = False

        image = Queen.images[self.key]
        self.image = image
        self.speed = 2

    def update(self, **kwargs):
        pass

    def move(self):
        pass
