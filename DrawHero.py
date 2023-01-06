import pygame
import sys
from PyQt5.QtWidgets import QApplication, QColorDialog


pygame.init()

diction = {0: (254, 253, 251, 255)}
diction_colors = {(255, 255, 255, 255): 0}
app = QApplication(sys.argv)
size = w, h = 1600, 1000
screen = pygame.display.set_mode(size)
sprites = pygame.sprite.Group()
color = None


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 20

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, display):
        for i in range(self.height):
            start_y = self.top + self.cell_size * i
            start_x = self.left
            for j in range(self.width):
                if self.board[i][j] in diction.keys():
                    r, g, b, a = diction[self.board[i][j]]
                    pygame.draw.rect(display, (r, g, b), (start_x, start_y, self.cell_size, self.cell_size))
                pygame.draw.rect(display, (55, 0, 0), (start_x, start_y, self.cell_size, self.cell_size), 1)
                start_x = start_x + self.cell_size

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if x in range(self.left, self.left + self.cell_size * self.width):
            if y in range(self.top, self.top + self.cell_size * self.height):
                return (x - self.left) // self.cell_size, (y - self.top) // self.cell_size
        return False

    def on_click(self, cell_coords):
        global color
        if not color or not cell_coords:
            return
        x, y = cell_coords
        self.board[y][x] = diction_colors[color.getRgb()]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def save_image(self, name='image.png'):
        print('save image')
        image = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
        for i in range(self.height):
            for j in range(self.width):
                r, g, b, a = diction[self.board[i][j]]
                pygame.draw.rect(image, (r, g, b), (i, j, 1, 1))
        pygame.image.save(image, name)


class ButtonChangeColor(pygame.sprite.Sprite):
    def __init__(self):
        super(ButtonChangeColor, self).__init__(sprites)
        self.rect = pygame.Rect((w - 100 * 5, h - 50 * 3, 100, 50))
        self.image = pygame.Surface((100, 50))
        pygame.draw.rect(self.image, 'blue', (0, 0, 100, 50))

    def is_clicked(self, pos):
        if pos[0] in range(self.rect.x, self.rect.x + self.rect.w + 1):
            if pos[1] in range(self.rect.y, self.rect.y + self.rect.h + 1):
                return True
        return


board = Board(50, 50)
btn_change_color = ButtonChangeColor()
if __name__ == '__main__':
    key = 1
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            '''if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_change_color.is_clicked(event.pos):
                    color = QColorDialog.getColor()
                    if color.isValid():
                        if color.getRgb() not in diction_colors:
                            diction_colors[color.getRgb()] = key
                        if key not in diction and color.getRgb() not in diction.values():
                            diction[key] = color.getRgb()
                            key += 1
                board.get_click(event.pos)'''
            if event.type == pygame.MOUSEBUTTONDOWN and event.button != 1:
                board.save_image('test2.png')
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            pos = pygame.mouse.get_pos()
            if btn_change_color.is_clicked(pos):
                color = QColorDialog.getColor()
                if color.isValid():
                    if color.getRgb() not in diction_colors:
                        diction_colors[color.getRgb()] = key
                    if key not in diction and color.getRgb() not in diction.values():
                        diction[key] = color.getRgb()
                        key += 1
            board.get_click(pos)
        sprites.draw(screen)
        board.render(screen)
        pygame.display.flip()
