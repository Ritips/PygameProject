from StartScreen import start_screen
from Player import Player
from Queen import Queen
from LoadImage import load_image
from Slime import Slime
from Constructions import *
from LoadLevel import *
from DefinePlayerLevel import *
from SETTINGS import *
import pygame


pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


class EscMenu(pygame.sprite.Sprite):
    def __init__(self):
        super(EscMenu, self).__init__(sprites)
        settings_width = 400 * width // 800
        settings_height = 400 * height // 600
        space_x = 200 * width // 800
        space_y = 100 * height // 600
        self.exit_width = button_width
        self.exit_height = button_height
        self.exit_space_x, self.exit_space_y = (settings_width - self.exit_width) // 2, settings_height // 2
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
            pygame.draw.rect(self.image, dark_grey, (0, 0, settings_width, self.exit_height))
            pygame.draw.rect(self.image, dark_grey, (0, 0, settings_width, settings_height), 1)
        self.rect = pygame.Rect((space_x, space_y, settings_width, settings_height))
        font_size_menu = 40 * width // 800
        self.font = pygame.font.Font(None, font_size_menu)
        self.btn_exit()

    def btn_exit(self):
        try:
            image = load_image('InterfaceSettingsButtonExit.png')
            image = pygame.transform.scale(image, (self.exit_width, self.exit_height))
        except ValueError:
            image = pygame.Surface((self.exit_width, self.exit_height), pygame.SRCALPHA)
            pygame.draw.rect(image, dark_grey, (0, 0, self.exit_width, self.exit_height))
            text = self.font.render('  Close Game', True, white)
            image.blit(text, (0, (8 * width // 800)))
        self.image.blit(image, (self.exit_space_x, self.exit_space_y))

    def close(self, pos):
        range_x = self.rect.x + self.exit_space_x
        if pos[0] in range(range_x, range_x + self.exit_width + 1):
            range_y = self.rect.y + self.exit_space_y
            if pos[1] in range(range_y, range_y + self.exit_height + 1):
                return True
        return False


def draw_level(level_draw=None, index=0):
    if not index or not level_draw:
        player = Player((tile_width, tile_height))
        return black, player
    if index == 1:
        for i in range(len(level_draw)):
            for j in range(len(level_draw[i])):
                if level_draw[i][j] == 'W':
                    WallQueen((j, i))
                else:
                    PathQueen((j, i))
        player = Player((7 * tile_width, tile_height))
        queen = Queen()
        queen.set_target(player)
        return purple, player
    return black


def start_game():
    class_level = LEVELS.get_level()
    level_to_draw, index = class_level.get_level()
    color, player = draw_level(index=index, level_draw=level_to_draw)
    change_image_time = 0
    esc_menu = None
    while True:
        screen.fill(color)
        if esc_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and esc_menu.close(event.pos):
                    exit()
            continue
        change_image_time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not player.check_kd():
                player.func_attack(True)
            if event.type == pygame.KEYDOWN and event.key == 27:
                esc_menu = EscMenu()
        if not change_image_time % 80:
            change_image_time = 0

        sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time)
        sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
start_game()

