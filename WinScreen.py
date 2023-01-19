import pygame
from SETTINGS import *


pygame.init()
screen = pygame.display.set_mode(size)
win_group_sprites = pygame.sprite.Group()


class BackGround(pygame.sprite.Sprite):
    def __init__(self):
        super(BackGround, self).__init__(win_group_sprites)
        space_x = 200 * width // 800
        space_y = 100 * height // 600
        back_width = 400 * width // 800
        back_height = 400 * height // 600
        self.rect = pygame.Rect(space_x, space_y, back_width, back_height)
        self.image = pygame.Surface((back_width, back_height), pygame.SRCALPHA)
        self.font = pygame.font.Font(None, font_size)

        pygame.draw.rect(self.image, black, (0, 0, back_width, back_height))
        pygame.draw.rect(self.image, dark_grey, (0, 0, back_width, back_height), 3)
        text = self.font.render('  LEVEL PASSED', True, white)
        self.image.blit(text, (50 * width // 800, 25 * height // 600))
        self.start_menu()

    def start_menu(self):
        image = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        pygame.draw.rect(image, dark_grey, (0, 0, button_width, button_height))
        pygame.draw.rect(image, light_grey, (0, 0, button_width, button_height), 3)
        text = self.font.render('  Continue', True, white)
        image.blit(text, (5 * width // 800, 8 * height // 600))
        self.image.blit(image, (self.rect.x - button_width // 2, self.rect.y + button_height // 2))

    def is_clicked(self, pos):
        range_start_menu_x = self.rect.x + button_width // 2
        if pos[0] in range(range_start_menu_x, range_start_menu_x + button_width):
            range_y = self.rect.y * 2 + button_height // 2
            if pos[1] in range(range_y, range_y + button_height):
                return 123
        return 0


def win_screen(more_sprites=None):
    pygame.mouse.set_visible(True)
    background = BackGround()
    if more_sprites:
        more_sprites.add(win_group_sprites)
    else:
        more_sprites = win_group_sprites.copy()
    running = True
    while running:
        more_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if background.is_clicked(event.pos) == 123:
                    for sprite in win_group_sprites:
                        sprite.kill()
                    return 123
        pygame.display.flip()
