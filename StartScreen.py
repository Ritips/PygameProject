from DefinePlayerLevel import LEVELS
import pygame
from LoadImage import load_image
from SETTINGS import *


pygame.font.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
start_sprites = pygame.sprite.Group()
size_set = size


class Button(pygame.sprite.Sprite):  # Button that can carry out click function
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
                pygame.draw.rect(self.image, dark_grey, (0, 0, button_width, button_height))
                pygame.draw.rect(self.image, light_grey, (0, 0, button_width, button_height), 3)
        self.font = pygame.font.Font(None, font_size)
        self.space_y = int(8 * height / 600)

    def is_clicked(self, pos):
        if pos[0] in range(self.rect.x, self.rect.x + self.rect.w + 1):
            if pos[1] in range(self.rect.y, self.rect.y + self.rect.h + 1):
                return True
        return False


class ButtonStartGame(Button):  # text if Start Game
    def __init__(self):
        super(ButtonStartGame, self).__init__(file_name='btn_start_game.png')
        self.rect = pygame.Rect(self.pos_x, self.pos_y, button_width, button_height)
        text = self.font.render('Start Game', True, white)
        space_x = int(7 * width / 800)
        self.image.blit(text, (space_x, self.space_y))


class ButtonExitGame(Button):  # text is Exit
    def __init__(self):
        super(ButtonExitGame, self).__init__(file_name='btn_start_game.png')
        pos_y = self.pos_y + button_height + 5
        self.rect = pygame.Rect(self.pos_x, pos_y, button_width, button_height)
        text = self.font.render('Exit', True, white)
        space_x = int(65 * width / 800)
        self.image.blit(text, (space_x, self.space_y))


class ButtonSettings(Button):  # text is size of the screen
    def __init__(self):
        super(ButtonSettings, self).__init__(file_name='btn_settings.png')
        pos_y = self.pos_y + 2 * button_height + 10
        self.rect = pygame.Rect(self.pos_x, pos_y, button_width, button_height)
        text = self.font.render('Settings', True, white)
        space_x = int(30 * width / 800)
        self.image.blit(text, (space_x, self.space_y))


class ButtonChoseLevel(Button):  # text is the value(index) of the level
    def __init__(self):
        super(ButtonChoseLevel, self).__init__(file_name='btn_choose_level.png')
        pos_y = self.pos_y + 3 * button_height + 15
        self.rect = pygame.Rect(self.pos_x, pos_y, button_width, button_height)
        text = self.font.render('Set level', True, white)
        space_x = int(30 * width / 800)
        self.image.blit(text, (space_x, self.space_y))


class StartScreen(pygame.sprite.Sprite):  # background
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


class InterfaceSettings(pygame.sprite.Sprite):  # Interface that include some buttons (Settings buttons)
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
            pygame.draw.rect(self.image, dark_grey, (0, 0, settings_width, self.exit_height))
            pygame.draw.rect(self.image, dark_grey, (0, 0, settings_width, settings_height), 1)
        self.rect = pygame.Rect((space_x, space_y, settings_width, settings_height))
        self.message = None
        self.btn_exit()
        self.btn_settings()

    def btn_exit(self):
        try:
            image = load_image('InterfaceSettingsButtonExit.png')
            image = pygame.transform.scale(image, (self.exit_width, self.exit_height))
        except ValueError:
            line_width = 2 * width // 800
            image = pygame.Surface((self.exit_width, self.exit_height), pygame.SRCALPHA)
            pygame.draw.rect(image, red, (0, 0, self.exit_width, self.exit_height))
            pygame.draw.rect(image, light_grey, (0, 0, self.exit_width, self.exit_height), 2)
            pygame.draw.line(image, light_grey, (0, 0), (self.exit_width, self.exit_height), line_width)
            pygame.draw.line(image, light_grey, (0, self.exit_height), (self.exit_width, 0), line_width)
        self.image.blit(image, (self.exit_space_x, self.exit_space_y))

    def close(self, pos):
        range_x = self.rect.x + self.exit_space_x
        if pos[0] in range(range_x, range_x + self.exit_width + 1):
            range_y = self.rect.y + self.exit_space_y
            if pos[1] in range(range_y, range_y + self.exit_height + 1):
                if self.message:
                    self.message.kill()
                return True
        return False

    def btn_settings(self):
        font = pygame.font.Font(None, font_size)
        font_space_y = int(8 * height / 600)
        for i in range(len(self.settings)):
            space_y = self.btn_settings_space_y + button_height * i + 5 * i
            image = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
            pygame.draw.rect(image, dark_grey, (0, 0, button_width, button_height))
            pygame.draw.rect(image, light_grey, (0, 0, button_width, button_height), 3)
            get_text = ' '.join(map(str, self.settings[i]))
            text = font.render(get_text, True, white)
            space_x = button_width // len(get_text)
            image.blit(text, (space_x, font_space_y))
            self.image.blit(image, (self.btn_settings_space_x, space_y))
            self.btn_settings_coords.append((self.btn_settings_space_x + self.rect.x, self.rect.y + space_y))

    def change_settings(self, pos):
        if self.message:
            return
        for i in range(len(self.btn_settings_coords)):
            start_coord = self.btn_settings_coords[i]
            if pos[0] in range(start_coord[0], start_coord[0] + button_width):
                if pos[1] in range(start_coord[1], start_coord[1] + button_height):
                    self.message = Message()
                    return self.settings[i]
        return False

    def btn_close_message(self, pos):
        if self.message and self.message.close(pos):
            self.message.kill()
            self.message = None


