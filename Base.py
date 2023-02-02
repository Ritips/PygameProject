from DefinePlayerLevel import LEVELS
from QueenLevel import queen_level
from StartScreen import start_screen
from StartLevel import start_level_game
from SecondLevel import second_level


def main(lobby=True, index=None):
    if lobby:
        start_screen()
        level, index = LEVELS.get_level().get_level()
    else:
        if index:
            LEVELS.chose_level(level_chosen=index)

    if index == 0:
        flag = start_level_game()
        if flag == 110101:
            main()
        if flag == 110102:
            main(lobby=False, index=1)

    if index == 1:
        flag = second_level()
        if flag == 110101:
            main()
    # тут получается переход надо. Флаг окончания лвла - 110103


if __name__ == '__main__':
    main()
