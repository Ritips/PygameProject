from StartScreen import start_screen
from DeathHero import end_screen
from Player import Player
from Queen import Queen, Valkyrie
from Constructions import *
from LoadLevel import *
from DefinePlayerLevel import *
from SETTINGS import *
from WinScreen import win_screen
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
        Valkyrie(pos=(7 * tile_width, tile_height))
        queen = Queen()
        queen.set_target(player)
        return purple, player
    return black


def pass_level(index):
    with open('data/levels.txt', 'r') as file_levels:
        contain = list(map(str.strip, file_levels.readlines())) + [index, ]
        with open('data/levels.txt', 'w', newline='\n') as file_levels_write:
            for el in contain:
                print(el, file=file_levels_write)


def start_game():
    class_level = LEVELS.get_level()
    level_to_draw, index = class_level.get_level()
    color, player = draw_level(index=index, level_draw=level_to_draw)
    change_image_time = 0
    esc_menu = None
    running = True
    while running:
        screen.fill(color)
        if player not in sprites:
            return 2
        if not enemies.sprites():
            pass_level(index)
            return 3
        if esc_menu:
            pygame.mouse.set_visible(True)
            sprites.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if esc_menu.close(event.pos):
                        exit()
                    elif esc_menu.continue_game(event.pos):
                        esc_menu.kill()
                        esc_menu = None
                    elif esc_menu.return_start_menu(event.pos):
                        sprites.empty()
                        enemies.empty()
                        group_player.empty()
                        return 1
                if event.type == pygame.KEYDOWN and event.key == 27:
                    esc_menu.kill()
                    esc_menu = None
            pygame.display.flip()
            continue
        pygame.mouse.set_visible(False)
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
        sprites.draw(screen)
        sprites.update(check=pygame.key.get_pressed(), flag_change_image=change_image_time)
        pygame.display.set_caption(str(clock.get_fps()))
        pygame.display.flip()
        clock.tick()
    return 0


def restart():
    result = end_screen(more_sprites=sprites)
    if result == 11:
        main()
    elif result == 22:
        main(restart_func=True)


def show_win_menu():
    result = win_screen(more_sprites=sprites)
    if result == 123:
        main()


def main(restart_func=False):
    for sprite in sprites:
        sprite.kill()
    if not restart_func:
        start_screen()
    flag = start_game()
    if flag == 1:
        main()
    elif flag == 2:
        restart()
    elif flag == 3:
        show_win_menu()


if __name__ == '__main__':
    main()
