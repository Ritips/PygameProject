from LoadLevel import *
from DefinePlayerLevel import *
from SETTINGS import *
import pygame


pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
group_text = pygame.sprite.Group()
back_to_start = False


def draw_level(level_draw=None, index=0):
    if index == 2:
        return black, None


class Text(pygame.sprite.Sprite):
    def __init__(self, pos, content):
        super(Text, self).__init__(group_text)
        # self.pos = pos[0] * tile_width, pos[1] * tile_height
        self.pos = 0, 0
        self.width = screen.get_width()
        self.height = tile_height
        self.font_size = tile_width
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.font = pygame.font.Font(None, self.font_size)
        self.content = content.copy()
        self.render_text()

    def update(self, **kwargs):
        global back_to_start
        self.rect = self.rect.move(0, 1)
        if self.rect.y > screen.get_size()[-1]:
            back_to_start = True
            self.kill()

    def render_text(self):
        content = self.content.copy()
        for i in range(len(content)):
            text = self.font.render(content[i], True, white)
            self.image.blit(text, (0, 0))


def start_last_level():
    [sprite.kill() for sprite in sprites]
    [construction.kill() for construction in constructions]
    class_level = LEVELS.get_level()
    level_to_draw, index = class_level.get_level()
    color, player = draw_level(level_to_draw, index)
    running = True
    count = 0
    while running:
        screen.fill(color)
        [exit() for event in pygame.event.get() if event.type == pygame.QUIT]
        if pygame.key.get_pressed()[pygame.K_ESCAPE] or back_to_start:
            return 110110
        if not count:
            Text((0, 0), ['Thanks for gaming. The End.'])
            count = 1
        group_text.draw(screen)
        group_text.update()
        pygame.display.set_caption(str(clock.get_fps()))
        pygame.display.flip()
        clock.tick(FPS)
    return 0
