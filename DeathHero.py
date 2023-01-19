import pygame
from SETTINGS import *
from LoadImage import load_image


pygame.init()
screen = pygame.display.set_mode(size)
end_sprites = pygame.sprite.Group()


class Button(pygame.sprite.DirtySprite):
    def __init__(self):
        super(Button, self).__init__(end_sprites)
        self.pos_x = 200 * width // 800
        self.pos_y = 500 * height // 600
        self.image = pygame.Surface((button_width, button_height), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, dark_grey, (0, 0, button_width, button_height))
        pygame.draw.rect(self.image, light_grey, (0, 0, button_width, button_height), 3)
        self.font = pygame.font.Font(None, font_size)
        self.space_y = int(8 * height / 600)

    def is_clicked(self, pos):
        if pos[0] in range(self.rect.x, self.rect.x + self.rect.w + 1):
            if pos[1] in range(self.rect.y, self.rect.y + self.rect.h + 1):
                return True
        return False


class StartMenuButton(Button):
    def __init__(self):
        super(StartMenuButton, self).__init__()
        self.rect = pygame.Rect(self.pos_x, self.pos_y, button_width, button_height)
        self.text = self.font.render('Start Menu', True, white)
        self.image.blit(self.text, (8 * width // 800, self.space_y))


class RestartLevelButton(Button):
    def __init__(self):
        super(RestartLevelButton, self).__init__()
        pos_x = self.pos_x + button_width
        self.rect = pygame.Rect(pos_x, self.pos_y, button_width, button_height)
        self.text = self.font.render('    Restart', True, white)
        self.image.blit(self.text, (0, self.space_y))


class InterfaceEndScreen(pygame.sprite.Sprite):
    def __init__(self):
        super(InterfaceEndScreen, self).__init__(end_sprites)
        settings_width = 400 * width // 800
        settings_height = 400 * height // 600
        space_x = 200 * width // 800
        space_y = 100 * height // 600
        self.exit_width = 20 * width // 800
        self.exit_height = 20 * height // 600
        self.image = pygame.Surface((settings_width, settings_height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, purple, (0, 0, settings_width, settings_height))
        pygame.draw.rect(self.image, dark_grey, (0, 0, settings_width, self.exit_height))
        self.image = pygame.transform.scale(load_image('EndScreen.jpg'), (settings_width, settings_height))
        pygame.draw.rect(self.image, dark_grey, (0, 0, settings_width, settings_height), 1)
        self.rect = pygame.Rect((space_x, space_y, settings_width, settings_height))


def end_screen(more_sprites=None):
    running = True
    InterfaceEndScreen()
    start_menu = StartMenuButton()
    restart_level = RestartLevelButton()
    if more_sprites:
        more_sprites.add(end_sprites)
        to_draw = more_sprites
    else:
        to_draw = end_sprites
    pygame.mouse.set_visible(True)
    while running:
        to_draw.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not (start_menu.is_clicked(event.pos) and restart_level.is_clicked(event.pos)):
                    if start_menu.is_clicked(event.pos):
                        more_sprites.remove(end_sprites)
                        return 11
                    if restart_level.is_clicked(event.pos):
                        more_sprites.remove(end_sprites)
                        return 22
        pygame.display.flip()
