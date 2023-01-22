from DefinePlayerLevel import LEVELS
from QueenLevel import queen_level
from StartScreen import start_screen
from StartLevel import start_level_game
import pygame


pygame.init()


def main():
    start_screen()
    level, index = LEVELS.get_level().get_level()
    if index == 0:
        flag = start_level_game()
        if flag == 110101:
            main()
    if index == 1:
        flag = queen_level()
        if flag == 110101:
            main()


if __name__ == '__main__':
    main()
