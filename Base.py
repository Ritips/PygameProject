import pygame
from SETTINGS import *
from StartScreen import start_screen
from LoadImage import load_image, load_level


pygame.init()
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Player, self).__init__()
        self.rect = pygame.Rect(pos[0], pos[1], player_width, player_height)
        try:
            image = load_image('test2.png', -2)
            self.image = image
        except ValueError:
            self.image = pygame.Surface((player_width, player_height))
            pygame.draw.circle(self.image, 'red', (player_width // 2, player_height // 2), player_height // 2)
        self.speed = player_speed

    def move(self, check):
        if check[pygame.K_UP] or check[pygame.K_w]:
            self.rect = self.rect.move(0, -self.speed)
        if check[pygame.K_RIGHT] or check[pygame.K_d]:
            self.rect = self.rect.move(self.speed, 0)
        if check[pygame.K_LEFT] or check[pygame.K_a]:
            self.rect = self.rect.move(-self.speed, 0)
        if check[pygame.K_DOWN] or check[pygame.K_s]:
            self.rect = self.rect.move(0, self.speed)


player = Player((100, 100))
sprites.add(player)


def start_game():
    while True:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        player.move(pygame.key.get_pressed())
        sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
start_game()
