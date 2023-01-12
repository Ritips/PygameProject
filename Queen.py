import pygame
from SETTINGS import *
from queen_images import queen_images
from magic_ball_images import magic_ball_images
from meteor_images import meteor_images


class Queen(pygame.sprite.Sprite):
    images = queen_images

    def __init__(self, pos):
        super(Queen, self).__init__()
        self.rect = pygame.Rect(pos[0], pos[1], player_width, player_height)
        self.key = 'front_stay'
        self.bullets = pygame.sprite.Group()  # for some bullets like magic ball and meteor
        self.allies = pygame.sprite.Group()  # to spawn more enemies

        # queen constants
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


class Meteor(pygame.sprite.Sprite):
    images = meteor_images

    def __init__(self, pos):
        super(Meteor, self).__init__()
        self.rect = pygame.Rect(pos[0], pos[1], meteor_width, meteor_height)
        self.damage_box = self.rect
        self.damage = 15
        self.index = 0
        self.image = Meteor.images[self.index]
        self.kd = 0

    def update(self, flag_change_image=0, **kwargs):
        self.kd += 1
        if not self.kd % 20:
            self.index += 1
            self.kd = 0
            self.image = Meteor.images[self.index]
            if self.index == 3:
                pass
            elif self.index == 4:
                self.kill()

    def check_damage_someone(self, sprite):
        if pygame.sprite.spritecollideany(self, sprite):
            sprite.update(dmg_dealer=self)


class MagicBall(pygame.sprite.Sprite):
    images = magic_ball_images

    def __init__(self, pos):
        super(MagicBall, self).__init__()
        self.rect = pygame.Rect(pos[0], pos[1], magic_ball_width, magic_ball_height)
        self.damage_box = self.rect
        self.index = 0
        self.image = MagicBall.images[self.index]
        self.damage = 8
        self.speed = 1

    def update(self, flag_change_image=0, **kwargs):
        if not flag_change_image % 8:
            self.index += 1
        if not flag_change_image % 4:
            self.rect = self.rect.move(self.speed)
        self.image = MagicBall.images[self.index % len(MagicBall.images)]

    def check_self_destroy(self, sprite):
        if pygame.sprite.spritecollideany(self, sprite):
            sprite.update(dmg_dealer=self)
            self.kill()
