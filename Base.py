from DefinePlayerLevel import LEVELS
from QueenLevel import queen_level
from StartScreen import start_screen
from StartLevel import start_level_game
from LastLevel import start_last_level
from SecondLevel import second_level
from FreezeLevel import freeze_level


def main(lobby=True, index=None):  # carry out switching between levels
    if lobby:
        start_screen()
        level, index = LEVELS.get_level().get_level()
    else:
        if index.__class__ == int:
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
        if flag == 110105:
            main(lobby=False, index=2)
    if index == 2:
        flag = queen_level()
        if flag == 110101:
            main()
        if flag == 110105:
            main(lobby=False, index=3)
    if index == 3:
        flag = freeze_level()
        if flag == 110101:
            main()
        if flag == 110105:
            main(lobby=False, index=4)
    if index == 4:
        flag = start_last_level()
        if flag == 110110:
            main(index=0)


if __name__ == '__main__':
    main()
