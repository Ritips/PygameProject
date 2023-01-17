import random
import pygame
import time
from SETTINGS import *
from ghost_images import ghost_images


class Ghost(pygame.sprite.Sprite):
    images = ghost_images

    def __init__(self, pos):
        super(Ghost, self).__init__()
        self.rect = pygame.Rect(pos[0], pos[1], ghost_width, ghost_height)
        self.key = 'move1'

        # ghost constants
        self.vector = random.choice(['up', 'side'])
        self.damage = 10
        self.health = 8
        self.count_steps = 0
        self.attack = False
        self.image = Ghost.images['move2']
        self.speed = slime_speed
        self.attack_time = 0
        self.flag = 2

    def move(self, flag_change_image):
        if flag_change_image:
            self.count_steps += 1
            if not self.attack:
                if self.key == 'move1':
                    self.key = 'move2'
                elif self.key == 'move2':
                    self.key = 'move3'
                else:
                    self.key = 'move1'
            else:
                if self.key == 'attack1':
                    self.key = 'attack2'
                elif self.key == 'attack2':
                    self.key = 'move1'
                elif self.key == 'move1_reverse':
                    self.key = 'move2_reverse'
                elif self.key == 'move2_reverse':
                    self.key = 'move3_reverse'
                elif self.key == 'move3_reverse':
                    self.key = 'move1_reverse'
                elif self.key == 'attack1_reverse':
                    self.key = 'attack2_reverse'
                elif self.key == 'attack2_reverse':
                    self.key = 'move1_reverse'
                else:
                    self.key = 'attack1'

        if self.count_steps == 2:
            if self.vector == 'up':
                self.rect = self.rect.move(0, ghost_speed * (-1) ** self.flag)
            else:
                self.rect = self.rect.move(ghost_speed * (-1) ** self.flag, 0)
            if self.flag == 2:
                self.flag = 1
            else:
                self.flag = 2
            self.count_steps = - 2

    def update(self, flag_change_image=0, **kwargs):
        if not flag_change_image % 8:
            self.move(flag_change_image=True)
        else:
            self.move(flag_change_image=False)
        # give coords
        if self.can_attack_player((1, 1), (1, 1)):
            if abs(self.attack_time - time.time()) > 5:
                self.attack = True
            else:
                self.attack = False
        self.image = Ghost.images[self.key]

    def func_attack(self, event):
        self.attack = event

    def can_attack_player(self, slime_coords, player_coords):
        if abs(slime_coords[0] - player_coords[0]) < 3 and abs(slime_coords[1] - player_coords[1]) < 3:
            return True
        return False