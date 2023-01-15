from DefinePlayerLevel import LEVELS
import pygame
from LoadImage import load_image
from SettingsRebase import *


pygame.font.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
start_sprites = pygame.sprite.Group()
size_set = size


class Button(pygame.sprite.Sprite):
    def __init__(self, file_name=None):
        super(Button, self).__init__(start_sprites)
        self.pos_x = 290 * width // 800 + (270 * width // 800 - button_width) // 2
        self.pos_y = 220 * height // 600
        if file_name:
            try:
                btn_image = load_image(file_name)
                self.image = btn_image
            except ValueError:
                self.image = pygame.Surface((button_width, button_height), pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, btn_start_game_color, (0, 0, button_width, button_height))
        self.font = pygame.font.Font(None, font_size)
        self.space_y = int(8 * height / 600)

    def is_clicked(self, pos):
        if pos[0] in range(self.rect.x, self.rect.x + self.rect.w + 1):
            if pos[1] in range(self.rect.y, self.rect.y + self.rect.h + 1):
                return True
        return False


class ButtonStartGame(Button):
    def __init__(self):
        super(ButtonStartGame, self).__init__(file_name='btn_start_game.png')
        self.rect = pygame.Rect(self.pos_x, self.pos_y, button_width, button_height)
        text = self.font.render('Start Game', True, white)
        space_x = int(7 * width / 800)
        self.image.blit(text, (space_x, self.space_y))


class ButtonExitGame(Button):
    def __init__(self):
        super(ButtonExitGame, self).__init__(file_name='btn_start_game.png')
        pos_y = self.pos_y + button_height + 5
        self.rect = pygame.Rect(self.pos_x, pos_y, button_width, button_height)
        text = self.font.render('Exit', True, white)
        space_x = int(65 * width / 800)
        self.image.blit(text, (space_x, self.space_y))


class ButtonSettings(Button):
    def __init__(self):
        super(ButtonSettings, self).__init__(file_name='btn_settings.png')
        pos_y = self.pos_y + 2 * button_height + 10
        self.rect = pygame.Rect(self.pos_x, pos_y, button_width, button_height)
        text = self.font.render('Settings', True, white)
        space_x = int(30 * width / 800)
        self.image.blit(text, (space_x, self.space_y))


class ButtonChoseLevel(Button):
    def __init__(self):
        super(ButtonChoseLevel, self).__init__(file_name='btn_choose_level.png')
        pos_y = self.pos_y + 3 * button_height + 15
        self.rect = pygame.Rect(self.pos_x, pos_y, button_width, button_height)
        text = self.font.render('Set level', True, white)
        space_x = int(30 * width / 800)
        self.image.blit(text, (space_x, self.space_y))


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


class InterfaceSettings(pygame.sprite.Sprite):
    def __init__(self):
        super(InterfaceSettings, self).__init__(start_sprites)
        settings_width = 400 * width // 800
        settings_height = 400 * height // 600
        space_x = 200 * width // 800
        space_y = 100 * height // 600
        self.exit_width = 20 * width // 800
        self.exit_height = 20 * height // 600
        self.exit_space_x, self.exit_space_y = settings_width - self.exit_width, 0
        self.btn_settings_space_x = 200 * settings_width // 800
        self.btn_settings_space_y = 100 * settings_height // 600
        self.btn_settings_coords = []
        self.settings = [(800, 600), (1280, 720), (1920, 1080)]
        try:
            image = load_image('InterfaceSettings.png')
            image = pygame.transform.scale(image, (settings_width, settings_height))
            self.image = image
        except ValueError:
            self.image = pygame.Surface((settings_width, settings_height), pygame.SRCALPHA)
            pygame.draw.rect(self.image, black, (0, 0, settings_width, settings_height))
        self.rect = pygame.Rect((space_x, space_y, settings_width, settings_height))
        self.btn_exit()
        self.btn_settings()

    def btn_exit(self):
        try:
            image = load_image('InterfaceSettingsButtonExit.png')
            image = pygame.transform.scale(image, (self.exit_width, self.exit_height))
        except ValueError:
            image = pygame.Surface((self.exit_width, self.exit_height), pygame.SRCALPHA)
            pygame.draw.rect(image, red, (0, 0, self.exit_width, self.exit_height))
        self.image.blit(image, (self.exit_space_x, self.exit_space_y))

    def close(self, pos):
        range_x = self.rect.x + self.exit_space_x
        if pos[0] in range(range_x, range_x + self.exit_width + 1):
            range_y = self.rect.y + self.exit_space_y
            if pos[1] in range(range_y, range_y + self.exit_height + 1):
                return True
        return False

    def btn_settings(self):
        for i in range(len(self.settings)):
            space_y = self.btn_settings_space_y + button_height * i + 5 * i
            image = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
            pygame.draw.rect(image, btn_start_game_color, (0, 0, button_width, button_height))
            self.image.blit(image, (self.btn_settings_space_x, space_y))
            self.btn_settings_coords.append((self.btn_settings_space_x + self.rect.x, self.rect.y + space_y))

    def change_settings(self, pos):
        for i in range(len(self.btn_settings_coords)):
            start_coord = self.btn_settings_coords[i]
            if pos[0] in range(start_coord[0], start_coord[0] + button_width):
                if pos[1] in range(start_coord[1], start_coord[1] + button_height):
                    return self.settings[i]
        return False


def start_screen():
    LEVELS.chose_level()
    StartScreen()
    btn_start = ButtonStartGame()
    btn_exit = ButtonExitGame()
    btn_settings = ButtonSettings()
    btn_chose_level = ButtonChoseLevel()
    interface_settings = None
    while True:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not interface_settings:
                    if btn_start.is_clicked(event.pos):
                        screen.fill(black)
                        return
                    if btn_exit.is_clicked(event.pos):
                        exit()
                    if btn_settings.is_clicked(event.pos):
                        interface_settings = InterfaceSettings()
                    if btn_chose_level.is_clicked(event.pos):
                        pass
                else:
                    if interface_settings.close(event.pos):
                        interface_settings.kill()
                        interface_settings = None
                    if interface_settings:
                        change_settings = interface_settings.change_settings(event.pos)
                        if change_settings:
                            rebase_size(change_settings)
                            print(change_settings)

        start_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

