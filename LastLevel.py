import random
from LoadLevel import *
from DefinePlayerLevel import *
from SETTINGS import *
import pygame
import time


pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
group_text = pygame.sprite.Group()
effects = pygame.sprite.Group()
back_to_start = False
booster = 1


def draw_level(level_draw=None, index=0):
    if index == 4:
        return black, None


class Text(pygame.sprite.Sprite):
    def __init__(self, pos, content):
        super(Text, self).__init__(group_text)
        y_height = -len(content) * tile_width
        self.pos = 0, y_height
        self.width = screen.get_width()
        self.height = tile_height * len(content) * 2
        self.font_size = tile_width
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.font = pygame.font.Font(None, self.font_size)
        self.content = content.copy()
        self.speed = 0
        self.start_time = time.time()
        self.render_text()

    def change_speed(self):
        self.speed = 1

    def manual_move(self):
        self.rect = self.rect.move(0, self.font_size)

    def update(self, **kwargs):
        global back_to_start
        if self.speed:
            end = time.time()
            if abs(self.start_time - end) >= 0.005:
                self.start_time = end
                self.rect = self.rect.move(0, booster * self.speed)
        if self.rect.y > screen.get_size()[-1]:
            back_to_start = True
            self.kill()

    def render_text(self):
        content = self.content.copy()
        for i in range(len(content)):
            text = self.font.render(content[i], True, white)
            self.image.blit(text, (0, self.font_size * i))


def start_last_level():
    [sprite.kill() for sprite in sprites]
    [construction.kill() for construction in constructions]
    with open('data/finish.txt', 'r', encoding='utf-8') as f_text_finish:
        sp = list(map(str.strip, f_text_finish.readlines()))[::-1]
        text = Text((0, 0), sp)
    class_level = LEVELS.get_level()
    level_to_draw, index = class_level.get_level()
    color, player = draw_level(level_to_draw, index)
    running = True
    start_time = time.time()
    start_count = start_time
    best_effects = False
    while running:
        end_time = time.time()
        screen.fill(color)
        [exit() for event in pygame.event.get() if event.type == pygame.QUIT]
        if pygame.key.get_pressed()[pygame.K_ESCAPE] or back_to_start:
            LEVELS.finish_level()
            [el.kill() for el in effects], [el.kill() for el in group_text]
            return 110110
        if abs(start_time - end_time) >= 2 / booster:
            if abs(start_count - end_time) <= 14 / booster:
                text.manual_move()
            elif abs(start_count - end_time) <= 16 / booster:
                text.change_speed()
            elif 34 / booster <= abs(start_count - end_time) <= 36 / booster:
                best_effects = True
            start_time = end_time

        if best_effects:
            for i in range(1000):
                screen.fill(white, (random.random() * width, random.random() * height, 1, 1))

        effects.draw(screen)
        group_text.draw(screen)
        group_text.update()
        effects.update()
        pygame.display.set_caption(str(clock.get_fps()))
        pygame.display.flip()
        clock.tick(FPS)
    return 0
