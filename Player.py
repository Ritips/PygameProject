from LoadLevel import *
import pygame
from SETTINGS import *
from player_images import player_images


class Player(pygame.sprite.Sprite):
    images = player_images

    def __init__(self, pos):
        super(Player, self).__init__(group_player, sprites)
        self.rect = pygame.Rect(pos[0], pos[1], player_width, player_height)
        self.key = 'front_stay'

        # hero constants
        self.weapon = 'punch'
        self.damage = 5
        self.kd = 0
        self.kd_reset = 40
        self.health = 60
        self.attack = False

        self.damage_box = pygame.sprite.Sprite()
        w, h = (65 * width // 800), (65 * height // 600)
        box_image = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(box_image, black, (0, 0, w, h))
        self.damage_box.image = box_image
        self.rewrite_damage_box()
        image = Player.images[self.key]
        self.image = image
        self.speed = player_speed

    def update(self, check=None, flag_change_image=0, dmg_dealer=None, **kwargs):
        if check:
            if not flag_change_image % 8:
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
        if dmg_dealer:
            self.get_hit(dmg_dealer)
        self.image = Player.images[self.key]

    def move(self, check=None, flag_change_image=False):
        move_side = any_move = False
        if not check:
            return
        if not any(check):
            if self.attack and 'side' in self.key:
                if flag_change_image:
                    if 'reverse' in self.key:
                        self.hit_animation(reverse=True, stay=True)
                    else:
                        self.hit_animation(reverse=False, stay=True)
                return
        if (check[pygame.K_LEFT] or check[pygame.K_a]) and (check[pygame.K_RIGHT] or check[pygame.K_d]):
            pass
        else:
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
        if (check[pygame.K_UP] or check[pygame.K_w]) and (check[pygame.K_DOWN] or check[pygame.K_s]):
            pass
        else:
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
        self.rewrite_damage_box()

    def hit_animation(self, reverse=False, stay=False):
        if self.weapon == 'punch':
            if not stay:
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
            else:
                if not reverse:
                    if self.key == 'side_stay_push1':
                        self.key = 'side_stay_push2'
                    elif self.key == 'side_stay_push2':
                        self.key = 'side_stay_push1'
                    else:
                        self.key = 'side_stay_push1'
                else:
                    if self.key == 'side_stay_push1_reverse':
                        self.key = 'side_stay_push2_reverse'
                    elif self.key == 'side_stay_push2_reverse':
                        self.key = 'side_stay_push1_reverse'
                    else:
                        self.key = 'side_stay_push1_reverse'

    def update_weapon(self, weapon):
        self.weapon = weapon

    def rewrite_damage_box(self):
        w, h = 50, 50
        x, y = self.rect.x, self.rect.y

        dx, dy = Player.images[self.key].get_size()
        if 'reverse' in self.key and 'side' in self.key:
            dx, w, h = dx * width // 800, w * width // 800, h * height // 600
            self.damage_box.rect = pygame.Rect(x - 2 * dx, y, w, h)
        elif 'side' in self.key:
            dx, w, h = dx * width // 800, w * width // 800, h * height // 600
            self.damage_box.rect = pygame.Rect(x + dx, y, w, h)
        elif 'front' in self.key:
            dy, w, h = dy * height // 600, w * width // 800, h * h // 600
            self.damage_box.rect = pygame.Rect(x - (dx // 2), y + dy, h, w)
        elif 'back' in self.key:
            dy, w, h = dy * height // 600, w * width // 800, h * height // 600
            self.damage_box.rect = pygame.Rect(x - (dx // 2), y - dy, h, w)

    def check_kd(self):
        return self.kd

    def func_attack(self, event):
        self.attack = event
        if pygame.sprite.spritecollideany(self.damage_box, enemies):
            enemies.update(dmg_dealer=self)

    def get_damage_box(self):
        return self.damage_box

    def get_hit(self, dmg_dealer):
        pass
