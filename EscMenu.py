from SETTINGS import *
from Constructions import *
import pygame


class EscMenu(pygame.sprite.Sprite):
    def __init__(self):
        super(EscMenu, self).__init__(sprites)
        settings_width = 400 * width // 800
        settings_height = 400 * height // 600
        space_x = 200 * width // 800
        space_y = 100 * height // 600
        self.exit_width = button_width
        self.exit_height = button_height
        self.exit_space_x, self.exit_space_y = (settings_width - self.exit_width) // 2, settings_height // 3
        self.image = pygame.Surface((settings_width, settings_height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, black, (0, 0, settings_width, settings_height))
        pygame.draw.rect(self.image, dark_grey, (0, 0, settings_width, self.exit_height))
        pygame.draw.rect(self.image, dark_grey, (0, 0, settings_width, settings_height), 2)
        self.rect = pygame.Rect((space_x, space_y, settings_width, settings_height))
        font_size_menu = 40 * width // 800
        self.font = pygame.font.Font(None, font_size_menu)
        self.btn_exit()
        self.btn_continue()
        self.btn_return_start_menu()

    def btn_exit(self):
        image = pygame.Surface((self.exit_width, self.exit_height), pygame.SRCALPHA)
        pygame.draw.rect(image, dark_grey, (0, 0, self.exit_width, self.exit_height))
        pygame.draw.rect(image, light_grey, (0, 0, self.exit_width, self.exit_height), 3)
        text = self.font.render('  Close Game', True, white)
        image.blit(text, (0, (8 * width // 800)))
        self.image.blit(image, (self.exit_space_x, self.exit_space_y))

    def btn_continue(self):
        image = pygame.Surface((self.exit_width, self.exit_height), pygame.SRCALPHA)
        pygame.draw.rect(image, dark_grey, (0, 0, self.exit_width, self.exit_height))
        pygame.draw.rect(image, light_grey, (0, 0, self.exit_width, self.exit_height), 3)
        text = self.font.render('    Continue', True, white)
        image.blit(text, (0, (8 * width // 800)))
        self.image.blit(image, (self.exit_space_x, self.exit_space_y + button_height + 15 * height // 600))

    def close(self, pos):
        range_x = self.rect.x + self.exit_space_x
        if pos[0] in range(range_x, range_x + self.exit_width + 1):
            range_y = self.rect.y + self.exit_space_y
            if pos[1] in range(range_y, range_y + self.exit_height + 1):
                return True
        return False

    def continue_game(self, pos):
        range_x = self.rect.x + self.exit_space_x
        if pos[0] in range(range_x, range_x + self.exit_width + 1):
            range_y = self.rect.y + self.exit_space_y + button_height + 15 * height // 600
            if pos[1] in range(range_y, range_y + self.exit_height + 1):
                return True
        return False

    def btn_return_start_menu(self):
        image = pygame.Surface((self.exit_width, self.exit_height), pygame.SRCALPHA)
        pygame.draw.rect(image, dark_grey, (0, 0, self.exit_width, self.exit_height))
        pygame.draw.rect(image, light_grey, (0, 0, self.exit_width, self.exit_height), 3)
        text = self.font.render('    Start menu', True, white)
        image.blit(text, (0, (8 * width // 800)))
        self.image.blit(image, (self.exit_space_x, self.exit_space_y + button_height * 2 + 30 * height // 600))

    def return_start_menu(self, pos):
        range_x = self.rect.x + self.exit_space_x
        if pos[0] in range(range_x, range_x + self.exit_width + 1):
            range_y = self.rect.y + self.exit_space_y + button_height * 2 + 30 * height // 600
            if pos[1] in range(range_y, range_y + self.exit_height + 1):
                return True
        return False