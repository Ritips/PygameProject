from LoadLevel import *
import pygame
from SETTINGS import *
from queen_images import queen_images
from magic_ball_images import magic_ball_images
from meteor_images import meteor_images
import random


class Queen(pygame.sprite.Sprite):
    images = queen_images

    def __init__(self, pos, target=None):
        super(Queen, self).__init__(enemies, sprites)
        self.rect = pygame.Rect(pos[0], pos[1], player_width, player_height)
        self.target = target
        self.key = 'front_stay'
        self.bullets = pygame.sprite.Group()  # for some bullets like magic ball and meteor
        self.allies = pygame.sprite.Group()  # to spawn more enemies
        image = Queen.images[self.key]
        self.image = image

        # queen constants
        self.max_health = 500
        self.health = 500
        self.previous = None
        self.damage = 100
        self.kd = 0
        self.kd_reset = 240
        self.attack = False
        self.speed = 1

        self.health_bar = pygame.sprite.Sprite()
        self.draw_health_bar()

        self.define_direction = pos

        self.kd_self_bar_show = 100
        self.status_self_bar_show = False
        self.ways_to_attack = [0, 1, 2, 3, 4]  # 0-meteor, 1-magic_ball, 2-meteor2, 3-spawn enemy, 4-magic_ball_chase

    def draw_health_bar(self):
        self.health_bar.rect = pygame.Rect(self.rect.x, self.rect.y - (10 * height // 600), player_width, hp_bar_height)
        image = pygame.Surface((player_width, hp_bar_height), pygame.SRCALPHA)
        length_line = player_width * self.health // self.max_health
        pygame.draw.rect(image, red, (0, 0, length_line, hp_bar_height))
        pygame.draw.rect(image, black, (0, 0, player_width, hp_bar_height), 1)
        self.health_bar.image = image

    def update(self, flag_change_image=0, dmg_dealer=None, **kwargs):
        if not self.status_self_bar_show and not self.health:
            self.kill()
            return
        if dmg_dealer:
            self.get_hit(dmg_dealer)
        if self.status_self_bar_show:
            if self.status_self_bar_show == self.kd_self_bar_show:
                self.status_self_bar_show = False
                self.health_bar.remove(sprites)
            else:
                self.status_self_bar_show += 1
            self.show_health_bar()
        if self.attack:
            self.kd += 1
            if self.kd == self.kd_reset:
                self.kd = 0
                self.attack = False
        self.logic_attack()

        self.logic_move(flag_change_image=(False if flag_change_image % 8 else True))
        self.image = Queen.images[self.key]

    def logic_move(self, flag_change_image=False):
        if not self.previous:
            self.previous = self.health
        if self.health < 100:
            self.speed += 1
        if self.previous and self.previous - self.health >= 50:
            while True:
                x, y = random.randint(0, width - self.rect.x), random.randint(0, height - self.rect.y)
                if pygame.sprite.spritecollideany(self, constructions):
                    continue
                self.previous = None
                self.define_direction = (x, y)
                break
        x, y = self.define_direction
        dx, dy = x - self.rect.x, y - self.rect.y
        if not dx:
            if not dy:
                self.move()
            elif dy > 0:
                self.move(flag_change_image=flag_change_image, down=True)
            else:
                self.move(flag_change_image=flag_change_image, up=True)
        elif dx > 0:
            if not dy:
                self.move(flag_change_image=flag_change_image, right=True)
            elif dy > 0:
                self.move(flag_change_image=flag_change_image, down=True, right=True)
            else:
                self.move(flag_change_image=flag_change_image, up=True, right=True)
        else:
            if not dy:
                self.move(flag_change_image=flag_change_image, left=True)
            elif dy > 0:
                self.move(flag_change_image=flag_change_image, down=True, left=True)
            else:
                self.move(flag_change_image=flag_change_image, up=True, left=True)

    def logic_attack(self):
        if not self.target or not group_player.has(self.target):
            self.key = 'front_stay'
            return
        x, y = self.target.rect.x, self.target.rect.y
        if not self.kd:
            self.kd = 1
            self.attack = True
            way_attack = random.choice(self.ways_to_attack)
            if not way_attack:  # meteor
                for _ in range(15):
                    meteor_x = x + random.randint(-player_width * 2, player_width * 2)
                    meteor_y = y + random.randint(-player_height * 2, player_height * 2)
                    Meteor((meteor_x, meteor_y))
            elif way_attack == 1 and self.target:
                x1, y1 = self.rect.x, self.rect.y
                count_magic_ball = random.randint(2, 4)
                dy = -count_magic_ball // 2 * magic_ball_height
                for i in range(count_magic_ball):  # magic_ball
                    dy += magic_ball_height
                    MagicBall((x1, y1 + dy), target=self.target)
            elif way_attack == 2:  # more meteors, xD
                for _ in range(5):
                    meteor_x = x + random.randint(-player_width * 2, player_width * 2)
                    meteor_y = y + random.randint(-player_height * 2, player_height * 2)
                    Meteor((meteor_x, meteor_y), kd_limit=10)
            elif way_attack == 3:  # spawn enemy
                pass
            elif way_attack == 4:
                x1, y1 = self.rect.x, self.rect.y
                count_magic_ball = random.randint(2, 4)
                dy = -count_magic_ball // 2 * magic_ball_height
                for i in range(count_magic_ball):  # magic_ball_chase
                    dy += magic_ball_height
                    MagicBall((x1, y1 + dy), target=self.target, chase_player=True)

    def move(self, flag_change_image=False, up=False, down=False, left=False, right=False):
        move_side = False
        if not (left and right):
            move_side = True
            if left:
                self.rect = self.rect.move(-self.speed, 0)
                for construction in constructions:
                    if pygame.sprite.collide_mask(self, construction):
                        self.rect = self.rect.move(self.speed, 0)
                if flag_change_image:
                    if self.key == 'side_stay':
                        self.key = 'side_step'
                    else:
                        self.key = 'side_stay'
            if right:
                self.rect = self.rect.move(self.speed, 0)
                for construction in constructions:
                    if pygame.sprite.collide_mask(self, construction):
                        self.rect = self.rect.move(-self.speed, 0)
                if flag_change_image:
                    if self.key == 'side_stay_reverse':
                        self.key = 'side_step_reverse'
                    else:
                        self.key = 'side_stay_reverse'
        if not (up and down):
            if up:
                self.rect = self.rect.move(0, -self.speed)
                for construction in constructions:
                    if pygame.sprite.collide_mask(self, construction):
                        self.rect = self.rect.move(0, self.speed)
                if flag_change_image and not move_side:
                    if self.key == 'back_stay':
                        self.key = 'back_step'
                    else:
                        self.key = 'back_stay'
            if down:
                self.rect = self.rect.move(0, self.speed)
                for construction in constructions:
                    if pygame.sprite.collide_mask(self, construction):
                        self.rect = self.rect.move(0, -self.speed)
                if flag_change_image and not move_side:
                    if self.key == 'front_stay':
                        self.key = 'front_step'
                    else:
                        self.key = 'front_stay'
        if not any((up, down, right, left)):
            self.key = 'front_stay'

    def get_hit(self, dmg_dealer):
        damage_box = dmg_dealer.damage_box
        if pygame.sprite.collide_rect(self, damage_box):
            self.health -= dmg_dealer.damage
            if self.health > 0:
                self.status_self_bar_show = 1
            else:
                self.health = 0
                self.status_self_bar_show = False
                self.kill(), self.health_bar.kill()

    def show_health_bar(self):
        if not sprites.has(self.health_bar) and self.status_self_bar_show:
            sprites.add(self.health_bar)
        self.draw_health_bar()

    def set_target(self, target):
        self.target = target


class Meteor(pygame.sprite.Sprite):
    images = meteor_images

    def __init__(self, pos, kd_limit=20):
        super(Meteor, self).__init__(bullets, sprites)
        self.rect = pygame.Rect(pos[0], pos[1], meteor_width, meteor_height)
        self.damage_box = self.rect
        self.damage = 15
        self.index = 0
        self.image = Meteor.images[self.index]
        self.kd = 0
        self.kd_limit = kd_limit

    def update(self, flag_change_image=0, **kwargs):
        self.kd += 1
        if not self.kd % self.kd_limit:
            self.index += 1
            self.kd = 0
            self.image = Meteor.images[self.index]
            if self.index == 3:
                pass
            elif self.index == 4:
                for sprite in group_player:
                    if pygame.sprite.collide_mask(sprite, self):
                        group_player.update(dmg_dealer=self)
                self.kill()


class MagicBall(pygame.sprite.Sprite):
    images = magic_ball_images

    def __init__(self, pos, target, chase_player=False):
        super(MagicBall, self).__init__(bullets, sprites)
        self.rect = pygame.Rect(pos[0], pos[1], magic_ball_width, magic_ball_height)
        self.damage_box = self.rect
        self.target = target
        self.index = 0
        self.damage = 0.5
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


