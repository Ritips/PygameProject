import time
from LoadLevel import *
import pygame
from SETTINGS import *
import random
from wizard_images import wizard_images, wizard_ball_images


class Wizard(pygame.sprite.Sprite):
    images = wizard_images

    def __init__(self, pos, target):
        super(Wizard, self).__init__(enemies, sprites)
        self.rect = pygame.Rect(pos[0] * tile_width, pos[1] * tile_height, player_width, player_height)

        self.target = target
        self.key = 'move1'

        # wizard constants
        self.health = 1
        self.attack = False
        self.image = Wizard.images[self.key]
        self.speed = wizard_speed
        self.count_steps = 0
        self.flag = 2
        self.vector = random.choice(['forward', 'side'])
        self.left = False  # if vector: left or right side
        self.attack_time = time.time()

    def move(self, flag_change_image):
        if flag_change_image:
            if not self.attack:
                if self.vector == 'forward':
                    if self.key == 'move1':
                        self.key = 'move2'
                    elif self.key == 'move2':
                        self.key = 'move3'
                    elif self.key == 'move3':
                        self.key = 'move1'
                    else:
                        self.key = 'move1'
                else:
                    if self.left:
                        if self.key == 'move_side1':
                            self.key = 'move_side2'
                        elif self.key == 'move_side2':
                            self.key = 'move_side3'
                        elif self.key == 'move_side3':
                            self.key = 'move_side1'
                        else:
                            self.key = 'move_side1'
                    else:
                        if self.key == 'move_side1_reverse':
                            self.key = 'move_side2_reverse'
                        elif self.key == 'move_side2_reverse':
                            self.key = 'move_side3_reverse'
                        elif self.key == 'move_side3_reverse':
                            self.key = 'move_side1_reverse'
                        else:
                            self.key = 'move_side1_reverse'
            else:
                if self.key == 'attack1':
                    self.key = 'attack2'
                elif self.key == 'attack2':
                    self.attack = False
                    if self.vector == 'forward':
                        self.key = 'move1'
                    else:
                        if self.left:
                            self.key = 'move_side1_reverse'
                        else:
                            self.key = 'move_side1'

        if self.count_steps > 0:
            self.left = False
        else:
            self.left = True
        self.count_steps += 1
        if self.vector == 'forward':
            self.rect = self.rect.move(0, wizard_speed * (-1) ** self.flag)
        else:
            self.rect = self.rect.move(wizard_speed * (-1) ** self.flag, 0)
        if self.count_steps == 5:
            if self.flag == 2:
                self.flag = not self.flag
                self.flag = 1
            else:
                self.flag = 2
            self.count_steps = - 5

    def get_hit(self, dmg_dealer):
        damage_box = dmg_dealer.damage_box
        if pygame.sprite.collide_rect(self, damage_box):
            self.health -= dmg_dealer.damage
            if self.health <= 0:
                self.kill()

    def wizard_attack(self):
        x1, y1 = self.rect.x, self.rect.y
        count_magic_ball = random.randint(2, 4)
        dy = -count_magic_ball // 2 * magic_ball_height
        for i in range(count_magic_ball):  # magic_ball_chase
            dy += magic_ball_height
            MagicBall((x1, y1 + dy), target=self.target, chase_player=True)

    def update(self, flag_change_image=0, dmg_dealer=None, **kwargs):
        if self.health <= 0:
            self.kill()
            return
        if dmg_dealer:
            self.get_hit(dmg_dealer)
        if not flag_change_image % 8:
            self.move(flag_change_image=True)
        else:
            self.move(flag_change_image=False)
        if abs(self.attack_time - time.time()) >= 5:
            self.attack = True
            self.attack_time = time.time()
            self.key = 'attack1'
            self.wizard_attack()
        self.image = Wizard.images[self.key]

    def func_attack(self, event):
        self.attack = event


class MagicBall(pygame.sprite.Sprite):
    images = wizard_ball_images

    def __init__(self, pos, target, chase_player=False):
        super(MagicBall, self).__init__(bullets, sprites)
        self.rect = pygame.Rect(pos[0], pos[1], magic_ball_width, magic_ball_height)
        self.damage_box = self.rect
        self.target = target
        self.index = random.choice([0, 1])
        self.damage = 15
        self.life_time = 200
        self.life_time_count = 0
        self.speed = random.randint(1, 3)
        self.image = MagicBall.images[self.index]
        self.chase_player = chase_player
        if not self.chase_player:
            self.distance_x, self.distance_y = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
            speed_x, speed_y = round(self.distance_x * self.speed / FPS), round(self.distance_y * self.speed / FPS)
            self.speed_x, self.speed_y = speed_x, speed_y

    def update(self, flag_change_image=0, **kwargs):
        self.life_time_count += 1
        if not flag_change_image % 8:
            self.index += 1
        if not flag_change_image % 2:
            if self.chase_player:
                distance_x, distance_y = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
                k = 2
                speed_x, speed_y = round(distance_x / FPS / self.speed * k), round(distance_y / FPS / self.speed * k)
                dx_s = -1 if speed_x < 0 else 1
                dy_s = -1 if speed_y < 0 else 1
                self.rect = self.rect.move(speed_x + dx_s, speed_y + dy_s)
            else:
                self.rect = self.rect.move(self.speed_x, self.speed_y)
        if self.life_time_count == self.life_time:
            self.kill()
        if pygame.sprite.spritecollideany(self, constructions):
            self.kill()
        if pygame.sprite.spritecollideany(self, group_player):
            group_player.update(dmg_dealer=self)
            self.kill()
        self.image = MagicBall.images[self.index % len(MagicBall.images)]
        self.transform_image()

    def transform_image(self):
        if self.target.rect.x - self.rect.x > 0:
            self.image = pygame.transform.flip(self.image, True, False)