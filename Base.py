import pygame
from SETTINGS import *
from StartScreen import start_screen
from LoadImage import load_image, load_level


pygame.init()
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    try:
        front_stay = load_image('HeroFrontStay.png')
        front_right_leg = load_image('HeroFrontRightLeg.png')
        front_left_leg = load_image('HeroFrontLeftLeg.png')
        side_left_leg = load_image('HeroSideLeftLeg.png')
        side_right_leg = load_image('HeroSideRightLeg.png')
        side_stay = load_image('HeroSideStay.png')
        back_stay = load_image('HeroBackStay.png')
        back_right_leg = load_image('HeroBackRightLeg.png')
        back_left_leg = load_image('HeroBackLeftLeg.png')
    except ValueError:
        safe_image = pygame.Surface((player_width, player_height))
        front_stay = front_right_leg = front_left_leg = side_stay = safe_image
        side_left_leg, side_right_leg = back_stay = back_right_leg = safe_image
        back_left_leg = safe_image
        pygame.draw.circle(safe_image, 'red', (player_width // 2, player_height // 2), player_height // 2)
    images = {
        'front_stay': front_stay,
        'front_right_leg': front_right_leg,
        'front_left_leg': front_left_leg,
        'side_left_leg': side_left_leg,
        'side_right_leg': side_right_leg,
        'side_stay': side_stay,
        'back_stay': back_stay,
        'back_right_leg': back_right_leg,
        'back_left_leg': back_left_leg,
        'side_left_leg_reverse': pygame.transform.flip(side_left_leg, True, False),
        'side_right_leg_reverse': pygame.transform.flip(side_right_leg, True, False),
        'side_stay_reverse': pygame.transform.flip(side_stay, True, False)
    }

    def __init__(self, pos):
        super(Player, self).__init__()
        self.rect = pygame.Rect(pos[0], pos[1], player_width, player_height)
        self.key = 'front_stay'
        image = Player.images[self.key]

        self.image = image
        self.speed = player_speed

    def update(self, check=None, flag_change_image=False):
        move_side = False
        if not check:
            return
        if check[pygame.K_LEFT] or check[pygame.K_a]:
            move_side = True
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
        self.image = Player.images[self.key]


player = Player((100, 100))
sprites.add(player)


def start_game():
    change_image_time = 0
    while True:
        screen.fill(black)
        change_image_time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        if change_image_time == 8:
            change_image_time = 0
            sprites.update(check=pygame.key.get_pressed(), flag_change_image=True)
        else:
            sprites.update(check=pygame.key.get_pressed())
        sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
start_game()
