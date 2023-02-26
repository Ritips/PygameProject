import random
import time
import pygame
from SETTINGS import size


def start_riddle():
    pygame.init()
    screen = pygame.display.set_mode(size)
    task_solved = False
    flag_exit = False
    rectangles = pygame.sprite.Group()

    class WhatIsIt(pygame.sprite.Sprite):
        def __init__(self, x=0, y=0, position='horizontal', position_number=0):
            super(WhatIsIt, self).__init__(rectangles)
            self.position = position
            self.position_number = position_number
            self.size = [30, 60]  # this is not real size this is dx dy
            self.rect = pygame.Rect(x, y, self.size[0], self.size[1])
            self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32)
            if self.position_number in (0, 1, 2, 3, 13, 23, 33, 34, 44, 54, 55, 65, 66, 76, 77, 78, 88, 89, 99):
                self.color = 'red'
            else:
                self.color = 'white'
            pygame.draw.rect(self.image, self.color, (0, 0, self.size[0], self.size[1]))

            if position != 'vertical':
                self.update(self.rect, ignore=True)

        def update(self, pos_click=None, ignore=False, **kwargs):
            if pos_click and self.near(pos_click, self.rect):
                if not ignore:
                    if self.position == 'horizontal':
                        self.position = 'vertical'
                    else:
                        self.position = 'horizontal'
                x, y, w, h = self.rect
                self.rect = pygame.Rect(x, y, h, w)
                self.image = pygame.Surface((h, w), pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, self.color, (0, 0, h, w))

        @staticmethod
        def near(point, coords):
            if (coords[0] <= point[0] <= coords[0] + coords[2]) and (coords[1] <= point[1] <= coords[1] + coords[3]):
                return True
            return False

    def correct_pos(pos, num):
        d = {0: 'vertical',
             1: 'vertical',
             2: 'vertical',
             3: 'horizontal',
             13: 'horizontal',
             23: 'horizontal',
             33: 'vertical',
             34: 'horizontal',
             44: 'horizontal',
             54: 'vertical',
             55: 'horizontal',
             65: 'vertical',
             66: 'horizontal',
             76: 'vertical',
             77: 'vertical',
             78: 'horizontal',
             88: 'vertical',
             89: 'horizontal',
             99: 'horizontal'}

        if num in d.keys():
            return pos == d[num]
        return True

    count = 0
    for i in range(10):
        for j in range(10):
            rectangles.add(WhatIsIt(i * 30 + 30 * i, j * 60, position=random.choice(['horizontal', 'vertical']),
                                    position_number=count))
            count += 1

    count = 0
    t = time.time()
    while not task_solved:
        if abs(t - time.time()) > 30:
            return 1
        screen.fill('black')
        something_like_exit = pygame.Rect(600, 540, 30, 70)
        pygame.draw.rect(screen, 'red', something_like_exit)
        if flag_exit:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag_exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                rectangles.update(pos_click=event.pos)
                count = 0
                for i in rectangles:
                    if correct_pos(i.position, i.position_number):
                        count += 1
                    else:
                        break
        if count == 100:
            return 0
        pygame.display.set_caption(str(round(30 - abs(t - time.time()))))
        rectangles.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    start_riddle()
