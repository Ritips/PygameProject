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

    def update(self, flag_change_image=0, dealer_damage=None, **kwargs):
        if not flag_change_image % 8:
            self.move(flag_change_image=True)
        if dealer_damage:
            self.get_hit(dealer_damage)

        self.image = Queen.images[self.key]

    def move(self, flag_change_image=False):
        if flag_change_image:
            if self.key == 'front_stay':
                self.key = 'side_stay'
            elif self.key == 'side_stay':
                self.key = 'side_stay_reverse'
            elif self.key == 'side_stay_reverse':
                self.key = 'back_stay'
            elif self.key == 'back_stay':
                self.key = 'back_step'
            elif self.key == 'back_step':
                self.key = 'front_stay'
            else:
                self.key = 'front_stay'

    def get_hit(self, dmg_dealer):
        damage_box = dmg_dealer.damage_box
        if pygame.sprite.collide_rect(self, damage_box):
            self.health -= dmg_dealer.damage
            print(self.health)
