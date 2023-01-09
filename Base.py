import pygame
from SETTINGS import *
from StartScreen import start_screen
from player_images import player_images


pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    images = player_images

    def __init__(self, pos):
        super(Player, self).__init__()
        self.rect = pygame.Rect(pos[0], pos[1], player_width, player_height)
        self.key = 'front_stay'
        self.weapon = 'punch'
        image = Player.images[self.key]

        self.image = image
        self.speed = player_speed

    def update(self, check=None, flag_change_image=0, check_punch=False):

        if not check_punch and check:
            if not flag_change_image % 8:
                self.move(check=check, flag_change_image=True)
            else:
                self.move(check=check)
        if check_punch and not flag_change_image % 4:
            self.move(check=check)
            self.hit(check=check, flag_change_image=True)
        self.image = Player.images[self.key]

    def hit(self, check=None, flag_change_image=False):
        pass

    def move(self, check=None, flag_change_image=False):
        move_side = any_move = False
        if not check:
            return
        if check[pygame.K_LEFT] or check[pygame.K_a]:
            move_side = True
            any_move = True
            self.rect = self.rect.move(-self.speed, 0)
            if flag_change_image:
                if self.key == 'side_stay_reverse':
                    self.key = 'side_right_leg_reverse'
                elif self.key == 'side_right_leg_reverse':
                    self.key = 'side_left_leg_reverse'
                elif self.key == 'side_left_leg_reverse':
                    self.key = 'side_stay_reverse'
                else:
                    self.key = 'side_stay_reverse'
        if check[pygame.K_RIGHT] or check[pygame.K_d]:
            move_side = True
            any_move = True
            self.rect = self.rect.move(self.speed, 0)
            if flag_change_image:
                if self.key == 'side_stay':
                    self.key = 'side_right_leg'
                elif self.key == 'side_right_leg':
                    self.key = 'side_left_leg'
                elif self.key == 'side_left_leg':
                    self.key = 'side_stay'
                else:
                    self.key = 'side_stay'
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
        self.image = Player.images[self.key]

    def update_weapon(self, weapon):
        self.weapon = weapon


player = Player((100, 100))
sprites.add(player)


def start_game():
    global_const_check_punch = False
    change_image_time = 0
    while True:
        screen.fill(black)
        change_image_time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        if not change_image_time % 80:
            change_image_time = 0
        sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time,
                       check_punch=global_const_check_punch)
        sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
start_game()
