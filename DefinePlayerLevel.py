from LoadLevel import load_level


class Level:  # Parent
    def __init__(self, current_level=None, level=None):
        self.finished = False
        self.current_level = current_level if current_level.__class__ == int else -2
        try:
            self.level = load_level(level) if level else ''
        except FileNotFoundError:
            self.level = None

    def get_level(self):
        return self.level, self.current_level

    def change_status(self):
        self.finished = True

    def get_status(self):
        return self.finished


# children
class QueenLevel(Level):
    def __init__(self):
        super(QueenLevel, self).__init__(current_level=2, level='first_level.txt')


class StartLevel(Level):
    def __init__(self):
        super(StartLevel, self).__init__(current_level=0, level='start_level.txt')


class SecondLevel(Level):
    def __init__(self):
        super(SecondLevel, self).__init__(current_level=1, level='slime_level.txt')


class FinishLevel(Level):
    def __init__(self):
        super(FinishLevel, self).__init__(current_level=4, level='last_level.txt')


class FreezeLevel(Level):
    def __init__(self):
        super(FreezeLevel, self).__init__(current_level=3, level='FreezeLevel.txt')


class GhostLevel(Level):
    def __init__(self):
        super(GhostLevel, self).__init__(current_level=5, level='CheckDefinePlayer.py to define txt file of the level')


class Levels:  # List of the levels. It must include all available levels
    def __init__(self):
        # self.all_levels: levels should be in logical order
        self.all_levels = [StartLevel(), SecondLevel(), QueenLevel(), FreezeLevel(), FinishLevel(), GhostLevel()]
        with open('data/levels.txt') as f:  # load available levels
            self.available_levels = list(map(int, map(str.strip, f.readlines())))
        self.current_level_index = None
        self.current_level = None

    def finish_level(self):  # finish level and write it in the levels.txt
        if self.current_level:
            self.current_level.change_status()
            with open('data/levels.txt', 'r') as file_levels:
                contain = list(map(str.strip, file_levels.readlines()))
                if str(self.current_level_index) in contain:
                    return
                contain.append(self.current_level_index)
                with open('data/levels.txt', 'w', newline='\n') as file_levels_write:
                    for el in contain:
                        print(el, file=file_levels_write)
            self.available_levels.append(self.current_level_index)

    def chose_level(self, level_chosen=None):  # selection of the levels
        if level_chosen.__class__ == int:
            self.current_level_index = level_chosen
        elif not self.available_levels:
            self.current_level_index = 0

        self.current_level = self.all_levels[self.current_level_index]

    def get_level(self):
        return self.all_levels[self.current_level_index]


LEVELS = Levels()  # this class combine all levels. It allows to switch between levels
