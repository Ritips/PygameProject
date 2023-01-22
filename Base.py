from SETTINGS import *
from DefinePlayerLevel import LEVELS
from QueenLevel import queen_level
from StartScreen import start_screen
import pygame


pygame.init()


def main():
    start_screen()
    level, index = LEVELS.get_level().get_level()
    if index == 1:
        flag = queen_level()
        if flag == 110101:
            main()


if __name__ == '__main__':
    main()

