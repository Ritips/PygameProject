from DefinePlayerLevel import LEVELS
import pygame
from LoadImage import load_image
from SETTINGS import *


pygame.font.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
start_sprites = pygame.sprite.Group()


class ButtonStartGame(pygame.sprite.Sprite):
    def __init__(self):
        super(ButtonStartGame, self).__init__(start_sprites)
        pos_x, pos_y = (width - button_width) // 2, height // 3
        self.rect = pygame.Rect(pos_x, pos_y, button_width, button_height)
        try:
            btn_image = load_image('btn_start_game.png')
            self.image = btn_image
        except ValueError:
            self.image = pygame.Surface((button_width, button_height), pygame.SRCALPHA, 32)
            pygame.draw.rect(self.image, btn_start_game_color, (0, 0, button_width, button_height))
        font = pygame.font.Font(None, font_size)
        text = font.render('Start Game', True, white)
        space_x, space_y = int(7 * width / 800), int(10 * height / 600)
        self.image.blit(text, (space_x, space_y))

    def is_clicked(self, pos):
        if pos[0] in range(self.rect.x, self.rect.x + self.rect.w + 1):
            if pos[1] in range(self.rect.y, self.rect.y + self.rect.h + 1):
                return True
        return


class ButtonExitGame(pygame.sprite.Sprite):
    def __init__(self):
        super(ButtonExitGame, self).__init__(start_sprites)
        pos_x, pos_y = (width - button_width) // 2, height // 3 + button_height * 2
        self.rect = pygame.Rect(pos_x, pos_y, button_width, button_height)
        try:
            btn_image = load_image('btn_start_game.png')
            self.image = btn_image
        except ValueError:
            self.image = pygame.Surface((button_width, button_height), pygame.SRCALPHA, 32)
            pygame.draw.rect(self.image, btn_start_game_color, (0, 0, button_width, button_height))
        font = pygame.font.Font(None, font_size)
        text = font.render('Exit', True, white)
        space_x, space_y = int(65 * width / 800), int(10 * height / 600)
        self.image.blit(text, (space_x, space_y))

    def is_clicked(self, pos):
        if pos[0] in range(self.rect.x, self.rect.x + self.rect.w + 1):
            if pos[1] in range(self.rect.y, self.rect.y + self.rect.h + 1):
                return True
        return


class StartScreen(pygame.sprite.Sprite):
    def __init__(self):
        super(StartScreen, self).__init__(start_sprites)
        try:
            image = load_image('StartScreen.png')
            image = pygame.transform.scale(image, (width, height))
            self.image = image
            self.rect = self.image.get_rect()
        except ValueError:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            self.rect = pygame.Rect((0, 0, width, height))
            pygame.draw.rect(self.image, black, (0, 0, width, height))


def start_screen():
    LEVELS.chose_level()
    StartScreen()
    btn_start = ButtonStartGame()
    btn_exit = ButtonExitGame()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_start.is_clicked(event.pos):
                    screen.fill(black)
                    return
                if btn_exit.is_clicked(event.pos):
                    exit()
        start_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

