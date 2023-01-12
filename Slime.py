import random
import pygame
import time
from SETTINGS import *
from slime_images import slime_images


class Slime(pygame.sprite.Sprite):
    images = slime_images

    def __init__(self, pos):
        super(Slime, self).__init__()
        self.rect = pygame.Rect(pos[0], pos[1], slime_width, slime_height)
        self.key = 'move1'

        # slime constants
        self.damage = 10
        self.health = 8
        self.attack = False
        self.image = Slime.images[self.key]
        self.speed = slime_speed
        self.attack_time = 0

    def move(self, flag_change_image):
        if flag_change_image:
            if self.key == 'move1':
                self.key = 'move2'
            elif self.key == 'move2':
                self.key = 'move3'
            elif self.key == 'move3':
                self.key = 'move4'
            elif self.key == 'move4':
                self.key = 'move1'
            elif self.key == 'attack1':
                self.key = 'attack2'
            elif self.key == 'attack2':
                self.key = 'attack3'
            elif self.key == 'attack3':
                self.key = 'move1'
            elif self.key == 'move1_reverse':
                self.key = 'move2_reverse'
            elif self.key == 'move2_reverse':
                self.key = 'move3_reverse'
            elif self.key == 'move3_reverse':
                self.key = 'move4_reverse'
            elif self.key == 'move4_reverse':
                self.key = 'move1_reverse'
            elif self.key == 'attack1_reverse':
                self.key = 'attack2_reverse'
            elif self.key == 'attack2_reverse':
                self.key = 'attack3_reverse'
            elif self.key == 'attack3_reverse':
                self.key = 'move1_reverse'
        if random.randint(0, 1):
            self.rect = self.rect.move(random.randint(0, slime_speed) - random.randint(0, slime_speed),
                                       random.randint(0, slime_speed) - random.randint(0, slime_speed))

    def update(self, flag_change_image=0, **kwargs):
        if not flag_change_image % 8:
            self.move(flag_change_image=True)
        else:
            self.move(flag_change_image=False)
        if self.can_attack_player(1, 1):
            if abs(self.attack_time - time.time()) > 0.5:
                self.attack = True
        self.image = Slime.images[self.key]

    def attack_animation(self, reverse=False):
        if not reverse:
            if self.key == 'slime_attack1':
                self.key = 'slime_attack2'
            elif self.key == 'slime_attack2':
                self.key = 'slime_attack3'
            elif self.key == 'slime_attack3':
                self.key = 'slime_attack1'
            else:
                self.key = 'slime_attack1'
        else:
            if self.key == 'slime_attack1_reverse':
                self.key = 'slime_attack2_reverse'
            elif self.key == 'slime_attack2_reverse':
                self.key = 'slime_attack3_reverse'
            elif self.key == 'slime_attack3_reverse':
                self.key = 'slime_attack1_reverse'
            else:
                self.key = 'slime_attack1_reverse'

    def func_attack(self, event):
        self.attack = event

    def can_attack_player(self, slime_coords, player_coords):
        return True