class Message(pygame.sprite.Sprite):  # notification to user
    def __init__(self):
        super(Message, self).__init__(start_sprites)
        space_x = 200 * width // 800
        space_y = 400 * height // 600
        self.message_width = 400 * width // 800
        self.message_height = button_height * 2
        self.rect = pygame.Rect((space_x, space_y, self.message_height, self.message_width))
        self.exit_width = 20 * width // 800
        self.exit_height = 20 * height // 600
        self.exit_space_x, self.exit_space_y = self.message_width - self.exit_width, 0
        self.image = pygame.Surface((self.message_width, self.message_height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, white, (0, 0, self.message_width, self.message_height), 3)
        self.font = pygame.font.Font(None, int(40 * width / 800))
        # if size of the screen is changed the game should be restarted
        self.text = '   Restart the game for the'
        self.text2 = '    changes to take effect'
        self.exit_btn()

    def exit_btn(self):
        image = pygame.Surface((self.exit_width, self.exit_height), pygame.SRCALPHA)
        pygame.draw.rect(image, red, (0, 0, self.exit_width, self.exit_height))
        pygame.draw.rect(image, white, (0, 0, self.exit_width, self.exit_height), 2)

        line_width = 2 * width // 800
        pygame.draw.line(image, white, (0, 0), (self.exit_width, self.exit_height), line_width)
        pygame.draw.line(image, white, (0, self.exit_height), (self.exit_width, 0), line_width)
        text = self.font.render(self.text, True, white)
        text2 = self.font.render(self.text2, True, white)
        self.image.blit(text, (5, 8))
        self.image.blit(text2, (5, int(40 * width / 800) + 8))
        self.image.blit(image, (self.exit_space_x, self.exit_space_y))

    def close(self, pos):
        range_x = self.rect.x + self.exit_space_x
        if pos[0] in range(range_x, range_x + self.exit_width + 1):
            range_y = self.rect.y + self.exit_space_y
            if pos[1] in range(range_y, range_y + self.exit_height + 1):
                return True
        return False


class ButtonLevel(pygame.sprite.Sprite):  # button which include value(index) of the level and can carry out click func
    def __init__(self, pos, text):
        super(ButtonLevel, self).__init__(start_sprites)
        self.rect = pygame.Rect(pos[0], pos[1], tile_width, tile_height)
        self.image = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, dark_grey, (0, 0, tile_width, tile_height), 3 * width // 800)
        self.font = pygame.font.Font(None, 30 * width // 800)
        self.text_string = text
        self.text = self.font.render(text, True, white)
        self.image.blit(self.text, (0, 0))

    def is_clicked(self, pos):
        if pos[0] in range(self.rect.x, self.rect.x + self.rect.w):
            if pos[1] in range(self.rect.y, self.rect.y + self.rect.h):
                return True

    def get_surface(self):
        return self.image

    def get_text(self):
        return self.text_string


class InterfaceChoseLevel(pygame.sprite.Sprite):
    def __init__(self):
        super(InterfaceChoseLevel, self).__init__(start_sprites)
        self.x = 200 * width // 800
        self.y = 100 * height // 600
        self.width = 400 * width // 800
        self.height = 400 * height // 600
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, dark_grey, (0, 0, self.width, self.height), 3 * width // 800)
        pygame.draw.rect(self.image, dark_grey, (0, 0, self.width, self.height // 20))

        self.x2 = self.width - self.width // 10 // 2
        self.y2 = self.y
        self.w2 = self.width // 20
        self.h2 = self.height // 20

        pygame.draw.rect(self.image, red, (self.x2, 0, self.w2, self.h2))
        line_width = 1 * width // 800
        pygame.draw.rect(self.image, light_grey, (self.x2, 0, self.w2, self.h2), line_width)
        pygame.draw.line(self.image, light_grey, (self.x2, 0), (self.width, self.h2), line_width)
        pygame.draw.line(self.image, light_grey, (self.x2, self.h2 - 1), (self.width, 0), line_width)

        self.content = []
        self.buttons = []

    def update(self, read_file=False):  # read txt file of available(finished) levels
        if not read_file:
            return
        with open('data/levels.txt', 'r') as f_read:
            [self.content.append(el) for el in map(str.strip, f_read.readlines()) if el not in self.content]
            self.output_levels_buttons()

    def output_levels_buttons(self):  # show available levels to select
        box = self.width // tile_width, self.height // tile_height
        space_y = 10 * height // 600
        index = 0
        for i in range(box[1]):
            if index >= len(self.content):
                break
            for j in range(box[0]):
                if index >= len(self.content):
                    break
                content = self.content[index]
                pos_x, pos_y = self.rect.x + tile_width * j, self.rect.y + tile_height * i + self.h2 + space_y
                btn = ButtonLevel((pos_x, pos_y), content)  # create button
                self.buttons.append(btn)
                index += 1

    def get_click(self, pos):
        btn = list(filter(lambda x: x.is_clicked(pos), self.buttons))  # filter and check if the button is clicked
        if not btn:
            return -182  # error
        return int(btn[0].get_text())  # return value(index) of the level

    def close(self, pos):  # if close button is clicked InterfaceChoseLevel will be closed
        if pos[0] in range(self.x + self.x2, self.rect.x + self.width):
            if pos[1] in range(self.rect.y, self.rect.y + self.y2):
                [btn.kill() for btn in self.buttons]
                return True


def start_screen():
    LEVELS.chose_level(level_chosen=0)  # standard value (0 is start_level. It can be changed for tests)
    StartScreen()  # Sprite. It is a picture of the castle
    # Sprites that contain background and text of the button. If they are clicked they will carry out some functions
    btn_start = ButtonStartGame()
    btn_exit = ButtonExitGame()
    btn_settings = ButtonSettings()
    btn_chose_level = ButtonChoseLevel()
    # Menu where size of the screen can be selected
    interface_settings = None
    # Menu where level can be selected
    interface_level = None
    pygame.mouse.set_visible(True)  # make cursor visible
    while True:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # event left button mouse is clicked
                if not interface_settings and not interface_level:  # check are interfaces opened
                    if btn_start.is_clicked(event.pos):  # start game
                        screen.fill(black)
                        # delete all sprites to minimise resources
                        for sprite in start_sprites:
                            sprite.kill()
                        return
                    if btn_exit.is_clicked(event.pos):  # close game
                        exit()
                    if btn_settings.is_clicked(event.pos):  # interface settings open
                        interface_settings = InterfaceSettings()
                    if btn_chose_level.is_clicked(event.pos):  # interface level open
                        interface_level = InterfaceChoseLevel()
                        interface_level.update(read_file=True)  # levels are saved into file when they are finished
                elif interface_settings:  # interface is settings opened
                    if interface_settings.close(event.pos):  # close interface
                        interface_settings.kill()
                        interface_settings = None
                    if interface_settings:  # check is interface opened to except error
                        change_settings = interface_settings.change_settings(event.pos)  # select size of the screen
                        if change_settings:  # update file with settings
                            with open(settings_file_name, 'w') as f_write:
                                f_write.writelines('\n'.join(map(str, change_settings)))
                        interface_settings.btn_close_message(event.pos)
                elif interface_level:  # interface level is opened
                    if interface_level.close(event.pos):  # close interface
                        interface_level.kill()
                        interface_level = None
                    if interface_level:  # check is interface opened to except error
                        index_level = interface_level.get_click(event.pos)  # select level
                        if index_level >= 0:
                            LEVELS.chose_level(level_chosen=index_level)  # level is selected

        start_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

