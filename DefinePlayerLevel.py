from SETTINGS import level_first, start_level
from LoadLevel import load_level


class Level:
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


class QueenLevel(Level):
    def __init__(self):
        super(QueenLevel, self).__init__(current_level=1, level='first_level.txt')


class StartLevel(Level):
    def __init__(self):
        super(StartLevel, self).__init__(current_level=0, level='start_level.txt')


class SecondLevel(Level):
    def __init__(self):
        super(SecondLevel, self).__init__(current_level=3, level='slime_level.txt')


class FinishLevel(Level):
    def __init__(self):
        super(FinishLevel, self).__init__(current_level=2, level='last_level.txt')


class Levels:
    def __init__(self):
        self.all_levels = [StartLevel(), SecondLevel(), QueenLevel(), FinishLevel()]
        with open('data/levels.txt') as f:
            self.available_levels = list(map(int, map(str.strip, f.readlines())))
        self.current_level_index = None
        self.current_level = None

    def finish_level(self):
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

    def chose_level(self, level_chosen=None):
        if not self.available_levels:
            self.current_level_index = 0
        elif not level_chosen:
            self.current_level_index = 0
        else:
            self.current_level_index = level_chosen
        self.current_level = self.all_levels[self.current_level_index]

    def get_level(self):
        return self.all_levels[self.current_level_index]


LEVELS = Levels()
