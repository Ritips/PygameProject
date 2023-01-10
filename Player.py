import pygame
from SETTINGS import *
from player_images import player_images


class Player(pygame.sprite.Sprite):
    images = player_images

    def __init__(self, pos):
        super(Player, self).__init__()
        self.rect = pygame.Rect(pos[0], pos[1], player_width, player_height)
        self.key = 'front_stay'
        self.weapon = 'punch'
        self.kd = 0
        self.kd_reset = 40
        self.attack = False
        image = Player.images[self.key]

        self.image = image
        self.speed = player_speed

    def update(self, check=None, flag_change_image=0):
        if check:
            if not flag_change_image % 8 and any(check):
                self.move(check=check, flag_change_image=True)
            else:
                self.move(check=check)
        if not self.kd and self.attack:
            self.kd = 1
        elif self.kd == self.kd_reset:
            self.attack = False
            self.kd = 0
        elif self.kd > 0:
            self.kd += 1
        self.image = Player.images[self.key]

    def move(self, check=None, flag_change_image=False):
        move_side = any_move = False
        if not check:
            return
        if check[pygame.K_LEFT] or check[pygame.K_a]:
            move_side = True
            any_move = True
            self.rect = self.rect.move(-self.speed, 0)
            if flag_change_image:
                if not self.attack:
                    if self.key == 'side_stay_reverse':
                        self.key = 'side_right_leg_reverse'
                    elif self.key == 'side_right_leg_reverse':
                        self.key = 'side_left_leg_reverse'
                    elif self.key == 'side_left_leg_reverse':
                        self.key = 'side_stay_reverse'
                    else:
                        self.key = 'side_stay_reverse'
                else:
                    self.hit_animation(reverse=True)
        if check[pygame.K_RIGHT] or check[pygame.K_d]:
            move_side = True
            any_move = True
            self.rect = self.rect.move(self.speed, 0)
            if flag_change_image:
                if not self.attack:
                    if self.key == 'side_stay':
                        self.key = 'side_right_leg'
                    elif self.key == 'side_right_leg':
                        self.key = 'side_left_leg'
                    elif self.key == 'side_left_leg':
                        self.key = 'side_stay'
                    else:
                        self.key = 'side_stay'
                else:
                    self.hit_animation(reverse=False)
        if check[pygame.K_UP] or check[pygame.K_w]:
            any_move = True
            self.rect = self.rect.move(0, -self.speed)
            if flag_change_image and not move_side:
                if self.key == 'back_stay':
                    self.key = 'back_right_leg'
                elif self.key == 'back_right_leg':
                    self.key = 'back_left_leg'
                elif self.key == 'back_left_leg':
                    self.key = 'back_stay'
                else:
                    self.key = 'back_stay'
        if check[pygame.K_DOWN] or check[pygame.K_s]:
            any_move = True
            self.rect = self.rect.move(0, self.speed)
            if flag_change_image and not move_side:
                if self.key == 'front_stay':
                    self.key = 'front_right_leg'
                elif self.key == 'front_right_leg':
                    self.key = 'front_left_leg'
                elif self.key == 'front_left_leg':
                    self.key = 'front_stay'
                else:
                    self.key = 'front_stay'
        if not any_move:
            if 'front' in self.key:
                self.key = 'front_stay'
            elif 'back' in self.key:
                self.key = 'back_stay'
            elif 'reverse' in self.key:
                self.key = 'side_stay_reverse'
            else:
                self.key = 'side_stay'

    def hit_animation(self, reverse=False):
        if self.weapon == 'punch':
            if not reverse:
                if self.key == 'side_stay_push1':
                    self.key = 'side_right_leg_push1'
                elif self.key == 'side_right_leg_push1':
                    self.key = 'side_left_leg_push2'
                elif self.key == 'side_left_leg_push2':
                    self.key = 'side_stay_push1'
                else:
                    self.key = 'side_stay_push1'
            else:
                if self.key == 'side_stay_push1_reverse':
                    self.key = 'side_right_leg_push1_reverse'
                elif self.key == 'side_right_leg_push1_reverse':
                    self.key = 'side_left_leg_push2_reverse'
                elif self.key == 'side_left_leg_push2_reverse':
                    self.key = 'side_stay_push1_reverse'
                else:
                    self.key = 'side_stay_push1_reverse'

    def update_weapon(self, weapon):
        self.weapon = weapon

    def check_kd(self):
        return self.kd

    def func_attack(self, event):
        self.attack = event
